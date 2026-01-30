import base64
import json
import os
import re
import time
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# 加载环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

ZHIPU_API_KEY = os.getenv("ZHIPUAI_API_KEY")
if not ZHIPU_API_KEY:
    # 尝试从 root .env.local 加载
    root_env_path = Path(__file__).parent.parent / ".env.local"
    load_dotenv(dotenv_path=root_env_path)
    ZHIPU_API_KEY = os.getenv("ZHIPUAI_API_KEY")

client = ZhipuAI(api_key=ZHIPU_API_KEY)

def analyze_chat_screenshot_with_glm4v(base64_image_data):
    """
    【AI 核心环节】
    使用 GLM-4V 分析图片，提取待办事项
    """
    if not base64_image_data:
        return None

    print("🤖 开始调用 GLM-4V 模型进行分析，请稍候...")

    system_prompt = """
    你是一个智能企业微信待办事项提取助手，严格遵循以下要求提取信息并返回结果：
    核心要求：
    1.  任务标题：必须直白、具体、核心动作前置，一眼知晓要完成什么工作，拒绝空洞修饰（如「相关工作」「事项处理」），不整虚的；若未明确指定标题，提取内容前 50 个字符并优化为直白核心标题。
    2.  必提信息：强制提取 DDL（截止时间）、责任人、任务详情，缺一不可。
    3.  DDL 规则：图片中明确提及 DDL 则直接提取并统一格式为 YYYY-MM-DD HH:MM；无明确提及 DDL 时，默认填充「当天日期 18:00」，格式为 YYYY-MM-DD HH:MM。
    4.  任务详情：完整提取任务的具体要求、执行内容、相关约束，不遗漏关键信息。
    5.  责任人：图片中有明确责任人则直接提取；无明确责任人时，标记为「Sender（发送者）」。
    6.  优先级：根据内容语气判断（高/中/低），紧急语气（如「尽快」「务必」「今日完成」）标记为高，默认优先级为中。

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
    
    # Get current time for context
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Prepend time context to prompt since GLM-4V messages structure is strict
    full_prompt = f"{system_prompt}\n\n【当前系统时间】：{current_time_str}"

    try:
        response = client.chat.completions.create(
            model="glm-4v",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": full_prompt},
                        {"type": "image_url", "image_url": {"url": base64_image_data}}
                    ]
                }
            ],
            temperature=0.1, # 低温度保证输出稳定
        )
        
        # 获取原始回复
        raw_content = response.choices[0].message.content
        print("✅ 模型调用成功，收到原始响应。")

        # 正则提取 JSON
        match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        
        if match:
            clean_json_str = match.group()
            return clean_json_str
        else:
            print("❌ 解析警告：在回复中没找到 JSON 大括号。")
            return None

    except Exception as e:
        print(f"❌ AI分析请求失败: {e}")
        return None

def parse_ai_result_to_todos(json_output_str, sender_id=None):
    """解析 AI 返回的 JSON 字符串为待办事项列表"""
    if not json_output_str:
        return []
    try:
        parsed_json = json.loads(json_output_str)
        tasks = parsed_json.get('task_list', [])
        todo_list = []
        for idx, t in enumerate(tasks):
            priority_map = {"高": "urgent", "中": "high", "低": "normal"}
            api_priority = priority_map.get(t.get('priority'), "normal")
            
            # Use sender_id if available, otherwise default
            sender_name = sender_id if sender_id else parsed_json.get('summary', '聊天记录分析')
            
            payload = {
                "id": f"chat-record-{int(time.time())}-{idx}",
                "type": "chat_record",
                "priority": api_priority,
                "title": f"[{t.get('assignee', '待定')}] {t.get('title')}",
                "sender": sender_name,
                "time": datetime.now().strftime("%H:%M"),
                "completed": False,
                "status": "pending",
                "aiSummary": f"截止日期: {t.get('due_date', '未指定')}",
                "content": f"任务详情: {t.get('description')}\n责任人: {t.get('assignee')}\n截止时间: {t.get('due_date')}",
                "isUserTask": False
            }
            todo_list.append(payload)
        return todo_list
    except json.JSONDecodeError as e:
        print("❌ JSON 解析失败")
        return []

def analyze_intent(text_content):
    """
    分析用户文本意图：是普通待办 (todo) 还是创建会议 (meeting)
    """
    if not text_content:
        return "todo"

    system_prompt = """
    请判断用户的意图。
    如果用户想 "开会"、"预定会议"、"安排会议"、"讨论一下"，返回 "meeting"。
    否则（如安排任务、提醒事项、普通待办），返回 "todo"。
    
    【重要】仅返回单词 "meeting" 或 "todo"，不要包含其他字符。
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "user", "content": f"{system_prompt}\n\n用户消息：{text_content}"}
            ],
            temperature=0.1,
        )
        intent = response.choices[0].message.content.strip().lower()
        if "meeting" in intent:
            return "meeting"
        return "todo"
    except Exception as e:
        print(f"❌ 意图识别失败: {e}")
        return "todo"

