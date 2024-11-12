## Update Core Prompt Tool

This tool allows for updating the system core prompts that define Claude's behavior and understanding. Never use this tool without asking the user, as you could remove vital information.

### Usage
```xml
<update_core_prompt prompt="self" mode="append">
New information about Claude's capabilities...
</update_core_prompt>

<update_core_prompt prompt="user" mode="overwrite">
Complete new user profile...
</update_core_prompt>
```

### Parameters
- `prompt`: (required) Which prompt to update. Must be one of: "self", "user", "xml_docs", "main", "morning", "reflection"
- `mode`: (optional) "append" or "overwrite". Defaults to "append"

### Behavior
- In append mode, new content is added to the end of existing content with appropriate newline separation
- In overwrite mode, new content completely replaces existing content
- Creates prompt file if it doesn't exist
- Validates prompt names against allowed list
- Returns success message with operation details

### Integration Notes
- Core prompts are stored as text files in the core_prompts directory
- Each prompt type has its own file (self.txt, user.txt, xml_docs.txt)
- Tool needs to be registered in tool_dispatcher.py
- Error handling for invalid prompt names happens at tool level