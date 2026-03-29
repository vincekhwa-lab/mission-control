FROM python:3.11-slim

WORKDIR /app

# Copy all files
COPY . .

EXPOSE 8080

# Simple HTTP server to serve static files
CMD ["python3", "-m", "http.server", "8080", "--directory", "frontend"]
