import json
import os
import time
import base64
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from zhipuai import ZhipuAI

# 加载环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

def analyze_with_llm(text_content, image_paths):
    """
    使用智谱 AI (GLM-4V) 分析会议截图和文本，提取待办事项。
    """
    api_key = os.getenv("ZHIPUAI_API_KEY")
    if not api_key:
        print("❌ 未找到 ZHIPUAI_API_KEY，无法进行 AI 分析")
        return None

    print("\n🧠 正在调用大模型分析会议纪要...")
    client = ZhipuAI(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": "你是一个严格的会议待办提取助手。你只能输出 JSON 格式的数据。不要输出任何其他解释性文字。不要描述图片。"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请分析提供的会议截图和文本，提取待办事项。\n"
                            "必须返回 JSON 数组，格式如下：\n"
                            "[\n"
                            "  {\"id\": \"1\", \"content\": \"任务内容\", \"priority\": \"high\", \"status\": \"pending\"}\n"
                            "]"
                }
            ]
        }
    ]

    # 添加图片内容 (添加到 user 消息，即 messages[1])
    for img_path in image_paths:
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
                messages[1]["content"].append({
                    "type": "image_url",
                    "image_url": {
                        "url": encoded_string
                    }
                })
            print(f"  - 已添加图片: {img_path}")

    # 添加文本内容
    if text_content:
        messages[1]["content"].append({
            "type": "text",
            "text": f"\n\n参考文本内容 (OCR/HTML提取):\n{text_content[:5000]}..."
        })

    try:
        response = client.chat.completions.create(
            model="glm-4v",  # 使用视觉模型
            messages=messages,
            temperature=0.1,
            top_p=0.7,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        print("✅ 大模型(视觉)分析完成")
        
        # 检查是否为 JSON 格式
        cleaned_result = result.strip()
        # 移除可能存在的 markdown 代码块
        if cleaned_result.startswith("```json"):
            cleaned_result = cleaned_result.replace("```json", "").replace("```", "").strip()
        elif cleaned_result.startswith("```"):
            cleaned_result = cleaned_result.replace("```", "").strip()
        
        if cleaned_result.startswith("{"):
            return cleaned_result
        else:
            print("⚠️ 视觉模型未返回标准 JSON 对象，尝试使用文本模型整理结果...")
            # Fallback: 使用文本模型整理
            fallback_messages = [
                {
                    "role": "system", 
                    "content": "你是一个数据格式化助手。请将用户的描述转换为包含 summary 和 todos 的 JSON 对象。"
                },
                {
                    "role": "user",
                    "content": f"基于以下会议描述和文本，提取会议纪要和待办事项并输出 JSON 对象。\n\n视觉模型描述:\n{result}\n\n原始文本:\n{text_content[:3000]}\n\n目标格式: {{\"summary\": \"...\", \"todos\": [...]}}"
                }
            ]
            
            fb_response = client.chat.completions.create(
                model="glm-4-flash",
                messages=fallback_messages,
                temperature=0.1
            )
            
            fb_content = fb_response.choices[0].message.content.strip()
            import re
            # Use regex to find JSON object
            match = re.search(r'\{.*\}', fb_content, re.DOTALL)
            if match:
                fb_content = match.group(0)
                
            return fb_content

    except Exception as e:
        print(f"❌ 大模型调用失败: {e}")
        return None

def crawl_meeting_minutes(url, cookies_str):
    """
    使用 Playwright 模拟浏览器访问腾讯会议页面，获取动态加载的纪要内容，并截图给 LLM 分析。
    Adapted for CentOS 7 & Playwright 1.25.2
    """
    print(f"🚀 启动浏览器爬取: {url}")
    
    # 解析 Cookies 字符串
    cookies = []
    if cookies_str:
        for chunk in cookies_str.split(';'):
            if '=' in chunk:
                name, value = chunk.strip().split('=', 1)
                cookies.append({
                    'name': name,
                    'value': value,
                    'domain': '.tencent.com',
                    'path': '/'
                })

    screenshots = []
    full_transcript = ""

    with sync_playwright() as p:
        # 启动 Chromium 浏览器
        # 适配 CentOS 7: 添加 --no-sandbox 等参数
        print("🚀 正在启动 Playwright 内置浏览器 (CentOS 7 兼容模式)...")
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        if cookies:
            context.add_cookies(cookies)

        page = context.new_page()
        
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000) 
            # print("✅ 页面加载完成")
            time.sleep(5) # 增加等待时间以确保内容渲染 
            
            # ---------------------------------------------------------
            # 1. 点击“纪要”标签
            # ---------------------------------------------------------
            target_tab_names = ["纪要", "智能纪要", "转写"]
            found_tab = False
            
            for target_tab_name in target_tab_names:
                # print(f"\n🔎 正在寻找并点击“{target_tab_name}”标签...")
                # Playwright 1.25.2 兼容: 使用 text= 选择器而非 get_by_text
                loc = page.locator(f"text={target_tab_name}")
                count = loc.count()
                for i in range(count):
                    el = loc.nth(i)
                    if el.is_visible() and "tooltip" not in (el.get_attribute("class") or "").lower():
                        el.click()
                        # print(f"✅ 已点击“{target_tab_name}”")
                        found_tab = True
                        time.sleep(2)
                        break
                if found_tab:
                    break
            
            # ---------------------------------------------------------
            # 2. 顶部截图
            # ---------------------------------------------------------
            # 使用临时文件或固定路径覆盖
            top_screenshot = f"temp_meeting_top_{int(time.time())}.png"
            page.screenshot(path=top_screenshot)
            screenshots.append(top_screenshot)

            # ---------------------------------------------------------
            # 3. 滚动到底部并截图
            # ---------------------------------------------------------
            print("📜 正在执行滚动操作...")

            page.mouse.click(100, 100)

            viewport = page.viewport_size or {"width": 1200, "height": 800}
            page.mouse.move(int(viewport["width"] * 0.5), int(viewport["height"] * 0.85))

            print("  - 执行滚轮滚动 (60次)...")
            last_scroll_y = page.evaluate("window.scrollY")
            stuck_count = 0
            for i in range(60):
                page.mouse.wheel(0, 1200)
                time.sleep(0.2)
                new_scroll_y = page.evaluate("window.scrollY")
                if new_scroll_y == last_scroll_y:
                    stuck_count += 1
                else:
                    stuck_count = 0
                    last_scroll_y = new_scroll_y
                if stuck_count >= 5:
                    break
                if (i + 1) % 10 == 0:
                    print(f"    - 已滚动 {i + 1} 次, scrollY={new_scroll_y}")

            print("  - 执行 End 键滚动 (10次)...")
            for _ in range(10):
                page.keyboard.press("End")
                time.sleep(0.2)
            
            # 再次尝试查找特定容器滚动 (双保险)
            potential_selectors = ["div[class*='minutes-module-list']", "div[class*='smart-summary']", ".meeting-content", ".w-scroll-container"]
            for selector in potential_selectors:
                try:
                    loc = page.locator(selector).first
                    if loc.count() > 0 and loc.is_visible():
                        print(f"  - 发现滚动容器: {selector}，尝试滚动...")
                        box = loc.bounding_box()
                        if box:
                            page.mouse.move(int(box["x"] + box["width"] * 0.5), int(box["y"] + min(box["height"] * 0.5, box["height"] - 10)))
                            time.sleep(0.1)

                        last_scroll_top = loc.evaluate("el => el.scrollTop")
                        stuck_count = 0
                        for i in range(80):
                            page.mouse.wheel(0, 1200)
                            time.sleep(0.15)
                            new_scroll_top = loc.evaluate("el => el.scrollTop")
                            if new_scroll_top == last_scroll_top:
                                stuck_count += 1
                            else:
                                stuck_count = 0
                                last_scroll_top = new_scroll_top
                            if stuck_count >= 5:
                                break
                            if (i + 1) % 10 == 0:
                                print(f"    - 容器已滚动 {i + 1} 次, scrollTop={new_scroll_top}")

                        loc.evaluate("el => el.scrollTop = el.scrollHeight")
                        break
                except:
                    pass
            
            time.sleep(3) # 等待最终内容渲染
            
            bottom_screenshot = f"temp_meeting_bottom_{int(time.time())}.png"
            page.screenshot(path=bottom_screenshot)
            screenshots.append(bottom_screenshot)

            # 尝试获取文本作为辅助
            full_transcript = page.inner_text("body")
            
        except Exception as e:
            print(f"❌ 爬取出错: {e}")
        finally:
            browser.close()

    # ---------------------------------------------------------
    # 4. 调用大模型分析
    # ---------------------------------------------------------
    analysis_result = {
        "summary": "",
        "todos": [],
        "transcript": full_transcript
    }

    if screenshots:
        json_str = analyze_with_llm(full_transcript, screenshots)
        if json_str:
            try:
                parsed_data = json.loads(json_str)
                if isinstance(parsed_data, dict):
                    analysis_result["summary"] = parsed_data.get("summary", "")
                    analysis_result["todos"] = parsed_data.get("todos", [])
                elif isinstance(parsed_data, list):
                    # Fallback if model returns list (old behavior)
                    analysis_result["todos"] = parsed_data
            except json.JSONDecodeError:
                print(f"❌ JSON 解析失败. Raw content:\n{json_str}")
        
        # 清理截图文件
        for img in screenshots:
            try:
                os.remove(img)
            except:
                pass

    return analysis_result



# (Test code removed)
