from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from utils.icons import load_icon
from utils.styles import load_stylesheet

class NavigationControls(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.web_view = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)

        self.back_button = self._create_nav_button('backwards.svg')
        self.forward_button = self._create_nav_button('forward.svg')
        self.refresh_button = self._create_nav_button('refresh.svg')

        layout.addWidget(self.back_button)
        layout.addWidget(self.forward_button)
        layout.addWidget(self.refresh_button)

    def _create_nav_button(self, icon_name):
        button = QPushButton()
        button.setIcon(load_icon(icon_name))
        button.setFixedSize(28, 28)
        button.setStyleSheet(load_stylesheet('search-control-icons.qss'))
        return button

    def set_web_view(self, web_view):
        self.web_view = web_view

        if self.web_view:
            self.back_button.clicked.connect(self.web_view.go_back)
            self.forward_button.clicked.connect(self.web_view.go_forward)
            self.refresh_button.clicked.connect(self.web_view.refresh)