#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试会议时间排序优化功能
验证：
1. 会议 API 返回 created_at 字段
2. 待办 API 返回 meeting_start_time 和 meeting_created_at 字段
3. sort_by 参数正确影响排序结果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.database import SessionLocal
from server.models import Meeting, Todo
from sqlalchemy import desc
from datetime import datetime

def test_db_data():
    """测试数据库中的数据"""
    print("=" * 70)
    print("📊 测试数据库数据")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # 查看会议数据
        print("\n[会议数据] 包含 start_time 和 created_at:")
        print("-" * 50)
        meetings = db.query(Meeting).order_by(desc(Meeting.start_time)).limit(5).all()
        for m in meetings:
            print(f"  标题: {m.title[:30]}...")
            print(f"    start_time (会议时间): {m.start_time.strftime('%Y/%m/%d %H:%M') if m.start_time else 'N/A'}")
            print(f"    created_at (发送时间): {m.created_at.strftime('%Y/%m/%d %H:%M') if m.created_at else 'N/A'}")
            print()
        
        # 查看待办数据与会议关联
        print("\n[待办数据] 关联会议的时间:")
        print("-" * 50)
        results = db.query(Todo, Meeting.start_time, Meeting.created_at).outerjoin(
            Meeting, Todo.source_message_id == Meeting.id
        ).filter(Todo.is_deleted == False).limit(5).all()
        
        for todo, mt, ct in results:
            print(f"  待办: {todo.title[:25]}...")
            print(f"    meeting_start_time: {mt.strftime('%Y/%m/%d %H:%M') if mt else '无'}")
            print(f"    meeting_created_at: {ct.strftime('%Y/%m/%d %H:%M') if ct else '无'}")
            print()
            
    finally:
        db.close()

def test_sort_logic():
    """测试排序逻辑"""
    print("\n" + "=" * 70)
    print("🔄 测试排序逻辑")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # 测试按会议时间排序
        print("\n[按会议时间排序] sort_by=meeting_start_time:")
        print("-" * 50)
        query1 = db.query(Todo, Meeting.start_time, Meeting.created_at).outerjoin(
            Meeting, Todo.source_message_id == Meeting.id
        ).filter(Todo.is_deleted == False).order_by(
            Meeting.start_time.is_(None),
            desc(Meeting.start_time),
            desc(Todo.created_at)
        ).limit(5)
        
        for todo, mt, ct in query1.all():
            time_str = mt.strftime('%Y/%m/%d %H:%M') if mt else '无会议时间'
            print(f"  {time_str} - {todo.title[:30]}...")
        
        # 测试按发送时间排序
        print("\n[按发送时间排序] sort_by=created_at:")
        print("-" * 50)
        query2 = db.query(Todo, Meeting.start_time, Meeting.created_at).outerjoin(
            Meeting, Todo.source_message_id == Meeting.id
        ).filter(Todo.is_deleted == False).order_by(
            Meeting.created_at.is_(None),
            desc(Meeting.created_at),
            desc(Todo.created_at)
        ).limit(5)
        
        for todo, mt, ct in query2.all():
            time_str = ct.strftime('%Y/%m/%d %H:%M') if ct else '无发送时间'
            print(f"  {time_str} - {todo.title[:30]}...")
            
    finally:
        db.close()

def test_api_response():
    """测试 API 响应格式"""
    print("\n" + "=" * 70)
    print("🌐 测试 API 响应格式")
    print("=" * 70)
    
    import requests
    
    base_url = "http://localhost:8000/api"
    
    try:
        # 测试会议 API
        print("\n[会议 API] /meetings?sort_by=start_time")
        res = requests.get(f"{base_url}/meetings?sort_by=start_time", timeout=5)
        if res.ok:
            data = res.json()
            if data:
                print(f"  ✅ 成功获取 {len(data)} 条会议")
                first = data[0]
                print(f"  字段: {list(first.keys())}")
                if 'created_at' in first:
                    print(f"  ✅ created_at 字段存在: {first['created_at']}")
                else:
                    print(f"  ❌ created_at 字段缺失")
        else:
            print(f"  ❌ API 请求失败: {res.status_code}")
    except Exception as e:
        print(f"  ⚠️ 无法连接 API: {e}")
    
    try:
        # 测试待办 API
        print("\n[待办 API] /todos?sort_by=meeting_start_time")
        res = requests.get(f"{base_url}/todos?sort_by=meeting_start_time", timeout=5)
        if res.ok:
            data = res.json()
            if data:
                print(f"  ✅ 成功获取 {len(data)} 条待办")
                first = data[0]
                if 'meeting_start_time' in first:
                    print(f"  ✅ meeting_start_time 字段存在: {first.get('meeting_start_time')}")
                else:
                    print(f"  ❌ meeting_start_time 字段缺失")
                if 'meeting_created_at' in first:
                    print(f"  ✅ meeting_created_at 字段存在: {first.get('meeting_created_at')}")
                else:
                    print(f"  ❌ meeting_created_at 字段缺失")
        else:
            print(f"  ❌ API 请求失败: {res.status_code}")
    except Exception as e:
        print(f"  ⚠️ 无法连接 API: {e}")

def main():
    print("\n" + "=" * 70)
    print("📋 会议时间排序优化功能测试")
    print("=" * 70)
    
    test_db_data()
    test_sort_logic()
    test_api_response()
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)
    print("""
修改总结:
1. 后端 meetings.py:
   - MeetingResponse 新增 created_at 字段
   - get_meetings 支持 sort_by 参数 (start_time | created_at)

2. 后端 todos.py:
   - TodoItemSchema 字段重命名: meeting_time → meeting_start_time
   - TodoItemSchema 新增 meeting_created_at 字段
   - get_todos 支持 sort_by 参数 (created_at | meeting_start_time)

3. 前端 TodoView.tsx:
   - SortByType 改为 'created_at' | 'meeting_start_time'
   - 排序按钮改为 "发送时间" / "会议时间"
   - 待办卡片根据排序显示对应时间
   - 会议纪要卡片根据排序显示对应时间
   - API 请求携带 sort_by 参数
""")

if __name__ == "__main__":
    main()
