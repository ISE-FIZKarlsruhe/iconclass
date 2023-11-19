#!/usr/bin/env python3

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import spacy
from spacy.tokens import Token, Span
from typing import List, Annotated, Union

from extract_iconclass_codes import extract_iconclass_codes
from utils.os_ import get_env

load_dotenv()

SPACY_MODEL_PATH = get_env("SPACY_MODEL_PATH")
nlp = spacy.load(SPACY_MODEL_PATH)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/annotate")
async def get_iconclass_codes(
    text: Annotated[str, Form()], request: Request, response: Response
):
    codes = extract_iconclass_codes(text, nlp=nlp)
    annotations = [{"text": text, "codes": codes}]

    return templates.TemplateResponse(
        "annotated.html", {"request": request, "annotations": annotations}
    )
