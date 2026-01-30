from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from zhipuai import ZhipuAI
import os
import json
import httpx
import uuid
# Explicit absolute import to ensure singleton sharing
from routers.todos import create_todo_internal

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "glm-4-flash"
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
async def chat_endpoint(request: ChatRequest):
    api_key = os.getenv("LOCAL_ZHIPU_APIKEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="LOCAL_ZHIPU_APIKEY not configured")

    client = ZhipuAI(api_key=api_key)
    
    # 1. Intent Detection
    last_user_message = next((m.content for m in reversed(request.messages) if m.role == "user" or m.role == "user"), "")
    
    intent_instruction = """
    Analyze the user's message to determine if they want to create a todo task, reminder, or schedule something.
    Return ONLY a JSON object with the following fields:
    - is_todo: boolean (true if the user wants to create a task/todo)
    - title: string (a short title for the task, max 10 chars)
    - summary: string (a detailed summary of the task)
    - priority: string (one of: "urgent", "high", "normal")
    - category: string (one of: "email", "meeting", "approval", "chat_record")
      - email: for sending emails, checking emails, writing drafts
      - meeting: for scheduling meetings, reminders about meetings
      - approval: for reviewing documents, approving requests
      - chat_record: for general reminders, miscellaneous tasks, or anything that doesn't fit in other categories
    
    Example JSON:
    {"is_todo": true, "title": "Buy Milk", "summary": "Buy milk from the supermarket tomorrow morning", "priority": "normal", "category": "chat_record"}
    
    If it's just a chat or question, return:
    {"is_todo": false}
    """
    
    try:
        intent_response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "system", "content": intent_instruction},
                {"role": "user", "content": last_user_message}
            ],
            stream=False
        )
        
        intent_content = intent_response.choices[0].message.content
        # Clean up code blocks if present
        if intent_content.startswith("```json"):
            intent_content = intent_content[7:]
        if intent_content.startswith("```"):
            intent_content = intent_content[3:]
        if intent_content.endswith("```"):
            intent_content = intent_content[:-3]
            
        intent_data = json.loads(intent_content)
        
        if intent_data.get("is_todo"):
            # 2. Create Todo
            title = intent_data.get("title", "New Task")
            summary = intent_data.get("summary", last_user_message)
            priority = intent_data.get("priority", "high")
            category = intent_data.get("category", "chat_record")
            
            # Map LLM output to valid categories just in case
            valid_categories = ["email", "meeting", "approval", "chat_record"]
            if category not in valid_categories:
                category = "chat_record"
            
            new_todo = create_todo_internal(title, summary, priority, category)
            
            # 3. Stream Confirmation
            async def generate_confirmation():
                msg = f"已为您创建待办事项：**{title}**\n\n分类：{category}\n摘要：{summary}\n优先级：{priority}"
                # Simulate streaming for consistent UX
                for char in msg:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                    # await asyncio.sleep(0.01) # Optional delay
                yield "data: [DONE]\n\n"
                
            return StreamingResponse(generate_confirmation(), media_type="text/event-stream")

    except Exception as e:
        print(f"Intent detection failed: {e}")
        # Fallback to normal chat if intent detection fails or it's not a todo

    # 4. Normal Chat Flow
    rag_context = ""
    if request.use_rag:
        # Extract last user message for RAG query
        # We need to find the last message that is from user to use as query
        query_msg = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
        if query_msg:
            print(f"🔍 Fetching RAG context for: {query_msg}")
            rag_context = await fetch_rag_context(query_msg)
            if rag_context:
                print(f"📚 RAG Context retrieved (length: {len(rag_context)})")
            else:
                print("⚠️ No RAG context retrieved")

    system_instruction = """
    你是一个战略智僚助手。请以专业、简洁、有深度的风格直接回答用户的问题。
    """

    if rag_context:
        system_instruction += f"\n\n【参考知识库信息】\n{rag_context}\n\n请结合以上参考信息回答用户的问题。如果参考信息与问题不相关，请忽略它。"

    messages_payload = [
        {"role": "system", "content": system_instruction}
    ]
    for msg in request.messages:
        role = "assistant" if msg.role == "model" else msg.role
        messages_payload.append({"role": role, "content": msg.content})

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=messages_payload,
            stream=True
        )

        def generate():
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield f"data: {json.dumps({'content': chunk.choices[0].delta.content})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")
            
    except Exception as e:
        print(f"Error calling ZhipuAI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

