from PyQt6.QtWidgets import QMenu, QMessageBox
from PyQt6.QtCore import Qt

class HelpMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__("&Help", parent)
        self._setup_menu()
        
    def _setup_menu(self):
        self.addAction("Settings")
        self.addSeparator()
        
        about = self.addAction("About Browser")
        about.triggered.connect(self._show_about_dialog)
        
    def _show_about_dialog(self):
        about_box = QMessageBox(self)
        about_box.setWindowTitle("About Browser")
        about_box.setText("Pybrowser - Computer Programming 2 Final Project\nSean Coyne © 2025")
        about_box.setStyleSheet("""
            QMessageBox {
                min-width: 300px;
                width: 300px;
                padding: 20px;
            }
            QMessageBox QLabel {
                min-width: 300px;
                width: 300px;
            }
        """)
        about_box.exec()