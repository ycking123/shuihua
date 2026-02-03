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
from ..security import verify_token
# 引入同步的创建函数
from .todos import create_todo_internal

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "glm-4" # Updated default to standard glm-4 or glm-4-flash as requested
    use_rag: bool = False

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
                print(f"✅ RAG API Raw Response: {json.dumps(data, ensure_ascii=False)[:1000]}...") # Print first 1000 chars of raw response
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

@router.post("/api/chat")
async def chat_endpoint(request: ChatRequest, http_request: Request, db: Session = Depends(get_db)):
    api_key = os.getenv("LOCAL_ZHIPU_APIKEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="LOCAL_ZHIPU_APIKEY not configured")

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

    client = ZhipuAI(api_key=api_key)
    
    # 1. Intent Detection & Todo Extraction
    last_user_message = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
    
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

        intent_data = extract_todos_from_text(last_user_message)
            
        # If valid todo data found
        if intent_data and intent_data.get("task_list"):
            task_list = intent_data.get("task_list", [])
            summary_text = intent_data.get("summary", "已为您创建相关待办事项")
            
            created_tasks = []
            
            for t in task_list:
                # Map fields
                title = t.get('title', '新任务')
                description = t.get('description', '')
                priority_map = {"高": "urgent", "中": "high", "低": "normal"}
                priority = priority_map.get(t.get('priority'), "high")
                due_date = t.get('due_date')
                assignee = t.get('assignee')
                
                # Create in DB
                new_todo = create_todo_internal(
                    db, 
                    title, 
                    description, # Use description as summary/content
                    priority, 
                    "chat_record",
                    due_date,
                    assignee,
                    user_id=user_id # Pass the authenticated user_id
                )
                created_tasks.append(f"- **{title}** (责任人: {assignee}, 截止: {due_date})")
            
            # 3. Stream Confirmation
            async def generate_confirmation():
                msg = f"{summary_text}\n\n已创建 {len(created_tasks)} 个任务：\n" + "\n".join(created_tasks)
                    
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

        traceback.print_exc()
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

        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": system_instruction},
                *([{"role": m.role, "content": m.content} for m in request.messages])
            ],
            stream=True,
        )

        async def generate():
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
                    await asyncio.sleep(0.005)
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
    
    except Exception as e:
        import traceback
        print(f"❌ Chat generation failed: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


