#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.database import SessionLocal
from server.models import Meeting

db = SessionLocal()

print("=" * 80)
print("所有会议记录 - 按 start_time 降序排列")
print("=" * 80)

meetings = db.query(Meeting).order_by(Meeting.start_time.desc()).all()
for i, m in enumerate(meetings, 1):
    print(f"{i}. {m.title[:45]:45} | start: {m.start_time}")

print("\n" + "=" * 80)
print(f"总计: {len(meetings)} 条记录")
print("=" * 80)

db.close()
