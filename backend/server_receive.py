import os
import logging
import json
import base64
import time
import httpx
import fitz  # PyMuPDF
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
from backend.ai_handler import analyze_chat_screenshot_with_glm4v, parse_ai_result_to_todos, analyze_text_message, analyze_intent, extract_meeting_info
from backend.url_crawler import extract_meeting_url
from backend.crawl_with_browser import crawl_meeting_minutes

try:
    from pypinyin import lazy_pinyin
except ImportError:
    lazy_pinyin = None
    print("⚠️ pypinyin module not found. Name conversion will be disabled.")

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
# 爬虫 Cookies
WECOM_MEETING_COOKIES = os.getenv("WECOM_MEETING_COOKIES")

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
    textType: int = 0  # 0: Image/Default, 1: Text Message

# --- Global Storage ---
todos_store: List[TodoItem] = []
DB_FILE = Path(__file__).parent.parent / "data" / "todos.json"

def save_todos():
    """持久化待办事项到 JSON 文件"""
    try:
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump([item.dict() for item in todos_store], f, ensure_ascii=False, indent=2)
        logger.info(f"💾 已保存 {len(todos_store)} 条数据到 {DB_FILE}")
    except Exception as e:
        logger.error(f"❌ 保存数据库失败: {e}")

def load_todos():
    """从 JSON 文件加载待办事项"""
    global todos_store
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                todos_store = [TodoItem(**item) for item in data]
            logger.info(f"📂 已加载 {len(todos_store)} 条数据")
        except Exception as e:
            logger.error(f"❌ 加载数据库失败: {e}")

# 初始化加载
load_todos()

