from fastapi import Body, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import clip, faiss, torch, sqlite3, gc
from PIL import Image
from io import BytesIO
import base64
import gc
from collections import Counter
import uvicorn
import iconclass

INDEX = faiss.read_index('data/knn.index')
img_db = db = sqlite3.connect("data/imgs.sqlite3")


app = FastAPI()

subapi = FastAPI(openapi_prefix="/iconclass/multimodal")


subapi.mount("/", StaticFiles(directory="static"), name="static")

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device, jit=False)


class UploadPayload(BaseModel):
    file_base64: bytes



@subapi.get("/api/similarity_text")
async def ai_search(q: str):
    with torch.no_grad():
        tokens = clip.tokenize([q]).to(device)
        text_features = model.encode_text(tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    text_embeddings = text_features.cpu().detach().numpy().astype("float32")
    del tokens
    del text_features
    gc.collect()
    torch.cuda.empty_cache()
    r = await results_from_embeddings(text_embeddings)
    return r


@subapi.post("/api/similarity")
async def post_upload(file_base64: str = Body(..., embed=True)):
    print(f"Received base64 of length {len(file_base64)}")
    contents = base64.b64decode(file_base64)
    print(f"And file is length {len(contents)}")

    image = Image.open(BytesIO(contents)).resize((256, 256))
    with torch.no_grad():
        image_tensor = preprocess(image)
        image_features = model.encode_image(torch.unsqueeze(image_tensor.to(device), dim=0))
    image_features /= image_features.norm(dim=-1, keepdim=True)
    image_embeddings = image_features.cpu().detach().numpy().astype("float32")
    del image_tensor
    del image_features
    gc.collect()
    torch.cuda.empty_cache()
    r = await results_from_embeddings(image_embeddings)
    return r


async def results_from_embeddings(embeddings):
    D, I = INDEX.search(embeddings, 32)
    query = "SELECT * FROM image_ic WHERE idx IN ("+", ".join(str(i) for i in I[0])+")"
    filenames = []
    returned_ics = []
    labels = {}
    for result in img_db.execute(query).fetchall():
        filename = result[0]
        ics = result[2].split("\n")
        filenames.append(filename)
        returned_ics.append(ics)
        for notation in ics:
            try:
                ic_dict = iconclass.get(notation)
                label = ic_dict["txt"]["en"]
                labels[notation]=label
            except:
                labels[notation]=""
    result = {"filenames":filenames,"ics":returned_ics, "labels":labels}
    return result


app.mount("/iconclass/multimodal", subapi)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50000)
