from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QTabBar, QLabel
from PyQt6.QtCore import QSize, Qt
from components.webview import BaseWebView
from components.searchbar.component import SearchBar
from utils.settings import settings
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
            QTabBar::tab:last {{
                min-width: 32px;
                max-width: 32px;
                min-height: 32px;
                max-height: 32px;
                background: #1c1c1c;
                border-radius: 6px;
                margin: 2px;
                padding: 2px;
            }}
            QTabBar::tab:last:hover {{
                background: #353535;
            }}
        """)
        
        self.setMovable(True)
        
        self.tabBar().installEventFilter(self)
        
        # create the new tab button
        plus_label = QLabel()
        plus_icon = load_icon('plus.svg')
        plus_label.setPixmap(plus_icon.pixmap(QSize(16, 16)))
        plus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plus_label.setFixedSize(QSize(32, 32))
        plus_label.setContentsMargins(8, 8, 8, 8)
        
        self.addTab(QWidget(), "")
        self.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
        self.tabBar().setTabButton(0, QTabBar.ButtonPosition.LeftSide, plus_label)
        
        self.create_new_tab()
        
    def eventFilter(self, obj, event):
        if obj == self.tabBar() and event.type() == event.Type.MouseButtonPress:
            index = self.tabBar().tabAt(event.pos())
            if index != -1 and index == self.count() - 1:
                self.create_new_tab()
                return True
        return super().eventFilter(obj, event)
        
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
        
        index = self.count() - 1
        index = self.insertTab(index, container, "New Tab")
        self.setCurrentIndex(index)

        web_view.get_web_view().titleChanged.connect(
            lambda title, view=web_view: self.update_tab_title(title, view)
        )
        web_view.get_web_view().iconChanged.connect(
            lambda icon, view=web_view: self.update_tab_icon(icon, view)
        )

        search_bar.omnibox.set_web_view(web_view)
        search_bar.controls.set_web_view(web_view)
        search_bar.secondary_controls.set_web_view(web_view)

        # todo: allow user to change search engine
        home_page = settings.get("settings", "home_page")
        web_view.load_url(home_page)
        return web_view
        
    def close_tab(self, index):
        if self.count() > 2:
            current_index = self.currentIndex()
            
            if index == current_index and index > 0:
                self.setCurrentIndex(index - 1)
                
            self.removeTab(index)
        
    def update_tab_title(self, title, web_view):
        for i in range(self.count()):
            if i < self.count() - 1:
                if web_view in self.widget(i).findChildren(BaseWebView):
                    self.setTabText(i, title or "New Tab")

    def update_tab_icon(self, icon, web_view):
        for i in range(self.count()):
            if i < self.count() - 1:
                if web_view in self.widget(i).findChildren(BaseWebView):
                    self.setTabIcon(i, icon)