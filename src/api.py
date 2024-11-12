import anthropic
import dotenv
import pathlib
from typing import *
from datetime import datetime

from src.core_prompts.prompts import load_system_prompt
from src.scaffolding.status import basic_status
from src.scaffolding.tool_dispatcher import ToolServer
from src.scaffolding.xml_parser import ParsedTag
from src.utils import ROOT

dotenv.load_dotenv()

client = anthropic.Anthropic()
# claude_model = "claude-3-5-sonnet-20241022"
claude_model = "claude-3-5-sonnet-20240620"
max_tokens_per_message = 8192


def message_from_text(text: str) -> Dict:
    return {"role": "user", "content": [{"type": "text", "text": text}]}


class Channel:
    CHAT = (0,)
    SMS = 1


class Conversation:
    messages: List[Dict]
    tool_server: ToolServer
    chat_storage: pathlib.Path

    def __init__(self, with_system_prompt: bool = True) -> None:
        self.messages = []
        self.tool_server = ToolServer()
        
        now = datetime.now()
        self.chat_storage = ROOT / "data" / "chat_storage" / f"{now.month}_{now.day}_{now.year}__{now.hour}:{now.minute}:{now.second}.txt"

        if with_system_prompt:
            system_prompt = load_system_prompt()
            system_message = message_from_text(system_prompt)
            system_message["content"][0]["cache_control"] = {"type": "ephemeral"}
            self.messages.append(system_message)

            status = basic_status()
            status_message = message_from_text(status)
            self.messages.append(status_message)
            
            self.messages.append({
                "role": "assistant",
                "content":
                    [{"type": "text", "text": 'Let me check my memories. \n<memory_load limit="15" sort="date"></memory_load>'}]
            })
            
            
            memory_response = self.tool_server.use_tools([ParsedTag(tag="memory_load", attributes={"limit": "15", "sort": "date"}, content=" ")])
            with open(self.chat_storage, "a+") as f:
                f.write(memory_response)
            memory_message = message_from_text(memory_response)
            memory_response
            memory_message["content"][0]["cache_control"] = {"type": "ephemeral"}
            self.messages.append(memory_message)
            
            
    def _send_and_receive(self) -> str:
        response = client.beta.prompt_caching.messages.create(
            model=claude_model,
            max_tokens=max_tokens_per_message,
            messages=self.messages,
            
        )

        if response.type == "error":
            raise "API ERROR!"
        elif response.type == "message":
            content = response.content
            self.messages.append(
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": block.text} for block in content
                    ],
                }
            )
            assert len(content) == 1
            response_text = content[0].text
            with open(self.chat_storage, "a+") as f:
                f.write(response_text)
                
            return response_text

    # TODO: Add support for images
    # TODO: Add handling for running out of tokens
    # TODO: Handle running out of API Credits
    def query(self, user_content: str, channel: Channel) -> str:
        if channel == Channel.CHAT:
            channel = "chat"
        elif channel == Channel.SMS:
            channel = "sms"

        user_content = f"<user_input channel={channel}>{user_content}</user_input>"

        self.messages.append(message_from_text(user_content))
        
        with open(self.chat_storage, "a") as f:
            f.write(user_content)

        return self._send_and_receive()

    def last_assistant_block(self) -> List[Dict]:
        messages = []
        seen_assistant = False
        for message in self.messages[::-1]:
            if message["role"] == "assistant" and seen_assistant:
                return messages
            else:
                if message["role"] == "assistant":
                    seen_assistant = True
                messages.insert(0, message)
        return messages
    
    def use_tools(self, tool_calls: List[ParsedTag]) -> Optional[str]:
        # If the tools provide system responses to be processed by 
        # the assistant, this will call the tools, call the model,
        # and then finally return the new response.
        # If none of the tools need to be looked at, simply processes the 
        # tool calls and returns None
        
        system_response = self.tool_server.use_tools(tool_calls)
        
        if system_response is not None:
            with open(self.chat_storage, "a+") as f:
                f.write(system_response)
            self.messages.append(message_from_text(system_response))
            return self._send_and_receive()