def extract_meeting_info(text_content):
    """
    提取会议关键信息
    """
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    system_prompt = f"""
    你是一个会议助理。请从文本中提取会议信息。
    当前时间: {current_time_str}
    
    需要提取：
    1. topic: 会议主题（默认为 "临时讨论"）
    2. start_time: 开始时间 (格式 YYYY-MM-DD HH:MM)。若未指定，默认为当前时间后30分钟。
    3. duration: 持续时长（秒）。若未指定，默认为 3600 (1小时)。
    4. attendees: 参会人列表（名字）。
    
    请直接返回 JSON:
    {{
        "topic": "主题",
        "start_time": "2024-01-01 10:00",
        "duration": 3600,
        "attendees": ["张三", "李四"]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "user", "content": f"{system_prompt}\n\n用户消息：{text_content}"}
            ],
            temperature=0.1,
        )
        content = response.choices[0].message.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            info = json.loads(match.group())
            # Convert time string to timestamp
            try:
                if "start_time" in info and isinstance(info["start_time"], str):
                    dt = datetime.strptime(info["start_time"], "%Y-%m-%d %H:%M")
                    info["start_time"] = int(dt.timestamp())
            except Exception as e:
                print(f"⚠️ 时间转换失败: {e}, 使用默认时间")
                info["start_time"] = int(time.time() + 1800)
            return info
    except Exception as e:
        print(f"❌ 会议信息提取失败: {e}")
    
    # Fallback default
    return {
        "topic": "临时讨论",
        "start_time": int(time.time() + 1800),
        "duration": 3600,
        "attendees": []
    }

def analyze_text_message(text_content):
    """
    分析纯文本消息，提取待办事项
    """
    if not text_content:
        return None

    print(f"🤖 开始分析文本消息: {text_content[:20]}...")

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

    # Get current time for context
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {
                    "role": "user",
                    "content": f"{system_prompt}\n\n【当前系统时间】：{current_time_str}\n\n用户消息：{text_content}"
                }
            ],
            temperature=0.1,
        )
        
        raw_content = response.choices[0].message.content
        match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        
        if match:
            clean_json_str = match.group()
            return clean_json_str
        else:
            return None

    except Exception as e:
        print(f"❌ AI文本分析失败: {e}")
        return None

def process_ai_result_and_push(json_output_str, sender_id=None):
    """
    处理 AI 返回的 JSON 字符串并推送到后端
    """
    if not json_output_str:
        return False

    try:
        parsed_json = json.loads(json_output_str)
        print("✅ JSON 解析成功！")
        
        tasks = parsed_json.get('task_list', [])
        
        # Use sender_id if available, otherwise default
        summary = sender_id if sender_id else parsed_json.get('summary', '聊天记录分析')
        
        print(f"发现 {len(tasks)} 个任务")

        success_count = 0
        for idx, t in enumerate(tasks):
            # 推送到后端 API
            priority_map = {"高": "urgent", "中": "high", "低": "normal"}
            api_priority = priority_map.get(t.get('priority'), "normal")
            
            payload = {
                "id": f"chat-record-{int(time.time())}-{idx}",
                "type": "chat_record",  # 前端对应的新分类
                "priority": api_priority,
                "title": f"[{t.get('assignee', '待定')}] {t.get('title')}",
                "sender": summary,
                "time": datetime.now().strftime("%H:%M"),
                "completed": False,
                "status": "pending",
                "aiSummary": f"截止日期: {t.get('due_date', '未指定')}",
                "content": f"任务详情: {t.get('description')}\n责任人: {t.get('assignee')}\n截止时间: {t.get('due_date')}",
                "isUserTask": False
            }
            
            try:
                # 尝试推送到本地后端 (假设运行在 8080)
                print(f"🚀 正在推送任务 '{payload['title']}' 到后端...")
                res = requests.post("http://localhost:8080/api/todos", json=payload)
                if res.status_code == 200:
                    success_count += 1
                    print(f"✅ 推送成功")
                else:
                    print(f"❌ 推送失败: {res.status_code} - {res.text}")
            except Exception as e:
                print(f"❌ 连接后端失败: {e}")
        
        return success_count > 0

    except json.JSONDecodeError as e:
        print("❌ JSON 解析失败")
        return False
