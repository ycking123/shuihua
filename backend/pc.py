import time
from playwright.sync_api import sync_playwright

def scrape_tencent_meeting(url):
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()

        print(f"正在打开网页: {url}")
        page.goto(url)

        # ------------------------------------------------------------------
        # 等待登录
        # ------------------------------------------------------------------
        input(">>> 请在弹出的浏览器中手动登录。\n>>> 登录成功并看到会议内容后，请在此处按【回车键】继续...")

        # ==================== 1. 获取【纪要】 ====================
        print("正在获取【纪要】数据...")
        try:
            # 【修复点 1】：使用更精准的选择器
            # 只查找包含“纪要”文字的 <a> 标签 (链接/按钮)，过滤掉 Tooltip 和 Span
            summary_tab = page.locator("a").filter(has_text="纪要")
            
            # 如果页面上还是有多个 <a> 包含纪要（极少见），强制点第一个可见的
            if summary_tab.count() > 1:
                summary_tab = summary_tab.first
            
            # 只有当它显示在页面上时才点击
            if summary_tab.is_visible():
                summary_tab.click()
                print("点击成功，等待内容加载...")
                time.sleep(3) # 给一点时间渲染
                
                # 尝试抓取正文
                # 这里使用 body.inner_text 获取全文，你也可以按 F12 找具体的 class 替换 "body"
                summary_content = page.locator("body").inner_text()
                
                with open("会议纪要.txt", "w", encoding="utf-8") as f:
                    f.write(summary_content)
                print(f"✅ 会议纪要已保存，长度: {len(summary_content)} 字符")
            else:
                print("⚠️ 未找到可见的【纪要】按钮。")
        except Exception as e:
            print(f"❌ 获取纪要失败: {e}")

        # ==================== 2. 获取【转写】 ====================
        print("正在切换至【转写】...")
        try:
            # 【修复点 2】：同样的逻辑修复转写按钮
            transcript_tab = page.locator("a").filter(has_text="转写")
            
            if transcript_tab.count() > 1:
                transcript_tab = transcript_tab.first

            if transcript_tab.is_visible():
                transcript_tab.click()
                print("点击成功，等待转写内容加载...")
                time.sleep(3) 
                
                # 模拟滚动加载（防止内容太长没加载完）
                for i in range(3): 
                    page.mouse.wheel(0, 10000)
                    time.sleep(1)
                
                transcript_content = page.locator("body").inner_text()
                
                with open("会议转写.txt", "w", encoding="utf-8") as f:
                    f.write(transcript_content)
                print(f"✅ 会议转写已保存，长度: {len(transcript_content)} 字符")
            else:
                print("⚠️ 未找到可见的【转写】按钮。")
        except Exception as e:
            print(f"❌ 获取转写失败: {e}")

        print("任务完成，关闭浏览器。")
        browser.close()

if __name__ == "__main__":
    target_url = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"
    scrape_tencent_meeting(target_url)