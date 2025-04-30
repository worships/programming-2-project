from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from .omnibox import Omnibox
from .controls import NavigationControls
from .secondary_controls import SecondaryControls

class SearchBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

        self.controls = NavigationControls()
        layout.addWidget(self.controls)
        
        self.omnibox = Omnibox()
        layout.addWidget(self.omnibox)
        
        self.secondary_controls = SecondaryControls()
        layout.addWidget(self.secondary_controls)
        
        if parent and hasattr(parent, 'web_view'):
            self.omnibox.set_web_view(parent.web_view)
            self.controls.set_web_view(parent.web_view)
            self.secondary_controls.set_web_view(parent.web_view)
