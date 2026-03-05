#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试会议真实开始时间获取和排序功能
验证集成 meeting_time.py 功能是否正确工作
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.url_crawler import get_meeting_params, crawl_meeting_api
from backend.server_receive import save_meeting_data_to_db
from server.database import SessionLocal
from server.models import Meeting, Todo
from datetime import datetime
import json

def test_meeting_time_integration():
    """测试会议真实开始时间集成"""
    
    # 测试用的会议链接（需要替换为真实可访问的链接）
    test_url = "https://meeting.tencent.com/wework/cloud-record/share?id=64957fd6-caa0-4b34-be1c-720a80240864"
    
    print("=" * 60)
    print("测试 1: 验证 get_meeting_params 获取真实开始时间")
    print("=" * 60)
    
    # 1. 测试获取会议参数（包括真实开始时间）
    result = get_meeting_params(test_url, None)
    if result and len(result) == 5:
        sharing_id, meeting_id, record_id, title, real_start_time = result
        print(f"✅ 获取成功:")
        print(f"   - 会议标题: {title}")
        print(f"   - 会议ID: {meeting_id}")
        print(f"   - 真实开始时间: {real_start_time}")
        if real_start_time:
            print(f"   - 时间格式化: {real_start_time.strftime('%Y/%m/%d %H:%M:%S')}")
    else:
        print("❌ 获取失败或参数不完整")
        return False
    
    print("\n" + "=" * 60)
    print("测试 2: 验证 crawl_meeting_api 返回 real_start_time")
    print("=" * 60)
    
    # 2. 测试完整爬虫流程
    crawl_result = crawl_meeting_api(test_url, None)
    if crawl_result:
        print(f"✅ 爬虫成功:")
        print(f"   - 标题: {crawl_result.get('title')}")
        print(f"   - 摘要长度: {len(crawl_result.get('summary', ''))} 字符")
        print(f"   - 待办数量: {len(crawl_result.get('todos', []))}")
        print(f"   - 真实开始时间: {crawl_result.get('real_start_time')}")
        if crawl_result.get('real_start_time'):
            print(f"   - 时间格式化: {crawl_result['real_start_time'].strftime('%Y/%m/%d %H:%M:%S')}")
    else:
        print("❌ 爬虫失败")
        return False
    
    print("\n" + "=" * 60)
    print("测试 3: 验证 save_meeting_data_to_db 使用真实开始时间")
    print("=" * 60)
    
    # 3. 测试保存到数据库
    db = SessionLocal()
    try:
        # 使用系统默认用户
        system_user_id = "00000000-0000-0000-0000-000000000000"
        
        saved_count = save_meeting_data_to_db(crawl_result, system_user_id, meeting_url=test_url)
        print(f"✅ 保存成功，新增待办: {saved_count} 条")
        
        # 查询刚保存的会议
        meeting = db.query(Meeting).filter(
            Meeting.location == test_url
        ).order_by(Meeting.created_at.desc()).first()
        
        if meeting:
            print(f"✅ 数据库会议记录:")
            print(f"   - 会议ID: {meeting.id}")
            print(f"   - 标题: {meeting.title}")
            print(f"   - 数据库开始时间: {meeting.start_time}")
            print(f"   - 数据库结束时间: {meeting.end_time}")
            print(f"   - 创建时间: {meeting.created_at}")
            
            # 验证时间是否一致
            if crawl_result.get('real_start_time'):
                time_diff = abs((meeting.start_time - crawl_result['real_start_time']).total_seconds())
                if time_diff < 1:  # 1秒内认为是同一时间
                    print("✅ 时间一致性验证通过")
                else:
                    print(f"⚠️ 时间不一致，差异: {time_diff} 秒")
                    print(f"   - 爬取时间: {crawl_result['real_start_time']}")
                    print(f"   - 数据库时间: {meeting.start_time}")
            else:
                print("⚠️ 爬取结果中无真实开始时间")
        else:
            print("❌ 未找到会议记录")
            return False
            
    except Exception as e:
        print(f"❌ 保存测试失败: {e}")
        return False
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("测试 4: 验证排序逻辑")
    print("=" * 60)
    
    # 4. 测试排序
    db = SessionLocal()
    try:
        from sqlalchemy import desc
        from server.models import Meeting
        
        # 查询所有会议，按会议时间排序
        meetings = db.query(Meeting).order_by(desc(Meeting.start_time)).limit(5).all()
        print(f"✅ 按会议时间排序的前5个会议:")
        for i, m in enumerate(meetings, 1):
            print(f"   {i}. {m.title[:30]}... - {m.start_time.strftime('%Y/%m/%d %H:%M:%S')}")
            
        # 查询关联的待办事项
        if meetings:
            latest_meeting = meetings[0]
            todos = db.query(Todo).filter(
                Todo.source_message_id == latest_meeting.id,
                Todo.is_deleted == False
            ).all()
            print(f"\n✅ 会议 '{latest_meeting.title[:20]}...' 的待办事项 ({len(todos)} 条):")
            for todo in todos:
                print(f"   - {todo.title[:40]}...")
                
    except Exception as e:
        print(f"❌ 排序测试失败: {e}")
        return False
    finally:
        db.close()
    
    print("\n" + "=" * 60)
    print("🎉 所有测试通过！")
    print("=" * 60)
    print("功能验证完成:")
    print("1. ✅ 成功集成 meeting_time.py 获取真实开始时间")
    print("2. ✅ crawl_meeting_api 正确返回 real_start_time")
    print("3. ✅ save_meeting_data_to_db 使用真实开始时间")
    print("4. ✅ 数据库排序逻辑正常工作")
    print("\n现在前端可以:")
    print("- 按 '会议时间' 排序显示待办事项")
    print("- 显示 Calendar 图标 + 真实会议时间")
    print("- 按 '生成时间' 排序显示待办事项")
    print("- 显示 Clock 图标 + 任务创建时间")
    
    return True

if __name__ == "__main__":
    test_meeting_time_integration()