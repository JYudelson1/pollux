import pathlib
from typing import Optional

from src.utils import ROOT

class FilesTool:
    def __init__(self) -> None:
        # Base path for all file operations - this would be set to the reserved folder
        self.base_path = ROOT / "data" / "files"
        
        self.write_file(content="blah", path="test.txt")
    
    def write_file(self, path: str, content: str, mode: str = "overwrite") -> None:
        """Write content to a file in the reserved directory"""
        full_path = (self.base_path / path).resolve()
        
        # Security check - ensure we're still in base_path
        if self.base_path not in full_path.parents:
            raise ValueError("Cannot write outside reserved directory")
            
        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with appropriate mode
        write_mode = "w" if mode == "overwrite" else "a"
        with open(full_path, write_mode) as f:
            f.write(content)
    
    def read_file(self, path: str) -> str:
        """Read content from a file in the reserved directory"""
        full_path = (self.base_path / path).resolve()
        
        # Security check
        if self.base_path not in full_path.parents:
            raise ValueError("Cannot read outside reserved directory")
            
        if not full_path.exists():
            raise FileNotFoundError(f"File {path} not found")
            
        with open(full_path, "r") as f:
            return f.read()
    
    def list_files(self, path: Optional[str] = None) -> str:
        """List files in the given directory (or root if none specified)"""
        if path is None:
            target_path = self.base_path
        else:
            target_path = (self.base_path / path).resolve()
            
        # Security check
        if self.base_path not in target_path.parents and target_path != self.base_path:
            raise ValueError("Cannot list outside reserved directory")
            
        if not target_path.exists():
            raise FileNotFoundError(f"Directory {path} not found")
            
        # Get all files and directories
        items = list(target_path.glob("*"))
        
        # Format output
        return "\n".join(str(item.relative_to(self.base_path)) for item in items)