from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QStyle, QPushButton
from PyQt6.QtCore import QSize, Qt
from components.webview import BaseWebView
from components.searchbar.component import SearchBar
from utils.styles import load_stylesheet
from utils.icons import get_icon_path, load_icon

class BrowserTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setStyleSheet(load_stylesheet('tab-container.qss'))
        
        close_icon_path = get_icon_path('close.svg').as_posix()
        self.setStyleSheet(self.styleSheet() + f"""
            QTabBar::close-button {{
                image: url("{close_icon_path}");
                width: 24px;
                height: 24px;
            }}
            QTabBar::close-button:hover {{
                background: #454545;
                border-radius: 4px;
            }}
            QTabBar {{
                qproperty-elideMode: ElideRight;
            }}
        """)
        
        plus_button = QPushButton(self)
        plus_button.setIcon(load_icon('plus.svg'))
        plus_button.setFixedSize(32, 32)
        plus_button.setStyleSheet("""
            QPushButton {
                background: #2d2d2d;
                border: none;
                border-radius: 6px;
                margin: 2px;
                padding: 4px;
            }
            QPushButton:hover {
                background: #353535;
            }
        """)
        plus_button.clicked.connect(self.create_new_tab)
        self.setCornerWidget(plus_button, Qt.Corner.TopRightCorner)
        
        self.setMovable(True)
        
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

        # todo: allow user to change search engine
        web_view.load_url("https://duckduckgo.com")
        return web_view
        
    def close_tab(self, index):
        if self.count() > 1:
            self.removeTab(index)
        
    def update_tab_title(self, title, web_view):
        for i in range(self.count()):
            if web_view in self.widget(i).findChildren(BaseWebView):
                self.setTabText(i, title or "New Tab")