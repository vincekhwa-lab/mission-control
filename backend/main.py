from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# ── Data Models ──
class DebateRequest(BaseModel):
    topic: str
    experts: List[str]

# ── Mock Debate Data ──
MOCK_DEBATES = {
    "claude": {
        "role": "首席架構師",
        "model": "Claude",
        "color": "claude",
        "emoji": "🧑‍🔬",
        "response": "從技術架構面分析，CoWoS（Chip-on-Wafer-on-Substrate）目前幾乎由台積電獨家供應，NVIDIA 尋求第二供應商是合理的風險分散策略。Samsung 的 I-Cube 與日月光的 SoIC 技術在良率上仍落後台積電約 18-24 個月。短期內（12個月）找到真正可量產的替代方案難度極高，建議 NVIDIA 應採漸進式導入策略，從非旗艦產品開始驗證替代供應商。"
    },
    "gemini": {
        "role": "市場戰略長",
        "model": "Gemini",
        "color": "gemini",
        "emoji": "📈",
        "response": "市場戰略視角：台積電 CoWoS 的定價權極強，過去兩年漲幅超過 30%，NVIDIA 的議價空間幾乎為零。引入第二供應商不只是技術問題，更是談判籌碼。從市場時機看，AMD 已開始布局 Samsung 封裝，若 NVIDIA 不採取行動，供應鏈議價能力將進一步削弱。預估台積電會在 NVIDIA 正式宣布多元化策略後 60-90 天內主動提出更優惠的長約條件。"
    },
    "deepseek": {
        "role": "紅軍反方",
        "model": "DeepSeek",
        "color": "deepseek",
        "emoji": "😈",
        "response": "⚠️ 潑冷水時間：以上分析都低估了切換成本。CoWoS 的介電層配方、UBM 設計、熱阻係數都是台積電專有 IP，替代供應商需要 NVIDIA 大幅重新設計 interposer，這意味著至少 2 個晶片世代的延遲風險。更關鍵的是：GB200/GB300 的交期壓力讓 NVIDIA 根本沒有時間做供應商切換實驗。這則新聞更可能是 NVIDIA 的公關施壓，而非真實的採購意圖。建議維持現有供應鏈，但加速佈局 2027 年後的 SoW 技術路線圖。"
    }
}

CONSENSUS = "綜合三方觀點，建議採取「以壓促談」策略：公開宣示多元化意圖以獲取談判籌碼，同時在非關鍵產品線（如 L40S、A800 後繼機種）開始實質驗證 Samsung 與日月光的封裝方案。真正的供應鏈轉換目標設定在 2027 年後，屆時替代技術成熟度將足以支撐量產需求。台積電的反應將在 90 天內揭曉，這是觀察的關鍵時間窗口。"

@app.post("/api/debate")
async def debate(req: DebateRequest):
    results = []
    for expert in req.experts:
        key = expert.lower().replace(" ", "")
        for k, v in MOCK_DEBATES.items():
            if k in key or expert.lower() in v["model"].lower():
                results.append(v)
                break
    
    if not results:
        results = list(MOCK_DEBATES.values())
    
    return {
        "topic": req.topic,
        "experts": results,
        "consensus": CONSENSUS
    }

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "Decision Hub API"}

# Mount static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")
