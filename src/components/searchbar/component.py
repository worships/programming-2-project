from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from .omnibox import Omnibox
from .controls import NavigationControls

class SearchBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        self.controls = NavigationControls()
        layout.addWidget(self.controls)
        
        self.omnibox = Omnibox()
        if parent and hasattr(parent, 'web_view'):
            self.omnibox.set_web_view(parent.web_view)
            self.controls.set_web_view(parent.web_view)
            
        layout.addWidget(self.omnibox)
