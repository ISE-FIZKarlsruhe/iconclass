#!/usr/bin/env python3

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import spacy
from spacy.tokens import Token
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

            bracket_code = extract_bracket_details(ent[-1])
            if bracket_code is not None:
                code += bracket_code

            codes.append(code)
            last_start_code = codes[-1]

        elif ent.label_ == "IC_CONTD":
            # edge case, where wrongly detected cont before
            # first starting iconclass code.
            if last_start_code is None:
                continue

            cont_code = ent.text.strip()

            bracket_code = extract_bracket_details(ent[-1])
            if bracket_code is not None:
                cont_code += bracket_code

            if " " in last_start_code:
                new_code = f"{last_start_code} {cont_code}"
            else:
                new_code = f"{last_start_code}{cont_code}"

            codes.append(new_code)

    return codes


def extract_bracket_details(token: Token) -> Union[str, None]:
    if "(" not in token.nbor().text.strip():
        return None

    bracket_start_i = token.i + 1
    bracket_end_i = None

    for i in range(1, 10):  # 10 as arbitrary max threshold
        if ")" in token.nbor(i).text.strip():
            bracket_end_i = token.i + i
            break

    else:
        return None

    return token.doc[bracket_start_i : bracket_end_i + 1].text.strip()


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
