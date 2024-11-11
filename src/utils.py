import pathlib
from typing import *

ROOT = pathlib.Path(__file__).parent.parent


def get_raw_text(messages: List[Dict]) -> str:
    text = ""

    for message in messages:
        text += message["content"]["text"]
        text += "\n"

    return text[:-1]
