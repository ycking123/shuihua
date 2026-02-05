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
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ChatSession, ChatMessage
from ..database import SessionLocal
from ..security import verify_token
from .todos import create_todo_internal
from ..services.llm_factory import LLMFactory

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "glm-4-flash"
    use_rag: bool = False

@router.get("/api/chat/models")
def get_available_models():
    """List all available LLM models."""
    return LLMFactory.get_all_models()

async def fetch_rag_context(query: str) -> str:
    url = "https://devmass.xunmei.com/xmmaas/maas/api/v1/chat/completions"
    
    payload = {
        "chatId": "65FA3539-B7C5-DE27-4E6C-FBA5E44E57D5", 
        "apiKey": "5041b9db97ed41d29fdf05c106f4371a",
        "messages": [
            {
                "guid": str(uuid.uuid4()),
                "role": "user",
                "content": [{
                    "type": "text",
                    "value": query
                }]
            }
        ]
    }
    
    try:
        async with httpx.AsyncClient() as client:
            print(f"🚀 Sending RAG request to {url} with query: {query}")
            response = await client.post(url, json=payload, timeout=30.0)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ RAG API Raw Response: {json.dumps(data, ensure_ascii=False)[:1000]}...")
                if data.get("code") == 200 and data.get("data"):
                    content_list = data["data"].get("content", [])
                    if content_list:
                        val = content_list[0].get("value", "")
                        print(f"📄 RAG Extracted Content Preview: {val[:500]}...") 
                        return val
            else:
                print(f"❌ RAG API Error Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
        print(f"❌ RAG API Exception: {e}")
        
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
    user_id = "00000000-0000-0000-0000-000000000000"
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
    user_id = "00000000-0000-0000-0000-000000000000"
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
    
    # 1. Intent Detection & Todo Extraction
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

        # Prepare context (exclude the last message which is the current one)
        context_msgs = [{"role": m.role, "content": m.content} for m in request.messages[:-1]]
        
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
    
    try:
        # 4. Normal Chat Flow (Fallthrough)
        rag_context = ""
        if request.use_rag:
            query_msg = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
            if query_msg:
                print(f"🔍 Fetching RAG context for: {query_msg}")
                rag_context = await fetch_rag_context(query_msg)

        system_instruction = """
        你是一个战略智僚助手。请以专业、简洁、有深度的风格直接回答用户的问题。
        """

        if rag_context:
            system_instruction += f"\n\n【参考知识库信息】\n{rag_context}\n\n请结合以上参考信息回答用户的问题。如果参考信息与问题不相关，请忽略它。"

        # Use LLM Factory to get provider and stream response
        provider = LLMFactory.get_provider(request.model)
        
        # Convert Pydantic messages to dict
        messages_dicts = [{"role": m.role, "content": m.content} for m in request.messages]
        
        response_generator = provider.chat_stream(
            model=request.model,
            messages=messages_dicts,
            system_instruction=system_instruction
        )

        async def generate():
            full_response = ""
            for content in response_generator:
                full_response += content
                yield f"data: {json.dumps({'content': content})}\n\n"
                await asyncio.sleep(0.005)
            
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



