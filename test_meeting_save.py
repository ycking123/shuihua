import sys
import os
import logging
import json
import re
import requests
from urllib.parse import urljoin
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestSave")

try:
    from backend.url_crawler import crawl_and_parse_meeting, extract_server_data_objects, extract_next_payloads, extract_next_data_json, fetch_content_with_cookies
    from backend.server_receive import save_meeting_data_to_db, get_system_user_id
    from server.database import SessionLocal
    from server.models import Meeting, Todo
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_crawl_and_save():
    url = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"
    print(f"🚀 [1/4] 开始测试爬取: {url}")
    
    # 1. Crawl
    try:
        # Use None for cookies as we implemented direct fetching
        result = crawl_and_parse_meeting(url, None)
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        import traceback
        traceback.print_exc()
        return

    if not result:
        print("❌ 爬取结果为空")
        return

    print("\n✅ [2/4] 爬取成功! 解析结果如下:")
    print("-" * 50)
    print(f"📌 标题: {result.get('title')}")
    summary = result.get('summary', '')
    print(f"📝 摘要 (前100字): {summary[:100]}...")
    print(f"🗣️ 转写 (前100字): {result.get('transcript', '')[:100]}...")
    
    todos = result.get('todos', [])
    print(f"\n📋 会议待办 ({len(todos)}条):")
    for t in todos:
        if isinstance(t, dict):
            print(f"  - [{t.get('assignee')}] {t.get('title')}")
        else:
            print(f"  - {t}")
            
    personal_todos = result.get('personal_todos', [])
    print(f"\n👤 个人待办 ({len(personal_todos)}条):")
    for t in personal_todos:
        print(f"  - [{t.get('assignee')}] {t.get('title')}")

    # 1.5 Output to file
    output_file = "crawl_result.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"=== 爬取结果 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n\n")
        f.write(f"📌 标题: {result.get('title')}\n\n")
        f.write(f"📝 摘要:\n{result.get('summary', '')}\n\n")
        f.write(f"🗣️ 转写:\n{result.get('transcript', '')}\n\n")
        
        f.write(f"📋 会议待办 ({len(todos)}条):\n")
        for t in todos:
            if isinstance(t, dict):
                f.write(f"  - [{t.get('assignee')}] {t.get('title')}\n")
                f.write(f"    详情: {t.get('description')}\n")
                f.write(f"    截止: {t.get('due_date')}\n")
            else:
                f.write(f"  - {t}\n")
        f.write("\n")
                
        f.write(f"👤 个人待办 ({len(personal_todos)}条):\n")
        for t in personal_todos:
            f.write(f"  - [{t.get('assignee')}] {t.get('title')}\n")
            f.write(f"    详情: {t.get('description')}\n")
            f.write(f"    优先级: {t.get('priority')}\n")
        f.write("\n")
        
    print(f"\n📄 爬取内容已输出到文件: {output_file}")
    
    print("-" * 50)
    
    # 2. Save to DB
    print("\n💾 [3/4]正在存入数据库...")
    
    # Mock system user id or use real one
    # Assuming "LanJing" as user for testing, or let system decide
    # We can try to get a system user id first
    user_id = get_system_user_id("LanJing") 
    print(f"   使用用户ID: {user_id}")
    
    try:
        saved_count = save_meeting_data_to_db(result, user_id, meeting_url=url)
        print(f"✅ 存入成功! 返回待办数量: {saved_count}")
    except Exception as e:
        print(f"❌ 存入失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 3. Verify in DB
    print("\n🔍 [4/4] 验证数据库记录...")
    db = SessionLocal()
    try:
        # Check Meeting
        # Order by created_at desc to get the latest
        latest_meeting = db.query(Meeting).filter(Meeting.location == url).order_by(Meeting.created_at.desc()).first()
        
        if latest_meeting:
            print(f"✅ 找到会议记录 (ID: {latest_meeting.id})")
            print(f"   标题: {latest_meeting.title}")
            print(f"   摘要 (summary): \n{latest_meeting.summary}")
            print(f"   转写长度: {len(latest_meeting.transcript) if latest_meeting.transcript else 0}")
        else:
            print("❌ 未找到会议记录!")

        # Check Todos
        # Find todos linked to this meeting
        if latest_meeting:
            meeting_todos = db.query(Todo).filter(Todo.source_message_id == latest_meeting.id).all()
            print(f"\n✅ 找到关联待办 ({len(meeting_todos)}条):")
            for t in meeting_todos:
                print(f"   - [ID: {t.id}] {t.title} (责任人: {t.sender})")
                print(f"     内容: {t.content[:50]}...")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_crawl_and_save()
