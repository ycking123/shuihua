import base64
import json
import os
import re  # <--- 【必须新增】导入正则模块
import requests
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from zhipuai import ZhipuAI

# ==========================================
# 配置区域
# ==========================================
# 加载环境变量
# env_path = Path(__file__).parent / ".env"
# load_dotenv(dotenv_path=env_path)
# root_env_path = Path(__file__).parent.parent / ".env.local"
# load_dotenv(dotenv_path=root_env_path)

ZHIPU_API_KEY = "cbbbe21037004729b1f65d80892c8bdc.cSRkRIEdSfNnBOIG" 

LOCAL_IMAGE_PATH = r"F:\成都实习文件夹\QQ截图20260126173813.png"

client = ZhipuAI(api_key=ZHIPU_API_KEY)

# ==========================================
# 辅助函数：转 Base64 (保持不变)
# ==========================================
def encode_local_image_to_base64(image_path):
    if not os.path.exists(image_path):
        print(f"错误：找不到本地图片文件: {image_path}")
        return None
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"❌ 图片处理失败: {e}")
        return None

# ==========================================
# AI 核心函数 (已修复解析逻辑)
# ==========================================
def analyze_chat_screenshot_with_glm4v(base64_image_data):
    """
    【AI 核心环节】
    修复版：使用正则表达式强行提取 JSON，忽略模型的废话
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
        # print(f"DEBUG-原始回复: {raw_content}") # 调试用

        # ---------------------------------------------------------
        # 核心修复代码：正则提取
        # ---------------------------------------------------------
        # 说明：
        # r'\{.*\}' : 查找从第一个 { 开始，到最后一个 } 结束的内容
        # re.DOTALL : 让 . 符号能匹配换行符 (因为JSON里肯定有换行)
        match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        
        if match:
            clean_json_str = match.group()
            return clean_json_str
        else:
            print("❌ 解析警告：在回复中没找到 JSON 大括号。")
            print("模型可能回复了纯文本：", raw_content)
            return None

    except Exception as e:
        print(f"❌ AI分析请求失败: {e}")
        return None

# ==========================================
# 主程序
# ==========================================
if __name__ == "__main__":
    # if ZHIPU_API_KEY == "你的_NEW_API_KEY":
    #      print("⚠️ 请先填写正确的 ZHIPU_API_KEY")
    #      exit()

    print(f"--- 开始处理流程，目标图片: {LOCAL_IMAGE_PATH} ---")

    # 1. 转码
    base64_data = encode_local_image_to_base64(LOCAL_IMAGE_PATH)

    # 模拟图片缺失的情况
    if not base64_data:
         print("⚠️ 图片未找到，跳过真实调用，使用模拟数据演示...")
         # 构造模拟数据
         json_output_str = json.dumps({
             "summary": "关于项目进度的讨论",
             "task_list": [
                 {
                     "title": "更新前端界面",
                     "description": "根据最新的设计稿更新首页和详情页的UI",
                     "due_date": "2026-02-01",
                     "assignee": "前端组",
                     "priority": "高"
                 },
                 {
                     "title": "后端接口优化",
                     "description": "优化数据查询接口的响应速度",
                     "due_date": "2026-02-05",
                     "assignee": "后端组",
                     "priority": "中"
                 }
             ]
         }, ensure_ascii=False)
    else:
        # 2. AI 分析
        json_output_str = analyze_chat_screenshot_with_glm4v(base64_data)
        
        # 如果 AI 分析失败（返回 None），则不进行后续处理或抛出错误
        if not json_output_str:
            print("⚠️ AI 分析未返回有效结果。")

    # 3. 结果验证
    if json_output_str:
        print("\n--- [提取到的干净 JSON] ---")
        print(json_output_str)
        print("---------------------------\n")

        try:
            parsed_json = json.loads(json_output_str)
            print("✅ JSON 解析成功！业务测试通过！")
            
            # 模拟业务展示
            tasks = parsed_json.get('task_list', [])
            print(f"发现 {len(tasks)} 个任务：")
            
            summary = parsed_json.get('summary', '聊天记录分析')

            for idx, t in enumerate(tasks):
                print(f"   - [{t.get('priority')}] {t.get('title')} (责任人: {t.get('assignee')})")
                print(f"     详情: {t.get('description')[:30]}...") 
                
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
                    print(f"🚀 正在推送任务 '{payload['title']}' 到后端...")
                    res = requests.post("http://localhost:8002/api/todos", json=payload)
                    if res.status_code == 200:
                        print(f"✅ 推送成功")
                    else:
                        print(f"❌ 推送失败: {res.status_code} - {res.text}")
                except Exception as e:
                    print(f"❌ 连接后端失败: {e}")

        except json.JSONDecodeError as e:
            print("❌ 依然解析失败，请检查 JSON 格式。")
            print(f"错误: {e}")
    else:
        print("流程异常终止。")