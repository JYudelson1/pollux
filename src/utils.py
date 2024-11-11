import pathlib
from typing import *

ROOT = pathlib.Path(__file__).parent.parent


def get_raw_text(messages: List[Dict]) -> str:
    text = ""

    for message in messages:
        content = message["content"]
        for block in content:
            text += block["text"]
            text += "\n"

    return text[:-1]
