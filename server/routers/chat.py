from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from zhipuai import ZhipuAI
import os
import json
import httpx
import uuid
import re
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ChatSession, ChatMessage
from ..database import SessionLocal
from ..security import verify_token
from .todos import create_todo_internal
from ..services.llm_factory import LLMFactory
from ..services.search_service import SearchService
from ..services.dialogue_processor import dialogue_processor

# --- LlamaIndex Integration ---
try:
    from llamaindex.rag_manager import KnowledgeBaseManager
except ImportError:
    # Add root to sys.path if not found
    import sys
    from pathlib import Path
    root_path = str(Path(__file__).resolve().parent.parent.parent)
    if root_path not in sys.path:
        sys.path.append(root_path)
    from llamaindex.rag_manager import KnowledgeBaseManager

# Initialize KnowledgeBaseManager
# Load API Key from environment (similar to ai_service)
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)
ZHIPU_API_KEY = os.getenv("ZHIPUAI_API_KEY") or os.getenv("LOCAL_ZHIPU_APIKEY")

rag_manager = None
if ZHIPU_API_KEY:
    try:
        # Base dir is project_root/llamaindex
        project_root = Path(__file__).resolve().parent.parent.parent
        rag_base_dir = project_root / "llamaindex"
        
        rag_manager = KnowledgeBaseManager(
            api_key=ZHIPU_API_KEY,
            base_data_dir=str(rag_base_dir / "data"),
            base_storage_dir=str(rag_base_dir / "storage_multi"),
            # 管道步骤开关 — 可通过环境变量灵活配置
            enable_context_compression=os.getenv("RAG_ENABLE_COMPRESSION", "false").lower() == "true",
            enable_query_rewrite=os.getenv("RAG_ENABLE_QUERY_REWRITE", "true").lower() == "true",
            num_query_rewrites=int(os.getenv("RAG_NUM_QUERY_REWRITES", "2")),
            enable_rerank=os.getenv("RAG_ENABLE_RERANK", "true").lower() == "true",
        )
        print("✅ Local RAG Manager initialized successfully.")
    except Exception as e:
        print(f"❌ Failed to initialize RAG Manager: {e}")
else:
    print("⚠️ RAG Manager skipped: No ZHIPUAI_API_KEY found.")

router = APIRouter()
search_service = SearchService()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "Qwen/Qwen3.5-397B-A17B-FP8"
    use_rag: bool = True  # Default to True for enterprise knowledge base
    use_search: bool = False

@router.get("/api/chat/models")
def get_available_models():
    """List all available LLM models."""
    return LLMFactory.get_all_models()

async def fetch_rag_context(query: str) -> str:
    """
    Retrieve relevant context from the local multi-source knowledge base.
    """
    if not rag_manager:
        print("⚠️ KnowledgeBaseManager is not initialized. Skipping RAG.")
        return ""
    
    print(f"🚀 [Local-RAG] Searching knowledge base for: {query}")
    try:
        # Since retrieve_all_documents is synchronous (calling APIs internally), 
        # run it in a thread to avoid blocking the event loop.
        context = await asyncio.to_thread(rag_manager.retrieve_all_documents, query)
        
        if context:
            print(f"✅ [Local-RAG] Retrieved context length: {len(context)} chars")
            # Log preview safely
            preview = context[:200].replace('\n', ' ')
            print(f"📄 Preview: {preview}...")
            return context
        else:
            print("ℹ️ [Local-RAG] No relevant documents found.")
            return ""
            
    except Exception as e:
        print(f"❌ [Local-RAG] Search failed with error: {e}")
        return ""

