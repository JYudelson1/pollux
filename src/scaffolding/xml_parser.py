# NB: This was written by Claude

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List, Optional
from io import StringIO


@dataclass
class ParsedTag:
    tag: str
    attributes: Dict[str, str]
    content: str


def parse_claude_output(text: str) -> tuple[List[ParsedTag], Optional[str]]:
    # Wrap in root tag to handle multiple top-level elements
    wrapped = f"<root>{text}</root>"

    try:
        root = ET.parse(StringIO(wrapped)).getroot()
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}")

    tags = []
    response = None

    for elem in root:
        if elem.tag == "response":
            if response is not None:
                raise ValueError("Multiple response tags found")
            response = elem.text.strip() if elem.text else ""
        else:
            tags.append(
                ParsedTag(
                    tag=elem.tag,
                    attributes=elem.attrib,
                    content=elem.text.strip() if elem.text else "",
                )
            )

    return tags, response