def sync_todo_to_main_server(todo_item: TodoItem):
    """
    Syncs the new todo item to the main server (port 8000).
    """
    try:
        # Assuming main server is on localhost:8000
        # In a real deployment, this might need a configurable URL
        url = "http://localhost:8000/api/todos"
        # Use a timeout to prevent blocking for too long
        response = httpx.post(url, json=todo_item.dict(), timeout=5.0)
        if response.status_code == 200:
            logger.info(f"✅ 同步待办到主服务器成功: {todo_item.title}")
        else:
            logger.error(f"❌ 同步待办到主服务器失败: Status {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"❌ 同步待办到主服务器异常: {e}")


import uuid
from server.database import SessionLocal
from server.models import Todo, Meeting, User

# --- Helper Functions ---
def clean_text(text):
    """Remove 4-byte characters (emojis) for MySQL utf8 compatibility"""
    if not text: return ""
    return "".join(c for c in text if len(c.encode('utf-8')) <= 3)

def save_meeting_data_to_db(crawl_result, user_wecom_id):
    """
    Save crawled meeting data to database directly.
    """
    db = SessionLocal()
    try:
        # 1. Find User
        # msg.source is usually WeCom UserID.
        # Try to find user by wecom_userid
        user = None
        if user_wecom_id:
            user = db.query(User).filter(User.wecom_userid == user_wecom_id).first()
        
        # Fallback: try to match by username if wecom_userid not set or match failed
        if not user and user_wecom_id:
             user = db.query(User).filter(User.username == user_wecom_id).first()
        
        # Absolute fallback: use the first user found (system owner?)
        if not user:
            user = db.query(User).first()
            logger.warning(f"⚠️ save_meeting_data_to_db: User {user_wecom_id} not found, associating with default user {user.username if user else 'None'}")
        
        if user:
            user_id = user.id
        else:
            # Create default user if no users exist to avoid FK error
            default_user_id = "00000000-0000-0000-0000-000000000000"
            user = User(
                id=default_user_id,
                username="system_default",
                password_hash="invalid",
                full_name="System Default",
                is_active=True
            )
            db.add(user)
            db.commit() # Commit immediately to persist user
            user_id = default_user_id
            logger.info(f"✅ Created default user {user_id}")

        # 2. Save Meeting Record
        new_meeting = Meeting(
            id=str(uuid.uuid4()),
            organizer_id=user_id,
            title=clean_text(crawl_result.get("title", "会议纪要")),
            start_time=datetime.now(),
            end_time=datetime.now(),
            location="腾讯会议",
            summary=clean_text(crawl_result.get("summary", "")),
            transcript=clean_text(crawl_result.get("transcript", "")),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_meeting)
        
        # 3. Save Todos
        extracted_todos = crawl_result.get("todos", [])
        # Parse if string
        if isinstance(extracted_todos, str):
            try:
                parsed = json.loads(extracted_todos)
                if isinstance(parsed, dict):
                    extracted_todos = parsed.get("task_list", [])
                elif isinstance(parsed, list):
                    extracted_todos = parsed
            except:
                extracted_todos = []
        
        count = 0
        if extracted_todos and isinstance(extracted_todos, list):
            for t in extracted_todos:
                # Handle if t is just a string
                if isinstance(t, str):
                    t = {
                        "title": t,
                        "description": t,
                        "priority": "medium",
                        "assignee": "待定"
                    }
                
                # Map priority to allowed values
                raw_priority = t.get("priority", "normal").lower()
                if "high" in raw_priority or "urgent" in raw_priority:
                    safe_priority = "high"
                elif "low" in raw_priority:
                    safe_priority = "low"
                else:
                    safe_priority = "normal"

                new_todo = Todo(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    title=clean_text(t.get("title", "未命名任务")[:255]),
                    content=clean_text(f"详情: {t.get('description', '')}\n责任人: {t.get('assignee', '')}"),
                    type="task",
                    priority=safe_priority,
                    status="pending",
                    sender="会议纪要助手",
                    ai_summary=f"截止: {t.get('due_date', '无')}",
                    source_origin="meeting_minutes",
                    source_message_id=new_meeting.id, # Link to meeting
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                db.add(new_todo)
                count += 1
                
        # 4. Save Meeting Record Todo
        meeting_todo = Todo(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=clean_text(f"【会议】{new_meeting.title}"),
            content=clean_text(f"【会议纪要】\n{new_meeting.summary[:500]}...\n\n已提取待办: {count}条"),
            type="meeting",
            priority="high",
            status="completed", # It's a record
            sender="会议助手",
            source_origin="meeting_minutes",
            source_message_id=new_meeting.id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(meeting_todo)
        
        db.commit()
        logger.info(f"✅ [DB] 已保存会议纪要及 {count} 条待办到数据库")
        return count
        
    except Exception as e:
        db.rollback()
        import traceback
        with open("db_error_log.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: {e}\n")
            traceback.print_exc(file=f)
        logger.error(f"❌ [DB] 保存会议数据失败: {e}")
        return 0
    finally:
        db.close()

def convert_name_to_userid(name: str) -> str:
    """
    尝试将中文姓名转换为 UserID
    1. 优先使用通讯录搜索（如果有权限）
    2. 降级为拼音 UserID (首字母大写)
    """
    # 动态检查 pypinyin 是否可用（防止服务启动时未安装）
    global lazy_pinyin
    if lazy_pinyin is None:
        try:
            from pypinyin import lazy_pinyin
            logger.info("✅ pypinyin module loaded dynamically.")
        except ImportError:
            logger.error("❌ pypinyin module not found. Cannot convert name to UserID.")
            return name
    
    # 策略 1: 拼音转换
    try:
        pinyin_list = lazy_pinyin(name)
        # Title case each part: 张笑颜 -> ZhangXiaoYan
        userid = "".join([p.title() for p in pinyin_list])
        logger.info(f"🔄 Name Conversion: {name} -> {userid}")
        return userid
    except Exception as e:
        logger.error(f"❌ Name conversion failed for {name}: {e}")
        return name

def process_image_sync(media_id: str, user_id: str = None):
    """
    Synchronous function to process image, to be run in background task.
    """
    if not wechat_client:
        logger.error("❌ 无法处理图片：未初始化 WeChatClient (缺少 WECOM_SECRET)")
        return

    logger.info(f"🔄 开始后台处理图片 MediaId: {media_id} from User: {user_id}")
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
            new_todos = parse_ai_result_to_todos(json_result, user_id)
            if new_todos:
                for todo_data in new_todos:
                    # Convert dict to TodoItem model
                    try:
                        todo_item = TodoItem(**todo_data)
                        todos_store.insert(0, todo_item) # Add to top
                        # Sync to main server
                        sync_todo_to_main_server(todo_item)
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

def create_wecom_meeting(meeting_info, creator_id):
    """
    通过企业微信 API 创建日程 (Schedule)
    """
    if not wechat_client:
        logger.error("❌ 无法创建会议：未初始化 WeChatClient")
        return False
        
    try:
        # 使用 OA 日程接口 (schedule)
        # https://developer.work.weixin.qq.com/document/path/93648
        
        # 构造参与者列表 (包含创建者)
        # 注意: 真实环境需要将 extracted names 转换为 userids
        # 这里仅演示将 creator_id 加入参与者，确保用户能看到日程
        attendee_list = [{"userid": creator_id}]
        
        # 处理 AI 提取的参会人
        extracted_attendees = meeting_info.get("attendees", [])
        for name in extracted_attendees:
            # 简单去重 (如果名字和 creator_id 相同则跳过)
            # 注意: 这里假设 creator_id 已经是 UserID 格式，而 name 可能是中文
            # 实际生产中应更严谨判断
            if name == creator_id:
                continue
                
            userid = convert_name_to_userid(name)
            if userid:
                attendee_list.append({"userid": userid})
        
        # 必需参数
        start_time = int(meeting_info.get("start_time", time.time() + 1800))
        end_time = start_time + int(meeting_info.get("duration", 3600))
        summary = meeting_info.get("topic", "临时会议")
        
        payload = {
            "schedule": {
                "summary": summary,
                "description": f"由 AI 助手自动创建。\n详情: {summary}",
                "start_time": start_time,
                "end_time": end_time,
                "attendees": attendee_list
                # "cal_id": "" # 不填则使用应用默认日历
            }
        }
        
        # 调用 wechatpy client 的 post 方法直接请求 API
        res = wechat_client.post('oa/schedule/add', data=payload)
        logger.info(f"✅ 会议创建成功: {res}")
        return True
        
    except Exception as e:
        logger.error(f"❌ 创建会议失败: {e}")
        # 如果是因为 UserID 不存在，尝试降级处理（仅创建者自己可见）
        if "60111" in str(e):
             logger.warning("⚠️ 检测到 UserID 错误，尝试移除参会人重新创建...")
             try:
                 # 重置参与者列表，仅保留创建者
                 payload["schedule"]["attendees"] = [{"userid": creator_id}]
                 res = wechat_client.post('oa/schedule/add', data=payload)
                 logger.info(f"✅ (降级) 会议创建成功: {res}")
                 return True
             except Exception as retry_e:
                 logger.error(f"❌ (降级) 创建会议再次失败: {retry_e}")
                 
        return False

def process_text_sync(text_content: str, user_id: str = None):
    """
    Synchronous function to process text message
    """
    logger.info(f"📝 开始后台处理文本消息 from User: {user_id}")
    try:
        # 0. 优先检查是否包含会议链接
        meeting_url = extract_meeting_url(text_content)
        if meeting_url:
            logger.info(f"🔗 检测到会议链接: {meeting_url}")
            if not WECOM_MEETING_COOKIES:
                logger.warning("⚠️ 未配置 WECOM_MEETING_COOKIES，爬虫可能无法访问受限内容")
            
            # 启动爬虫
            crawl_result = crawl_meeting_minutes(meeting_url, WECOM_MEETING_COOKIES)
            
            if crawl_result:
                # 直接存入数据库，不通过前端API传输
                saved_count = save_meeting_data_to_db(crawl_result, user_id)
                logger.info(f"✅ 会议链接处理完成，已存入数据库 (待办数: {saved_count})")
                return # 结束处理
            else:
                logger.warning("⚠️ 爬虫未返回有效结果")
                # 如果爬取失败，继续走下面的逻辑吗？或者直接返回？
                # 暂时选择继续，可能用户只是发了个坏链接，但想表达其他意思
        
        # 1. Analyze Intent
        intent = analyze_intent(text_content)
        logger.info(f"🧠 意图识别结果: {intent}")
        
        if intent == "meeting":
            # Process Meeting
            meeting_info = extract_meeting_info(text_content)
            logger.info(f"📅 提取会议信息: {meeting_info}")
            
            # Create Meeting
            if create_wecom_meeting(meeting_info, user_id):
                # Notify success (optional, could add a system notification todo)
                try:
                    # Construct meeting todo item
                    meeting_time_str = datetime.fromtimestamp(meeting_info.get("start_time")).strftime("%Y-%m-%d %H:%M")
                    
                    todo_item = TodoItem(
                        id=f"meeting-{int(time.time())}",
                        type="meeting",
                        priority="high",
                        title=f"📅 {meeting_info.get('topic', '会议')}",
                        sender="会议助手",
                        time=datetime.now().strftime("%H:%M"),
                        status="pending",
                        aiSummary=f"时间: {meeting_time_str}",
                        content=f"会议主题: {meeting_info.get('topic')}\n时间: {meeting_time_str}\n时长: {int(meeting_info.get('duration', 3600)/60)}分钟\n参会人: {', '.join(meeting_info.get('attendees', []))}",
                        isUserTask=False
                    )
                    
                    # Store locally
                    todos_store.insert(0, todo_item)
                    
                    # Sync to main server
                    sync_todo_to_main_server(todo_item)
                    logger.info(f"✅ 新增会议待办事项: {todo_item.title}")
                    
                except Exception as e:
                    logger.error(f"❌ 创建会议待办失败: {e}")
            else:
                # Fallback to todo if meeting creation fails? Or just log error
                pass
                
        else:
            # Process Todo (Original Logic)
            # 1. Call AI Analysis (reuse logic)
            json_result = analyze_text_message(text_content)
            
            # 2. Parse and Store Results
            if json_result:
                new_todos = parse_ai_result_to_todos(json_result, user_id)
                if new_todos:
                    for todo_data in new_todos:
                        # Update specific fields for text message
                        todo_data['textType'] = 1
                        
                        # Fallback defaults if AI missed them (though AI prompt handles most)
                        if todo_data.get('title') == "待定":
                            todo_data['title'] = text_content[:50]
                        
                        # Convert dict to TodoItem model
                        try:
                            todo_item = TodoItem(**todo_data)
                            todos_store.insert(0, todo_item)
                            # Sync to main server
                            sync_todo_to_main_server(todo_item)
                            logger.info(f"✅ 新增文本待办事项: {todo_item.title}")
                        except Exception as e:
                            logger.error(f"❌ 数据模型转换失败: {e}")
                    logger.info(f"✅ 文本分析完成，已添加 {len(new_todos)} 条待办")
                else:
                    logger.warning("⚠️ 文本AI分析结果解析为空")
            else:
                logger.warning("⚠️ 文本AI分析未返回有效 JSON")

    except Exception as e:
        logger.error(f"❌ 文本处理流程异常: {e}")

def process_file_sync(media_id: str, file_name: str, file_ext: str, user_id: str):
    """
    Synchronous function to process file message
    """
    logger.info(f"📂 开始后台处理文件消息 from User: {user_id}, File: {file_name}")
    try:
        if not wechat_client:
            logger.error("❌ WeChatClient 未初始化，无法下载文件")
            return

        # 1. 下载文件
        logger.info(f"⬇️ 正在下载文件 media_id: {media_id}...")
        res = wechat_client.media.download(media_id)
        
        # res.content contains the file bytes
        file_content = res.content
        file_size = len(file_content)
        logger.info(f"✅ 文件下载成功，大小: {file_size} bytes")

        # 2. 提取文本
        extracted_text = ""
        
        if file_ext.lower() == 'txt':
            try:
                extracted_text = file_content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    extracted_text = file_content.decode('gbk')
                except Exception:
                    logger.error("❌ TXT 文件编码识别失败")
                    return
                    
        elif file_ext.lower() == 'pdf':
            try:
                with fitz.open(stream=file_content, filetype="pdf") as doc:
                    for page in doc:
                        extracted_text += page.get_text()
            except Exception as e:
                logger.error(f"❌ PDF 解析失败: {e}")
                return
        
        else:
            logger.warning(f"⚠️ 暂不支持的文件格式: {file_ext}")
            # 可以考虑添加 TODO 提醒用户
            return

        if not extracted_text.strip():
            logger.warning("⚠️ 文件提取内容为空")
            return

        logger.info(f"📄 文件内容提取成功，长度: {len(extracted_text)} 字符")
        
        # 3. 复用文本处理逻辑
        # 我们可以给文本加个前缀说明来源
        context_text = f"【文件内容分析：{file_name}】\n{extracted_text}"
        process_text_sync(context_text, user_id)

    except Exception as e:
        logger.error(f"❌ 文件处理流程异常: {e}")


# --- API Routes ---

@app.get("/api/todos", response_model=List[TodoItem])
async def get_todos():
    return todos_store

@app.post("/api/todos", response_model=TodoItem)
async def add_todo(todo: TodoItem):
    todos_store.append(todo)
    # Also sync to main server when receiving via API
    sync_todo_to_main_server(todo)
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
            # 启动后台任务处理文本
            background_tasks.add_task(process_text_sync, msg.content, msg.source)
            reply = create_reply("已收到您的文本消息，正在分析生成待办...", msg).render()
        elif msg.type == 'image':
            # 启动后台任务处理图片
            background_tasks.add_task(process_image_sync, msg.media_id, msg.source)
            reply = create_reply("正在分析图片内容生成待办事项，请稍候...", msg).render()
        elif msg.type == 'file':
            # 启动后台任务处理文件
            background_tasks.add_task(process_file_sync, msg.media_id, msg.filename, msg.ext, msg.source)
            reply = create_reply(f"已收到文件【{msg.filename}】，正在提取内容分析...", msg).render()
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
    uvicorn.run(app, host="0.0.0.0", port=8080)

