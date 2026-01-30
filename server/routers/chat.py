from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from zhipuai import ZhipuAI
import os
import json
try:
    from .todos import create_todo_internal
except ImportError:
    from routers.todos import create_todo_internal

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "glm-4-flash"

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
    
    Example JSON:
    {"is_todo": true, "title": "Buy Milk", "summary": "Buy milk from the supermarket tomorrow morning", "priority": "normal"}
    
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
            
            new_todo = create_todo_internal(title, summary, priority)
            
            # 3. Stream Confirmation
            async def generate_confirmation():
                msg = f"已为您创建待办事项：**{title}**\n\n摘要：{summary}\n优先级：{priority}"
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
    system_instruction = """
    你是一个战略智僚助手。请以专业、简洁、有深度的风格直接回答用户的问题。
    """

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
