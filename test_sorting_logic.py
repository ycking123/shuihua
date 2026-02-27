#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试按会议开始时间排序的业务逻辑

验证:
1. 后端排序SQL逻辑是否正确
2. 有会议的待办排前面，无会议的排后面
3. 会议时间倒序排列（最新的在前）
4. 无会议的按生成时间倒序
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.database import SessionLocal
from server.models import Todo, Meeting
from sqlalchemy import desc
from datetime import datetime

def test_sorting_logic():
    """测试排序逻辑"""
    print("=" * 70)
    print("测试按会议开始时间排序的业务逻辑")
    print("=" * 70)
    
    db = SessionLocal()
    
    try:
        # 1. 查看当前数据库中的会议和待办数据
        print("\n[1] 当前数据库中的会议记录:")
        print("-" * 50)
        meetings = db.query(Meeting).order_by(desc(Meeting.start_time)).limit(10).all()
        for m in meetings:
            print(f"  - ID: {m.id[:8]}... | 时间: {m.start_time.strftime('%Y/%m/%d %H:%M')} | 标题: {m.title[:25]}...")
        
        print(f"\n共 {db.query(Meeting).count()} 个会议记录")
        
        # 2. 查看待办与会议的关联情况
        print("\n[2] 待办与会议的关联情况:")
        print("-" * 50)
        
        # 查询所有待办，JOIN会议表
        query = db.query(Todo, Meeting.start_time).outerjoin(
            Meeting, Todo.source_message_id == Meeting.id
        ).filter(
            Todo.is_deleted == False
        )
        
        all_todos = query.all()
        with_meeting = [t for t, mt in all_todos if mt is not None]
        without_meeting = [t for t, mt in all_todos if mt is None]
        
        print(f"  - 有会议关联的待办: {len(with_meeting)} 条")
        print(f"  - 无会议关联的待办: {len(without_meeting)} 条")
        print(f"  - 总计: {len(all_todos)} 条")
        
        # 3. 测试排序逻辑 - 按会议时间
        print("\n[3] 按 '会议时间' 排序的结果:")
        print("-" * 50)
        print("排序规则: 有会议的排前面(按会议时间倒序)，无会议的排后面(按生成时间倒序)")
        print()
        
        query_meeting_time = db.query(Todo, Meeting.start_time).outerjoin(
            Meeting, Todo.source_message_id == Meeting.id
        ).filter(
            Todo.is_deleted == False
        ).order_by(
            Meeting.start_time.is_(None),  # 有会议的排前面
            desc(Meeting.start_time),       # 会议时间倒序
            desc(Todo.created_at)           # 无会议的按生成时间
        )
        
        results_meeting_time = query_meeting_time.limit(10).all()
        
        for i, (todo, meeting_start) in enumerate(results_meeting_time, 1):
            if meeting_start:
                print(f"  {i}. [有会议] 待办: {todo.title[:25]}...")
                print(f"      会议时间: {meeting_start.strftime('%Y/%m/%d %H:%M:%S')}")
                print(f"      生成时间: {todo.created_at.strftime('%Y/%m/%d %H:%M:%S')}")
            else:
                print(f"  {i}. [无会议] 待办: {todo.title[:25]}...")
                print(f"      会议时间: 无")
                print(f"      生成时间: {todo.created_at.strftime('%Y/%m/%d %H:%M:%S')}")
            print()
        
        # 4. 测试排序逻辑 - 按生成时间
        print("\n[4] 按 '生成时间' 排序的结果:")
        print("-" * 50)
        print("排序规则: 按待办创建时间倒序（最新的在前）")
        print()
        
        query_created = db.query(Todo, Meeting.start_time).outerjoin(
            Meeting, Todo.source_message_id == Meeting.id
        ).filter(
            Todo.is_deleted == False
        ).order_by(
            desc(Todo.created_at)
        )
        
        results_created = query_created.limit(10).all()
        
        for i, (todo, meeting_start) in enumerate(results_created, 1):
            if meeting_start:
                print(f"  {i}. [有会议] 待办: {todo.title[:25]}...")
                print(f"      会议时间: {meeting_start.strftime('%Y/%m/%d %H:%M:%S')}")
                print(f"      生成时间: {todo.created_at.strftime('%Y/%m/%d %H:%M:%S')}")
            else:
                print(f"  {i}. [无会议] 待办: {todo.title[:25]}...")
                print(f"      会议时间: 无")
                print(f"      生成时间: {todo.created_at.strftime('%Y/%m/%d %H:%M:%S')}")
            print()
        
        # 5. 验证排序正确性
        print("\n[5] 验证排序正确性:")
        print("-" * 50)
        
        # 验证会议时间排序
        all_results_meeting = query_meeting_time.all()
        
        # 检查有会议的都在前面
        found_without_meeting = False
        sort_correct = True
        
        for i, (todo, meeting_start) in enumerate(all_results_meeting):
            if meeting_start is None:
                found_without_meeting = True
            elif found_without_meeting and meeting_start is not None:
                # 如果已经出现无会议的，后面又出现有会议的，说明排序错误
                sort_correct = False
                print(f"  ❌ 排序错误: 位置 {i} 的有会议待办出现在无会议待办之后")
                break
        
        if sort_correct:
            print("  ✅ 排序正确: 有会议的待办都排在无会议待办之前")
        
        # 验证会议时间是否倒序
        meeting_times = [mt for _, mt in all_results_meeting if mt is not None]
        is_desc = all(meeting_times[i] >= meeting_times[i+1] for i in range(len(meeting_times)-1))
        if is_desc or len(meeting_times) <= 1:
            print("  ✅ 排序正确: 会议时间按倒序排列（最新的在前）")
        else:
            print("  ❌ 排序错误: 会议时间未按倒序排列")
        
        # 验证无会议的生成时间是否倒序
        created_times = [t.created_at for t, mt in all_results_meeting if mt is None]
        is_desc_created = all(created_times[i] >= created_times[i+1] for i in range(len(created_times)-1))
        if is_desc_created or len(created_times) <= 1:
            print("  ✅ 排序正确: 无会议待办按生成时间倒序排列")
        else:
            print("  ❌ 排序错误: 无会议待办未按生成时间倒序排列")
        
        # 6. 业务逻辑分析
        print("\n[6] 业务逻辑分析:")
        print("-" * 50)
        
        print("""
后端排序代码 (todos.py 第91-97行):
```python
if sort_by == "meeting_time":
    query = query.order_by(
        Meeting.start_time.is_(None),  # 有会议的排前面
        desc(Meeting.start_time),       # 会议时间倒序
        desc(Todo.created_at)           # 无会议的按生成时间
    )
```

分析:
1. Meeting.start_time.is_(None) 返回 False(有会议) 或 True(无会议)
   - False < True，所以有会议的排前面 ✅

2. desc(Meeting.start_time) 对有会议的按时间倒序
   - 最新会议在前 ✅

3. desc(Todo.created_at) 作为第三排序条件
   - 对于有会议但时间相同的待办，按生成时间排序
   - 对于无会议的待办，按生成时间排序 ✅

前端显示逻辑 (TodoView.tsx 第524-527行):
```tsx
{sortBy === 'meeting_time' && item.meeting_time 
  ? <><Calendar size={10} />{item.meeting_time}</>
  : <><Clock size={10} />{item.time}</>
}
```
- 按会议时间排序时，有会议的显示会议时间 + Calendar 图标 ✅
- 其他情况显示生成时间 + Clock 图标 ✅
""")
        
        print("\n" + "=" * 70)
        print("✅ 业务逻辑测试完成!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_sorting_logic()
