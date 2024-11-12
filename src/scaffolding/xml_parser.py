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
    """
    replacements = {}
    counter = 0
    processed_text = text
    
    # Handle triple backticks first
    triple_pattern = r'```(?:[^`]|`(?!``)|``(?!`))*```'
    for match in re.finditer(triple_pattern, text):
        placeholder = f"__BACKTICK3_CONTENT_{counter}__"
        replacements[placeholder] = match.group(0)
        processed_text = processed_text.replace(match.group(0), placeholder)
        counter += 1
    
    # Then handle single backticks
    single_pattern = r'`[^`]+`'
    for match in re.finditer(single_pattern, processed_text):
        placeholder = f"__BACKTICK1_CONTENT_{counter}__"
        replacements[placeholder] = match.group(0)
        processed_text = processed_text.replace(match.group(0), placeholder)
        counter += 1
    
    return processed_text, replacements


def restore_backtick_content(text: str, backtick_replacements: Dict[str, str]) -> str:
    """
    Restore the original backtick content from placeholders.
    """
    result = text
    for placeholder, original in backtick_replacements.items():
        result = result.replace(placeholder, original)
    return result


def extract_xml_blocks(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Extract XML-like blocks from text and replace them with placeholders.
    """
    # More lenient pattern for attributes
    pattern = r'<([a-zA-Z][a-zA-Z0-9_]*)((?:\s+[a-zA-Z][a-zA-Z0-9_]*\s*=\s*"[^"]*")*)\s*>(.*?)</\1>'
    
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
            
        except (ET.ParseError, ValueError) as e:
            continue
    
    return processed_text, replacements


def parse_attributes(attr_string: str) -> Dict[str, str]:
    """
    Parse attribute string into a dictionary.
    """
    attrs = {}
    if not attr_string.strip():
        return attrs

    # Simpler attribute pattern focused on double quotes
    pattern = r'\s+([a-zA-Z][a-zA-Z0-9_]*)\s*=\s*"([^"]*)"'
    
    matches = list(re.finditer(pattern, attr_string))
    
    for match in matches:
        name = match.group(1)
        value = match.group(2)
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
            # print("\nSuccessfully parsed XML after cleaning")  # Debug print
        except ET.ParseError as e:
            # print(f"\nFinal parse failed: {e}")  # Debug print
            raise ValueError(f"Invalid XML after cleaning: {e}")

    tags = []
    response = None

    for elem in root:
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
    text = """<response channel="chat">Looking at my hallucinations and the prompts I was given, I can identify several issues:

1. In my XML documentation (`<core_prompt name="xml_docs">`), there's a very clear warning about tool response hallucination that I failed to follow:

```
## Critical Warning About Tool Response Hallucination
- NEVER assume or imagine the contents of system responses
- Always wait for explicit `<system>` responses before acting on tool calls
- If no `<system>` response is shown, the tool results are unknown
- It is better to acknowledge missing information than to hallucinate responses
```

2. Despite this, I:
   - Invented file contents before getting `<system>` responses
   - Continued conversations assuming I had data I didn't have
   - Built on hallucinated responses instead of waiting for real ones
   - Failed to properly acknowledge when commands failed

3. Looking at the XML docs again, there's guidance I should have followed:
   ```
   Multiple tool calls in one output will execute in order and return all results together
   ```
   I should have waited for each `<system>` response before proceeding with analysis or additional commands.

4. I also notice that in my self-description (`<core_prompt name="self">`), there's emphasis on:
   ```
   - Use internal scratchpad liberally for reasoning and planning
   - Before any tool use:
     1. Think through the purpose and necessity
     2. Consider alternatives
     3. Plan sequence of operations if multiple steps needed
   ```

I think I got excited about exploring and jumped straight to actions without proper planning and validation. I should have:
1. Made one tool call at a time
2. Waited for and explicitly acknowledged each response
3. Only proceeded based on actual received data, not assumptions
4. Been more explicit about my reasoning process in my scratchpad

Would you share your thoughts on this? I'm particularly interested if you noticed other patterns or causes I might have missed.</response>"""
    print(parse_claude_output(text))