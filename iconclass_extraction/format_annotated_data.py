#!/usr/bin/env python3

from dotenv import load_dotenv
import json
from os import getenv, path, makedirs, listdir
from random import random
import spacy
from spacy.tokens import DocBin, Doc
from tqdm import tqdm
from typing import Iterator, List, Tuple, Dict

from utils.os_ import get_env

load_dotenv()

TRAIN_TEST_SPLIT: float = 0.7

# Removes whitespaces for percentage of labels
AUGMENTATION_PROBABILITY: float = 0.5

ANNOTATIONS_DIR = get_env("ANNOTATIONS_DIR")
SPACY_TARGET_DIR = get_env("SPACY_ANNOTATIONS_DIR")


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

    for text, annotations in tqdm(train_data):
        doc = nlp.make_doc(text)

        ents = []
        for start, end, label in annotations["entities"]:  # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")

            if span is None:
                continue

            ents.append(span)

        doc.ents = ents
        yield doc


def format_annotated_data_with_augmentation(
    annotation_path: str, nlp: spacy.language.Language
) -> Iterator[Doc]:
    # Inspired by https://github.com/dreji18/NER-Training-Spacy-3.0/blob/main/NER%20Training%20Data%20Annotation.ipynb

    train_data: List[Tuple[str, Dict]] = None
    with open(annotation_path) as data_file:
        data = json.load(data_file)

        train_data = [tuple(item) for item in data["annotations"]]

        for k, (text, annotations) in enumerate(train_data):
            # Sort annotations by start index
            annotations["entities"].sort(key=lambda item: item[0])

            whitespace_offset = 0
            for i in range(len(annotations["entities"])):
                start, end, label = annotations["entities"][i]

                start -= whitespace_offset
                end -= whitespace_offset

                if random() <= AUGMENTATION_PROBABILITY:
                    labelled_text = text[start:end]

                    space_indexes = [
                        start + i for i, char in enumerate(labelled_text) if char == " "
                    ]

                    # Reverse order, to avoid having to adjust later indexes.
                    for j in reversed(space_indexes):
                        text = text[:j] + text[j + 1 :]

                    end -= len(space_indexes)
                    whitespace_offset += len(space_indexes)

                annotations["entities"][i] = (start, end, label)

            train_data[k] = (text, annotations)

    for text, annotations in tqdm(train_data):
        doc = nlp.make_doc(text)

        ents = []
        for start, end, label in annotations["entities"]:  # add character indexes
            span = doc.char_span(start, end, label=label, alignment_mode="contract")

            if span is None:
                continue

            ents.append(span)

        doc.ents = ents
        yield doc


def split_into_bins(docs: List[Doc], split: float = 0.7) -> Tuple[DocBin, DocBin]:
    train_bin = DocBin()
    dev_bin = DocBin()

    for doc in docs:
        if random() <= TRAIN_TEST_SPLIT:
            train_bin.add(doc)
        else:
            dev_bin.add(doc)

    return train_bin, dev_bin


if __name__ == "__main__":
    if not path.exists(SPACY_TARGET_DIR):
        makedirs(SPACY_TARGET_DIR)

    nlp = spacy.load("en_core_web_sm")  # load pretrained spacy model

    docs: List[Doc] = []
    for file_name in listdir(ANNOTATIONS_DIR):
        file_path = f"{ANNOTATIONS_DIR}/{file_name}"

        if not file_path.endswith(".json"):
            continue

        for doc in format_annotated_data_with_augmentation(annotation_path=file_path, nlp=nlp):
            docs.append(doc)

    spacy_train_path = f"{SPACY_TARGET_DIR}/train.spacy"
    spacy_dev_path = f"{SPACY_TARGET_DIR}/dev.spacy"

    train_bin, dev_bin = split_into_bins(docs, split=TRAIN_TEST_SPLIT)

    train_bin.to_disk(spacy_train_path)
    dev_bin.to_disk(spacy_dev_path)
