from PyQt6.QtWidgets import QMenu

class ViewMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&View", parent)
        self._setup_menu()
        
    def _setup_menu(self):
        toolbars = self.addMenu("Toolbars")
        navigation_bar = toolbars.addAction("Navigation Bar")
        navigation_bar.setCheckable(True)
        navigation_bar.setChecked(True)
        
        bookmarks_bar = toolbars.addAction("Bookmarks Bar")
        bookmarks_bar.setCheckable(True)
        bookmarks_bar.setChecked(True)
        
        self.addSeparator()
        
        status_bar = self.addAction("Status Bar")
        status_bar.setCheckable(True)
        status_bar.setChecked(True)
        status_bar.triggered.connect(lambda checked: self.parent().parent().toggle_status_bar(checked))
        
        self.addSeparator()
        
        text_size = self.addMenu("Text Size")
        larger = text_size.addAction("Larger")
        larger.setShortcut("Ctrl++")
        smaller = text_size.addAction("Smaller")
        smaller.setShortcut("Ctrl+-")
        
        self.addSeparator()
        view_source = self.addAction("Page Source")
        view_source.setShortcut("Ctrl+U")