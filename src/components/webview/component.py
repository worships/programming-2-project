from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from utils.settings import settings
from utils.history import history
from components.searchbar.component import SearchBar
import os

class BaseWebView(QWidget):
    statusMessage = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._web_view = QWebEngineView()
        self._web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._is_loading = False
        self._setup_ui()
        self._setup_signals()
        self._setup_shortcuts()
        self._apply_settings()

        # this is supposed to let the user copy & paste but literally it didnt work
        self._web_view.settings().setAttribute(self._web_view.settings().WebAttribute.JavascriptCanAccessClipboard, True)

        # set chromium flags (proxy)
        # maybe ill add a setting in the future that allows the user to specify other flags
        if settings.get("settings", "proxy", "enabled"):
            os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = f"--proxy-server=http={settings.get('settings','proxy','server')}"
        
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
        self._web_view.titleChanged.connect(self._on_title_changed)
    
    def _setup_shortcuts(self):
        QShortcut(QKeySequence.StandardKey.Copy, self._web_view, activated=self.copy)
        QShortcut(QKeySequence.StandardKey.Cut, self._web_view, activated=self.cut)
        QShortcut(QKeySequence.StandardKey.Paste, self._web_view, activated=self.paste)
        
    def _apply_settings(self):
        page = self._web_view.page()
        settings_obj = page.settings()
        
        js_enabled = settings.get("settings", "enable_javascript", default=True)
        settings_obj.setAttribute(settings_obj.WebAttribute.JavascriptEnabled, js_enabled)
        
        cookies_enabled = settings.get("settings", "enable_cookies", default=True)
        settings_obj.setAttribute(settings_obj.WebAttribute.LocalStorageEnabled, cookies_enabled)

    def reapply_settings(self):
        if self._web_view:
            # keep current url and state
            current_url = self._web_view.url()
            
            # find the parent container and search bar
            parent = self.parent()
            search_bar = None
            if parent and hasattr(parent, "layout"):
                containers = parent.findChildren(QWidget, "tab-container")
                if containers:
                    search_bars = containers[0].findChildren(SearchBar)
                    if search_bars:
                        search_bar = search_bars[0]
            
            # delete old web view
            old_view = self._web_view
            self.layout().removeWidget(old_view)
            
            # recreate the tab with the new settings
            self._web_view = QWebEngineView()
            self._web_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self._apply_settings()
            
            # restore signals
            self._web_view.loadStarted.connect(self._on_load_started)
            self._web_view.loadFinished.connect(self._on_load_finished)
            self._web_view.urlChanged.connect(self._on_url_changed)
            self._web_view.titleChanged.connect(self._on_title_changed)
            
            # reconnect search bar if it exists
            if search_bar:
                search_bar.omnibox.set_web_view(self)
                search_bar.controls.set_web_view(self)
                search_bar.secondary_controls.set_web_view(self)
                # update the URL in the search bar
                search_bar.omnibox.update_url(current_url.toString())
            
            # add to layout and restore state
            self.layout().addWidget(self._web_view)
            old_view.deleteLater()  # delete after adding new view to prevent flicker
            
            if not current_url.isEmpty():
                self._web_view.setUrl(current_url)
                
            # force tab widget to update title/icon state
            if parent and hasattr(parent.parent(), 'tab_widget'):
                tab_widget = parent.parent().tab_widget
                current_index = tab_widget.currentIndex()
                # this will trigger the title/icon update
                tab_widget.setCurrentIndex(current_index)
        
    def _on_load_started(self):
        self._is_loading = True
        self.statusMessage.emit("Loading...")
        
    def _on_load_finished(self, success):
        self._is_loading = False
        self.statusMessage.emit("Ready")
    
    def _on_url_changed(self, url):
        if not self._is_loading:
            self.statusMessage.emit("Ready")
            
    def _on_title_changed(self, title):
        if not self._is_loading and title:
            url = self._web_view.url().toString()
            if not url.startswith("data:"):
                history.add_entry(title, url)
        
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

    def cut(self):
        self._web_view.page().triggerAction(self._web_view.page().WebAction.Cut)
        
    def copy(self):
        self._web_view.page().triggerAction(self._web_view.page().WebAction.Copy)
        
    def paste(self):
        self._web_view.page().triggerAction(self._web_view.page().WebAction.Paste)