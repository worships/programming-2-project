from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal

class BaseWebView(QWidget):
    statusMessage = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._web_view = QWebEngineView()
        self._web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._is_loading = False
        self._setup_ui()
        self._setup_signals()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._web_view)
        self.setLayout(layout)
        
    def _setup_signals(self):
        self._web_view.loadStarted.connect(self._on_load_started)
        self._web_view.loadFinished.connect(self._on_load_finished)
        self._web_view.urlChanged.connect(self._on_url_changed)
    
    def _on_load_started(self):
        self._is_loading = True
        self.statusMessage.emit("Loading...")
        
    def _on_load_finished(self, success):
        self._is_loading = False
        self.statusMessage.emit("Ready")
    
    def _on_url_changed(self, url):
        if not self._is_loading:
            self.statusMessage.emit("Ready")
        
    def load_url(self, url: str):
        self._web_view.setUrl(QUrl(url))
        
    def get_web_view(self) -> QWebEngineView:
        return self._web_view
    
    def go_back(self):
        self._web_view.back()
        
    def go_forward(self):
        self._web_view.forward()
        
    def refresh(self):
        self._is_loading = True
        self.statusMessage.emit("Reloading...")
        self._web_view.reload()