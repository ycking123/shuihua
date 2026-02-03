
import os
import json
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# Load environment variables
# Try loading from .env in server root or project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

ZHIPU_API_KEY = os.getenv("ZHIPUAI_API_KEY")
if not ZHIPU_API_KEY:
    ZHIPU_API_KEY = os.getenv("LOCAL_ZHIPU_APIKEY")

client = ZhipuAI(api_key=ZHIPU_API_KEY)

def extract_todos_from_text(text_content):
    """
    从文本中提取待办事项
    """
    if not text_content:
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
    
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        response = client.chat.completions.create(
            model="glm-4",
            messages=[
                {"role": "system", "content": f"{system_prompt}\n\n【当前系统时间】：{current_time_str}"},
                {"role": "user", "content": text_content}
            ],
            temperature=0.1,
        )
        
        raw_content = response.choices[0].message.content
        print(f"🤖 AI Extraction Raw Response: {raw_content[:200]}...") # Log for debug
        
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
            print("❌ No JSON found in response")
            return None

    except Exception as e:
        print(f"❌ 文本待办提取失败: {e}")
        return None

