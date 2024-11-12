from typing import *

from src.tools.memory import MemoryTool
from src.tools.source import SourceTool
from src.tools.files import FilesTool

from src.scaffolding.xml_parser import ParsedTag

class ToolServer:
    def __init__(self) -> None:
        self.memory_tool: MemoryTool = MemoryTool()
        self.source_tool: SourceTool = SourceTool()
        self.files_tool: FilesTool = FilesTool()
        
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
            return f'<system type="{tag.tag}" status="success">{output if output is not None else ""}</system>'
        except Exception as e:
            return f'<system type="{tag.tag}" status="error">{e}</system>'
        
    def _try_use_tool(self, tag: ParsedTag) -> Optional[str]:
        if tag.tag == "memory_load":
            return self.memory_tool.load_memories(query=tag.content, **tag.attributes)
        elif tag.tag == "memory_save":
            return self.memory_tool.save_memory(text=tag.content, **tag.attributes)
        elif tag.tag == "memory_delete":
            return self.memory_tool.delete_memory(uuid=tag.attributes["id"])
        elif tag.tag == "src_read":
            return self.source_tool.read_src(**tag.attributes)
        elif tag.tag == "src_list":
            return self.source_tool.list_src(**tag.attributes)
        elif tag.tag == "file_write":
            self.files_tool.write_file(content=tag.content, **tag.attributes)
        elif tag.tag == "file_read":
            return self.files_tool.read_file(**tag.attributes)
        elif tag.tag == "file_list":
            return self.files_tool.list_files(**tag.attributes)
        else:
            raise NotImplementedError