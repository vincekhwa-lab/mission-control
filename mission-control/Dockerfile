# 使用輕量級的 Python 映像檔
FROM python:3.10-slim

# 設定容器內的工作目錄
WORKDIR /app

# 將套件清單複製到容器內並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 將你所有的程式碼 (backend, frontend, data) 複製到容器內
COPY . .

# 進入 backend 資料夾
WORKDIR /app/backend

# 設定伺服器啟動指令 (動態讀取雲端平台給的 PORT，預設 8080)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]