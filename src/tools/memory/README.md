# Memory Tool

Persistent memory system using Voyage AI embeddings for semantic search and retrieval. Supports importance-weighted, time-aware memory management.

## Usage

### XML Interface
```xml
<!-- Save a new memory -->
<memory_save importance="0.8">Memory content to save</memory_save>

<!-- Load memories -->
<memory_load limit="5" sort="combined">query text</memory_load>

<!-- Delete a memory -->
<memory_delete id="memory-uuid"></memory_delete>
```

### Attributes

#### memory_save
- `importance`: Float 0-1 as String (required) - Memory importance weight

#### memory_load
- `limit`: Integer as String (optional, default="5") - Maximum memories to return
- `sort`: String (optional, default="combined") - Sorting method:
  - "combined": Weighted combination of importance, recency, and relevance
  - "relevance": Pure semantic similarity
  - "date": Most recent first

#### memory_delete
- `id`: String (required) - UUID of memory to delete

### Examples
```xml
<!-- Save important memory -->
<memory_save importance="0.9">Critical system configuration detail</memory_save>

<!-- Load recent memories about tools -->
<memory_load limit="10" sort="date">tool implementation</memory_load>

<!-- Load most relevant memories -->
<memory_load sort="relevance">specific topic</memory_load>
```

## Implementation Details

### Dependencies
- Voyage AI for embeddings
- pickle for persistence
- pathlib for file handling

### Key Classes
- `Memory`: Dataclass containing:
  - content: str
  - timestamp: datetime
  - embedding: numpy array
  - uuid: UUID
  - importance: float

### Scoring System
Combined score = (IMPORTANCE_WEIGHT * importance) + (RECENCY_WEIGHT * time_score) + (RELEVANCE_WEIGHT * relevance)
- IMPORTANCE_WEIGHT = 0.1
- RECENCY_WEIGHT = 0.2
- RELEVANCE_WEIGHT = 1.0

### Error Handling
- EOFError handled during database initialization
- Invalid sort method raises ValueError
- UUID parsing errors handled in delete operation

## Development Notes

### Storage
- Memories stored in memories.pkl
- Pickle format for full object persistence
- Located alongside tool implementation

### Future Improvements
- Memory consolidation/summarization
- Importance auto-adjustment
- Memory cleanup strategies
- Backup/restore capabilities