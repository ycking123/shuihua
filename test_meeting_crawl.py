import sys
import os
import json
import logging
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

try:
    from backend.url_crawler import crawl_and_parse_meeting
    # 尝试导入 save_meeting_data_to_db，但如果不方便连接数据库，我们主要测试解析逻辑
    # from backend.server_receive import save_meeting_data_to_db 
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestCrawler")

def test_crawl():
    url = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"
    print(f"🚀 开始测试爬取: {url}")
    
    # 1. Test Crawl & Parse
    try:
        # 传入 None 作为 cookies，因为新逻辑不需要
        result = crawl_and_parse_meeting(url, None)
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        import traceback
        traceback.print_exc()
        return

    if not result:
        print("❌ 爬取结果为空")
        return

    print("\n✅ 爬取成功! 解析结果如下:")
    print("-" * 50)
    print(f"📌 标题: {result.get('title')}")
    print(f"📝 摘要 (前100字): {result.get('summary', '')[:100]}...")
    print(f"🗣️ 转写 (前100字): {result.get('transcript', '')[:100]}...")
    
    print("\n📋 会议待办 (Meeting Todos) - 将合并入会议纪要:")
    todos = result.get('todos', [])
    if todos:
        for idx, t in enumerate(todos):
            if isinstance(t, dict):
                print(f"  {idx+1}. [{t.get('assignee', '待定')}] {t.get('title')} (Due: {t.get('due_date')})")
            else:
                print(f"  {idx+1}. {t}")
    else:
        print("  (无 - 可能由 AI 从转写中提取)")

    print("\n👤 个人待办 (Personal Todos) - 将存入待办表:")
    personal_todos = result.get('personal_todos', [])
    if personal_todos:
        for idx, t in enumerate(personal_todos):
            print(f"  {idx+1}. [{t.get('assignee')}] {t.get('title')}")
            print(f"     详情: {t.get('description')[:50]}...")
    else:
        print("  (无)")
    
    print("-" * 50)
    
    # 2. Simulate DB Save Logic
    print("\n💾 模拟入库数据结构预览:")
    
    # Simulate Logic from server_receive.py
    meeting_summary = result.get("summary", "")
    extracted_todos = result.get("todos", [])
    
    # Format Meeting Summary
    todo_lines = []
    for idx, t in enumerate(extracted_todos or []):
        if isinstance(t, str):
            title = t
            item_desc = t
            assignee = "待定"
            due_date = "未指定"
        else:
            item_desc = t.get("description", "")
            assignee = t.get("assignee", "待定")
            due_date = t.get("due_date", "未指定")
            title = t.get("title", "未命名任务")
        todo_lines.append(f"{idx + 1}. {title}\n   - 详情: {item_desc}\n   - 责任人: {assignee}\n   - 截止: {due_date}")

    combined_summary = meeting_summary
    if todo_lines:
        if combined_summary:
            combined_summary = f"{combined_summary}\n\n【会议待办】\n" + "\n".join(todo_lines)
        else:
            combined_summary = "【会议待办】\n" + "\n".join(todo_lines)
            
    print(f"\n[Table: Meetings] summary 字段内容预览 (合并了纪要和待办):\n{combined_summary[:500]}..." if len(combined_summary) > 500 else f"\n[Table: Meetings] summary 字段内容预览:\n{combined_summary}")
    
    print(f"\n[Table: Meetings] transcript 字段内容预览 (转写):\n{result.get('transcript', '')[:200]}...")
    
    print(f"\n[Table: Todos] 预计插入 {len(personal_todos)} 条个人待办记录")

if __name__ == "__main__":
    test_crawl()
