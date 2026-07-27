from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import sys

class RequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

if __name__ == '__main__':
    port = 8000
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    print(f"Serving HTTP on port {port} (threaded)...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
