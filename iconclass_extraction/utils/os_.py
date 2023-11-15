#!/usr/bin/env python3

from os import getenv
from typing import Union, List, Tuple


def get_env(
    name: str, assert_value: bool = True, default: str = None
) -> Union[str, None]:
    value = getenv(name)

    if value is not None:
        return value

    if assert_value:
        raise AssertionError(f"The environment variable {name} has not been defined!")

    return default
