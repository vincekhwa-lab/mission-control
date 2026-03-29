from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import asyncio

app = FastAPI(title="Mission Control API")

# Absolute paths for deployment
BASE_DIR = "/app"
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_DIR = os.path.join(DATA_DIR, "memory")

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(FRONTEND_DIR, exist_ok=True)

class DebateRequest(BaseModel):
    topic: str
    agents: list[str]

@app.get("/api/daily")
async def list_memories():
    try:
        files = [f for f in os.listdir(MEMORY_DIR) if f.endswith('.md')]
        files.sort(reverse=True)
        return {"files": files}
    except Exception:
        return {"files": []}

@app.post("/api/debate")
async def start_debate(request: DebateRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="請輸入主題")
    
    await asyncio.sleep(1.5)
    
    return {
        "status": "success", 
        "topic": request.topic,
        "debate_memo": [
            {
                "agent": "Claude 3.5 Sonnet", 
                "role": "首席架構師",
                "style": "bg-blue-50 text-blue-800 border-blue-200",
                "content": f"針對「{request.topic}」，從架構來看，若導入新興技術能降功耗，但初期 NRE 成本會提高 25%。需考量封裝相容性。"
            },
            {
                "agent": "Gemini 1.5 Pro", 
                "role": "市場戰略長",
                "style": "bg-emerald-50 text-emerald-800 border-emerald-200",
                "content": "同意成本考量。但若能率先推出低功耗方案，預計在 Q4 能搶下 15% 市佔，足以攤平初期成本。"
            },
            {
                "agent": "DeepSeek V3", 
                "role": "反方/紅軍",
                "style": "bg-rose-50 text-rose-800 border-rose-200",
                "content": "太樂觀了。新製程良率目前低於 60%，一旦良率無法突破，可能被對手碾壓。強烈建議先在非核心產品線進行 Pilot Run。"
            },
            {
                "agent": "Executive Summary", 
                "role": "最終決策建議",
                "style": "bg-purple-50 text-purple-900 border-purple-200 font-bold",
                "content": "結論：技術上可行且具潛力，但風險高。建議：撥出 10% 研發預算啟動小規模試產。"
            }
        ]
    }

@app.get("/")
async def serve_frontend():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        return {"message": "Mission Control API is running. Place index.html in frontend folder."}
    return FileResponse(index_path)

# Mount static files for frontend
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
