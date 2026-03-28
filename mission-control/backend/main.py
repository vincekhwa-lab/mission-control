import http.server
import socketserver
import json
import os
from urllib.parse import urlparse

PORT = 8080
WORKSPACE = "/home/node/.openclaw/workspace"
WEB_DIR = os.path.join(WORKSPACE, "dashboard")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API Routes
        if parsed_path.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Get specific file content
            if parsed_path.path.startswith('/api/memory/'):
                filename = os.path.basename(parsed_path.path)
                try:
                    with open(os.path.join(WORKSPACE, 'memory', filename), 'r') as f:
                        content = f.read()
                    self.wfile.write(json.dumps({'content': content}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            
            # List memory files
            elif parsed_path.path == '/api/daily':
                try:
                    memory_dir = os.path.join(WORKSPACE, 'memory')
                    if os.path.exists(memory_dir):
                        files = os.listdir(memory_dir)
                    else:
                        files = []
                    self.wfile.write(json.dumps({'files': files}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
                    
            # Default response
            else:
                self.wfile.write(json.dumps({'status': 'ok', 'message': 'API is running'}).encode())
            return
            
        # For everything else, serve static files from WEB_DIR
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Mission Control Server running at http://localhost:{PORT}")
        httpd.serve_forever()
