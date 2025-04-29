from PyQt6.QtWidgets import QMenuBar
from .file_menu import FileMenu
from .edit_menu import EditMenu
from .view_menu import ViewMenu
from .bookmarks_menu import BookmarksMenu
from .help_menu import HelpMenu
from utils.styles import load_stylesheet

class BrowserToolbar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(26)
        self.setStyleSheet(load_stylesheet('menubar.qss'))
        
        self.addMenu(FileMenu(self))
        self.addMenu(EditMenu(self))
        self.addMenu(ViewMenu(self))
        self.addMenu(BookmarksMenu(self))
        self.addMenu(HelpMenu(self))