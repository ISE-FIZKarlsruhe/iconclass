#!/usr/bin/env python3

from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import List

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def extract_iconclass_codes(text: str) -> List[str]:
    pass


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
    for text in body["text"]:
        codes = extract_iconclass_codes(text)
        annotations.append({"text": text, "codes": codes})

    return templates.TemplateResponse(
        "annotated.html", {"request": request, "annotations": annotations}
    )
