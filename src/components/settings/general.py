from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QFileDialog, QPushButton, QHBoxLayout
from utils.settings import settings

class GeneralSettings(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._load_settings()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # search engine settings
        search_label = QLabel("Search Engine:")
        self.search_combo = QComboBox()
        self.search_combo.addItems(["Google", "DuckDuckGo", "Bing", "Yahoo", "Custom"])
        self.search_custom = QLineEdit()
        self.search_custom.setPlaceholderText("Enter custom search URL...")
        
        layout.addWidget(search_label)
        layout.addWidget(self.search_combo)
        layout.addWidget(self.search_custom)
        
        # homepage settings
        home_label = QLabel("Homepage:")
        self.home_combo = QComboBox()
        self.home_combo.addItems(["Google", "DuckDuckGo", "Bing", "Yahoo", "Custom"])
        self.home_custom = QLineEdit()
        self.home_custom.setPlaceholderText("Enter custom homepage URL...")
        
        layout.addWidget(home_label)
        layout.addWidget(self.home_combo)
        layout.addWidget(self.home_custom)
        
        # downloads settings
        downloads_layout = QHBoxLayout()
        downloads_label = QLabel("Download Location:")
        self.downloads_path = QLineEdit()
        self.downloads_path.setReadOnly(True)
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._browse_download_path)
        
        downloads_layout.addWidget(downloads_label)
        downloads_layout.addWidget(self.downloads_path)
        downloads_layout.addWidget(browse_button)
        layout.addLayout(downloads_layout)
        
        layout.addStretch()
        
        self.search_combo.currentTextChanged.connect(self._on_search_changed)
        self.home_combo.currentTextChanged.connect(self._on_home_changed)
        
    def _load_settings(self):
        # load search engine & homepage
        search_url = settings.get("settings", "search_engine")
        self._set_combo_from_url(self.search_combo, self.search_custom, search_url)
        
        home_url = settings.get("settings", "home_page")
        self._set_combo_from_url(self.home_combo, self.home_custom, home_url)
        
        self.downloads_path.setText(settings.get("settings", "download_path"))
        
    def _set_combo_from_url(self, combo, custom, url):
        # default search engines
        url_map = {
            "https://google.com/search": "Google",
            "https://duckduckgo.com": "DuckDuckGo",
            "https://bing.com/search": "Bing",
            "https://search.yahoo.com/search": "Yahoo"
        }
        
        if url in url_map:
            combo.setCurrentText(url_map[url])
            custom.hide()
        else:
            # if the url isnt in the list, show it as custom
            combo.setCurrentText("Custom")
            custom.setText(url)
            custom.show()
            
    def _get_url_from_engine(self, engine):
        # default search engines
        url_map = {
            "Google": "https://google.com/search",
            "DuckDuckGo": "https://duckduckgo.com",
            "Bing": "https://bing.com/search",
            "Yahoo": "https://search.yahoo.com/search"
        }
        return url_map.get(engine, "")
    
    def _on_search_changed(self, text):
        self.search_custom.setVisible(text == "Custom")
        if text != "Custom":
            self.search_custom.clear()
            
    def _on_home_changed(self, text):
        self.home_custom.setVisible(text == "Custom")
        if text != "Custom":
            self.home_custom.clear()
            
    def _browse_download_path(self):
        # open a file dialog to select download folder path
        path = QFileDialog.getExistingDirectory(self, "Select Download Location", self.downloads_path.text())
        if path:
            self.downloads_path.setText(path)
            
    def save_settings(self):
        if self.search_combo.currentText() == "Custom":
            search_url = self.search_custom.text()
        else:
            search_url = self._get_url_from_engine(self.search_combo.currentText())
        settings.set("settings", "search_engine", value=search_url)
        
        if self.home_combo.currentText() == "Custom":
            home_url = self.home_custom.text()
        else:
            home_url = self._get_url_from_engine(self.home_combo.currentText())
        settings.set("settings", "home_page", value=home_url)
        
        settings.set("settings", "download_path", value=self.downloads_path.text())
