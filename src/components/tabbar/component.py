from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from components.webview import BaseWebView
from components.searchbar.component import SearchBar
from utils.styles import load_stylesheet

class BrowserTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setStyleSheet(load_stylesheet('tab-container.qss'))
        self.create_new_tab()
        
    def create_new_tab(self):
        container = QWidget()
        container.setObjectName("tab-container")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        web_view = BaseWebView(self)
        search_bar = SearchBar(self)
        
        layout.addWidget(search_bar)
        layout.addWidget(web_view)
        
        index = self.addTab(container, "New Tab")
        self.setCurrentIndex(index)

        web_view.get_web_view().titleChanged.connect(
            lambda title, view=web_view: self.update_tab_title(title, view)
        )

        search_bar.omnibox.set_web_view(web_view)
        search_bar.controls.set_web_view(web_view)
        search_bar.secondary_controls.set_web_view(web_view)

        web_view.load_url("https://duckduckgo.com")
        return web_view
        
    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
        
    def update_tab_title(self, title, web_view):
        for i in range(self.count()):
            if web_view in self.widget(i).findChildren(BaseWebView):
                self.setTabText(i, title or "New Tab")
                break