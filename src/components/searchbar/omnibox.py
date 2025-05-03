from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

class Omnibox(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setPlaceholderText("Search or enter address")
        self.web_view = None
        self.returnPressed.connect(self._handle_search)

    def set_web_view(self, web_view):
        self.web_view = web_view
        self.web_view.get_web_view().urlChanged.connect(lambda url: self.update_url(url.toString()))

    def update_url(self, url):
        self.setText(url)

    def _handle_search(self):
        query = self.text().strip()
        if not query or not self.web_view:
            return

        if '.' in query and ' ' not in query:
            if not query.startswith(('http://', 'https://')):
                query = 'https://' + query
        else:
            # todo: allow user to change search engine
            query = f'https://duckduckgo.com/?q={query}'

        self.web_view.load_url(query)
