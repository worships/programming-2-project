from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from utils.icons import load_icon
from utils.styles import load_stylesheet

class SecondaryControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.web_view = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)

        self.home_button = self._create_button('home.svg')
        layout.addWidget(self.home_button)

    def _create_button(self, icon_name):
        button = QPushButton()

        button.setIcon(load_icon(icon_name))
        button.setFixedSize(28, 28)
        button.setStyleSheet(load_stylesheet('search-control-icons.qss'))

        return button

    def set_web_view(self, web_view):
        self.web_view = web_view
        
        if self.web_view:

            # todo: allow user to change search engine
            self.home_button.clicked.connect(lambda: self.web_view.load_url("https://duckduckgo.com"))