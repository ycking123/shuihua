import os
import time
import json
from playwright.sync_api import sync_playwright
from backend.ai_handler import extract_todos_from_text

def crawl_meeting_minutes(url, cookies_str=None):
    """
    使用 Playwright 模拟浏览器访问腾讯会议页面，需要用户手动登录。
    获取纪要和转写内容，并调用 LLM 分析。
    """
    print(f"🚀 启动浏览器爬取 (交互模式): {url}")
    
    summary_content = ""
    transcript_content = ""
    
    with sync_playwright() as p:
        # 启动 Chromium 浏览器，headless=False 以便用户可见并登录
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # 如果有 cookies，也可以设置，但主要依赖手动登录
        if cookies_str:
             cookies = []
             for chunk in cookies_str.split(';'):
                if '=' in chunk:
                    name, value = chunk.strip().split('=', 1)
                    cookies.append({
                        'name': name,
                        'value': value,
                        'domain': '.tencent.com',
                        'path': '/'
                    })
             context.add_cookies(cookies)

        page = context.new_page()
        
        try:
            print(f"正在打开网页: {url}")
            page.goto(url)

            # ------------------------------------------------------------------
            # 等待登录
            # ------------------------------------------------------------------
            print("\n" + "="*60)
            print(">>> 请在弹出的浏览器中手动登录。")
            print(">>> 登录成功并看到会议内容后，请在此处按【回车键】继续...")
            print("="*60 + "\n")
            input() # 等待用户按回车

            # ==================== 1. 获取【纪要】 ====================
            print("正在获取【纪要】数据...")
            try:
                # 只查找包含“纪要”文字的 <a> 标签
                summary_tab = page.locator("a").filter(has_text="纪要")
                
                if summary_tab.count() > 1:
                    summary_tab = summary_tab.first
                
                if summary_tab.is_visible():
                    summary_tab.click()
                    print("点击成功，等待内容加载...")
                    time.sleep(3) 
                    
                    summary_content = page.locator("body").inner_text()
                    print(f"✅ 获取纪要成功，长度: {len(summary_content)} 字符")
                else:
                    print("⚠️ 未找到可见的【纪要】按钮。")
            except Exception as e:
                print(f"❌ 获取纪要失败: {e}")

            # ==================== 2. 获取【转写】 ====================
            print("正在切换至【转写】...")
            try:
                transcript_tab = page.locator("a").filter(has_text="转写")
                
                if transcript_tab.count() > 1:
                    transcript_tab = transcript_tab.first

                if transcript_tab.is_visible():
                    transcript_tab.click()
                    print("点击成功，等待转写内容加载...")
                    time.sleep(3) 
                    
                    # 模拟滚动加载
                    for i in range(3): 
                        page.mouse.wheel(0, 10000)
                        time.sleep(1)
                    
                    transcript_content = page.locator("body").inner_text()
                    print(f"✅ 获取转写成功，长度: {len(transcript_content)} 字符")
                else:
                    print("⚠️ 未找到可见的【转写】按钮。")
            except Exception as e:
                print(f"❌ 获取转写失败: {e}")

        except Exception as e:
            print(f"❌ 爬取出错: {e}")
        finally:
            print("关闭浏览器...")
            browser.close()

    # ---------------------------------------------------------
    # 3. 调用大模型分析
    # ---------------------------------------------------------
    analysis_result = {
        "title": "会议纪要", # 暂时写死，或者从 content 解析
        "summary": "",
        "todos": [],
        "transcript": transcript_content,
        "personal_todos": [] # 兼容旧结构
    }
    
    # 优先使用转写内容进行分析，如果没有则使用纪要内容
    content_to_analyze = transcript_content if transcript_content else summary_content
    
    if content_to_analyze:
        print("\n🧠 正在调用 AI 分析会议内容...")
        # 如果有纪要内容，直接作为 summary
        # 但我们还是让 LLM 生成结构化的 todos
        
        # 尝试从内容中提取标题 (简单的第一行)
        lines = content_to_analyze.split('\n')
        if lines:
            analysis_result["title"] = lines[0][:50]

        ai_data = extract_todos_from_text(content_to_analyze)
        
        if ai_data:
            analysis_result["summary"] = ai_data.get("summary", summary_content[:500])
            analysis_result["todos"] = ai_data.get("task_list", [])
            print(f"✅ AI 分析完成: 提取到 {len(analysis_result['todos'])} 条待办")
        else:
            print("⚠️ AI 分析未返回有效结果")
            analysis_result["summary"] = summary_content
    else:
        print("❌ 未获取到任何会议内容，跳过 AI 分析")

    return analysis_result
