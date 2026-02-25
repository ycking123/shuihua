"""
测试会议纪要功能 - 完整流程
1. 爬取会议内容
2. 保存到数据库
3. 验证数据
"""
import sys
import os
import re
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "backend", ".env"))

from server.database import SessionLocal
from server.models import Meeting, Todo, User
from backend.url_crawler import crawl_and_parse_meeting
from backend.server_receive import save_meeting_data_to_db

DEFAULT_MEETING_URL = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"

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

def test_meeting_flow():
    """测试完整会议流程"""
    print("=" * 60)
    print("测试会议纪要功能 - 完整流程")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    meeting_url = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"
    cookies = os.getenv("WECOM_MEETING_COOKIES") or None

    db = SessionLocal()
    
    try:
        # 1. 查找 yc 用户（必须已存在）
        print("\n[步骤 1] 查找 yc 用户...")
        test_user = db.query(User).filter(User.username == "yc").first()
        if not test_user:
            print("  [ERROR] 错误: 数据库中不存在用户名为 'yc' 的用户！")
            print("  请先确保用户表中已有 yc 用户。")
            return None
        print(f"  [OK] 找到用户: {test_user.username} ({test_user.id})")
        
        # 2. 爬取会议内容
        print("\n[步骤 2] 爬取会议内容...")
        print(f"  [URL] 会议链接: {meeting_url}")
        print(f"  [Cookie] Cookie: {'已配置' if cookies else '未配置'}")

        # 直接调用 API 爬虫，不回退到浏览器爬虫
        from backend.url_crawler import crawl_meeting_api
        
        crawl_result = None
        
        # 1. 尝试带 Cookie (如果配置了)
        if cookies:
            print("  [API] 尝试带 Cookie 爬取...")
            try:
                crawl_result = crawl_meeting_api(meeting_url, cookies)
                if crawl_result:
                    print("  [OK] 带 Cookie 爬取成功")
            except Exception as e:
                print(f"  [WARN] 带 Cookie 爬取失败: {e}")
        
        # 2. 如果失败，尝试无 Cookie (公开模式)
        if not crawl_result:
            print("  [API] 尝试无 Cookie 爬取 (公开模式)...")
            try:
                crawl_result = crawl_meeting_api(meeting_url, None)
                if crawl_result:
                    print("  [OK] 无 Cookie 爬取成功")
            except Exception as e:
                print(f"  [ERROR] 无 Cookie 爬取失败: {e}")
        
        if not crawl_result:
            print("  [ERROR] 爬取失败：API 未返回结果")
            return None
        print(f"  [OK] 爬取成功: title={crawl_result.get('title', '')[:50]}")
        print(f"  [OK] 摘要长度: {len(crawl_result.get('summary') or '')}")
        print(f"  [OK] 转写长度: {len(crawl_result.get('transcript') or '')}")
        print(f"  [OK] 待办数量: {len(crawl_result.get('todos') or [])}")
        
        # 3. 保存会议记录与待办
        print("\n[步骤 3] 保存会议记录与待办...")
        saved_count = save_meeting_data_to_db(crawl_result, test_user.id, meeting_url=meeting_url)
        print(f"  [OK] 已保存待办: {saved_count} 条")
        
        # 4. 验证数据
        print("\n[步骤 4] 验证数据...")
        meeting = db.query(Meeting).filter(
            Meeting.organizer_id == test_user.id,
            Meeting.location == meeting_url
        ).order_by(Meeting.created_at.desc()).first()
        if not meeting:
            print("  [ERROR] 未找到刚保存的会议记录")
            return None
        print(f"  [OK] 会议ID: {meeting.id}")
        print(f"  [OK] 标题: {meeting.title[:60]}")
        
        # 查询会议
        meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).limit(5).all()
        print(f"\n  最近会议记录 ({len(meetings)} 条):")
        for m in meetings:
            print(f"    - [{m.start_time.strftime('%Y-%m-%d %H:%M')}] {m.title[:40]}...")
        
        # 查询待办
        todos = db.query(Todo).filter(
            Todo.source_message_id == meeting.id,
            Todo.is_deleted == False
        ).all()
        print(f"\n  关联待办 ({len(todos)} 条):")
        for t in todos:
            print(f"    - [{t.priority}] {t.title[:40]}...")
        
        print("\n" + "=" * 60)
        print("测试完成!")
        print("=" * 60)
        print(f"\n会议ID: {meeting.id}")
        print("请在前端待办事项页面查看 '会议纪要' 分类")
        
        return meeting.id
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    test_meeting_flow()
