from PyQt6.QtWidgets import QMenu

class EditMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&Edit", parent)
        self._setup_menu()
        
    def _setup_menu(self):
        cut = self.addAction("Cut")
        cut.setShortcut("Ctrl+X")
        
        copy = self.addAction("Copy")
        copy.setShortcut("Ctrl+C")
        
        paste = self.addAction("Paste")
        paste.setShortcut("Ctrl+V")
        
        self.addSeparator()
        
        find = self.addAction("Find...")
        find.setShortcut("Ctrl+F")