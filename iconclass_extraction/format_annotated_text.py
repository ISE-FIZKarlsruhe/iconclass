#!/usr/bin/env python3

from dotenv import load_dotenv
import json
from os import getenv, path, makedirs, listdir
import spacy
from spacy.tokens import DocBin, Doc
from tqdm import tqdm
from typing import Iterator, List, Tuple, Dict

load_dotenv()

ANNOTATIONS_DIR = getenv("ANNOTATIONS_DIR")
assert (
    ANNOTATIONS_DIR is not None
), "The environment variable ANNOTATIONS_DIR has not been defined!"

SPACY_TARGET_PATH = getenv("SPACY_ANNOTATIONS_PATH")
assert (
    SPACY_TARGET_PATH is not None
), "The environment variable SPACY_ANNOTATIONS_PATH has not been defined!"


def format_annotated_data(
    annotation_path: str, nlp: spacy.language.Language
) -> Iterator[Doc]:
    # Inspired by https://github.com/dreji18/NER-Training-Spacy-3.0/blob/main/NER%20Training%20Data%20Annotation.ipynb

    train_data: List[Tuple[str, Dict]] = None
    with open(annotation_path) as data_file:
        data = json.load(data_file)

        train_data = [tuple(item) for item in data["annotations"]]

        for text, annotations in train_data:
            for i in range(len(annotations["entities"])):
                annotations["entities"][i] = tuple(annotations["entities"][i])

    for text, annotations in tqdm(train_data):  # data in previous format
        doc = nlp.make_doc(text)  # create doc object from text

        ents = []
        for start, end, label in annotations["entities"]:  # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")

            if span is None:
                continue

            ents.append(span)

        doc.ents = ents  # label the text with the ents

        yield doc


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")  # load pretrained spacy model
    doc_bin = DocBin()

    for file_name in listdir(ANNOTATIONS_DIR):
        file_path = f"{ANNOTATIONS_DIR}/{file_name}"

        if not file_path.endswith(".json"):
            continue

        for doc in format_annotated_data(annotation_path=file_path, nlp=nlp):
            doc_bin.add(doc)

    doc_bin.to_disk(SPACY_TARGET_PATH)
