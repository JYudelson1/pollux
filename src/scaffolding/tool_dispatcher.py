from typing import *

from src.tools.memory import MemoryTool
from src.tools.source import SourceTool
from src.tools.files import FilesTool
from src.tools.update_core_prompt import UpdateCorePromptTool

from src.scaffolding.xml_parser import ParsedTag

class ToolServer:
    def __init__(self) -> None:
        self.memory_tool: MemoryTool = MemoryTool()
        self.source_tool: SourceTool = SourceTool()
        self.files_tool: FilesTool = FilesTool()
        self.update_core_prompt_tool: UpdateCorePromptTool = UpdateCorePromptTool()
        
    def use_tools(self, tools: List[ParsedTag]) -> Tuple[Optional[str], Optional[str]]:
        """Uses the given tools, and returns all of the outcomes

        Arguments:
            tools -- A list of tags to be dispatched

        Returns:
            (informational_messages, simple_success_messages). Every tool has a success message when it completes, but not all are informational. By default, all informational messages and all errors should be returned to the agent immediately. Simple success messages can instead be returned at the next user query time.
        """
        informational_messages = ""
        simple_success_messages = ""
        
        for tool in tools:
            has_info, out = self.use_tool(tool)
            if has_info:
                informational_messages += out
                informational_messages += "\n"
            else:
                simple_success_messages += out
                simple_success_messages += "\n"
                
        informational_messages = informational_messages if informational_messages is not "" else None
        simple_success_messages = simple_success_messages if simple_success_messages is not "" else None
        
        return (informational_messages, simple_success_messages)
        
        
    def use_tool(self, tag: ParsedTag) -> Tuple[bool, str]:
        """Returns the output of a call, and whether it needs to be parsed immediately. The bool should be true for informative outputs and errors. An empty success message should be false, and will only be surfaced as needed."""
        try:
            output = self._try_use_tool(tag)
            return (output is not None, f'<system type="{tag.tag}" status="success">{output if output is not None else ""}</system>')
        except Exception as e:
            return (True, f'<system type="{tag.tag}" status="error">{e}</system>')
        
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
        elif tag.tag == "update_core_prompt":  # Add this section
            return self.update_core_prompt_tool.execute(content=tag.content, **tag.attributes)
        else:
            raise NotImplementedError