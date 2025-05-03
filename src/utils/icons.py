from pathlib import Path
from PyQt6.QtGui import QIcon

def load_icon(name: str) -> QIcon:
    current_dir = Path(__file__).parent.parent
    icon_path = current_dir / 'resources' / 'icons' / name
    
    if not icon_path.exists():
        return QIcon()
        
    return QIcon(str(icon_path))

def get_icon_path(name: str) -> Path:
    current_dir = Path(__file__).parent.parent
    icon_path = current_dir / 'resources' / 'icons' / name
    return icon_path