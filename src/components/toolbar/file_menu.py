from PyQt6.QtWidgets import QMenu, QApplication

class FileMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&File", parent)
        self.window = parent.parent() if parent else None
        self._setup_menu()
        
    def _setup_menu(self):
        new_window = self.addAction("New Window")
        new_window.setShortcut("Ctrl+N")
        new_window.triggered.connect(self._new_window)
        
        new_tab = self.addAction("New Tab")
        new_tab.setShortcut("Ctrl+T")
        new_tab.triggered.connect(self._new_tab)
        
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
        
    def _new_window(self):
        if self.window:
            from window import MainWindow
            new_window = MainWindow()
            new_window.show()
            
    def _new_tab(self):
        if self.window and hasattr(self.window, 'tab_widget'):
            self.window.tab_widget.create_new_tab()