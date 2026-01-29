import fitz  # PyMuPDF
from zhipuai import ZhipuAI
import json
import re
import requests
import time
from datetime import datetime

ZHIPU_API_KEY = "cbbbe21037004729b1f65d80892c8bdc.cSRkRIEdSfNnBOIG" 

#
def extract_text_from_pdf(pdf_source):
    """
    使用 PyMuPDF 暴力提取 PDF 文本
    :param pdf_source: 文件路径(str) 或 文件二进制流(bytes)
    """
    text_content = []
    
    try:
        # 判断是文件路径还是二进制流（企微API下载通常是bytes）
        if isinstance(pdf_source, bytes):
            doc = fitz.open(stream=pdf_source, filetype="pdf")
        else:
            doc = fitz.open(pdf_source)

        print(f"📄 开始解析 PDF，共 {len(doc)} 页...")

        for page_num, page in enumerate(doc):
            # 提取文本，flag=0 为纯文本模式
            page_text = page.get_text("text") 
            if page_text.strip():
                text_content.append(f"--- 第 {page_num + 1} 页 ---\n{page_text}")
        
        doc.close()
        full_text = "\n".join(text_content)
        print(f"✅ 解析完成，提取字符数: {len(full_text)}")
        return full_text

    except Exception as e:
        print(f"❌ PDF 解析失败: {e}")
        return None

def analyze_with_zhipu(text_content):
    """
    调用智谱 GLM-4 模型提取待办事项
    """
    if not text_content:
        return None

    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    
    # 构造系统提示词 (System Prompt)
    system_prompt = """
    你是一个专业的会议纪要整理助手。请分析用户提供的会议记录文本，提取出明确的待办事项(Todo)。
    
    要求：
    1. 忽略闲聊和无关背景，只提取需要执行的任务。
    2. 如果文本中没有提到具体执行人，标记为 "待定"。
    3. 如果没有提到截止时间，根据上下文推断或标记为 null。
    4. **必须**只返回纯净的 JSON 格式字符串，不要包含 Markdown 标记（如 ```json）。
    
    输出数据结构示例：
    {
        "meeting_topic": "会议主题",
        "todos": [
            {
                "task": "任务描述",
                "owner": "责任人",
                "deadline": "YYYY-MM-DD"
            }
        ]
    }
    """

    print("🤖 正在请求智谱大模型分析...")
    
    try:
        response = client.chat.completions.create(
            model="glm-4",  # 推荐使用 glm-4 或 glm-4-flash (速度更快)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"以下是会议记录文本：\n\n{text_content}"}
            ],
            temperature=0.1,  # 低温度以保证输出格式稳定
            top_p=0.7,
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # 清洗可能存在的 Markdown 代码块标记
        result_text = result_text.replace("```json", "").replace("```", "")
        
        # 尝试解析 JSON 以验证格式
        json_data = json.loads(result_text)
        return json_data

    except json.JSONDecodeError:
        print("❌ 模型返回的不是合法的 JSON，原始返回:", result_text)
        return None
    except Exception as e:
        print(f"❌ 智谱 API 调用失败: {e}")
        return None

# --- 模拟运行流程 ---
if __name__ == "__main__":
    # 模拟场景：你从企微下载的 PDF 文件路径
    # 在实际企微回调中，你会先 requests.get(url) 拿到 bytes
    pdf_file_path = r"F:\成都实习文件夹\会议主题.pdf" 
    
    # 1. 提取文本
    # 注意：如果没有本地文件，这段代码会报错，请确保目录下有一个 test_meeting.pdf
    # 或者你可以传入一个 dummy text 进行测试
    
    # 这里演示如果只有路径的情况：
    content = extract_text_from_pdf(pdf_file_path)
    
    if not content:
        print("⚠️ 未找到PDF或解析失败，使用测试文本进行演示...")
        content = """
    会议记录 2026-01-27
    张三：我们要尽快上线“水华精灵”的V4版本。
    李四：好的，那我负责后端的API接口鉴权，下周三前搞定。
    王五：我去联系UI设计，让他们明天把设计图发出来。
    张三：记得把服务器扩容一下，还有要把会议纪要自动同步到网页端。
    """

    # 2. 大模型分析
    if content:
        todo_data = analyze_with_zhipu(content)
        
        # 3. 输出结果
        if todo_data:
            print("\n🎉 提取成功! 结果如下：")
            print(json.dumps(todo_data, indent=4, ensure_ascii=False))
            
            # 推送到后端待办事项 API
            print("\n🚀 正在推送至待办系统...")
            meeting_topic = todo_data.get("meeting_topic", "会议待办")
            
            for idx, todo in enumerate(todo_data.get("todos", [])):
                # 构造符合后端 API 的数据结构
                payload = {
                    "id": f"meeting-{int(time.time())}-{idx}",
                    "type": "meeting",
                    "priority": "high",
                    "title": f"[{todo.get('owner', '待定')}] {todo.get('task')}",
                    "sender": meeting_topic,
                    "time": datetime.now().strftime("%H:%M"),
                    "completed": False,
                    "status": "pending",
                    "aiSummary": f"截止日期: {todo.get('deadline', '未指定')}",
                    "content": f"任务详情: {todo.get('task')}\n责任人: {todo.get('owner')}\n截止时间: {todo.get('deadline')}",
                    "isUserTask": False
                }
                
                try:
                    res = requests.post("http://localhost:8002/api/todos", json=payload)
                    if res.status_code == 200:
                        print(f"✅ 任务 '{payload['title']}' 推送成功")
                    else:
                        print(f"❌ 推送失败: {res.status_code} - {res.text}")
                except Exception as e:
                    print(f"❌ 连接后端失败: {e}")
                    print("请确保后端服务已启动 (python -m uvicorn backend.main:app --port 8002)")
