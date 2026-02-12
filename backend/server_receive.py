import os
import logging
import json
import base64
import time
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

import requests  # Added for URL download

# --- Relaxed WeChat Crypto Imports ---
import struct
import socket
from wechatpy.crypto import PrpCrypto
from wechatpy.utils import byte2int, to_text

# --- Internal Imports ---
from backend.ai_handler import analyze_chat_screenshot_with_glm4v, parse_ai_result_to_todos, analyze_text_message, analyze_intent, extract_meeting_info
from backend.url_crawler import extract_meeting_url, crawl_and_parse_meeting

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

# --- Relaxed WeChat Crypto Implementation ---
class RelaxedPrpCrypto(PrpCrypto):
    """
    Relaxed PrpCrypto that skips CorpID/AppID validation during decryption.
    """
    def _decrypt(self, text, _id, exception=None):
        try:
            # Decrypt using parent's cipher
            plain_text = self.cipher.decrypt(base64.b64decode(text))
            padding = byte2int(plain_text[-1])
            content = plain_text[16:-padding]
            xml_length = socket.ntohl(struct.unpack(b'I', content[:4])[0])
            xml_content = to_text(content[4:xml_length + 4])
            # from_id = to_text(content[xml_length + 4:])
            # Skip validation: if from_id != _id: raise exception
            return xml_content
        except Exception as e:
            logger.error(f"Relaxed decryption failed: {e}")
            raise

class RelaxedWeChatCrypto(WeChatCrypto):
    """
    Relaxed WeChatCrypto that uses RelaxedPrpCrypto to skip validation.
    """
    def check_signature(self, signature, timestamp, nonce, echo_str):
        return self._check_signature(signature, timestamp, nonce, echo_str, RelaxedPrpCrypto)

    def decrypt_message(self, msg, signature, timestamp, nonce):
        return self._decrypt_message(msg, signature, timestamp, nonce, RelaxedPrpCrypto)

# Initialize WeChat Components
crypto = None
wechat_client = None

if all([WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID]):
    try:
        crypto = RelaxedWeChatCrypto(WECOM_TOKEN, WECOM_AES_KEY, WECOM_CORP_ID)
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

def get_system_user_id(wecom_user_id: Optional[str]) -> Optional[str]:
    db = SessionLocal()
    try:
        user = None
        if wecom_user_id:
            user = db.query(User).filter(
                User.wecom_userid == wecom_user_id,
                User.is_deleted == False
            ).first()
        if not user and wecom_user_id:
            user = db.query(User).filter(
                User.username == wecom_user_id,
                User.is_deleted == False
            ).first()
        if user:
            return user.id

        default_user_id = "00000000-0000-0000-0000-000000000000"
        default_user = db.query(User).filter(User.id == default_user_id).first()
        if default_user:
            return default_user.id

        default_user = User(
            id=default_user_id,
            username="system_default",
            password_hash="invalid",
            full_name="System Default",
            is_active=True
        )
        db.add(default_user)
        db.commit()
        return default_user_id
    finally:
        db.close()


import uuid
from server.database import SessionLocal
from server.models import Todo, Meeting, User

# --- Helper Functions ---
def clean_text(text):
    """Remove 4-byte characters (emojis) for MySQL utf8 compatibility"""
    if not text: return ""
    return "".join(c for c in text if len(c.encode('utf-8')) <= 3)

