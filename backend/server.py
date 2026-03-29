import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from http.server import SimpleHTTPRequestHandler

PORT = os.environ.get("PORT", 8080)
APP_DIR = "/app"

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API Routes
        if parsed_path.path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Get memory files from frontend folder (demo data)
            if parsed_path.path.startswith("/api/memory/"):
                filename = os.path.basename(parsed_path.path)
                try:
                    # Serve from frontend folder for demo
                    path = os.path.join(APP_DIR, "frontend", filename)
                    if os.path.exists(path):
                        with open(path, "r") as f:
                            content = f.read()
                        self.wfile.write(json.dumps({"content": content}).encode())
                    else:
                        self.wfile.write(json.dumps({"error": "File not found"}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            
            # List daily files
            elif parsed_path.path == "/api/daily":
                try:
                    frontend_dir = os.path.join(APP_DIR, "frontend")
                    files = sorted([f for f in os.listdir(frontend_dir) if f.endswith(".html")])
                    self.wfile.write(json.dumps({"files": files}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            
            else:
                self.wfile.write(json.dumps({"status": "ok", "message": "API running"}).encode())
            return
        
        # Serve static files
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    os.chdir(os.path.join(APP_DIR, "frontend"))
    
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"Mission Control running on port {PORT}")
        httpd.serve_forever()
