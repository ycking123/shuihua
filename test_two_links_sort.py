#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试两个会议链接的真实开始时间获取和排序验证
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs

def get_real_start_time_fast(share_url, user_cookie=None):
    """
    快速获取会议真实开始时间 (返回 datetime 对象)
    """
    parsed_url = urlparse(share_url)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]

    if not sharing_id:
        return None

    api_url = "https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/detail/common-record-info"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": share_url
    }
    if user_cookie:
        headers["Cookie"] = user_cookie

    payload = {
        "sharing_id": sharing_id,
        "is_single": False,
        "lang": "zh",
        "forward_cgi_path": "shares",
        "enter_from": "share"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        res_data = response.json()
        
        print(f"  API 响应码: {res_data.get('code', 'N/A')}")
        
        data = res_data.get("data", {})
        meeting_info = data.get("meeting_info", {})
        raw_start_time = meeting_info.get("start_time")
        meeting_title = meeting_info.get("subject", "未知")
        
        print(f"  会议标题: {meeting_title}")
        print(f"  原始时间戳: {raw_start_time}")

        if raw_start_time:
            ts = int(raw_start_time) / 1000
            return datetime.fromtimestamp(ts)
    except Exception as e:
        print(f"  获取失败: {e}")

    return None

def test_two_links():
    """测试两个会议链接的时间获取和排序"""
    
    # 两个测试链接
    url1 = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"
    url2 = "https://meeting.tencent.com/wework/cloud-record/share?id=64957fd6-caa0-4b34-be1c-720a80240864&hide_more_btn=true"
    
    print("=" * 70)
    print("测试两个会议链接的真实开始时间获取")
    print("=" * 70)
    
    results = []
    
    # 测试链接1
    print(f"\n[链接 1]")
    print(f"  ID: 9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd")
    print("-" * 50)
    
    start_time_1 = get_real_start_time_fast(url1, None)
    if start_time_1:
        print(f"✅ 获取成功!")
        print(f"   真实开始时间: {start_time_1.strftime('%Y/%m/%d %H:%M:%S')}")
        print(f"   时间戳: {start_time_1.timestamp()}")
        results.append(("链接1", start_time_1, url1))
    else:
        print("❌ 获取失败")
        results.append(("链接1", None, url1))
    
    # 测试链接2
    print(f"\n[链接 2]")
    print(f"  ID: 64957fd6-caa0-4b34-be1c-720a80240864")
    print("-" * 50)
    
    start_time_2 = get_real_start_time_fast(url2, None)
    if start_time_2:
        print(f"✅ 获取成功!")
        print(f"   真实开始时间: {start_time_2.strftime('%Y/%m/%d %H:%M:%S')}")
        print(f"   时间戳: {start_time_2.timestamp()}")
        results.append(("链接2", start_time_2, url2))
    else:
        print("❌ 获取失败")
        results.append(("链接2", None, url2))
    
    # 排序验证
    print("\n" + "=" * 70)
    print("排序验证结果")
    print("=" * 70)
    
    valid_results = [r for r in results if r[1] is not None]
    
    if len(valid_results) == 2:
        # 按时间排序（最新的在前）
        sorted_results = sorted(valid_results, key=lambda x: x[1], reverse=True)
        
        print("\n📊 按会议时间排序（最新的在前）:")
        print("-" * 50)
        for i, (name, st, url) in enumerate(sorted_results, 1):
            print(f"  {i}. {name}")
            print(f"     会议时间: {st.strftime('%Y/%m/%d %H:%M:%S')}")
            print(f"     链接ID: {url.split('id=')[1].split('&')[0][:20]}...")
        
        # 计算时间差
        time_diff = abs((valid_results[0][1] - valid_results[1][1]).total_seconds())
        print(f"\n⏱️ 两个会议的时间差: {time_diff:.0f} 秒 ({time_diff/3600:.2f} 小时)")
        
        # 判断哪个会议更早
        if valid_results[0][1] < valid_results[1][1]:
            print(f"\n📅 时间顺序: {valid_results[0][0]} 更早 → {valid_results[1][0]} 更晚")
        else:
            print(f"\n📅 时间顺序: {valid_results[1][0]} 更早 → {valid_results[0][0]} 更晚")
            
    elif len(valid_results) == 1:
        print(f"\n⚠️ 只有 1 个会议获取到时间")
        print(f"  {valid_results[0][0]}: {valid_results[0][1].strftime('%Y/%m/%d %H:%M:%S')}")
    else:
        print("\n❌ 没有会议获取到时间，无法进行排序验证")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
    
    return valid_results

if __name__ == "__main__":
    test_two_links()
