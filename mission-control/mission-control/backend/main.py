from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Mission Control API")

# 透過環境變數設定路徑，方便在雲端與本地切換。預設為相對路徑。
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
MEMORY_DIR = os.path.join(DATA_DIR, "memory")
FRONTEND_DIR = os.getenv("FRONTEND_DIR", os.path.join(BASE_DIR, "frontend"))

# 確保資料夾存在 (供雲端環境初始化時使用)
os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

# ---------------------------------------------------------
# API 路由 (相對路徑)
# ---------------------------------------------------------
@app.get("/api/daily")
async def list_daily_memories():
    """取得所有每日記憶日誌檔案清單"""
    try:
        files = [f for f in os.listdir(MEMORY_DIR) if f.endswith('.md')]
        # 依照日期反向排序 (最新的在最上面)
        files.sort(reverse=True)
        return {"files": files}
    except Exception as e:
        return {"error": str(e), "files": []}

@app.get("/api/memory/{filename}")
async def get_memory(filename: str):
    """讀取特定日誌的內容"""
    if not filename.endswith('.md'):
        raise HTTPException(status_code=400, detail="無效的檔案格式")
        
    filepath = os.path.join(MEMORY_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="找不到記憶檔案")
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------------
# 前端靜態檔案路由
# ---------------------------------------------------------
@app.get("/")
async def serve_frontend():
    """首頁路由，回傳 index.html"""
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        return {"message": "歡迎來到 Mission Control API。請將 index.html 放入 frontend 資料夾。"}
    return FileResponse(index_path)

# 將 frontend 資料夾掛載為靜態資源 (處理 css, js, 圖片等)
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="static")

# ---------------------------------------------------------
# 伺服器啟動設定 (支援雲端平台動態給予的 PORT)
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # 雲端平台(如 Render/Zeabur) 通常會透過環境變數注入 PORT
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
