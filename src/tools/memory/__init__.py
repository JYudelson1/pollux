import pathlib
import pickle as pkl
from typing import *
from uuid import UUID

from .memory import Memory, make_memory, relevance_scores, time_score
from .xml import make_xml

IMPORTANCE_WEIGHT = 0.2
RECENCY_WEIGHT = 0.2
RELEVANCE_WEIGHT = 1.0

class MemoryTool():
    def __init__(self) -> None:
        self.db_path = pathlib.Path(__file__).with_name("memories.pkl")
        with open(self.db_path, "rb+") as f:
            try:
                self.db: List[Memory] = pkl.load(f)
            except EOFError:
                self.db: List[Memory] = []
                                            
    def _save(self):
        with open(self.db_path, "wb") as f:
            pkl.dump(self.db, f)
    
    def save_memory(self, text: str, importance: str):
        memory = make_memory(text, float(importance))
        self.db.append(memory)
        self._save()
        
    def delete_memory(self, uuid: str) -> bool:
        # Returns true if a memory was successfully deleted
        uuid = UUID(hex=uuid)
        for i, mem in enumerate(self.db):
            if mem.uuid == uuid:
                del self.db[i]
                self._save()
                return True
        return False
    
    def load_memories(self, query: str, sort: str = "combined", limit: str = "5") -> str:
        
        if len(self.db) == 0:
            return "No memories yet saved"
        
        relevances = relevance_scores(query, self.db)
        
        if sort == "relevance":
            sorted_mems = sorted(self.db, key=lambda mem: relevances[mem.uuid], reverse=True)
        elif sort == "date":
            sorted_mems = sorted(self.db, key=lambda mem: mem.timestamp, reverse=True)
        elif sort == "combined":
            sorted_mems = sorted(self.db, key=lambda mem: 
                (IMPORTANCE_WEIGHT * mem.importance) 
                + (RECENCY_WEIGHT * time_score(mem)) 
                + (RELEVANCE_WEIGHT * relevances[mem.uuid]), 
                reverse=True
            )
        else:
            raise f"{sort} is an invalid argument!"
            
        result = sorted_mems[:int(limit)]
        
        return make_xml(result, relevances=relevances)
    
            
    
            
    
        
