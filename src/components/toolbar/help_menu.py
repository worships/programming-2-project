from PyQt6.QtWidgets import QMenu, QMessageBox

class HelpMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&Help", parent)
        self._setup_menu()
        
    def _setup_menu(self):
        # not sure what else to add right now
        self.addAction("action")
        self.addSeparator()
        
        about = self.addAction("About Browser")
        about.triggered.connect(self._show_about_dialog)
        
    def _show_about_dialog(self):
        QMessageBox.about(
            self,
            "About Browser",
            "Pybrowser\nVersion 1.0\n© 2025"
        )