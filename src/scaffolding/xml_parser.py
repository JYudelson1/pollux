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
        if elem.tag == 'response':
            if response is not None:
                raise ValueError("Multiple response tags found")
            response = elem.text.strip() if elem.text else ""
        else:
            tags.append(ParsedTag(
                tag=elem.tag,
                attributes=elem.attrib,
                content=elem.text.strip() if elem.text else ""
            ))
    
    return tags, response

# Example usage:
sample = '''
Some scratchpad text
<save_memory type="preference">Joey likes spicy food</save_memory>
More scratchpad
<load_memory limit="5" sort="date">food preferences</load_memory>
<response>Here's what I found about your food preferences</response>
'''

tags, response = parse_claude_output(sample)
for tag in tags:
    print(f"\nTag: {tag.tag}")
    print(f"Attributes: {tag.attributes}")
    print(f"Content: {tag.content}")
print(f"\nResponse: {response}")