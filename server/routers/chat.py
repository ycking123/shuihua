from fastapi import APIRouter, HTTPException, Depends
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
# 引入同步的创建函数
from .todos import create_todo_internal

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
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    api_key = os.getenv("LOCAL_ZHIPU_APIKEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="LOCAL_ZHIPU_APIKEY not configured")

    client = ZhipuAI(api_key=api_key)
    
    # 1. Intent Detection & Todo Extraction
    last_user_message = next((m.content for m in reversed(request.messages) if m.role == "user"), "")
    
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 使用 ai_handler.py 中的高质量 Prompt
    system_prompt = """
    你是一个智能企业微信待办事项提取助手，严格遵循以下要求提取信息并返回结果：
    核心要求：
    1.  任务标题：必须直白、具体、核心动作前置，一眼知晓要完成什么工作，拒绝空洞修饰（如「相关工作」「事项处理」），不整虚的；若未明确指定标题，提取消息前 50 个字符并优化为直白核心标题。
    2.  必提信息：强制提取 DDL（截止时间）、责任人、任务详情，缺一不可。
    3.  DDL 规则：文本中明确提及 DDL 则直接提取并统一格式为 YYYY-MM-DD HH:MM；无明确提及 DDL 时，默认填充「当天日期 18:00」，格式为 YYYY-MM-DD HH:MM。
    4.  任务详情：完整提取任务的具体要求、执行内容、相关约束，不遗漏关键信息。
    5.  责任人：文本中有明确责任人则直接提取；无明确责任人时，标记为「Sender（发送者）」。
    6.  优先级：根据文本语气判断（高/中/低），紧急语气（如「尽快」「务必」「今日完成」）标记为高，默认优先级为中。

    【重要】
    1.  直接返回 JSON 格式，无任何额外解释、备注、换行符之外的冗余内容。
    2.  JSON 结构严格遵循以下示例，字段不可增减、格式不可修改。
    JSON 结构示例：
    {
      "summary": "待办事项汇总（简要概括所有任务核心）",
      "task_list": [
        {
          "title": "撰写XX产品需求文档（V1.0版本）",
          "description": "1. 结合用户反馈梳理产品核心功能；2. 绘制产品原型流程图；3. 标注功能优先级和实现难点",
          "due_date": "2026-01-30 18:00",
          "assignee": "Sender（发送者）",
          "priority": "中"
        }
      ]
    }
    """
    
    # First, try to detect if it's a todo/intent request
    # Use a simpler check or just apply the extraction model directly?
    # Applying directly is safer as it can return empty task_list if no tasks found.
    
    print(f"🤖 Analyzing intent for: {last_user_message[:50]}...")
    
    try:
        intent_response = client.chat.completions.create(
            model="glm-4-flash", # Use flash for speed
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\n【当前系统时间】：{current_time_str}"},
                {"role": "user", "content": last_user_message}
            ],
            stream=False,
            temperature=0.1
        )
        
        intent_content = intent_response.choices[0].message.content
        # Clean up code blocks if present
        if intent_content.startswith("```json"):
            intent_content = intent_content[7:]
        if intent_content.startswith("```"):
            intent_content = intent_content[3:]
        if intent_content.endswith("```"):
            intent_content = intent_content[:-3]
            
        # Try to parse JSON
        intent_data = None
        try:
            match = re.search(r'\{.*\}', intent_content, re.DOTALL)
            if match:
                intent_data = json.loads(match.group())
        except:
            pass
            
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
                    assignee
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
        print(f"Intent detection/Creation failed: {e}")
        # Fallback to normal chat

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

