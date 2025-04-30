from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QStatusBar
from components.webview import BaseWebView
from components.toolbar import BrowserToolbar
from components.searchbar.component import SearchBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Browser")
        self.setGeometry(100, 100, 1024, 768) # 1024x768
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        self.setMenuBar(BrowserToolbar(self))
        
        central_widget = QWidget()
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.web_view = BaseWebView(self)
        self.web_view.statusMessage.connect(self.status_bar.showMessage)
        
        self.search_bar = SearchBar(self)
        self.search_bar.omnibox.set_web_view(self.web_view)
        
        layout.addWidget(self.search_bar)
        layout.addWidget(self.web_view)
        
        self.web_view.get_web_view().urlChanged.connect(
            lambda url: self.search_bar.omnibox.update_url(url.url())
        )
        
        # todo: allow user to change search engine
        self.web_view.load_url("https://duckduckgo.com")
    
    def toggle_status_bar(self, checked):
        if checked:
            self.status_bar.show()
            self.status_bar.showMessage("Ready")
        else:
            self.status_bar.hide()