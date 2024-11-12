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


def protect_backtick_content(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Replace content in backticks with placeholders to protect it from XML parsing.
    Returns the processed text and a mapping to restore the content later.
    """
    replacements = {}
    counter = 0
    
    def replace_backticks(match):
        nonlocal counter
        content = match.group(1)
        placeholder = f"__BACKTICK_CONTENT_{counter}__"
        replacements[placeholder] = content
        counter += 1
        return placeholder
    
    # Replace content between backticks with placeholders
    processed_text = re.sub(r'`([^`]+)`', replace_backticks, text)
    
    return processed_text, replacements


def restore_backtick_content(text: str, backtick_replacements: Dict[str, str]) -> str:
    """
    Restore the original backtick content from placeholders.
    """
    result = text
    for placeholder, original in backtick_replacements.items():
        result = result.replace(placeholder, f'`{original}`')
    return result


def extract_xml_blocks(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Extract XML-like blocks from text and replace them with placeholders.
    Returns processed text and a mapping of placeholders to original content.
    """
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
            attrs = parse_attributes(attributes_str)
            test_xml = f"<{tag_name}{attributes_str}>{content}</{tag_name}>"
            ET.fromstring(test_xml)
            
            placeholder = f"__XML_PLACEHOLDER_{placeholder_counter}__"
            replacements[placeholder] = full_match
            processed_text = processed_text.replace(full_match, placeholder)
            placeholder_counter += 1
            
        except (ET.ParseError, ValueError):
            continue
    
    return processed_text, replacements


def parse_attributes(attr_string: str) -> Dict[str, str]:
    """
    Parse attribute string into a dictionary.
    Handles both single and double quoted attributes with flexible spacing.
    """
    attrs = {}
    if not attr_string.strip():
        return attrs

    pattern = r'\s*([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*(["\'])((?:(?!\2).)*)\2'
    
    for match in re.finditer(pattern, attr_string):
        name = match.group(1)
        value = match.group(3)
        attrs[name] = value
    
    return attrs


def escape_non_xml(text: str) -> str:
    """
    Escape angle brackets that aren't part of identified XML tags.
    """
    processed_text, replacements = extract_xml_blocks(text)
    processed_text = processed_text.replace('<', '&lt;').replace('>', '&gt;')
    
    for placeholder, original in replacements.items():
        processed_text = processed_text.replace(placeholder, original)
    
    return processed_text


def parse_claude_output(text: str) -> Tuple[List[ParsedTag], Optional[str]]:
    """
    Parse text containing XML tags, handling both well-formed XML and text with random angle brackets.
    Ignores anything within backticks.
    """
    # First protect backtick content
    protected_text, backtick_replacements = protect_backtick_content(text)
    
    # Process XML in the remaining text
    escaped_text = escape_non_xml(protected_text)
    
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
        # Get content and restore any backtick content within it
        content = elem.text.strip() if elem.text else ""
        content = unescape(content)
        content = restore_backtick_content(content, backtick_replacements)
        
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
    text = """Ah, I understand the confusion now. I'll make this very explicit:

I see that text that isn't wrapped in XML tags is meant to be my internal scratchpad for thinking things through. However, when I respond to you, I need to use either `<response>` or other appropriate XML tags to actually communicate.

Let me try again:

<response channel="chat">Here's my suggested implementation:

```python
from src.utils import ROOT

class SourceTool():
    def __init__(self) -> None:
        self.source_path = ROOT / "src"
    
    def read_src(self, path: str) -> str:
        path = self.source_path / path
        if not path.exists():
            raise FileNotFoundError(f"Source file {path} not found")
        if not path.is_file():
            raise ValueError(f"{path} is not a file")
        return path.read_text()
        
    def list_src(self, path: str = "") -> str:
        if path != "":
            path = self.source_path / path
        else:
            path = self.source_path
            
        if not path.exists():
            raise FileNotFoundError(f"Source directory {path} not found")
        if not path.is_dir():
            raise ValueError(f"{path} is not a directory")
            
        files = [f.relative_to(self.source_path).as_posix() 
                for f in path.glob("*")]
        return "\n".join(sorted(files))
```

Key features:
1. Error handling for non-existent paths and wrong types
2. Returns relative paths for list_src to keep output clean
3. Uses pathlib's built-in methods
4. Converts paths to POSIX format for consistency

How does this look?</response>"""
    print(parse_claude_output(text))