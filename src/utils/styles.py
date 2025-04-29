import os

def load_stylesheet(name: str) -> str:
    """Load a stylesheet from the resources/styles directory"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    style_path = os.path.join(current_dir, 'resources', 'styles', name)
    
    if not os.path.exists(style_path):
        return ""
        
    with open(style_path, 'r') as f:
        return f.read()