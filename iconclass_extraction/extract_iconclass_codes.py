#!/usr/bin/env python3

from spacy.language import Language
from spacy.tokens import Token, Span
from typing import List, Union


def extract_iconclass_codes(text: str, nlp: Language) -> List[str]:
    doc = nlp(text)

    codes = []
    last_start_code = None

    for ent in doc.ents:
        if ent.label_ == "IC_START":
            code = extract_start_code(ent)
            codes.append(code)

            last_start_code = codes[-1]

        elif ent.label_ == "IC_CONTD":
            # edge case, where wrongly detected cont before
            # first starting iconclass code.
            if last_start_code is None:
                continue

            new_code = extract_continued_code(ent, last_start_code)
            codes.append(new_code)

    return codes


def extract_start_code(ent: Span) -> str:
    code = ent.text.strip()
    code = "".join(code.split(" "))

    try:
        bracket_code = extract_bracket_details(ent[-1])
        if bracket_code is not None:
            code += bracket_code
    except Exception as e:
        print(str(e))

    return code


def extract_continued_code(ent: Span, last_start_code: str) -> str:
    cont_code = ent.text.strip()
    cont_code = "".join(cont_code.split(" "))

    try:
        bracket_code = extract_bracket_details(ent[-1])
        if bracket_code is not None:
            cont_code += bracket_code
    except Exception as e:
        print(str(e))

    new_code = f"{last_start_code}{cont_code}"
    return new_code


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
