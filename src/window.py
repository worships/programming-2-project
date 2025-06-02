from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QStatusBar
from components.toolbar import BrowserToolbar
from components.tabbar import BrowserTabWidget
from components.webview import BaseWebView
from utils.settings import settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 1024, 768) # 1024x768
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        if settings.get("settings", "enable_status_bar", default=True):
            self.status_bar.show()
            self.status_bar.showMessage("Ready")
        else:
            self.status_bar.hide()
        
        self.setMenuBar(BrowserToolbar(self))
        
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tab_widget = BrowserTabWidget(self)
        layout.addWidget(self.tab_widget)
        
        container = self.tab_widget.currentWidget()
        self.web_view = container.findChild(BaseWebView)
        if self.web_view:
            self.web_view.statusMessage.connect(self.status_bar.showMessage)
        
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
            
    def toggle_status_bar(self, checked):
        if checked:
            self.status_bar.show()
            self.status_bar.showMessage("Ready")
        else:
            self.status_bar.hide()
        
            settings.set("settings", "enable_status_bar", value=checked)
            
    def _on_tab_changed(self, index):
        container = self.tab_widget.widget(index)
        if container:
            self.web_view = container.findChild(BaseWebView)
            if self.web_view:
                self.web_view.statusMessage.connect(self.status_bar.showMessage)