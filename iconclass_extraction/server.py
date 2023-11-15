#!/usr/bin/env python3

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import spacy
from spacy.tokens import Token, Span
from typing import List, Annotated, Union

load_dotenv()

nlp = spacy.load("./data/output/model-last")

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def extract_iconclass_codes(text: str) -> List[str]:
    doc = nlp(text)

    codes = []
    last_start_code = None

    for ent in doc.ents:
        if ent.label_ == "IC_START":
            code = ent.text.strip()
            code = "".join(code.split(" "))

            try:
                bracket_code = extract_bracket_details(ent[-1])
                if bracket_code is not None:
                    code += bracket_code
            except Exception as e:
                print(str(e))

            codes.append(code)
            last_start_code = codes[-1]

        elif ent.label_ == "IC_CONTD":
            # edge case, where wrongly detected cont before
            # first starting iconclass code.
            if last_start_code is None:
                continue

            cont_code = ent.text.strip()
            cont_code = "".join(cont_code.split(" "))

            try:
                bracket_code = extract_bracket_details(ent[-1])
                if bracket_code is not None:
                    cont_code += bracket_code
            except Exception as e:
                print(str(e))

            new_code = f"{last_start_code}{cont_code}"
            codes.append(new_code)

    return codes

def extract_bracket_details(token: Token) -> Union[str, None]:
    if token.nbor(1).text.strip()[0] != "(":
        return None

    for j in range(1, 10):  # 10 as arbitrary max threshold
        if token.i + j >= len(token.doc):
            return None

        # Avoid FP cases where brackets are included but not at the end
        # (ex. "(Stadt-)Türme")
        if ")" in token.nbor(j).text and not token.nbor(j).text.strip()[-1] == ")":
            return None

        if token.nbor(j).text.strip()[-1] == ")":
            return token.doc[token.i + 1 : token.i + j + 1].text.strip()

    return None


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/annotate")
async def get_iconclass_codes(
    text: Annotated[str, Form()], request: Request, response: Response
):
    codes = extract_iconclass_codes(text)
    annotations = [{"text": text, "codes": codes}]

    return templates.TemplateResponse(
        "annotated.html", {"request": request, "annotations": annotations}
    )
