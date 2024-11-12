from typing import *

from src.tools.memory import MemoryTool
from src.scaffolding.xml_parser import ParsedTag

class ToolServer:
    def __init__(self) -> None:
        self.memory_tool: MemoryTool = MemoryTool()
        
    def use_tools(self, tools: List[ParsedTag]) -> Optional[str]:
        system_response = ""
        
        for tool in tools:
            out = self.use_tool(tool)
            if out is not None:
                system_response += out
                system_response += "\n"
                
        if system_response != "":
            return system_response
        
    def use_tool(self, tag: ParsedTag) -> Optional[str]:
        try:
            output = self._try_use_tool(tag)
            if output is not None:
                return f'<system type="{tag.tag}" status="success">{output}</system>'
        except Exception as e:
            return f'<system type="{tag.tag}" status="error">{e}</system>'
        
    def _try_use_tool(self, tag: ParsedTag) -> Optional[str]:
        if tag.tag == "memory_load":
            return self.memory_tool.load_memories(query=tag.content, **tag.attributes)
        elif tag.tag == "memory_save":
            return self.memory_tool.save_memory(text=tag.content, **tag.attributes)
        elif tag.tag == "memory_delete":
            return self.memory_tool.delete_memory(uuid=tag.attributes["id"])
        else:
            raise NotImplementedError