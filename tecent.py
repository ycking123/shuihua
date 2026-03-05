import requests
import json
import time
from urllib.parse import urlparse, parse_qs

def get_all_recording_ids(share_url, user_cookie):
    parsed_url = urlparse(share_url)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]
    
    api_url = "https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/detail/common-record-info"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": user_cookie,
        "Content-Type": "application/json",
        "Referer": share_url
    }
    payload = {"sharing_id": sharing_id, "is_single": False, "lang": "zh", "forward_cgi_path": "shares", "enter_from": "share"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()
        data = res_data.get("data", {})
        
        # 重点：检查这里拿到了几个 ID
        recordings = data.get("recordings", [])
        recording_list = []
        for rec in recordings:
            recording_list.append({"id": rec.get("id"), "topic": rec.get("topic")})
        
        return sharing_id, data.get("meeting_info", {}).get("meeting_id"), recording_list
    except: return None, None, []

def crawl_full_meeting_refined(share_url, user_cookie):
    sharing_id, meeting_id, recording_list = get_all_recording_ids(share_url, user_cookie)
    
    if not recording_list:
        return

    detail_api_url = "https://meeting.tencent.com/wemeet-cloudrecording-webapi/v1/minutes/detail"
    # 模拟真实浏览器请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
        "Cookie": user_cookie,
        "Referer": "https://meeting.tencent.com/"
    }

    last_speaker = None
    merged_content = ""

    for rec_info in recording_list:
        rec_id = rec_info['id']
        current_pid = "0"
        
        while True: # 改为死循环，手动控制跳出
            params = {
                "id": sharing_id,
                "meeting_id": meeting_id,
                "recording_id": rec_id,
                "platform": "Web",
                "lang": "zh",
                "pid": current_pid, # 修正参数名为 pid
                "minutes_version": 0,
                "limit": 50
            }
            
            try:
                response = requests.get(detail_api_url, headers=headers, params=params, timeout=10)
                res_json = response.json()
                
                # 兼容解析
                data_root = res_json if "minutes" in res_json else res_json.get("data", {})
                minutes_obj = data_root.get("minutes", {})
                paragraphs = minutes_obj.get("paragraphs", [])
                
                if not paragraphs:
                    print(f"DEBUG: pid {current_pid} 未返回段落，尝试结束当前片段。")
                    break

                for p in paragraphs:
                    speaker = p.get("speaker", {}).get("user_name", "未知")
                    # 修正后的文本提取逻辑
                    text = "".join(["".join([w.get("text", "") for w in s.get("words", [])]) for s in p.get("sentences", [])])

                    if speaker == last_speaker:
                        merged_content += text
                    else:
                        if last_speaker: print(f"【{last_speaker}】: {merged_content}\n")
                        last_speaker = speaker
                        merged_content = text

                # 获取翻页参数
                server_has_more = data_root.get("has_more", minutes_obj.get("has_more", False))
                next_pid = data_root.get("next_pid", minutes_obj.get("next_pid", 0))

                # --- 强制探测逻辑 ---
                if next_pid and str(next_pid) != "0" and str(next_pid) != str(current_pid):
                    current_pid = str(next_pid)
                elif paragraphs:
                    # 如果 server 报 has_more: false，但返回了 paragraphs
                    # 尝试用当前页最后一段的 pid 进行下一次探测
                    last_pid_in_page = str(paragraphs[-1].get("pid"))
                    if last_pid_in_page != current_pid:
                        current_pid = last_pid_in_page
                    else:
                        break # 真的没有新数据了
                else:
                    break
            
                    
            except Exception as e:
                print(f"抓取中断: {e}")
                break
    
    if last_speaker: print(f"【{last_speaker}】: {merged_content}\n")
    
if __name__ == "__main__":
    crawl_full_meeting_refined("https://meeting.tencent.com/wework/cloud-record/share?id=64957fd6-caa0-4b34-be1c-720a80240864&hide_more_btn=true", "COOKIE")
