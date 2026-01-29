
import os
import json
import asyncio
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
# Try loading from backend/.env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Try loading from root .env.local
root_env_path = Path(__file__).parent.parent / ".env.local"
load_dotenv(dotenv_path=root_env_path)

API_KEY = os.getenv("ZHIPUAI_API_KEY") or os.getenv("Zhipuai_API_KEY")

if not API_KEY:
    raise ValueError("ZHIPUAI_API_KEY not found in .env or .env.local file")

# Initialize OpenAI client for Zhipu AI
client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class MindMapNode(BaseModel):
    label: str
    subNodes: Optional[List[str]] = []

class ConclusionCard(BaseModel):
    label: str
    value: str
    trend: str
    isGood: bool

class VisualData(BaseModel):
    type: str = "analysis"
    title: str
    conclusionCards: List[ConclusionCard]
    mindMap: List[MindMapNode]
    detailedReport: Optional[str] = None

class ChatResponse(BaseModel):
    category: str
    summary: str
    visualTitle: str
    conclusionCards: List[ConclusionCard]
    mindMap: List[MindMapNode]
    detailedReport: str

class ChatRequest(BaseModel):
    message: str

# Todo Data Models
class TodoItem(BaseModel):
    id: str
    type: str = "meeting"
    priority: str = "high"
    title: str
    sender: str = "会议纪要"
    time: str
    completed: bool = False
    status: str = "pending"
    aiSummary: Optional[str] = None
    aiAction: Optional[str] = None
    content: Optional[str] = None
    isUserTask: bool = False

# In-memory storage for todos
todos_store: List[TodoItem] = []

SYSTEM_PROMPT = """
你是一个战略智僚助手。你的职责是提供深度洞察、数据挖掘和可视化结论。
输出结构必须包含JSON，格式如下：
{
  "category": "urgent|strategic|standard",
  "summary": "一句简短的分析摘要",
  "visualTitle": "分析报告维度",
  "conclusionCards": [{"label": "关键指标", "value": "数据值", "trend": "+X%", "isGood": true}],
  "mindMap": [{"label": "逻辑节点", "subNodes": ["支撑项1", "支撑项2"]}],
  "detailedReport": "详细的推演逻辑和背景情报分析"
}
请确保返回的是纯JSON格式，不要包含Markdown代码块标记（如 ```json ... ```）。
"""

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",  # Use a cost-effective model or glm-4
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            response_format={"type": "json_object"} # Ensure JSON output
        )
        
        content = response.choices[0].message.content
        try:
            # Parse JSON to ensure it's valid
            data = json.loads(content)
            return data
        except json.JSONDecodeError:
            # Fallback if model returns text around json
            # Simple cleanup for common markdown fences
            clean_content = content.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_content)
            return data
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/todos", response_model=List[TodoItem])
async def get_todos():
    return todos_store

@app.post("/api/todos", response_model=TodoItem)
async def add_todo(todo: TodoItem):
    todos_store.append(todo)
    return todo

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            
            # Send "thinking" status or similar if needed
            # For now, just process and send back the result
            
            try:
                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": data}
                    ],
                    temperature=0.7,
                    stream=False # For now, no streaming of partial JSON
                )
                
                content = response.choices[0].message.content
                # Clean up if needed
                if "```json" in content:
                    content = content.replace("```json", "").replace("```", "").strip()
                
                await websocket.send_text(content)
                
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
                
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
