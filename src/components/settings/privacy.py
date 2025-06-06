from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLineEdit, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from utils.settings import settings

class PrivacySettings(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._load_settings()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # toggles for cookies, proxy, and js
        self.js_toggle = QCheckBox("Enable JavaScript")
        self.cookies_toggle = QCheckBox("Enable Cookies")
        self.proxy_toggle = QCheckBox("Enable Proxy")
        
        # proxy input
        proxy_layout = QHBoxLayout()
        proxy_label = QLabel("Proxy Server URL:")
        self.proxy_server = QLineEdit()
        self.proxy_server.setPlaceholderText("http://proxy.example.com:port")
        
        proxy_layout.addWidget(proxy_label)
        proxy_layout.addWidget(self.proxy_server)
        
        # have to show this since it doesnt automatically apply due to it being a chrome flag
        warning_label = QLabel("You must restart the browser for the proxy changes to take effect!")
        warning_label.setStyleSheet("color: #FFA500; font-size: 11px; padding-top: 5px;")
        warning_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(self.js_toggle)
        layout.addWidget(self.cookies_toggle)
        layout.addWidget(self.proxy_toggle)
        layout.addLayout(proxy_layout)
        layout.addWidget(warning_label)
        layout.addStretch()
        
        self.proxy_toggle.toggled.connect(self.proxy_server.setEnabled)
        
        self.proxy_server.setToolTip(
            "Proxy must be http only!"
        )
        
    def _load_settings(self):
        # load js & cookies
        self.js_toggle.setChecked(settings.get("settings", "enable_javascript", default=True)) 
        self.cookies_toggle.setChecked(settings.get("settings", "enable_cookies", default=True))

        # load proxy
        proxy = settings.get("settings", "proxy", default={"enabled": False, "server": ""})
        self.proxy_toggle.setChecked(proxy["enabled"])
        self.proxy_server.setText(proxy["server"])
        self.proxy_server.setEnabled(self.proxy_toggle.isChecked())
        
    def save_settings(self):
        settings.set("settings", "enable_javascript", value=self.js_toggle.isChecked())
        settings.set("settings", "enable_cookies", value=self.cookies_toggle.isChecked())

        settings.set("settings", "proxy", value={
            "enabled": self.proxy_toggle.isChecked(),
            "server": self.proxy_server.text()
        })
