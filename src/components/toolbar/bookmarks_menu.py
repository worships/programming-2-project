from PyQt6.QtWidgets import QMenu

class BookmarksMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&Bookmarks", parent)
        self._setup_menu()
        
    def _setup_menu(self):
        add_bookmark = self.addAction("Add Bookmark...")
        add_bookmark.setShortcut("Ctrl+D")
        
        self.addAction("Organize Bookmarks...")