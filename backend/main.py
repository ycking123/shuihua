import os
import logging
import json
import base64
import asyncio
from typing import List, Optional
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Response, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# --- WeChat Imports ---
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.enterprise import parse_message, create_reply, WeChatClient
from wechatpy.enterprise.messages import TextMessage, ImageMessage
# 异常处理兼容性修正
try:
    from wechatpy.exceptions import InvalidSignatureException, InvalidCorpIdException
except ImportError:
    from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException as InvalidCorpIdException

# --- Internal Imports ---
from backend.ai_handler import analyze_chat_screenshot_with_glm4v, parse_ai_result_to_todos

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UnifiedServer")

# --- Environment Setup ---
# Try loading from backend/.env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Try loading from root .env.local
root_env_path = Path(__file__).parent.parent / ".env.local"
load_dotenv(dotenv_path=root_env_path)

# --- Zhipu AI Config ---
API_KEY = os.getenv("ZHIPUAI_API_KEY") or os.getenv("Zhipuai_API_KEY")
if not API_KEY:
    logger.warning("ZHIPUAI_API_KEY not found in .env or .env.local file")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

# --- WeChat Config ---
WECOM_TOKEN = os.getenv("WECOM_TOKEN")
WECOM_AES_KEY = os.getenv("WECOM_AES_KEY")
WECOM_CORP_ID = os.getenv("WECOM_CORP_ID")
WECOM_SECRET = os.getenv("WECOM_SECRET")

if not all([WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID]):
    logger.error("❌ 缺少必要的企业微信配置 (WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID)，请检查 .env 文件")
    # 不退出，允许服务器启动以服务前端，但微信功能将不可用

# Initialize WeChat Components
crypto = None
wechat_client = None

if all([WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID]):
    try:
        crypto = WeChatCrypto(WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID)
        logger.info("✅ WeChatCrypto 初始化成功")
    except Exception as e:
        logger.error(f"❌ 初始化 WeChatCrypto 失败: {e}")

if WECOM_SECRET and WECOM_CORP_ID:
    try:
        wechat_client = WeChatClient(WECOM_CORP_ID, WECOM_SECRET)
        logger.info("✅ WeChatClient 初始化成功")
    except Exception as e:
        logger.warning(f"⚠️ 初始化 WeChatClient 失败: {e}，将无法下载图片")
else:
    logger.warning("⚠️ 未配置 WECOM_SECRET，将无法下载图片进行 AI 分析")


# --- FastAPI App ---
app = FastAPI(title="Water Essence Sprite Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---
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

# --- Global Storage ---
todos_store: List[TodoItem] = []

# --- Helper Functions ---
def process_image_sync(media_id: str):
    """
    Synchronous function to process image, to be run in background task.
    """
    if not wechat_client:
        logger.error("❌ 无法处理图片：未初始化 WeChatClient (缺少 WECOM_SECRET)")
        return

    logger.info(f"🔄 开始后台处理图片 MediaId: {media_id}")
    try:
        # 1. Download image
        response = wechat_client.media.download(media_id)
        image_content = response.content
        
        # 2. Convert to Base64
        base64_data = base64.b64encode(image_content).decode('utf-8')
        logger.info("✅ 图片下载并转码成功")

        # 3. Call AI Analysis
        # Note: calling synchronous OpenAI/Zhipu client here is fine as this is running in background thread
        json_result = analyze_chat_screenshot_with_glm4v(base64_data)
        
        # 4. Parse and Store Results
        if json_result:
            new_todos = parse_ai_result_to_todos(json_result)
            if new_todos:
                for todo_data in new_todos:
                    # Convert dict to TodoItem model
                    try:
                        todo_item = TodoItem(**todo_data)
                        todos_store.insert(0, todo_item) # Add to top
                        logger.info(f"✅ 新增待办事项: {todo_item.title}")
                    except Exception as e:
                        logger.error(f"❌ 数据模型转换失败: {e}")
                logger.info(f"✅ 图片分析完成，已添加 {len(new_todos)} 条待办")
            else:
                logger.warning("⚠️ AI 分析结果解析为空")
        else:
            logger.warning("⚠️ AI 分析未返回有效 JSON")

    except Exception as e:
        logger.error(f"❌ 图片处理流程异常: {e}")

# --- API Routes ---

@app.get("/api/todos", response_model=List[TodoItem])
async def get_todos():
    return todos_store

@app.post("/api/todos", response_model=TodoItem)
async def add_todo(todo: TodoItem):
    todos_store.append(todo)
    return todo

# New API for AI Analysis Results (Optional, as todos are merged)
@app.get("/api/analysis-results")
async def get_analysis_results():
    # Filter todos that are chat_records
    return [t for t in todos_store if t.type == "chat_record"]

# --- WeChat Callback Routes ---

@app.get("/wecom/callback")
async def wechat_verify(
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...)
):
    """
    企业微信回调验证接口
    """
    if not crypto:
        raise HTTPException(status_code=500, detail="WeChatCrypto not initialized")
        
    try:
        echo_str = crypto.check_signature(msg_signature, timestamp, nonce, echostr)
        return Response(content=echo_str, media_type="text/plain")
    except InvalidSignatureException:
        logger.error("❌ 签名验证失败")
        raise HTTPException(status_code=403, detail="Invalid Signature")
    except Exception as e:
        logger.error(f"❌ 验证过程异常: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/wecom/callback")
async def wechat_receive(
    request: Request,
    background_tasks: BackgroundTasks,
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...)
):
    """
    企业微信消息接收接口
    """
    if not crypto:
        raise HTTPException(status_code=500, detail="WeChatCrypto not initialized")

    body = await request.body()
    try:
        decrypted_xml = crypto.decrypt_message(body, msg_signature, timestamp, nonce)
    except InvalidSignatureException:
        logger.error("❌ 消息签名验证失败")
        raise HTTPException(status_code=403, detail="Invalid Signature")
    except Exception as e:
        logger.error(f"❌ 解密失败: {e}")
        raise HTTPException(status_code=400, detail="Decryption Failed")

    try:
        msg = parse_message(decrypted_xml)
        logger.info(f"📩 收到消息: {msg.type} from {msg.source}")

        if msg.type == 'text':
            reply = create_reply("已收到您的消息，我是水华精灵助手。", msg).render()
        elif msg.type == 'image':
            # 启动后台任务处理图片
            background_tasks.add_task(process_image_sync, msg.media_id)
            reply = create_reply("正在分析图片内容生成待办事项，请稍候...", msg).render()
        else:
            reply = create_reply("暂不支持该消息类型", msg).render()
            
        encrypted_xml = crypto.encrypt_message(reply, nonce, timestamp)
        return Response(content=encrypted_xml, media_type="application/xml")
        
    except Exception as e:
        logger.error(f"❌ 消息处理异常: {e}")
        # Return success to avoid WeChat retrying
        return Response(content="success", media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    # Use 0.0.0.0 to allow external access
    uvicorn.run(app, host="0.0.0.0", port=8002)