def send_wecom_text(user_id: str, content: str, chat_id: str = None) -> bool:
    """
    主动向企微用户发送文本消息
    如果提供了 chat_id，则发送到群聊 (AppChat)
    否则发送给指定用户 (Agent Message)
    """
    try:
        if not wechat_client:
            logger.warning("⚠️ WeChatClient 未初始化，无法主动发送消息")
            return False
            
        # 1. 优先尝试发送到群聊
        if chat_id:
            try:
                if hasattr(wechat_client, "appchat"):
                    wechat_client.appchat.send_text(chat_id, content)
                    logger.info(f"📨 已向群聊 {chat_id} 发送消息")
                    return True
                else:
                    logger.warning("⚠️ WeChatClient 不支持 appchat API")
            except Exception as e:
                logger.error(f"❌ 群聊消息发送失败: {e}")
                # 如果群发失败，是否降级发给个人？
                # 暂时选择不降级，避免打扰，或者用户可以看日志
                return False

        # 2. 发送给个人
        agent_id = os.getenv("WECOM_AGENT_ID")
        if hasattr(wechat_client, "message"):
            if agent_id:
                # 企业微信 work 签名：send_text(agent_id, user_id, content)
                wechat_client.message.send_text(agent_id, user_id, content)
            else:
                # 兼容旧 enterprise 版本：send_text(user_id, content)
                try:
                    wechat_client.message.send_text(user_id, content)
                except Exception as e:
                    # 如果失败，提示需要配置 AgentID
                    logger.warning(f"⚠️ 发送失败，可能缺少 WECOM_AGENT_ID: {e}")
                    return False
            logger.info(f"📨 已向企微用户 {user_id} 发送消息")
            return True
        logger.warning("⚠️ WeChatClient 不支持 message API")
        return False
    except Exception as e:
        logger.error(f"❌ 企微消息发送失败: {e}")
        return False

