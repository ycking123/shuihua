import requests
import json
import time
import random
import string
import re
from urllib.parse import urlparse, parse_qs

def get_random_str(length=9):
    """生成随机字符串用于指纹校验"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def clean_text(text):
    """清洗 HTML 标签，处理换行和列表符号"""
    if not text: return ""
    # 替换常见的 HTML 标签为易读格式
    text = text.replace("<p>", "").replace("</p>", "\n")
    text = text.replace("<ul>", "").replace("</ul>", "")
    text = text.replace("<li>", " • ").replace("</li>", "\n")
    text = text.replace("<h4>", "\n# ").replace("</h4>", "\n")
    # 移除其余所有 HTML 标签
    return re.sub('<.*?>', '', text).strip()

def get_meeting_params(share_url, user_cookie):
    """通过分享链接自动获取 sharing_id, meeting_id 和 record_id"""
    parsed_url = urlparse(share_url)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]
    
    if not sharing_id:
        print("❌ 无法从 URL 中解析出 ID")
        return None, None, None

    api_url = "https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/detail/common-record-info"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": user_cookie,
        "Content-Type": "application/json",
        "Referer": share_url
    }
    payload = {
        "sharing_id": sharing_id, 
        "is_single": False, 
        "lang": "zh", 
        "forward_cgi_path": "shares", 
        "enter_from": "share"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()
        data = res_data.get("data", {})
        meeting_id = data.get("meeting_info", {}).get("meeting_id")
        recordings = data.get("recordings", [])
        record_id = recordings[0].get("id") if recordings else None
        return sharing_id, meeting_id, record_id
    except Exception as e:
        print(f"❌ 获取会议参数失败: {e}")
        return None, None, None

def crawl_tencent_summary_by_url(share_url, user_cookie):
    share_id, meeting_id, record_id = get_meeting_params(share_url, user_cookie)
    if not all([share_id, meeting_id, record_id]): return

    nonce = get_random_str(9)
    timestamp = str(int(time.time() * 1000))
    trace_id = get_random_str(32).lower()

    api_url = (
        f"https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/record-detail/get-mul-summary-and-todo?"
        f"c_timestamp={timestamp}&c_nonce={nonce}&meeting_id={meeting_id}&trace-id={trace_id}&c_lang=zh-CN"
    )

    payload = {
        "record_id": record_id,
        "meeting_id": meeting_id,
        "lang": "zh",
        "share_id": share_id,
        "summary_type": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": user_cookie,
        "Content-Type": "application/json",
        "Referer": share_url
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        res_json = response.json()
        if res_json.get("code") != 0: return

        data = res_json.get("data", {})

        print(f"\n{'='*20} 会议 AI 内容整合 {'='*20}\n")

        # 1. DeepSeek 智能总结 (总览)
        ds_summary = data.get("deepseek_summary", {}).get("topic_summary", {})
        if ds_summary:
            print("【AI 智能总览】")
            print(ds_summary.get("begin_summary", ""))
            for point in ds_summary.get("sub_points", []):
                print(f"\n# {point.get('sub_point_title')}")
                for item in point.get("sub_point_vec_items", []):
                    print(f" • {item.get('point')}")
            print("-" * 50)

        # 2. 章节概览
        chapters = data.get("chapter_summary", {}).get("summary_list", [])
        if chapters:
            print("\n【章节内容详情】")
            for idx, c in enumerate(chapters, 1):
                print(f"{idx}. {c.get('title')}\n   内容: {c.get('summary')}")
            print("-" * 50)

        # 3. 发言人总结
        speakers = data.get("speaker_summary", {}).get("speakers_opinions", [])
        if speakers:
            print("\n【发言人观点整合】")
            for s in speakers:
                print(f"\n发言人: {s.get('speaker_id')}")
                for sp in s.get("sub_points", []):
                    print(f"  [{sp.get('sub_point_title')}]")
                    for item in sp.get("sub_point_vec_items", []):
                        print(f"   - {item.get('point')}")
            print("-" * 50)

        # 4. 待办事项
        todos = data.get("todo", {}).get("todo_list", [])
        if todos:
            print("\n【待办事项列表】")
            for idx, t in enumerate(todos, 1):
                print(f"[{idx}] {t.get('todo_name')}")

    except Exception as e:
        print(f"\n❌ [解析异常]: {e}")

if __name__ == "__main__":
    target_url = "https://meeting.tencent.com/wework/cloud-record/share?id=64957fd6-caa0-4b34-be1c-720a80240864&hide_more_btn=true"
    my_cookie = "Cookie"
    crawl_tencent_summary_by_url(target_url, my_cookie)
