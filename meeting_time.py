import requests
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs

def get_meeting_details(share_url, user_cookie):
    parsed_url = urlparse(share_url)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]
    
    # 你找到的 API 地址
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
        
        # --- 提取会议创建时间 (start_time) ---
        meeting_info = data.get("meeting_info", {})
        raw_start_time = meeting_info.get("start_time")  # 得到的是 "1769493618000"
        
        formatted_time = "未知"
        if raw_start_time:
            # 腾讯返回的是13位毫秒级时间戳，除以1000转为秒
            ts = int(raw_start_time) / 1000
            formatted_time = datetime.fromtimestamp(ts).strftime('%Y/%m/%d %H:%M:%S')
        
        # 提取录制列表
        recordings = data.get("recordings", [])
        recording_list = [{"id": rec.get("id"), "name": rec.get("name")} for rec in recordings]
        
        print(f"会议创建时间: {formatted_time}")
        
        return {
            "sharing_id": sharing_id,
            "meeting_id": meeting_info.get("meeting_id"),
            "start_time": formatted_time,
            "recordings": recording_list
        }
    except Exception as e:
        print(f"获取详情失败: {e}")
        return None


def get_real_start_time(share_url, user_cookie=None):
    """
    获取会议真实开始时间 (返回 datetime 对象)

    Args:
        share_url: 腾讯会议分享链接
        user_cookie: 可选的用户 Cookie

    Returns:
        datetime: 会议真实开始时间，失败返回 None
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
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()
        data = res_data.get("data", {})

        meeting_info = data.get("meeting_info", {})
        raw_start_time = meeting_info.get("start_time")

        if raw_start_time:
            # 腾讯返回的是13位毫秒级时间戳，除以1000转为秒
            ts = int(raw_start_time) / 1000
            return datetime.fromtimestamp(ts)
    except Exception as e:
        print(f"获取真实开始时间失败: {e}")

    return None

# 使用示例
if __name__ == "__main__":
    cookie = "..."
    url = "https://meeting.tencent.com/wework/cloud-record/share?id=64957fd6-caa0-4b34-be1c-720a80240864"
    result = get_meeting_details(url, cookie)
