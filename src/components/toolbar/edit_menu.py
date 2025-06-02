from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

class EditMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&Edit", parent)
        self.web_view = None
        if parent and hasattr(parent.parent(), 'web_view'):
            self.web_view = parent.parent().web_view
        self._setup_menu()
        
    def _setup_menu(self):
        # clipboard actions
        # todo: fix these, they still dont work
        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.addAction(self.cut_action)
        
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.addAction(self.copy_action)
        
        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.addAction(self.paste_action)
        
        self.addSeparator()
        
        # todo: make a find dialog
        find = self.addAction("Find...")
        find.setShortcut("Ctrl+F")

        if self.web_view:
            self.cut_action.triggered.connect(self.web_view.cut)
            self.copy_action.triggered.connect(self.web_view.copy)
            self.paste_action.triggered.connect(self.web_view.paste)