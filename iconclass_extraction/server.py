#!/usr/bin/env python3

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import spacy
from typing import List, Annotated

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
            codes.append(ent.text.strip())
            last_start_code = codes[-1]

        elif ent.label_ == "IC_CONTD":
            # edge case, where wrongly detected cont before
            # first starting iconclass code.
            if last_start_code is None:
                continue

            cont_code = ent.text.strip()

            if " " in last_start_code:
                new_code = f"{last_start_code} {cont_code}"
            else:
                new_code = f"{last_start_code}{cont_code}"

            codes.append(new_code)

    return codes


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
