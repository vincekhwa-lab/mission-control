import http.server
import socketserver
import json
import os
from urllib.parse import urlparse
from http.server import SimpleHTTPRequestHandler

PORT = os.environ.get("PORT", 8080)
WORKSPACE = "/home/node/.openclaw/workspace"

class APIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        # API Routes
        if parsed_path.path.startswith("/api/"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Get memory files
            if parsed_path.path.startswith("/api/memory/"):
                filename = os.path.basename(parsed_path.path)
                try:
                    with open(os.path.join(WORKSPACE, "memory", filename), "r") as f:
                        content = f.read()
                    self.wfile.write(json.dumps({"content": content}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            
            # List daily files
            elif parsed_path.path == "/api/daily":
                try:
                    memory_dir = os.path.join(WORKSPACE, "memory")
                    if os.path.exists(memory_dir):
                        files = sorted([f for f in os.listdir(memory_dir) if f.endswith(".md")])
                    else:
                        files = []
                    self.wfile.write(json.dumps({"files": files}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({"error": str(e)}).encode())
            
            # Default
            else:
                self.wfile.write(json.dumps({"status": "ok", "message": "API running"}).encode())
            return
        
        # Serve static files
        return SimpleHTTPRequestHandler.do_GET(self)

if __name__ == "__main__":
    # Change to frontend directory
    os.chdir("/app/frontend")
    
    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        print(f"Mission Control running on port {PORT}")
        httpd.serve_forever()
