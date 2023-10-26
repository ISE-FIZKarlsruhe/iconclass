#!/usr/bin/env python3

import spacy
from typing import Iterator


def load_test_texts(path: str) -> Iterator[str]:
    with open(path) as file:
        for line in file:
            if line.strip() == "":
                continue

            yield line


if __name__ == "__main__":
    test_path = "./data/descriptions/f38f204a-2a94-48d4-9018-0b96032b012a.txt"

    nlp = spacy.load("./data/output/model-last")

    docs = []

    for text in load_test_texts(test_path):
        doc = nlp(text)

        # if len(doc.ents) == 0:
        #     continue

        docs.append(doc)

        if len(docs) == 10:
            break 

    spacy.displacy.serve(docs, style="ent")
