from pathlib import Path

def show_page_source(window, web_view):
    if not window or not web_view:
        return
        
    def handle_source(source):
        new_tab = window.tab_widget.create_new_tab()
        escaped_source = (
            source.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
        
        template_path = Path(__file__).parent.parent.parent / 'pages' / 'view_source.html'
        template = template_path.read_text()
            
        html = template.replace('{source}', escaped_source)
        new_tab.get_web_view().setHtml(html)
            
    web_view.get_web_view().page().toHtml(handle_source)