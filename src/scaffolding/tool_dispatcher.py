from src.tools.memory import MemoryTool
from src.scaffolding.xml_parser import ParsedTag

class ToolServer:
    def __init__(self) -> None:
        self.memory_tool: MemoryTool = MemoryTool()
        
    def use_tool(self, tag: ParsedTag) -> str:
        try:
            output = self._try_use_tool(tag)
            return f'<system type="{tag.tag}" status="success">{output}</system>'
        except Exception as e:
            return f'<system type="{tag.tag}" status="error">{e}</system>'
        
    def _try_use_tool(self, tag: ParsedTag) -> str:
        if tag.tag == "memory_load":
            self.memory_tool.load_memories(query=tag.content, **tag.attributes)
        elif tag.tag == "memory_save":
            self.memory_tool.load_memories(text=tag.content, **tag.attributes)
        elif tag.tag == "memory_delete":
            self.memory_tool.delete_memory(uuid=tag.attributes["id"])
        else:
            raise NotImplementedError