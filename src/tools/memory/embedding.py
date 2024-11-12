import voyageai
import numpy as np
from typing import List

vo = voyageai.Client()

type Embedding = List[float]

def embed_memory(text: str) -> Embedding:
    return vo.embed([text], model="voyage-3", input_type="document").embeddings[0]

def embed_query(text: str) -> Embedding:
    return vo.embed([text], model="voyage-3", input_type="query").embeddings[0]