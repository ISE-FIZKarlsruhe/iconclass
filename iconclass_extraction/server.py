#!/usr/bin/env python3

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import spacy
from typing import List

load_dotenv()

nlp = spacy.load("./data/output/model-last")

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def extract_iconclass_codes(text: str) -> List[str]:
    doc = nlp(text)

    codes = []
    continued_codes = []

    for ent in doc.ents:
        if ent.label_ == "IC_START":
            codes.append(ent.text.strip())

        elif ent.label_ == "IC_CONTD":
            # edge case, where wrongly detected cont before
            # first starting iconclass code.
            if len(codes) == 0:
                continue

            cont_code = ent.text.replace("+", "").replace("(", "").replace(")", "")

            if " " in codes[-1]:
                new_code = f"{codes[-1]} {cont_code}"
            else:
                new_code = f"{codes[-1]}{cont_code}"

            continued_codes.append(new_code)

    codes = codes + continued_codes
    return codes


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/annotate")
async def get_iconclass_codes(request: Request, response: Response):
    body = await request.json()

    if not "texts" in body:
        response.status_code = 400
        return response

    annotations = []
    for text in body["texts"]:
        codes = extract_iconclass_codes(text)
        annotations.append({"text": text, "codes": codes})

    return templates.TemplateResponse(
        "annotated.html", {"request": request, "annotations": annotations}
    )