def save_meeting_data_to_db(crawl_result, system_user_id: Optional[str], meeting_url: str = ""):
    """
    Save crawled meeting data to database directly.
    """
    db = SessionLocal()
    try:
        user_id = system_user_id or get_system_user_id(None)

        meeting_summary = crawl_result.get("summary", "")
        extracted_todos = crawl_result.get("todos", [])
        personal_todos = crawl_result.get("personal_todos", [])
        if isinstance(extracted_todos, str):
            try:
                parsed = json.loads(extracted_todos)
                if isinstance(parsed, dict):
                    extracted_todos = parsed.get("task_list", [])
                elif isinstance(parsed, list):
                    extracted_todos = parsed
            except Exception:
                extracted_todos = []

        todo_lines = []
        for idx, t in enumerate(extracted_todos or []):
            if isinstance(t, str):
                title = t
                item_desc = t
                assignee = "待定"
                due_date = "未指定"
            else:
                item_desc = t.get("description", "")
                assignee = t.get("assignee", "待定")
                due_date = t.get("due_date", "未指定")
                title = t.get("title", "未命名任务")
            todo_lines.append(f"{idx + 1}. {title}\n   - 详情: {item_desc}\n   - 责任人: {assignee}\n   - 截止: {due_date}")

        combined_summary = meeting_summary
        if todo_lines:
            if combined_summary:
                combined_summary = f"{combined_summary}\n\n【会议待办】\n" + "\n".join(todo_lines)
            else:
                combined_summary = "【会议待办】\n" + "\n".join(todo_lines)

        # 1. Save Meeting Record
        new_meeting = Meeting(
            id=str(uuid.uuid4()),
            organizer_id=user_id,
            title=clean_text(crawl_result.get("title", "会议纪要")),
            start_time=datetime.now(),
            end_time=datetime.now(),
            location=meeting_url or "腾讯会议",
            summary=clean_text(combined_summary),
            transcript=clean_text(crawl_result.get("transcript", "")),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_meeting)
        
        # 2. Process Todos
        count = 0
        for t in personal_todos or []:
            if isinstance(t, str):
                title = t
                description = t
                assignee = "Sender（发送者）"
                priority = "normal"
                due_date = ""
            else:
                title = t.get("title") or "会议待办"
                description = t.get("description") or title
                assignee = t.get("assignee") or "Sender（发送者）"
                
                raw_priority = t.get("priority") or "normal"
                priority_map = {"高": "urgent", "中": "high", "低": "normal", "high": "high", "medium": "normal", "low": "low", "urgent": "urgent"}
                priority = priority_map.get(str(raw_priority).lower(), "normal")
                
                due_date = t.get("due_date") or ""

            content_parts = [f"任务详情: {description}", f"责任人: {assignee}"]
            if due_date:
                content_parts.append(f"截止时间: {due_date}")
            content = "\n".join(content_parts)

            meeting_todo = Todo(
                id=str(uuid.uuid4()),
                user_id=user_id,
                title=clean_text(f"[{assignee}] {title}"),
                content=clean_text(content),
                type="meeting",
                priority=priority,
                status="pending",
                sender="会议助手",
                source_origin="meeting_minutes",
                source_message_id=new_meeting.id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(meeting_todo)
            count += 1

        # If no todos, we don't create any Todo item. 
        # The meeting record itself is saved in step 1.
        
        db.commit()
        logger.info(f"✅ [DB] 已保存会议纪要到数据库")
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

def save_todos_to_db(todos_data: List[dict], user_id: Optional[str], source_origin: Optional[str] = None):
    if not todos_data:
        return 0
    db = SessionLocal()
    try:
        resolved_user_id = user_id or get_system_user_id(None)
        count = 0
        for todo_data in todos_data:
            if isinstance(todo_data, TodoItem):
                todo_data = todo_data.dict()
            title = todo_data.get("title") or "未命名任务"
            content = todo_data.get("content")
            todo_type = todo_data.get("type") or "task"
            priority = todo_data.get("priority") or "normal"
            status = todo_data.get("status") or "pending"
            sender = todo_data.get("sender")
            ai_summary = todo_data.get("aiSummary")
            ai_action = todo_data.get("aiAction")
            is_user_task = todo_data.get("isUserTask", False)
            text_type = todo_data.get("textType", 0)

            new_todo = Todo(
                id=str(uuid.uuid4()),
                user_id=resolved_user_id,
                title=clean_text(title[:255]),
                content=clean_text(content) if content else None,
                type=todo_type,
                priority=priority,
                status=status,
                sender=sender,
                ai_summary=ai_summary,
                ai_action=ai_action,
                is_user_task=is_user_task,
                text_type=text_type,
                source_origin=source_origin,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(new_todo)
            count += 1
        db.commit()
        return count
    except Exception as e:
        db.rollback()
        logger.error(f"❌ [DB] 保存待办失败: {e}")
        return 0
    finally:
        db.close()

def run_wecom_flow_test(wecom_user_id: str):
    system_user_id = get_system_user_id(wecom_user_id)
    mock_due = datetime.now().strftime("%Y-%m-%d %H:%M")
    mock_json = json.dumps({
        "summary": "企微模拟待办",
        "task_list": [
            {
                "title": "测试文本待办",
                "description": "验证企微文本流程写库",
                "due_date": mock_due,
                "assignee": "Sender（发送者）",
                "priority": "中"
            }
        ]
    }, ensure_ascii=False)

    text_todos = parse_ai_result_to_todos(mock_json, wecom_user_id)
    for todo in text_todos:
        todo["textType"] = 1
    saved_text = save_todos_to_db(text_todos, system_user_id, source_origin="wecom_text_test")

    image_todos = []
    for todo in text_todos:
        image_todo = dict(todo)
        image_todo["textType"] = 0
        image_todo["title"] = f"图片测试-{image_todo.get('title')}"
        image_todos.append(image_todo)
    saved_image = save_todos_to_db(image_todos, system_user_id, source_origin="wecom_image_test")

    meeting_mock = {
        "title": "企微会议测试",
        "summary": "验证会议流程写库",
        "transcript": "这是测试会议纪要内容",
        "todos": [
            {
                "title": "会议待办测试",
                "description": "完成会议待办写库验证",
                "priority": "high",
                "assignee": "测试人员",
                "due_date": mock_due
            }
        ]
    }
    saved_meeting = save_meeting_data_to_db(meeting_mock, system_user_id)
    return {
        "user_id": system_user_id,
        "saved_text": saved_text,
        "saved_image": saved_image,
        "saved_meeting": saved_meeting
    }

def analyze_and_save_image(image_content: bytes, user_id: str, source_origin: str = "wecom_image"):
    """
    通用图片分析与保存函数
    输入：图片二进制数据, 用户ID
    输出：None (异步处理结果直接存库)
    """
    try:
        # 1. Convert to Base64
        base64_data = base64.b64encode(image_content).decode('utf-8')
        logger.info("✅ 图片转码成功，开始 AI 分析...")

        # 2. Call AI Analysis
        json_result = analyze_chat_screenshot_with_glm4v(base64_data)
        
        # 3. Parse and Store Results
        system_user_id = get_system_user_id(user_id)

        if json_result:
            new_todos = parse_ai_result_to_todos(json_result, user_id)
            if new_todos:
                saved_count = save_todos_to_db(new_todos, system_user_id, source_origin=source_origin)
                for todo_data in new_todos:
                    try:
                        todo_item = TodoItem(**todo_data)
                        todos_store.insert(0, todo_item)
                    except Exception:
                        pass
                logger.info(f"✅ 图片分析完成，已添加 {saved_count} 条待办")
            else:
                logger.warning("⚠️ AI 分析结果解析为空")
        else:
            logger.warning("⚠️ AI 分析未返回有效 JSON")

    except Exception as e:
        logger.error(f"❌ 图片通用处理流程异常: {e}")

def process_image_url_sync(image_url: str, user_id: str = None, chat_id: str = None):
    """
    Synchronous function to process image from URL
    """
    logger.info(f"🔄 开始处理图片 URL: {image_url} from User: {user_id} (Chat: {chat_id})")
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        image_content = response.content
        
        analyze_and_save_image(image_content, user_id, source_origin="wecom_smartbot_image")
        # TODO: Send completion notification if needed? 
        # For now, analyze_and_save_image doesn't return result summary easily.
        # But we can add a simple "Done" message.
        send_wecom_text(user_id, "图片已接收并开始分析生成待办...", chat_id=chat_id)

    except Exception as e:
        logger.error(f"❌ 图片 URL 下载或处理失败: {e}")

def process_image_sync(media_id: str, user_id: str = None, chat_id: str = None):
    """
    Synchronous function to process image, to be run in background task.
    """
    if not wechat_client:
        logger.error("❌ 无法处理图片：未初始化 WeChatClient (缺少 WECOM_SECRET)")
        return

    logger.info(f"🔄 开始后台处理图片 MediaId: {media_id} from User: {user_id} (Chat: {chat_id})")
    try:
        # 1. Download image
        response = wechat_client.media.download(media_id)
        image_content = response.content
        
        # 2. Analyze and Save (Refactored)
        analyze_and_save_image(image_content, user_id, source_origin="wecom_image")
        send_wecom_text(user_id, "图片已接收并开始分析生成待办...", chat_id=chat_id)

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
        start_time_raw = meeting_info.get("start_time")
        if isinstance(start_time_raw, str):
            try:
                # 尝试解析 "YYYY-MM-DD HH:MM" 格式
                dt = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M")
                start_time = int(dt.timestamp())
            except ValueError:
                # 如果解析失败，尝试解析 "YYYY-MM-DD HH:MM:SS" 或 fallback
                try:
                    dt = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M:%S")
                    start_time = int(dt.timestamp())
                except ValueError:
                    logger.warning(f"⚠️ 无法解析时间 '{start_time_raw}'，使用默认时间")
                    start_time = int(time.time() + 1800)
        else:
            start_time = int(start_time_raw if start_time_raw else time.time() + 1800)

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

def process_text_sync(text_content: str, user_id: str = None, chat_id: str = None):
    """
    Synchronous function to process text message
    """
    logger.info(f"📝 开始后台处理文本消息 from User: {user_id} (Chat: {chat_id})")
    try:
        system_user_id = get_system_user_id(user_id)

        # 0. 优先检查是否包含会议链接
        meeting_url = extract_meeting_url(text_content)
        if meeting_url:
            logger.info(f"🔗 检测到会议链接: {meeting_url}")
            crawl_result = crawl_and_parse_meeting(meeting_url, WECOM_MEETING_COOKIES)
            
            if crawl_result:
                saved_count = save_meeting_data_to_db(crawl_result, system_user_id, meeting_url=meeting_url)
                logger.info(f"✅ 会议链接处理完成，已存入数据库 (待办数: {saved_count})")
                return # 结束处理
            else:
                logger.warning("⚠️ 爬虫未返回有效结果")
                # 如果爬取失败，继续走下面的逻辑吗？或者直接返回？
                # 暂时选择继续，可能用户只是发了个坏链接，但想表达其他意思
        
        # 1. Analyze Intent
        intent = analyze_intent(text_content)
        logger.info(f"🧠 意图识别结果: {intent}")
        
        if intent == "chat":
            # 闲聊/普通问答：直接调用大模型生成快速回复，不做待办处理
            try:
                messages = [
                    {"role": "system", "content": "你是一个企业微信智能助手，语气专业、简洁，直接回答用户问题。"},
                    {"role": "user", "content": text_content}
                ]
                resp = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=messages,
                    temperature=0.2
                )
                reply_text = resp.choices[0].message.content.strip()
                # 主动推送到企微
                send_wecom_text(user_id, reply_text, chat_id=chat_id)
                logger.info("✅ 闲聊回复已推送至企微")
            except Exception as e:
                logger.error(f"❌ 闲聊回复生成失败: {e}")
            return
        
        elif intent == "meeting":
            # Process Meeting
            meeting_info = extract_meeting_info(text_content)
            logger.info(f"📅 提取会议信息: {meeting_info}")
            
            # --- Normalize start_time to timestamp (int) ---
            start_time_raw = meeting_info.get("start_time")
            if isinstance(start_time_raw, str):
                try:
                    dt = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M")
                    meeting_info["start_time"] = int(dt.timestamp())
                except ValueError:
                    try:
                        dt = datetime.strptime(start_time_raw, "%Y-%m-%d %H:%M:%S")
                        meeting_info["start_time"] = int(dt.timestamp())
                    except ValueError:
                        logger.warning(f"⚠️ 无法解析时间 '{start_time_raw}'，使用默认时间")
                        meeting_info["start_time"] = int(time.time() + 1800)
            elif not start_time_raw:
                 meeting_info["start_time"] = int(time.time() + 1800)
            # -----------------------------------------------

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
                    
                    save_todos_to_db([todo_item], system_user_id, source_origin="wecom_meeting")
                    todos_store.insert(0, todo_item)
                    logger.info(f"✅ 新增会议待办事项: {todo_item.title}")
                    # 主动推送结构化信息到企微
                    push_text = f"会议已创建：{meeting_info.get('topic','会议')}\n时间：{meeting_time_str}\n参会人：{', '.join(meeting_info.get('attendees', []))}"
                    send_wecom_text(user_id, push_text, chat_id=chat_id)
                    
                except Exception as e:
                    logger.error(f"❌ 创建会议待办失败: {e}")
            else:
                # Fallback to todo if meeting creation fails? Or just log error
                pass
                
        elif intent == "todo":
            # Process Todo (Original Logic)
            # 1. Call AI Analysis (reuse logic)
            json_result = None
            try:
                json_result = analyze_text_message(text_content)
            except Exception as e:
                logger.error(f"❌ 文本待办分析失败: {e}")
            
            # 2. Parse and Store Results
            if json_result:
                new_todos = parse_ai_result_to_todos(json_result, user_id)
                if new_todos:
                    for todo_data in new_todos:
                        todo_data['textType'] = 1

                        if todo_data.get('title') == "待定":
                            todo_data['title'] = text_content[:50]
                    saved_count = save_todos_to_db(new_todos, system_user_id, source_origin="wecom_text")
                    for todo_data in new_todos:
                        try:
                            todo_item = TodoItem(**todo_data)
                            todos_store.insert(0, todo_item)

                            logger.info(f"✅ 新增文本待办事项: {todo_item.title}")
                        except Exception as e:
                            logger.error(f"❌ 数据模型转换失败: {e}")
                    logger.info(f"✅ 文本分析完成，已添加 {saved_count} 条待办")
                    
                    # 构造回复消息
                    reply_text = f"已为您创建 {saved_count} 条待办事项：\n"
                    for i, t in enumerate(new_todos, 1):
                        reply_text += f"{i}. {t.get('title')} (截止: {t.get('aiSummary')})\n"
                    
                    send_wecom_text(user_id, reply_text, chat_id=chat_id)
                else:
                    logger.warning("⚠️ AI 分析结果解析为空")
            else:
                # 智能兜底：调用大模型生成解释性回复
                try:
                    messages = [
                        {"role": "system", "content": "你是一个企业微信智能助手。用户希望创建任务，但系统暂未提取到有效结构。请用简洁可执行的建议回复，并提示用户补充任务关键字段（标题/时间/责任人/优先级）。"},
                        {"role": "user", "content": text_content}
                    ]
                    resp = client.chat.completions.create(
                        model="glm-4-flash",
                        messages=messages,
                        temperature=0.3
                    )
                    reply_text = resp.choices[0].message.content.strip()
                    send_wecom_text(user_id, reply_text, chat_id=chat_id)
                except Exception as e:
                    logger.error(f"❌ 智能兜底失败: {e}")

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
    save_todos_to_db([todo], get_system_user_id(None), source_origin="api")
    return todo

# New API for AI Analysis Results (Optional, as todos are merged)
@app.get("/api/analysis-results")
async def get_analysis_results():
    # Filter todos that are chat_records
    return [t for t in todos_store if t.type == "chat_record"]

@app.get("/api/debug/test-wecom-flow")
async def trigger_wecom_flow_test(user_id: str = "test_admin"):
    """
    手动触发企微全流程测试 (Mock 数据)
    """
    try:
        result = run_wecom_flow_test(user_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- WeChat Callback Routes ---

@app.get("/wecom/smartbot/callback")
async def smartbot_verify(
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...)
):
    """
    智能机器人回调验证接口 (GET)
    文档: https://developer.work.weixin.qq.com/document/path/100719
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

@app.post("/wecom/smartbot/callback")
async def smartbot_receive(
    request: Request,
    background_tasks: BackgroundTasks,
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...)
):
    """
    智能机器人回调接口 (JSON格式)
    文档: https://developer.work.weixin.qq.com/document/path/100719
    """
    if not crypto:
        raise HTTPException(status_code=500, detail="WeChatCrypto not initialized")

    try:
        # 1. Read body
        body = await request.body()
        # SmartBot usually sends JSON with "encrypt" field, or XML? 
        # Documentation says "Receiver message protocol format... JSON"
        # but also "Receiving messages... are encrypted".
        # Assuming standard WeCom JSON encryption envelope:
        # { "encrypt": "BASE64..." }
        # Or standard XML envelope but user wants separate endpoint?
        # User said: "New interface... handling JSON format callback".
        
        try:
            # Try parsing as JSON first
            json_body = await request.json()
            encrypt_data = json_body.get("encrypt")
            if not encrypt_data:
                 # Some callbacks might be plain JSON if not encrypted (but WeCom usually encrypts)
                 # Or maybe the structure is different.
                 # If no encrypt field, assume it's already decrypted (unlikely for WeCom)
                 # Let's assume standard encrypted JSON: {"ToUserName":..., "Encrypt":...}
                 # Note: standard WeCom callback POSTs XML. 
                 # But SmartBot might POST JSON.
                 # Let's check if 'Encrypt' or 'encrypt' exists.
                 encrypt_data = json_body.get("Encrypt")
        except json.JSONDecodeError:
            # Fallback to XML if JSON parse fails (should not happen if user says it's JSON)
            logger.warning("⚠️ SmartBot callback received non-JSON body, trying XML path")
            return await wechat_receive(request, background_tasks, msg_signature, timestamp, nonce)

        if not encrypt_data:
             logger.error("❌ JSON body missing 'encrypt' field")
             raise HTTPException(status_code=400, detail="Missing encrypt field")

        # 2. Decrypt
        # WeChatCrypto.decrypt_message expects XML format usually, but internally it just decrypts the string.
        # Actually decrypt_message implementation:
        # def decrypt_message(self, msg, signature, timestamp, nonce):
        #     ... extracts encrypt from xml ...
        # So we cannot use decrypt_message directly if input is JSON string or just the encrypt string.
        # We should use decrypt() method if available, or construct a fake XML.
        # Looking at wechatpy source, there is a `decrypt` method:
        # def decrypt(self, text, receiveid): ...
        # But we need to verify signature first.
        # `check_signature` verifies signature.
        
        # Correct flow for custom encrypted data:
        # 1. Verify signature
        # signature = get_sha1(token, timestamp, nonce, encrypt_data)
        # if signature != msg_signature: raise...
        # 2. Decrypt
        # content = decrypt(encrypt_data)
        
        # Let's use crypto._check_signature and crypto.decrypt
        # Accessing protected members is risky, let's see public API.
        # crypto.check_signature(signature, timestamp, nonce, echo_str) is for GET verification.
        
        # We can simulate an XML for decrypt_message because it extracts <Encrypt> node.
        fake_xml = f"<xml><ToUserName><![CDATA[toUser]]></ToUserName><Encrypt><![CDATA[{encrypt_data}]]></Encrypt></xml>"
        decrypted_xml = crypto.decrypt_message(fake_xml, msg_signature, timestamp, nonce)
        
        # 3. Parse Decrypted Content (It should be JSON string according to SmartBot docs)
        # The decrypted content from SmartBot is JSON string.
        try:
            msg_data = json.loads(decrypted_xml)
        except json.JSONDecodeError:
            # It might be XML after all?
            # User said "JSON format callback".
            # If it fails, maybe it is XML.
            logger.warning("⚠️ Decrypted content is not JSON, falling back to XML parse")
            # If it's XML, we can reuse existing logic or parse it here
            # But let's stick to user requirement: JSON handling.
            raise
            
        logger.info(f"📩 SmartBot 收到消息: {msg_data}")

        # 4. Dispatch Logic
        msg_type = msg_data.get("msgtype")
        user_id = msg_data.get("from", {}).get("userid")
        # Extract chat_id if available (SmartBot in group)
        # Structure might be at root or inside specific fields depending on bot type
        # For SmartBot, sometimes it is in "chat_info": {"chat_id": "..."}
        chat_id = msg_data.get("chat_info", {}).get("chat_id")
        # Or maybe "chatid" at root?
        if not chat_id:
            chat_id = msg_data.get("chatid")
        
        if msg_type == "text":
            content = msg_data.get("text", {}).get("content", "")
            background_tasks.add_task(process_text_sync, content, user_id, chat_id)
            
        elif msg_type == "image":
            image_url = msg_data.get("image", {}).get("url")
            if image_url:
                background_tasks.add_task(process_image_url_sync, image_url, user_id, chat_id)
            else:
                logger.warning("⚠️ 图片消息缺少 URL")
                
        elif msg_type == "mixed":
             # Mixed type: text + image
             # Handle each item
             items = msg_data.get("mixed", {}).get("msg_item", [])
             for item in items:
                 m_type = item.get("msgtype")
                 if m_type == "text":
                     t_content = item.get("text", {}).get("content", "")
                     background_tasks.add_task(process_text_sync, t_content, user_id, chat_id)
                 elif m_type == "image":
                     img_url = item.get("image", {}).get("url")
                     if img_url:
                         background_tasks.add_task(process_image_url_sync, img_url, user_id, chat_id)
        
        else:
            logger.info(f"⚠️ SmartBot 暂不支持的消息类型: {msg_type}")

        # 5. Response
        # SmartBot expects a JSON response or empty/success?
        # "Developers can choose to generate streaming message replies... or reply directly with template card messages"
        # If we just want to acknowledge, we can return success.
        # But wait, the response also needs to be encrypted?
        # "Receiving messages and passive replies are encrypted"
        # If we just return 200 OK, it might be fine for async handling (we push messages actively later).
        return Response(content="success", media_type="text/plain")

    except InvalidSignatureException:
        logger.error("❌ 消息签名验证失败")
        raise HTTPException(status_code=403, detail="Invalid Signature")
    except Exception as e:
        logger.error(f"❌ SmartBot 处理异常: {e}")
        # Return success to avoid retry loop
        return Response(content="success", media_type="text/plain")

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
        
        # Check for ChatId in XML message (if available in wechatpy parser)
        # Wechatpy might not map ChatId for standard messages unless it's specific type.
        # But we can try to access it if it exists in the raw dict or object.
        chat_id = None
        # Try to access chat_id if available on msg object
        if hasattr(msg, 'chat_id'):
            chat_id = msg.chat_id
        # Also check common field name for group chat id in callbacks
        elif hasattr(msg, 'chatid'):
            chat_id = msg.chatid
            
        if msg.type == 'text':
            # 启动后台任务处理文本
            background_tasks.add_task(process_text_sync, msg.content, msg.source, chat_id)
            reply = create_reply("已收到您的文本消息，正在分析生成待办...", msg).render()
        elif msg.type == 'image':
            # 启动后台任务处理图片
            background_tasks.add_task(process_image_sync, msg.media_id, msg.source, chat_id)
            reply = create_reply("正在分析图片内容生成待办事项，请稍候...", msg).render()
        elif msg.type == 'file':
            # 启动后台任务处理文件
            # process_file_sync needs update too if we want group support there
            # For now just update text/image as requested
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
