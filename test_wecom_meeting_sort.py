#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试企微发送会议链接 -> 后端处理 -> 数据库排序验证
模拟完整的企微消息流程
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from datetime import datetime
import time
from backend.url_crawler import crawl_and_parse_meeting
from backend.server_receive import save_meeting_data_to_db, get_system_user_id
from server.database import SessionLocal
from server.models import Meeting

# 两个测试链接
URL_1 = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"
URL_2 = "https://meeting.tencent.com/wework/cloud-record/share?id=64957fd6-caa0-4b34-be1c-720a80240864&hide_more_btn=true"

def test_direct_crawl_and_save():
    """
    直接测试爬虫 + 保存到数据库流程
    """
    print("=" * 70)
    print("测试流程: 爬取会议 -> 保存数据库 -> 验证排序")
    print("=" * 70)
    
    # 获取系统用户ID
    system_user_id = get_system_user_id("test_user")
    print(f"\n📌 系统用户ID: {system_user_id}")
    
    # 先发送链接2（时间更晚），再发送链接1（时间更早）
    # 这样可以验证排序是否按时间而非插入顺序
    test_order = [
        ("链接2 (2026/01/27)", URL_2),
        ("链接1 (2026/01/22)", URL_1)
    ]
    
    saved_meetings = []
    
    for name, url in test_order:
        print(f"\n{'='*50}")
        print(f"🔄 处理 {name}")
        print(f"   URL: {url[:60]}...")
        print("-" * 50)
        
        # 1. 爬取会议数据
        print("   [1/2] 正在爬取会议数据...")
        crawl_result = crawl_and_parse_meeting(url, None)
        
        if crawl_result:
            real_start_time = crawl_result.get("real_start_time")
            print(f"   ✅ 爬取成功!")
            print(f"   📅 会议时间: {real_start_time.strftime('%Y/%m/%d %H:%M:%S') if real_start_time else 'N/A'}")
            print(f"   📝 标题: {crawl_result.get('title', 'N/A')[:40]}")
            
            # 2. 保存到数据库
            print("   [2/2] 正在保存到数据库...")
            saved_count = save_meeting_data_to_db(crawl_result, system_user_id, url)
            print(f"   ✅ 已保存 {saved_count} 条待办")
            
            saved_meetings.append({
                "name": name,
                "start_time": real_start_time,
                "url": url
            })
        else:
            print(f"   ❌ 爬取失败")
        
        time.sleep(0.5)
    
    return saved_meetings

def verify_db_sorting():
    """
    验证数据库中的会议是否按开始时间排序
    """
    print("\n" + "=" * 70)
    print("验证数据库排序 (按 start_time DESC)")
    print("=" * 70)
    
    db = SessionLocal()
    try:
        # 按照前端 API 的排序方式查询
        meetings = db.query(Meeting).order_by(Meeting.start_time.desc()).limit(10).all()
        
        print(f"\n📊 数据库中的会议 (按 start_time 降序):")
        print("-" * 70)
        
        for i, m in enumerate(meetings, 1):
            print(f"  {i}. {m.title[:30]:30} | {m.start_time.strftime('%Y/%m/%d %H:%M:%S')}")
        
        # 验证排序是否正确
        if len(meetings) >= 2:
            print("\n🔍 排序验证:")
            if meetings[0].start_time >= meetings[1].start_time:
                print("   ✅ 排序正确! 最新的会议在前面")
            else:
                print("   ❌ 排序错误! 会议顺序不对")
        
        return meetings
        
    finally:
        db.close()

def test_api_endpoint():
    """
    测试前端 API 接口返回的数据排序
    """
    print("\n" + "=" * 70)
    print("测试前端 API 接口排序")
    print("=" * 70)
    
    api_url = "http://localhost:8080/api/meetings/"
    
    try:
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            meetings = response.json()
            print(f"\n📊 API 返回的会议 (共 {len(meetings)} 条):")
            print("-" * 70)
            
            for i, m in enumerate(meetings[:5], 1):
                title = m.get("title", "N/A")[:30]
                start_time = m.get("start_time", "N/A")
                print(f"  {i}. {title:30} | {start_time}")
            
            return meetings
        else:
            print(f"   ⚠️ API 返回状态码: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print("   ⚠️ 无法连接到后端服务 (localhost:8080)")
        print("   请确保后端服务已启动: python -m backend.server_receive")
        return None
    except Exception as e:
        print(f"   ❌ API 请求失败: {e}")
        return None

def main():
    print("\n" + "=" * 70)
    print("🧪 企微会议链接排序测试")
    print("=" * 70)
    print(f"\n测试链接:")
    print(f"  1. {URL_1}")
    print(f"     预期时间: 2026/01/22 15:28:11")
    print(f"  2. {URL_2}")
    print(f"     预期时间: 2026/01/27 14:00:18")
    
    # 1. 直接爬取并保存
    saved_meetings = test_direct_crawl_and_save()
    
    # 2. 验证数据库排序
    db_meetings = verify_db_sorting()
    
    # 3. 测试 API 接口
    print("\n尝试测试 API 接口...")
    api_meetings = test_api_endpoint()
    
    # 总结
    print("\n" + "=" * 70)
    print("📋 测试总结")
    print("=" * 70)
    
    if len(saved_meetings) == 2:
        t1 = saved_meetings[0].get("start_time")
        t2 = saved_meetings[1].get("start_time")
        
        if t1 and t2:
            print(f"\n✅ 两个会议都成功爬取并保存:")
            print(f"   - {saved_meetings[0]['name']}: {t1.strftime('%Y/%m/%d %H:%M')}")
            print(f"   - {saved_meetings[1]['name']}: {t2.strftime('%Y/%m/%d %H:%M')}")
            
            if t1 > t2:
                print(f"\n📊 预期排序: {saved_meetings[0]['name']} (新) -> {saved_meetings[1]['name']} (旧)")
            else:
                print(f"\n📊 预期排序: {saved_meetings[1]['name']} (新) -> {saved_meetings[0]['name']} (旧)")
    
    if api_meetings and len(api_meetings) >= 2:
        print(f"\n✅ 前端 API 可访问，返回 {len(api_meetings)} 条会议记录")
    else:
        print(f"\n⚠️ 前端 API 未启动或无数据")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)

if __name__ == "__main__":
    main()
