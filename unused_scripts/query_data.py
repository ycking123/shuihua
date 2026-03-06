"""查询数据库中的会议和待办数据"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.database import SessionLocal
from server.models import Meeting, Todo
from datetime import datetime

db = SessionLocal()

# 查询最近的会议
print('=== 最近会议 ===')
meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).limit(5).all()
for m in meetings:
    print(f'{m.id[:8]}... | {m.title[:40]} | {m.start_time}')

# 查询会议纪要来源的待办
print('\n=== 会议纪要待办 ===')
todos = db.query(Todo).filter(Todo.source_origin == 'meeting_minutes').order_by(Todo.created_at.desc()).limit(5).all()
for t in todos:
    print(f'{t.id[:8]}... | {t.title[:40]} | {t.created_at}')

# 统计总数
print(f'\n会议总数: {db.query(Meeting).count()}')
print(f'待办总数: {db.query(Todo).count()}')

db.close()
