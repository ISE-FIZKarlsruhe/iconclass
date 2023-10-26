#!/usr/bin/env python3

from dotenv import load_dotenv
import hashlib
from os import getenv, path, makedirs
import re
from typing import Iterator, List
from uuid import uuid4

load_dotenv()

BATCH_SIZE: int = 100
MAX_ENTRIES: int = 10000

DATA_SOURCE_PATH = getenv("SOURCE_DATA_FILE")
assert (
    DATA_SOURCE_PATH is not None
), "The environment variable SOURCE_DATA_FILE has not been defined!"

TARGET_DIR = getenv("EXTRACTED_TEXT_DIR")
assert (
    DATA_SOURCE_PATH is not None
), "The environment variable TARGET_DIR has not been defined!"


def load_nt_texts(path: str) -> Iterator[str]:
    with open(path) as file:
        for line in file:
            components = line.split(" ")

            # remove id, description, and closing "."
            cleansed_line = " ".join(components[2:-1])
            cleansed_line = cleansed_line.replace('"', "")
            cleansed_line = cleansed_line.strip()

            yield cleansed_line


def contains_iconclass(text: str) -> bool:
    match = re.search(r"\d{2} ?[a-zA-Z]{1,2} ?\d{1,2}", text)
    return not match is None


def save_batch(data_batch: List[str], dir_path: str) -> None:
    file_path = f"{dir_path}/{uuid4()}.txt"

    with open(file_path, "w") as target_file:
        for i, entry in enumerate(data_batch):
            if i > 0:
                target_file.write("\n\n")

            target_file.write(entry)


def has_been_encountered(text: str) -> bool:
    if not hasattr(has_been_encountered, "hash_set"):
        has_been_encountered.hash_set = set()

    text_hash = str(
        hashlib.md5(text.encode("utf-8"), usedforsecurity=False).hexdigest()
    )

    if text_hash in has_been_encountered.hash_set:
        return True

    has_been_encountered.hash_set.add(text_hash)
    return False


if __name__ == "__main__":
    if not path.exists(TARGET_DIR):
        makedirs(TARGET_DIR)

    entry_counter: int = 0

    current_batch: List[str] = []
    for line in load_nt_texts(DATA_SOURCE_PATH):
        if not contains_iconclass(line):
            continue

        # avoid duplicates
        if has_been_encountered(line):
            continue

        current_batch.append(line)

        entry_counter += 1
        if entry_counter == MAX_ENTRIES:
            break

        if len(current_batch) == BATCH_SIZE:
            save_batch(current_batch, TARGET_DIR)
            current_batch = []

    if len(current_batch) > 0:
        save_batch(current_batch, TARGET_DIR)
