from src.utils import ROOT

class SourceTool():
    def __init__(self) -> None:
        self.source_path = ROOT / "src"
    
    def read_src(self, path: str) -> str:
        path = self.source_path / path

        if not path.exists():
            raise FileNotFoundError(f"Source file {path} not found")
        if not path.is_file():
            raise ValueError(f"{path} is not a file")
        return path.read_text()
        
    def list_src(self, path: str = "") -> str:
        if path != "":
            path = self.source_path / path
        else:
            path = self.source_path
            
        if not path.exists():
            raise FileNotFoundError(f"Source directory {path} not found")
        if not path.is_dir():
            raise ValueError(f"{path} is not a directory")
            
        files = [f.relative_to(self.source_path).as_posix() 
                for f in path.glob("*")]
        return "\n".join(sorted(files))