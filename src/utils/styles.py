from pathlib import Path

def load_stylesheet(name: str) -> str:
    current_dir = Path(__file__).parent.parent
    style_path = current_dir / 'resources' / 'styles' / name
    
    if not style_path.exists():
        return ""
        
    return style_path.read_text()