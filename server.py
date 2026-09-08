from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import sys, os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class CleanURLHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def translate_path(self, path):
        # Remove query parameters and anchors
        clean_path = path.split('?')[0].split('#')[0]
        
        # Default translation from base handler
        filepath = super().translate_path(clean_path)
        
        # If file exists, return it
        if os.path.exists(filepath):
            return filepath
            
        # Try appending .html
        if not clean_path.endswith('.html') and not clean_path.endswith('/'):
            html_filepath = filepath + '.html'
            if os.path.isfile(html_filepath):
                return html_filepath
                
        # Try index.html for directories
        if clean_path.endswith('/'):
            index_filepath = os.path.join(filepath, 'index.html')
            if os.path.isfile(index_filepath):
                return index_filepath

        return filepath

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, CleanURLHandler)
    print(f"Serving HTTP on port {port} (threaded clean URL server)...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