def get_or_create_default_session(db: Session, user_id: str):
    # Find the most recent active session for the user
    session = db.query(ChatSession).filter(
        ChatSession.user_id == user_id, 
        ChatSession.is_deleted == False
    ).order_by(ChatSession.updated_at.desc()).first()
    
    if not session:
        session = ChatSession(
            user_id=user_id,
            title="新对话",
            summary="默认会话"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    return session

def save_message(session_id: str, role: str, content: str):
    try:
        db = SessionLocal()
        msg = ChatMessage(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()
        db.close()
    except Exception as e:
        print(f"❌ Failed to save message: {e}")

@router.get("/api/chat/history")
def get_chat_history(http_request: Request, db: Session = Depends(get_db)):
    # Authenticate
    user_id = "0"
    auth_header = http_request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user_id = payload["user_id"]
        except Exception:
            pass # Fallback to default/error handling
            
    # Get latest session
    session = db.query(ChatSession).filter(
        ChatSession.user_id == user_id, 
        ChatSession.is_deleted == False
    ).order_by(ChatSession.updated_at.desc()).first()
    
    if not session:
        return []
        
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    return [
        {"id": m.id, "role": m.role, "content": m.content, "created_at": m.created_at.isoformat() if m.created_at else None}
        for m in messages
    ]

@router.post("/api/chat")
async def chat_endpoint(request: ChatRequest, http_request: Request, db: Session = Depends(get_db)):
    # Extract user_id from token if available
    user_id = "0"
    auth_header = http_request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            if payload and "user_id" in payload:
                user_id = payload["user_id"]
                print(f"👤 Chat Request from User ID: {user_id}")
        except Exception as e:
            print(f"⚠️ Token verification failed in chat: {e}")

    # 0. Persistence: Get Session and Save User Message
    session = get_or_create_default_session(db, user_id)
    session_id = session.id
    
    last_user_message = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
    
    # Only save if not empty (though request validation usually handles this)
    if last_user_message:
        save_message(session_id, "user", last_user_message)
    
    # 0.5 多轮对话参数收集处理（会议/群聊/待办）
    context_msgs = [{"role": m.role, "content": m.content} for m in request.messages[:-1]]
    
    try:
        dialogue_result = await dialogue_processor.process_message(
            user_input=last_user_message,
            user_id=user_id,
            context_messages=context_msgs,
            db=db
        )
        
        # 如果需要追问或确认，直接返回流式响应
        if dialogue_result["type"] in ["clarification", "confirmation"]:
            content = dialogue_result["content"]
            data = dialogue_result.get("data", {})
            print(f"🔄 多轮对话: {dialogue_result['type']} - {content[:50]}...")
            
            async def generate_dialogue_response():
                save_message(session_id, "assistant", content)
                for char in content:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                    await asyncio.sleep(0.005)
                
                # 添加元数据
                metadata = {
                    "type": dialogue_result["type"],
                    "session_id": data.get("session_id"),
                    "intent": data.get("intent"),
                    "params": data.get("params"),
                    "missing_params": data.get("missing_params"),
                    "collected_params": data.get("collected_params")
                }
                yield f"data: {json.dumps({'metadata': metadata})}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(generate_dialogue_response(), media_type="text/event-stream")
        
        # 如果执行成功，返回执行结果
        elif dialogue_result["type"] == "execution":
            content = dialogue_result["content"]
            print(f"✅ 功能执行: {content[:50]}...")
            
            async def generate_execution_response():
                save_message(session_id, "assistant", content)
                for char in content:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                    await asyncio.sleep(0.005)
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(generate_execution_response(), media_type="text/event-stream")
        
        # type == "chat" 继续原有逻辑
        # dialogue_processor 已经用 LLM 判断了 intent == "chat"
        # 设置标记避免后续重复的意图检测（extract_todos_from_text 会做几乎相同的判断）
        skip_intent_detection = (dialogue_result["type"] == "chat")
    except Exception as e:
        print(f"⚠️ 多轮对话处理失败，回退到原有逻辑: {e}")
        import traceback
        traceback.print_exc()
        skip_intent_detection = False
    
    # 1. Intent Detection & Todo Extraction (原有逻辑)
    # 仅在 dialogue_processor 未判断为 "chat" 或处理失败时执行
    if not skip_intent_detection:
        print(f"🤖 Analyzing intent for: {last_user_message[:50]}...")
        
        try:
            # Use shared function from server/services/ai_service.py
            try:
                from ..services.ai_service import extract_todos_from_text
            except ImportError:
                # Fallback if relative import fails (e.g. running script directly)
                import sys
                from pathlib import Path
                root_path = str(Path(__file__).resolve().parent.parent.parent)
                if root_path not in sys.path:
                    sys.path.append(root_path)
                from server.services.ai_service import extract_todos_from_text

            intent_data = extract_todos_from_text(last_user_message, context_messages=context_msgs)
                
            # If valid todo data found
            if intent_data and intent_data.get("is_todo"):
                # Case 1: Clarification Needed
                if intent_data.get("status") == "clarification_needed":
                    question = intent_data.get("clarification_question", "请补充缺失的信息。")
                    print(f"❓ Clarification needed: {question}")
                    
                    async def generate_question():
                        save_message(session_id, "assistant", question)
                        for char in question:
                            yield f"data: {json.dumps({'content': char})}\n\n"
                            await asyncio.sleep(0.005)
                        yield "data: [DONE]\n\n"
                    
                    return StreamingResponse(generate_question(), media_type="text/event-stream")

                # Case 2: Completed (Create Task)
                elif intent_data.get("status") == "completed" or intent_data.get("task_list"):
                    task_list = intent_data.get("task_list", [])
                    summary_text = intent_data.get("summary", "已为您创建相关待办事项")
                    
                    created_tasks = []
                    
                    for t in task_list:
                        # Map fields
                        title = t.get('title', '新任务')
                        description = t.get('description', '')
                        
                        # 优先级映射逻辑优化
                        # AI 返回的可能是：高、紧急、High、Urgent 等
                        # 数据库通常使用：high (高/重要), urgent (紧急), normal (普通), low (低)
                        raw_priority = t.get('priority', '').strip()
                        
                        priority = "high" # 默认为 high
                        
                        if raw_priority in ["紧急", "Urgent", "urgent", "Critical", "critical"]:
                             priority = "urgent"
                        elif raw_priority in ["高", "High", "high", "重要", "Important"]:
                             priority = "high"
                        elif raw_priority in ["中", "Medium", "medium", "普通", "Normal"]:
                             priority = "normal"
                        elif raw_priority in ["低", "Low", "low"]:
                             priority = "low"
                             
                        due_date = t.get('due_date')
                        assignee = t.get('assignee')
                        task_type = t.get('type', 'task')
                        
                        # Create in DB
                        new_todo = create_todo_internal(
                            db, 
                            title, 
                            description, # Use description as summary/content
                            priority, 
                            task_type,
                            due_date,
                            assignee,
                            user_id=user_id # Pass the authenticated user_id
                        )
                        created_tasks.append(f"- **{title}** (责任人: {assignee}, 截止: {due_date})")
                    
                    # 3. Stream Confirmation
                    async def generate_confirmation():
                        msg = f"{summary_text}\n\n已创建 {len(created_tasks)} 个任务：\n" + "\n".join(created_tasks)
                        
                        # Save Assistant Response to DB
                        save_message(session_id, "assistant", msg)
                        
                        # Simulate streaming for consistent UX
                        for char in msg:
                            yield f"data: {json.dumps({'content': char})}\n\n"
                            await asyncio.sleep(0.005) 
                        yield "data: [DONE]\n\n"
                        
                    return StreamingResponse(generate_confirmation(), media_type="text/event-stream")

        except Exception as e:
            import traceback
            print(f"❌ Intent detection/Creation failed: {e}")
            traceback.print_exc()
            
            # If we were trying to create a todo and failed, tell the user!
            # Do NOT fallback to normal chat, which would hallucinate success.
            if 'intent_data' in locals() and intent_data and intent_data.get("is_todo"):
                 async def generate_error():
                    err_msg = f"⚠️ 抱歉，任务创建失败。\n错误原因：{str(e)}\n请确保您已登录，且系统服务正常。"
                    save_message(session_id, "assistant", err_msg)
                    yield f"data: {json.dumps({'content': err_msg})}\n\n"
                    yield "data: [DONE]\n\n"
                 return StreamingResponse(generate_error(), media_type="text/event-stream")

            # Only fallback for non-todo errors (e.g. AI service failure)
            # Fallback to normal chat
    else:
        print(f"⏩ 跳过意图检测（dialogue_processor 已判断为普通聊天）")
    
    try:
        # 4. Normal Chat Flow (Fallthrough)
        rag_context = ""
        
        # 4a. Web Search (if enabled)
        search_context = ""
        if request.use_search:
            print(f"🌍 Web Search Enabled. Searching for: {last_user_message}")
            try:
                # We can use the whole message or extract keywords. 
                # For simplicity, using the message directly or a simplified version is often okay for Tavily.
                search_context = search_service.get_search_context(last_user_message)
                if search_context:
                    print(f"✅ Web Search Context found: {len(search_context)} chars")
            except Exception as e:
                print(f"❌ Web Search Failed: {e}")

        # 4b. Knowledge Base RAG (if enabled)
        if request.use_rag:
            if last_user_message:
                print(f"🔍 Fetching RAG context for: {last_user_message}")
                rag_context = await fetch_rag_context(last_user_message)

        # Combine Contexts
        system_instruction = "你是一个智能企业助手，名为“水华精灵”。请根据上下文回答用户问题。"
        
        additional_context = ""
        if search_context:
            additional_context += f"\n\n【联网搜索结果】\n{search_context}\n请结合以上搜索结果回答用户问题。如果搜索结果包含所需信息，请引用并综合回答。"
            
        if rag_context:
            additional_context += f"\n\n【企业知识库相关信息】\n{rag_context}\n请优先基于上述企业知识库信息回答。"

        if additional_context:
            system_instruction += additional_context

        # Use LLM Factory to get provider and stream response
        provider = LLMFactory.get_provider(request.model)
        
        # Convert Pydantic messages to dict
        messages_dicts = [{"role": m.role, "content": m.content} for m in request.messages]
        
        # 分层滑动窗口：保留最近 10 轮（20条消息），最近 3 轮原文，较早 7 轮截断压缩
        MAX_ROUNDS = 10          # 最多保留 10 轮对话
        FULL_ROUNDS = 3          # 最近 3 轮保留完整原文
        USER_TRUNCATE = 150      # 较早轮次用户消息截断字数
        ASSISTANT_TRUNCATE = 300 # 较早轮次AI回复截断字数
        
        max_messages = MAX_ROUNDS * 2  # 每轮 2 条（user + assistant）
        if len(messages_dicts) > max_messages:
            messages_dicts = messages_dicts[-max_messages:]
        
        full_count = FULL_ROUNDS * 2  # 最近 3 轮保留原文的消息数
        compressed_messages = []
        for i, msg in enumerate(messages_dicts):
            # 最后 full_count 条消息保留原文
            if i >= len(messages_dicts) - full_count:
                compressed_messages.append(msg)
            else:
                # 较早的消息做截断压缩
                content = msg["content"]
                limit = USER_TRUNCATE if msg["role"] == "user" else ASSISTANT_TRUNCATE
                if len(content) > limit:
                    content = content[:limit] + "..."
                compressed_messages.append({"role": msg["role"], "content": content})
        
        messages_dicts = compressed_messages
        
        response_generator = provider.chat_stream(
            model=request.model,
            messages=messages_dicts,
            system_instruction=system_instruction
        )

        async def generate():
            full_response = ""
            # 将同步 generator 放入线程中执行，避免阻塞事件循环
            import queue
            import threading
            
            chunk_queue = queue.Queue()
            
            def run_sync_generator():
                try:
                    for content in response_generator:
                        chunk_queue.put(content)
                except Exception as e:
                    chunk_queue.put(e)
                finally:
                    chunk_queue.put(None)  # 哨兵值表示结束
            
            thread = threading.Thread(target=run_sync_generator, daemon=True)
            thread.start()
            
            while True:
                # 非阻塞式等待队列数据
                while chunk_queue.empty():
                    await asyncio.sleep(0.01)
                
                item = chunk_queue.get()
                if item is None:
                    break
                if isinstance(item, Exception):
                    raise item
                
                full_response += item
                yield f"data: {json.dumps({'content': item})}\n\n"
            
            # Save Assistant Response to DB
            if full_response:
                save_message(session_id, "assistant", full_response)
                
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
    
    except Exception as e:
        import traceback
        print(f"❌ Chat generation failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")






