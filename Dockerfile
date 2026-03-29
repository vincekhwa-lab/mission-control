FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/ ./frontend/

EXPOSE 8080

CMD ["python", "-c", "
import http.server
import socketserver
import os

PORT = 8080
os.chdir('/app/frontend')
with socketserver.TCPServer(('', PORT), http.server.SimpleHTTPRequestHandler) as httpd:
    print(f'Mission Control running on port {PORT}')
    httpd.serve_forever()
"]
