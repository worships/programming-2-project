from PyQt6.QtWidgets import QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class BaseWebView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._web_view = QWebEngineView()
        self._setup_ui()
        
    def _setup_ui(self):
        # child classes implement this method
        pass
        
    def load_url(self, url: str):
        self._web_view.setUrl(QUrl(url))
        
    def get_web_view(self) -> QWebEngineView:
        return self._web_view
    
    def go_back(self):
        self._web_view.back()
        
    def go_forward(self):
        self._web_view.forward()
        
    def refresh(self):
        self._web_view.reload()