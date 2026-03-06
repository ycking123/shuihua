
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

def extract_todos_from_text(text_content, context_messages=None):
    """
    从文本和上下文中提取待办事项，支持缺省参数追问
    """
    if not text_content:
        return None

    # 构建上下文对话字符串供 LLM 参考
    context_str = ""
    if context_messages:
        # 取最近 5 条记录作为上下文
        recent_msgs = context_messages[-5:] 
        for msg in recent_msgs:
            role_name = "User" if msg.get("role") == "user" else "Assistant"
            content = msg.get("content", "")
            context_str += f"{role_name}: {content}\n"
    
    system_prompt = """
    你是一个智能企业助手。你的任务分两步：
    1. **意图判断**：判断用户是否想要创建待办、会议、提醒或日程。
    2. **待办提取**：如果是，则严格收集信息；如果不是，直接返回非待办标记。

    【第一步：意图判断（优先级最高）】
    - 如果用户的输入只是日常闲聊（如“你好”、“吃了吗”）、普通问答（如“介绍下公司”、“写首诗”）、或者与创建任务无关的内容：
      **直接返回**：{"is_todo": false}
    - 只有当用户明确表达了“安排”、“提醒”、“开会”、“要做...”等创建意图，或者正在回复之前的任务追问时，才进入第二步。

    【第二步：严格待办提取（仅当意图为创建任务时执行）】
    你的目标是：**收集完整的信息以创建任务，绝不通过猜测来补充缺失信息。**

    任何任务（Task/Meeting）必须**同时具备**以下 5 个要素才能创建，缺一不可：
    1. **主题 (title)**: 做什么？（例如：系统部署、周会）。
    2. **具体时间 (due_date)**: 什么时候？必须精确到“点”（例如：明天上午9点）。仅说“明天”是不够的，视为缺失。
    3. **责任人/参会人 (assignee)**: 谁？必须明确指定人名（例如：小张、王总）或明确说“我”。**如果没有提到人名，绝对视为缺失！禁止默认设为“我”！**
    4. **优先级 (priority)**: 紧急程度。必须明确提及（紧急/重要/一般/低）。如果不说，视为缺失。
    5. **类型 (type)**: 任务类型。必须是以下之一：task (普通任务), meeting (会议), chat_record (聊天记录), email (邮件), approval (审批)。如果不确定，默认为 task。

    【工作流程 - 严格执行】
    1. **合并信息**：阅读【对话上下文】和【当前输入】，将所有已知信息填入“信息槽”。
    2. **完整性检查**：
       - 检查 title 是否存在？
       - 检查 due_date 是否精确到分钟/小时？
       - 检查 assignee 是否明确提及？
       - 检查 priority 是否明确提及？
    3. **决策输出**：
       - **只要有任何一项缺失**（type 默认为 task，不算缺失）：
         - status = "clarification_needed"
         - missing_fields = [所有缺失的字段列表]
         - clarification_question = "收到[已有的信息]。请补充[缺失字段1]、[缺失字段2]..." (一次性问完！)
       - **只有当 4 项核心要素（title, due_date, assignee, priority）全部确切存在**：
         - status = "completed"
         - 生成 task_list (包含 type)

    【JSON输出结构】
    
    场景 A：非任务
    User: 你好
    { "is_todo": false }

    场景 B：任务信息不全
    User: 明天开会
    {
      "is_todo": true,
      "status": "clarification_needed",
      "missing_fields": ["title", "due_date", "assignee", "priority"],
      "clarification_question": "..."
    }

    场景 C：任务信息齐全
    User: ... (4要素齐备)
    {
      "is_todo": true,
      "status": "completed",
      "task_list": [
          {
              "title": "...",
              "description": "...",
              "due_date": "...",
              "assignee": "...",
              "priority": "...",
              "type": "meeting" 
          }
      ]
    }
    """
    
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 构建最终的 prompt messages
    messages_payload = [
        {"role": "system", "content": f"{system_prompt}\n\n【当前系统时间】：{current_time_str}"}
    ]
    
    if context_str:
        messages_payload.append({"role": "system", "content": f"【对话上下文参考】：\n{context_str}"})
        
    messages_payload.append({"role": "user", "content": text_content})

    try:
        response = client.chat.completions.create(
            model="glm-4.6",
            messages=messages_payload,
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

