"""
测试 API 爬虫 - 无需 Cookie，直接调用腾讯会议公开 API
"""
import requests
import json
import time
import random
import string
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# 测试链接
TEST_URL = "https://meeting.tencent.com/wework/cloud-record/share?id=9ce9ba1f-3f4b-4844-b6e5-705e7665b7cd&hide_more_btn=true"

def get_random_str(length=9):
    """生成随机字符串用于指纹校验"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_api_crawler():
    """测试 API 爬虫 - 无需 Cookie"""
    print("=" * 60)
    print("[API] 测试 API 爬虫（无需登录）")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[URL] 测试链接: {TEST_URL}")
    print("-" * 60)
    
    # 解析 URL 获取 sharing_id
    parsed_url = urlparse(TEST_URL)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]
    
    if not sharing_id:
        print("[ERROR] 无法从 URL 解析 sharing_id")
        return None
    
    print(f"[ID] sharing_id: {sharing_id}")
    
    # 步骤 1: 获取会议信息和录制列表
    print("\n[步骤 1] 获取会议信息和录制列表...")
    api_url = "https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/detail/common-record-info"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": TEST_URL
    }
    
    payload = {
        "sharing_id": sharing_id,
        "is_single": False,
        "lang": "zh",
        "forward_cgi_path": "shares",
        "enter_from": "share"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        print(f"  [Status] 响应状态码: {response.status_code}")
        
        res_data = response.json()
        
        if res_data.get("code") != 0:
            print(f"  [ERROR] API 返回错误: {res_data.get('message', '未知错误')}")
            print(f"  [DEBUG] 完整响应: {json.dumps(res_data, ensure_ascii=False, indent=2)}")
            return None
        
        data = res_data.get("data", {})
        meeting_info = data.get("meeting_info", {})
        recordings = data.get("recordings", [])
        
        meeting_id = meeting_info.get("meeting_id")
        meeting_title = meeting_info.get("subject", "未知会议")
        
        print(f"  [OK] 会议 ID: {meeting_id}")
        print(f"  [OK] 会议标题: {meeting_title}")
        print(f"  [OK] 录制片段数: {len(recordings)}")
        
        if not recordings:
            print("  [WARN] 没有录制片段")
            return None
        
        # 步骤 2: 获取 AI 摘要和待办
        print("\n[步骤 2] 获取 AI 摘要和待办...")
        record_id = recordings[0].get("id")
        print(f"  [ID] record_id: {record_id}")
        
        nonce = get_random_str(9)
        timestamp = str(int(time.time() * 1000))
        trace_id = get_random_str(32).lower()
        
        summary_api = (
            f"https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/record-detail/get-mul-summary-and-todo?"
            f"c_timestamp={timestamp}&c_nonce={nonce}&meeting_id={meeting_id}&trace-id={trace_id}&c_lang=zh-CN"
        )
        
        summary_payload = {
            "record_id": record_id,
            "meeting_id": meeting_id,
            "lang": "zh",
            "share_id": sharing_id,
            "summary_type": 0
        }
        
        response2 = requests.post(summary_api, headers=headers, json=summary_payload, timeout=15)
        print(f"  [Status] 响应状态码: {response2.status_code}")
        
        summary_data = response2.json()
        
        if summary_data.get("code") != 0:
            print(f"  [WARN] 摘要 API 错误: {summary_data.get('message')}")
        else:
            data2 = summary_data.get("data", {})
            
            # AI 智能总结
            ds_summary = data2.get("deepseek_summary", {}).get("topic_summary", {})
            if ds_summary:
                print("\n  [Info] AI 智能总览")
                begin = ds_summary.get("begin_summary", "")
                if begin:
                    print(f"     {begin[:200]}...")
            
            # 待办事项
            todos = data2.get("todo", {}).get("todo_list", [])
            if todos:
                print(f"\n  [Info] 待办事项 ({len(todos)} 条)")
                for i, t in enumerate(todos[:5], 1):
                    print(f"     {i}. {t.get('todo_name', t)}")
        
        # 步骤 3: 获取转写内容
        print("\n[步骤 3] 获取转写内容...")
        
        detail_api = "https://meeting.tencent.com/wemeet-cloudrecording-webapi/v1/minutes/detail"
        
        all_transcript = []
        for rec in recordings[:1]:  # 只取第一个录制片段
            rec_id = rec.get("id")
            current_pid = "0"
            
            while True:
                params = {
                    "id": sharing_id,
                    "meeting_id": meeting_id,
                    "recording_id": rec_id,
                    "platform": "Web",
                    "lang": "zh",
                    "pid": current_pid,
                    "minutes_version": 0,
                    "limit": 50
                }
                
                resp3 = requests.get(detail_api, headers=headers, params=params, timeout=15)
                res3 = resp3.json()
                
                data_root = res3 if "minutes" in res3 else res3.get("data", {})
                minutes = data_root.get("minutes", {})
                paragraphs = minutes.get("paragraphs", [])
                
                if not paragraphs:
                    break
                
                for p in paragraphs:
                    speaker = p.get("speaker", {}).get("user_name", "未知")
                    text = "".join(["".join([w.get("text", "") for w in s.get("words", [])]) for s in p.get("sentences", [])])
                    if text:
                        all_transcript.append(f"[{speaker}]: {text}")
                
                # 翻页
                next_pid = data_root.get("next_pid", minutes.get("next_pid", 0))
                if next_pid and str(next_pid) != "0" and str(next_pid) != current_pid:
                    current_pid = str(next_pid)
                else:
                    break
        
        if all_transcript:
            print(f"  [OK] 获取转写 {len(all_transcript)} 段")
            print(f"\n  [Info] 转写预览 (前 3 段)")
            for t in all_transcript[:3]:
                print(f"     {t[:100]}...")
        
        # 汇总结果
        result = {
            "title": meeting_title,
            "meeting_id": meeting_id,
            "summary": summary_data.get("data", {}) if summary_data.get("code") == 0 else {},
            "transcript": all_transcript,
            "todos": summary_data.get("data", {}).get("todo", {}).get("todo_list", []) if summary_data.get("code") == 0 else []
        }
        
        # 保存结果
        output_file = "test_crawl_result.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n[OK] 结果已保存到: {output_file}")
        
        print("\n" + "=" * 60)
        print("[OK] 测试完成!")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"\n[ERROR] 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_api_crawler()
