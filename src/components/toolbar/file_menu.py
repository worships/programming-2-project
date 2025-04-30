from PyQt6.QtWidgets import QMenu, QApplication

class FileMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&File", parent)
        self._setup_menu()
        
    def _setup_menu(self):
        new_window = self.addAction("New Window")
        new_window.setShortcut("Ctrl+N")
        
        new_tab = self.addAction("New Tab")
        new_tab.setShortcut("Ctrl+T")
        
        self.addSeparator()
        
        open_file = self.addAction("Open File...")
        open_file.setShortcut("Ctrl+O")
        
        save_as = self.addAction("Save Page As...")
        save_as.setShortcut("Ctrl+S")
        
        self.addSeparator()
        
        print_page = self.addAction("Print...")
        print_page.setShortcut("Ctrl+P")
        
        self.addSeparator()
        
        exit_action = self.addAction("Exit")
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(QApplication.quit)