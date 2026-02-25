"""
测试会议纪要功能 - 纯 API 爬取模式
1. 使用 API 爬取会议内容（不用浏览器）
2. 保存到数据库
3. 验证前端可展示
"""
import sys
import os
import uuid
import re
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "backend", ".env"))

from server.database import SessionLocal
from server.models import Meeting, Todo, User

# 测试会议链接
TEST_MEETING_URL = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"

def clean_text(text):
    """清洗文本"""
    if not text:
        return ""
    text = text.replace("<p>", "").replace("</p>", "\n")
    text = text.replace("<ul>", "").replace("</ul>", "")
    text = text.replace("<li>", " • ").replace("</li>", "\n")
    return re.sub('<.*?>', '', text).strip()

def generate_smart_title(title, summary):
    """智能标题生成"""
    default_patterns = ["的快速会议", "的会议", "快速会议"]
    
    for pattern in default_patterns:
        if pattern in title and len(title) < 30:
            if summary:
                sentences = re.split(r'[。！？\n]', summary)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) >= 5 and not sentence.startswith('【'):
                        return sentence[:50]
    return title

def test_api_crawler_and_save():
    """测试 API 爬取并保存到数据库"""
    print("=" * 60)
    print("测试会议纪要功能 - 纯 API 爬取模式")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试链接: {TEST_MEETING_URL}")
    print("-" * 60)
    
    # 1. 使用 API 爬取
    print("\n[步骤 1] 使用 API 爬取会议内容...")
    try:
        from backend.url_crawler import crawl_meeting_api
        
        # 纯 API 模式，不传 cookie
        result = crawl_meeting_api(TEST_MEETING_URL, None)
        
        if not result:
            print("  ❌ API 爬取返回空结果")
            return None
            
        print(f"  ✅ 爬取成功!")
        print(f"     标题: {result.get('title', 'N/A')[:50]}")
        print(f"     摘要长度: {len(result.get('summary', ''))} 字符")
        print(f"     转写长度: {len(result.get('transcript', ''))} 字符")
        print(f"     待办数量: {len(result.get('todos', []))} 条")
        
    except Exception as e:
        print(f"  ❌ API 爬取失败: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    # 2. 保存到数据库
    print("\n[步骤 2] 保存到数据库...")
    db = SessionLocal()
    
    try:
        # 获取或创建测试用户
        test_user = db.query(User).first()
        if not test_user:
            print("  创建测试用户...")
            test_user = User(
                id=str(uuid.uuid4()),
                username="test_user",
                email="test@example.com",
                password_hash="test_hash",
                is_active=True,
                created_at=datetime.now()
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
        print(f"  用户: {test_user.username} ({test_user.id})")
        
        # 智能标题生成
        original_title = result.get("title", "会议纪要")
        summary = result.get("summary", "")
        smart_title = generate_smart_title(original_title, summary)
        print(f"  原标题: {original_title}")
        print(f"  智能标题: {smart_title}")
        
        # 保存会议记录
        meeting = Meeting(
            id=str(uuid.uuid4()),
            organizer_id=test_user.id,
            title=clean_text(smart_title),
            start_time=datetime.now(),
            end_time=datetime.now(),
            location=TEST_MEETING_URL,
            summary=clean_text(result.get("summary", "")),
            transcript=clean_text(result.get("transcript", "")),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        print(f"  ✅ 会议已保存: {meeting.id}")
        
        # 保存待办事项
        todos = result.get("todos", [])
        todo_count = 0
        priority_map = {"高": "urgent", "中": "high", "低": "normal"}
        
        for t in todos:
            if isinstance(t, str):
                title = t
                content = ""
                assignee = "待定"
            else:
                title = t.get("title", "待办事项")
                content = t.get("description", "")
                assignee = t.get("assignee", "待定")
            
            raw_priority = t.get("priority", "中") if isinstance(t, dict) else "中"
            priority = priority_map.get(str(raw_priority).lower(), "normal")
            
            todo = Todo(
                id=str(uuid.uuid4()),
                user_id=test_user.id,
                title=clean_text(f"[{assignee}] {title}"),
                content=clean_text(content),
                type="meeting",
                priority=priority,
                status="pending",
                sender="会议助手",
                source_origin="meeting_minutes",
                source_message_id=meeting.id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            db.add(todo)
            todo_count += 1
        
        db.commit()
        print(f"  ✅ 已保存 {todo_count} 条待办")
        
        # 3. 验证数据
        print("\n[步骤 3] 验证数据...")
        
        # 查询会议
        meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).limit(3).all()
        print(f"\n  最近会议记录 ({len(meetings)} 条):")
        for m in meetings:
            print(f"    - [{m.start_time.strftime('%Y-%m-%d %H:%M')}] {m.title[:40]}...")
        
        # 查询待办
        db_todos = db.query(Todo).filter(
            Todo.source_message_id == meeting.id,
            Todo.is_deleted == False
        ).all()
        print(f"\n  关联待办 ({len(db_todos)} 条):")
        for t in db_todos:
            print(f"    - [{t.priority}] {t.title[:40]}...")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成!")
        print("=" * 60)
        print(f"\n会议ID: {meeting.id}")
        print("请在前端待办事项页面查看 '会议纪要' 分类")
        
        return meeting.id
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    test_api_crawler_and_save()
