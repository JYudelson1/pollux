from .memory import Memory
from datetime import datetime
from typing import *
from uuid import UUID

def make_xml_once(memory: Memory, relevance: float) -> str:
    return f'<memory id="{memory.uuid}" date="{timestamp(memory.timestamp)}" relevance={relevance:.3f}" importance="{memory.importance}">\n\t{memory.content}\n</memory>'

def make_xml(sorted_memories: List[Memory], relevances: Dict[UUID, float]) -> str:
    text = '<system type="memory_load">'
    
    for memory in sorted_memories:
        rel = relevances[memory.uuid]
        text += make_xml_once(memory=memory, relevance=rel)
    
    text += '</system>'
    
    return text

def timestamp(dt: datetime) -> str:
    return f"{dt.month} {dt.day} {dt.year} ({dt.hour}:{dt.minute})"