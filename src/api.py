import anthropic
import dotenv
from typing import *

from src.core_prompts.prompts import load_system_prompt
from src.scaffolding.status import basic_status

dotenv.load_dotenv()

client = anthropic.Anthropic()
claude_model = "claude-3-5-sonnet-20241022"
max_tokens_per_message = 4096

def message_from_text(text: str) -> Dict:
    return {
            "role": "user", 
            "content": [{
                "type": "text", 
                "text": text
            }]
        }

class Conversation:
    messages: List[Dict]
    
    def __init__(self, with_system_prompt: bool = True) -> None:
        self.messages = []
        
        if with_system_prompt:
            system_prompt = load_system_prompt()
            system_message = message_from_text(system_prompt)
            self.messages.append(system_message)
            
            status = basic_status()
            status_message = message_from_text(status)
            self.messages.append(status_message)

        
    
    # TODO: Add support for images
    # TODO: Add handling for running out of tokens
    # TODO: Handle running out of API Credits
    def query(self, user_content: str) -> str:
        
        self.messages.append(message_from_text(user_content))
        
        response = client.messages.create(
            model=claude_model,
            max_tokens=max_tokens_per_message,
            messages=self.messages
        )
        
        if response.get("type") == "error":
            raise "API ERROR!"
        elif response.get("type") == "message":
                content = response["content"]
                self.append({
                    "role": "assistant",
                    "content": content
                })
                assert len(content) == 1
                response_text = content["text"]
                return response_text
            
    def last_assistant_block(self) -> List[Dict]:
        messages = []
        seen_assistant = False
        for message in self.messages[::-1]:
            if messages["role"] == "assistant" and seen_assistant:
                return messages
            else:
                if messages["role"] == "assistant":
                    seen_assistant = True
                messages.insert(0, message)
        return messages
        