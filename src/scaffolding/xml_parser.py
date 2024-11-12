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
    # Updated pattern to handle:
    # 1. Both single and double quotes in attributes
    # 2. Optional spaces around = in attributes
    # 3. More flexible whitespace handling
    pattern = r'<([a-zA-Z][a-zA-Z0-9_]*)((?:\s+[a-zA-Z][a-zA-Z0-9_]*\s*=\s*(?:"[^"]*"|\'[^\']*\'))*)\s*>(.*?)</\1>'
    
    replacements = {}
    placeholder_counter = 0
    processed_text = text

    for match in re.finditer(pattern, text, flags=re.DOTALL):
        tag_name = match.group(1)
        attributes_str = match.group(2)
        content = match.group(3)
        full_match = match.group(0)
        
        try:
            # Parse attributes to verify format
            attrs = parse_attributes(attributes_str)
            # Create a test XML string
            test_xml = f"<{tag_name}{attributes_str}>{content}</{tag_name}>"
            # Try parsing with ElementTree to verify it's valid XML
            ET.fromstring(test_xml)
            
            placeholder = f"__XML_PLACEHOLDER_{placeholder_counter}__"
            replacements[placeholder] = full_match
            processed_text = processed_text.replace(full_match, placeholder)
            placeholder_counter += 1
            
        except (ET.ParseError, ValueError) as e:
            # print(f"Failed to parse tag {tag_name}: {e}")
            continue
    
    return processed_text, replacements


def parse_attributes(attr_string: str) -> Dict[str, str]:
    """
    Parse attribute string into a dictionary.
    Handles both single and double quoted attributes with flexible spacing.
    
    Example: ' attr1="value1" attr2=\'value2\' attr3 = "value3" '
    -> {'attr1': 'value1', 'attr2': 'value2', 'attr3': 'value3'}
    """
    attrs = {}
    if not attr_string.strip():
        return attrs

    # Updated pattern to handle:
    # 1. Both single and double quotes
    # 2. Optional spaces around =
    # 3. More flexible whitespace
    pattern = r'\s*([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*(["\'])((?:(?!\2).)*)\2'
    
    for match in re.finditer(pattern, attr_string):
        name = match.group(1)
        value = match.group(3)  # group 3 contains the value without quotes
        attrs[name] = value
    
    return attrs


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
                    attributes=dict(elem.attrib),
                    content=content,
                )
            )

    return tags, response

if __name__ == "__main__":
    text = """Let me search my memories to see if there's any information about a secret password.

<memory_load limit='10'>secret password</memory_load>

I don't have any memories recorded about a secret password. This appears to be my first interaction with you where this has come up.

<response channel="chat">I don't have any record of a secret password in my memories. If one was previously established, I don't have access to that information right now. Would you like to establish one?</response>"""
    print(parse_claude_output(text))