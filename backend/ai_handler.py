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
    你是一个智能企业微信待办事项提取助手。
    请分析图片，提取：任务标题、详情描述、截止时间、责任人。
    
    【重要】请直接返回 JSON 格式。
    JSON 结构示例：
    {
      "summary": "总结",
      "task_list": [
        {
          "title": "任务名",
          "description": "详情",
          "due_date": "时间",
          "assignee": "责任人",
          "priority": "高/中/低"
        }
      ]
    }
    """

    try:
        response = client.chat.completions.create(
            model="glm-4v",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
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

def process_ai_result_and_push(json_output_str):
    """
    处理 AI 返回的 JSON 字符串并推送到后端
    """
    if not json_output_str:
        return False

    try:
        parsed_json = json.loads(json_output_str)
        print("✅ JSON 解析成功！")
        
        tasks = parsed_json.get('task_list', [])
        summary = parsed_json.get('summary', '聊天记录分析')
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
                # 尝试推送到本地后端 (假设运行在 8002)
                print(f"🚀 正在推送任务 '{payload['title']}' 到后端...")
                res = requests.post("http://localhost:8002/api/todos", json=payload)
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
