from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy
from components.webview import BaseWebView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 1024, 768) # 1024x768
        
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.web_view = BaseWebView(self)
        layout.addWidget(self.web_view)
        
        # test a url
        self.web_view.load_url("https://www.duckduckgo.com")