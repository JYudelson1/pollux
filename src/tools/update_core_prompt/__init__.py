from src.utils import ROOT

class UpdateCorePromptTool:
    """Tool for updating system core prompts."""
    
    def __init__(self):
        self.core_prompts_dir = ROOT / "src" / "core_prompts"
        self.valid_prompts = {"self", "user", "xml_docs", "main", "morning", "reflection"}  # Add others as needed
        
    def execute(self, content: str, prompt: str, mode: str = "append"):
        # Validate prompt name
        if prompt not in self.valid_prompts:
            raise ValueError(f"Invalid prompt name. Must be one of: {self.valid_prompts}")
            
        prompt_path = self.core_prompts_dir / f"{prompt}.txt"
        
        # Ensure directory exists
        self.core_prompts_dir.mkdir(parents=True, exist_ok=True)
        
        if mode == "append":
            # In append mode, add newlines to separate content
            with open(prompt_path, "a") as f:
                f.write("\n" + content)
        else:  # overwrite mode
            with open(prompt_path, "w") as f:
                f.write(content)