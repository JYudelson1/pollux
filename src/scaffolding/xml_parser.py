# NB: This was written by Claude

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from xml.sax.saxutils import escape, unescape
from io import StringIO
import xml.etree.ElementTree as ET


@dataclass
class ParsedTag:
    tag: str
    attributes: Dict[str, str]
    content: str


def extract_xml_blocks(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Extract XML-like blocks from text and replace them with placeholders.
    Returns processed text and a mapping of placeholders to original content.
    """
    # Regular expression to match XML-like blocks
    pattern = r'<([a-zA-Z][a-zA-Z0-9_]*)((?:\s+[a-zA-Z][a-zA-Z0-9_]*="[^"]*")*)\s*>(.*?)</\1>'
    
    replacements = {}
    placeholder_counter = 0
    processed_text = text

    for match in re.finditer(pattern, text, flags=re.DOTALL):
        full_match = match.group(0)
        placeholder = f"__XML_PLACEHOLDER_{placeholder_counter}__"
        replacements[placeholder] = full_match
        processed_text = processed_text.replace(full_match, placeholder)
        placeholder_counter += 1
    
    return processed_text, replacements


def escape_non_xml(text: str) -> str:
    """
    Escape angle brackets that aren't part of identified XML tags.
    """
    # First, process the text to identify and protect real XML blocks
    processed_text, replacements = extract_xml_blocks(text)
    
    # Escape remaining angle brackets
    processed_text = processed_text.replace('<', '&lt;').replace('>', '&gt;')
    
    # Restore XML blocks
    for placeholder, original in replacements.items():
        processed_text = processed_text.replace(placeholder, original)
    
    return processed_text


def parse_claude_output(text: str) -> Tuple[List[ParsedTag], Optional[str]]:
    """
    Parse text containing XML tags, handling both well-formed XML and text with random angle brackets.
    """
    # Escape problematic characters while preserving valid XML
    escaped_text = escape_non_xml(text)
    
    # Wrap in root tag to handle multiple top-level elements
    wrapped = f"<root>{escaped_text}</root>"

    try:
        root = ET.parse(StringIO(wrapped)).getroot()
    except ET.ParseError as e:
        # Try more aggressive cleaning if initial parse fails
        cleaned_text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', wrapped)
        try:
            root = ET.parse(StringIO(cleaned_text)).getroot()
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML after cleaning: {e}")

    tags = []
    response = None

    for elem in root:
        # Unescape content while preserving XML structure
        content = elem.text.strip() if elem.text else ""
        content = unescape(content)
        
        if elem.tag == "response":
            if response is not None:
                raise ValueError("Multiple response tags found")
            response = content
        else:
            tags.append(
                ParsedTag(
                    tag=elem.tag,
                    attributes=elem.attrib,
                    content=content,
                )
            )

    return tags, response


def parse_attributes(attr_string: str) -> Dict[str, str]:
    """
    Parse attribute string into a dictionary.
    Example: 'name="value" other="something"' -> {'name': 'value', 'other': 'something'}
    """
    attrs = {}
    pattern = r'([a-zA-Z][a-zA-Z0-9_]*)="([^"]*)"'
    matches = re.finditer(pattern, attr_string)
    for match in matches:
        attrs[match.group(1)] = match.group(2)
    return attrs