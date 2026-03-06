# ============================================================================
# 文件: ai_handler.py
# 模块: backend
# 职责: AI 文本分析，使用智谱 AI 从会议文本中提取待办事项和摘要
#
# 依赖声明:
#   - 外部: base64, json, os, re, time, requests, logging, datetime, pathlib, dotenv
#   - 可选: zhipuai (ZhipuAI) - 智谱 AI SDK
#
# 主要接口:
#   - extract_todos_from_text(text) -> Dict: 从会议文本提取待办事项和摘要
#
# 环境变量:
#   - ZHIPUAI_API_KEY / Zhipuai_API_KEY: 智谱 AI API 密钥
#
# ============================================================================

import base64
import json
import os
import re
import time
import requests
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 配置日志
logger = logging.getLogger("AIHandler")

try:
    from zhipuai import ZhipuAI
except ImportError:
    ZhipuAI = None
    logger.error("❌ 未安装 zhipuai 库，AI 功能将不可用")

# 加载环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

ZHIPU_API_KEY = os.getenv("ZHIPUAI_API_KEY") or os.getenv("Zhipuai_API_KEY")
if not ZHIPU_API_KEY:
    # 尝试从 root .env.local 加载
    root_env_path = Path(__file__).parent.parent / ".env.local"
    load_dotenv(dotenv_path=root_env_path)
    ZHIPU_API_KEY = os.getenv("ZHIPUAI_API_KEY") or os.getenv("Zhipuai_API_KEY")

if not ZHIPU_API_KEY:
    # 尝试读取 LOCAL_ZHIPU_APIKEY (兼容 server/routers/chat.py 的配置)
    ZHIPU_API_KEY = os.getenv("LOCAL_ZHIPU_APIKEY")

client = None
if ZhipuAI and ZHIPU_API_KEY:
    try:
        client = ZhipuAI(api_key=ZHIPU_API_KEY)
    except Exception as e:
        logger.error(f"❌ ZhipuAI 客户端初始化失败: {e}")

def analyze_chat_screenshot_with_glm4v(base64_image_data):
    """
    【AI 核心环节】
    使用 GLM-4V 分析图片，提取待办事项
    """
    if not base64_image_data or not client:
        logger.warning("⚠️ 无法分析图片: 图片数据为空或客户端未初始化")
        return None

    logger.info("🤖 开始调用 GLM-4V 模型进行分析，请稍候...")

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
            model="glm-4.6",
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
    分析用户文本意图：闲聊 (chat) / 普通待办 (todo) / 创建会议 (meeting) / 创建群聊 (group_chat)
    """
    if not text_content:
        return "chat"

    system_prompt = """
    请判断用户的意图，只能返回以下四种之一：
    - chat：闲聊/普通问答/咨询（如"你好""怎么配置环境""介绍下公司"）。
    - meeting：与会议创建相关（如"安排会议""预定会议""讨论一下在几点开会"）。
    - todo：与任务创建/提醒相关（如"今天下班前提交报表""安排XX任务给小张"）。
    - group_chat：与创建群聊/建群/创建群组相关（如"创建群聊""建个群""拉个群讨论""创建项目群"）。

    只返回一个单词：chat / meeting / todo / group_chat，不要包含其他字符。
    """

    try:
        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {"role": "user", "content": f"{system_prompt}\n\n用户消息：{text_content}"}
            ],
            temperature=0.1,
        )
        intent = response.choices[0].message.content.strip().lower()
        if "meeting" in intent:
            return "meeting"
        if "todo" in intent:
            return "todo"
        if "group" in intent or "group_chat" in intent:
            return "group_chat"
        return "chat"
    except Exception as e:
        print(f"❌ 意图识别失败: {e}")
        return "chat"

def extract_group_chat_info(text_content):
    """
    提取创建群聊的关键信息
    """
    system_prompt = """
    你是一个群聊创建助手。请从文本中提取创建群聊所需的信息。

    需要提取：
    1. chat_name: 群聊名称（默认为 "新群聊"）
    2. user_ids: 成员UserID列表（从@用户名或"成员:"后提取）

    请直接返回 JSON:
    {
        "chat_name": "项目讨论群",
        "user_ids": ["user1", "user2", "user3"]
    }

    注意：
    - 群名称通常是"创建群聊"、"建群"等关键词后的第一个短语
    - 成员可以从@符号后提取，或从"成员:"、"用户:"后的逗号分隔列表中提取
    - 如果文本中没有明确指定成员，返回空列表
    """

    try:
        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {"role": "user", "content": f"{system_prompt}\n\n用户消息：{text_content}"}
            ],
            temperature=0.1,
        )
        content = response.choices[0].message.content

        # 尝试解析 JSON
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            json_str = match.group()
            result = json.loads(json_str)
            # 确保 user_ids 是列表
            if not isinstance(result.get("user_ids"), list):
                result["user_ids"] = []
            return result
        return {"chat_name": "新群聊", "user_ids": []}
    except Exception as e:
        print(f"❌ 群聊信息提取失败: {e}")
        return {"chat_name": "新群聊", "user_ids": []}


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
            model="glm-4.6",
            messages=[
                {"role": "user", "content": f"{system_prompt}\n\n用户消息：{text_content}"}
            ],
            temperature=0.1,
        )
        content = response.choices[0].message.content

        # 尝试解析 JSON
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            json_str = match.group()
            return json.loads(json_str)
        return None
    except Exception as e:
        print(f"❌ 会议信息提取失败: {e}")
        return None

def extract_todos_from_text(text_content):
    """
    从文本中提取待办事项
    """
    if not text_content or not client:
        if not client:
            logger.warning("⚠️ AI 客户端未初始化，跳过文本提取")
        return None

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
      "summary": "（这里必须生成一段针对输入文本的简要总结，概括核心议题和结论，不要抄示例）",
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
    
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 截断过长的文本，防止 token 溢出 (保留前 50000 字符)
    truncated_content = text_content[:50000] if text_content else ""

    try:
        response = client.chat.completions.create(
            model="glm-4.6",
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\n【当前系统时间】：{current_time_str}"},
                {"role": "user", "content": truncated_content}
            ],
            temperature=0.1,
        )
        
        raw_content = response.choices[0].message.content
        
        # 清理可能存在的 markdown 代码块标记
        if raw_content.startswith("```json"):
            raw_content = raw_content[7:]
        if raw_content.startswith("```"):
            raw_content = raw_content[3:]
        if raw_content.endswith("```"):
            raw_content = raw_content[:-3]
            
        # 正则提取 JSON
        match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        
        if match:
            clean_json_str = match.group()
            return json.loads(clean_json_str)
        else:
            return None

    except Exception as e:
        logger.error(f"❌ 文本待办提取失败: {e}")
        return None

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
            model="glm-4.6",
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

