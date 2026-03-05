"""创建测试会议数据 - 验证按会议时间排序"""
import sys
import os
import uuid
import re
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.database import SessionLocal
from server.models import Meeting, Todo, User

def create_test_meetings():
    print("=" * 60)
    print("创建测试会议数据 - 验证按会议时间排序")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # 获取用户
        user = db.query(User).first()
        if not user:
            print("❌ 没有用户")
            return
        
        # 创建两个不同时间的会议
        now = datetime.now()
        
        # 会议1: 较早的会议 (昨天)
        meeting1_time = now - timedelta(days=1, hours=2)
        meeting1 = Meeting(
            id=str(uuid.uuid4()),
            organizer_id=user.id,
            title="【测试会议A】产品需求评审会",
            start_time=meeting1_time,
            end_time=meeting1_time + timedelta(hours=1),
            location="https://meeting.tencent.com/test-meeting-a",
            summary="这是昨天的产品需求评审会议，主要讨论了新版本的功能规划。",
            transcript="【产品经理】: 我们需要讨论下个版本的功能优先级...\n【技术负责人】: 建议先完成核心功能...",
            created_at=now,  # 创建时间是现在
            updated_at=now
        )
        db.add(meeting1)
        
        # 会议2: 较晚的会议 (今天上午)
        meeting2_time = now - timedelta(hours=3)
        meeting2 = Meeting(
            id=str(uuid.uuid4()),
            organizer_id=user.id,
            title="【测试会议B】技术方案讨论会",
            start_time=meeting2_time,
            end_time=meeting2_time + timedelta(hours=1),
            location="https://meeting.tencent.com/test-meeting-b",
            summary="这是今天上午的技术方案讨论会，确定了架构选型。",
            transcript="【架构师】: 我建议使用微服务架构...\n【开发组长】: 同意，需要注意性能问题...",
            created_at=now,  # 创建时间是现在
            updated_at=now
        )
        db.add(meeting2)
        
        db.commit()
        db.refresh(meeting1)
        db.refresh(meeting2)
        
        print(f"\n✅ 创建会议1: {meeting1.title}")
        print(f"   会议时间: {meeting1.start_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   创建时间: {meeting1.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n✅ 创建会议2: {meeting2.title}")
        print(f"   会议时间: {meeting2.start_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   创建时间: {meeting2.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 为每个会议创建待办
        # 会议1的待办
        todo1 = Todo(
            id=str(uuid.uuid4()),
            user_id=user.id,
            title="[产品经理] 整理需求文档",
            content="根据评审结果整理详细需求文档",
            type="meeting",
            priority="high",
            status="pending",
            sender="会议助手",
            source_origin="meeting_minutes",
            source_message_id=meeting1.id,
            created_at=now,
            updated_at=now
        )
        db.add(todo1)
        
        # 会议2的待办
        todo2 = Todo(
            id=str(uuid.uuid4()),
            user_id=user.id,
            title="[架构师] 输出架构设计文档",
            content="完成微服务架构设计文档",
            type="meeting",
            priority="urgent",
            status="pending",
            sender="会议助手",
            source_origin="meeting_minutes",
            source_message_id=meeting2.id,
            created_at=now,
            updated_at=now
        )
        db.add(todo2)
        
        db.commit()
        
        print(f"\n✅ 创建待办1: {todo1.title}")
        print(f"   关联会议: {meeting1.title}")
        
        print(f"\n✅ 创建待办2: {todo2.title}")
        print(f"   关联会议: {meeting2.title}")
        
        # 验证排序
        print("\n" + "=" * 60)
        print("验证排序结果")
        print("=" * 60)
        
        from sqlalchemy import desc
        from server.models import Meeting as M
        
        # 按生成时间排序
        print("\n[按生成时间排序] (应该相同顺序，因为创建时间相同)")
        todos_by_created = db.query(Todo).filter(
            Todo.source_message_id.in_([meeting1.id, meeting2.id]),
            Todo.is_deleted == False
        ).order_by(desc(Todo.created_at)).all()
        
        for t in todos_by_created:
            meeting = db.query(M).filter(M.id == t.source_message_id).first()
            print(f"  - {t.title}")
            print(f"    会议时间: {meeting.start_time.strftime('%Y-%m-%d %H:%M')}")
        
        # 按会议时间排序
        print("\n[按会议时间排序] (会议B应该在前面，因为会议时间更晚)")
        todos_by_meeting = db.query(Todo, M.start_time).outerjoin(
            M, Todo.source_message_id == M.id
        ).filter(
            Todo.source_message_id.in_([meeting1.id, meeting2.id]),
            Todo.is_deleted == False
        ).order_by(
            M.start_time.is_(None),
            desc(M.start_time)
        ).all()
        
        for t, mt in todos_by_meeting:
            print(f"  - {t.title}")
            print(f"    会议时间: {mt.strftime('%Y-%m-%d %H:%M') if mt else '无'}")
        
        print("\n" + "=" * 60)
        print("✅ 测试数据创建完成!")
        print("=" * 60)
        print("\n请在前端刷新页面，切换排序方式验证:")
        print("1. 按'生成时间'排序 - 两条待办顺序应该相同")
        print("2. 按'会议时间'排序 - 会议B的待办应该排在前面")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_meetings()
