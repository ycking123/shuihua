#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.database import SessionLocal
from server.models import Meeting

db = SessionLocal()
meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).limit(5).all()
print("Recently created meetings:")
print("-" * 80)
for m in meetings:
    print(f"ID: {m.id[:20]}...")
    print(f"Title: {m.title[:50]}")
    print(f"start_time: {m.start_time}")
    print(f"created_at: {m.created_at}")
    print("-" * 80)

print("\n\nSorted by start_time DESC:")
print("-" * 80)
meetings_by_time = db.query(Meeting).order_by(Meeting.start_time.desc()).limit(5).all()
for m in meetings_by_time:
    print(f"Title: {m.title[:40]}")
    print(f"start_time: {m.start_time}")
    print("-" * 80)
db.close()
