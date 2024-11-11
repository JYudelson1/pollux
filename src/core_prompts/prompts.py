from pathlib import Path

def load_simple_prompt(name: str) -> str:
    if name in ["morning", "reflection", "self", "user", "xml_docs"]:
        with Path(__file__).with_name(f'{name}.txt').open('r') as file:
            return file.read()
    else:
        assert f"{name} is not a simple prompt!"
        
def load_system_prompt() -> str:
    with Path(__file__).with_name('main.txt').open('r') as file:
        main = file.read()
    user_prompt = load_simple_prompt("user")
    self_prompt = load_simple_prompt("self")
    xml_docs_prompt = load_simple_prompt("xml_docs")
    
    return main.format(
        user_prompt=user_prompt, 
        self_prompt=self_prompt, 
        xml_docs_prompt=xml_docs_prompt
    )
    
def load_reflection_prompt(minutes: int) -> str:
    with Path(__file__).with_name('reflection.txt').open('r') as file:
        reflection = file.read()
    return reflection.format(
        minutes=minutes
    )