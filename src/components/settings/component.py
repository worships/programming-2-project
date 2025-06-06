from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QPushButton, QHBoxLayout
from .general import GeneralSettings
from .privacy import PrivacySettings
from components.webview import BaseWebView

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tabs.addTab(GeneralSettings(), "General")
        self.tabs.addTab(PrivacySettings(), "Privacy")
        layout.addWidget(self.tabs)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
    def accept(self):
        # save settings from all tabs
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if hasattr(tab, 'save_settings'):
                tab.save_settings()
                
        # find the main window's tab widget
        main_window = self.parent()
        while main_window and not hasattr(main_window, 'tab_widget'):
            main_window = main_window.parent()
            
        # reapply settings to all tabs
        if main_window and hasattr(main_window, 'tab_widget'):
            for i in range(main_window.tab_widget.count() - 1):  # -1 to skip the new tab button
                container = main_window.tab_widget.widget(i)
                if container:
                    # get all web views in the container
                    web_views = container.findChildren(BaseWebView)
                    for web_view in web_views:
                        web_view.reapply_settings()

            main_window.tab_widget.update()
                        
        super().accept()