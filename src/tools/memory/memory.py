from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from uuid import uuid4, UUID

import numpy as np

from embedding import Embedding, embed_query, embed_memory

@dataclass
class Memory:
    content: str
    timestamp: datetime
    embedding: Embedding
    uuid: UUID
    importance: float
    
def make_memory(text: str, importance: float) -> Memory:
    embed = embed_memory(text)
    return Memory(content=text, timestamp=datetime.now(), embedding=embed, uuid=uuid4(), importance=importance)
    
def relevance_scores(text: str, memories: List[Memory]) -> Dict[UUID, float]:
    query_embed = embed_query(text)
    scores = np.dot([m.embedding for m in memories], query_embed)
    return {memories[i].uuid: scores[i] for i in range(len(memories))}

def time_score(memory: Memory) -> float:
    start = datetime(year=2024, month=11, day=11, hour=19, minute=30)
    total = datetime.now() - start
    
    span = memory.timestamp - start
    
    span / total
    
if __name__ == "__main__":
    m1 = make_memory("Pinapple apple banana pear")
    m2 = make_memory("Cars go vroom")
    
    print(relevance_scores("Fruit", [m1, m2]))