# ============================================================================
# 文件: url_crawler.py
# 模块: backend
# 职责: 会议 URL 爬虫，负责从腾讯会议等平台爬取会议数据
#
# 依赖声明:
#   - 外部: requests, logging, re, json, html, time, random, string, difflib, typing, urllib.parse
#   - 本模块: backend.ai_handler (extract_todos_from_text)
#   - 可选: backend.crawl_with_browser (crawl_meeting_minutes) - PLAYWRIGHT_AVAILABLE 标志位
#
# 主要接口:
#   - crawl_and_parse_meeting(url, cookies_str) -> Dict: 主入口，爬取会议数据
#   - crawl_meeting_api(share_url, user_cookie) -> Dict: API 爬虫方法
#   - crawl_meeting_transcript_api(share_url, user_cookie) -> str: 获取会议转写
#   - crawl_meeting_summary_api(share_url, user_cookie) -> Dict: 获取会议摘要
#
# ============================================================================

import requests
import logging
import re
import json
import html as html_lib
import time
import random
import string
from difflib import SequenceMatcher
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urljoin, urlparse, parse_qs
from backend.ai_handler import extract_todos_from_text

# Playwright 浏览器爬虫为可选依赖（API 爬虫不需要）
try:
    from backend.crawl_with_browser import crawl_meeting_minutes
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    crawl_meeting_minutes = None
    PLAYWRIGHT_AVAILABLE = False

logger = logging.getLogger("URLCrawler")

# ============================================================================
# 新的 API 爬虫方法 (基于 tecent.py 和 summary.py)
# ============================================================================

def get_random_str(length=9):
    """生成随机字符串用于指纹校验"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def _maybe_decode_base64_text(value: str) -> str:
    if not value:
        return value
    try:
        import base64
        decoded = base64.b64decode(value).decode("utf-8")
        return decoded or value
    except Exception:
        return value

def get_all_recording_ids(share_url, user_cookie: Optional[str] = None):
    """
    获取会议所有录制片段的 ID
    返回: (sharing_id, meeting_id, recording_list)
    """
    parsed_url = urlparse(share_url)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]
    
    api_url = "https://meeting.tencent.com/wemeet-tapi/v2/meetlog/public/detail/common-record-info"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Referer": share_url
    }
    if user_cookie:
        headers["Cookie"] = user_cookie
    payload = {"sharing_id": sharing_id, "is_single": False, "lang": "zh", "forward_cgi_path": "shares", "enter_from": "share"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()
        data = res_data.get("data", {})
        
        recordings = data.get("recordings", [])
        recording_list = []
        for rec in recordings:
            recording_list.append({"id": rec.get("id"), "topic": rec.get("topic")})
        
        return sharing_id, data.get("meeting_info", {}).get("meeting_id"), recording_list
    except Exception as e:
        logger.error(f"获取录制 ID 失败: {e}")
        return None, None, []

def crawl_meeting_transcript_api(share_url, user_cookie: Optional[str] = None):
    """
    使用 API 爬取完整的会议转写内容 (基于 tecent.py)
    返回: 按发言人分组的转写文本
    """
    sharing_id, meeting_id, recording_list = get_all_recording_ids(share_url, user_cookie)
    
    if not recording_list:
        logger.warning("未获取到录制片段")
        return ""

    detail_api_url = "https://meeting.tencent.com/wemeet-cloudrecording-webapi/v1/minutes/detail"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
        "Referer": "https://meeting.tencent.com/"
    }
    if user_cookie:
        headers["Cookie"] = user_cookie

    transcript_lines = []
    last_speaker = None
    merged_content = ""

    for rec_info in recording_list:
        rec_id = rec_info['id']
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
            
            try:
                response = requests.get(detail_api_url, headers=headers, params=params, timeout=10)
                res_json = response.json()
                
                data_root = res_json if "minutes" in res_json else res_json.get("data", {})
                minutes_obj = data_root.get("minutes", {})
                paragraphs = minutes_obj.get("paragraphs", [])
                
                if not paragraphs:
                    break

                for p in paragraphs:
                    speaker = p.get("speaker", {}).get("user_name", "未知")
                    text = "".join(["".join([w.get("text", "") for w in s.get("words", [])]) for s in p.get("sentences", [])])

                    if speaker == last_speaker:
                        merged_content += text
                    else:
                        if last_speaker:
                            transcript_lines.append(f"【{last_speaker}】: {merged_content}")
                        last_speaker = speaker
                        merged_content = text

                server_has_more = data_root.get("has_more", minutes_obj.get("has_more", False))
                next_pid = data_root.get("next_pid", minutes_obj.get("next_pid", 0))

                if next_pid and str(next_pid) != "0" and str(next_pid) != str(current_pid):
                    current_pid = str(next_pid)
                elif paragraphs:
                    last_pid_in_page = str(paragraphs[-1].get("pid"))
                    if last_pid_in_page != current_pid:
                        current_pid = last_pid_in_page
                    else:
                        break
                else:
                    break
                    
            except Exception as e:
                logger.error(f"爬取转写中断: {e}")
                break
    
    if last_speaker:
        transcript_lines.append(f"【{last_speaker}】: {merged_content}")
    
    return "\n\n".join(transcript_lines)

def get_meeting_params(share_url, user_cookie: Optional[str] = None):
    """通过分享链接自动获取 sharing_id, meeting_id 和 record_id"""
    parsed_url = urlparse(share_url)
    query_params = parse_qs(parsed_url.query)
    sharing_id = query_params.get('id', [None])[0]
    
    if not sharing_id:
        logger.error("无法从 URL 中解析出 ID")
        return None, None, None

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
        meeting_id = data.get("meeting_info", {}).get("meeting_id")
        meeting_title = data.get("meeting_info", {}).get("subject", "会议纪要")
        if meeting_title:
            meeting_title = _maybe_decode_base64_text(meeting_title)
        recordings = data.get("recordings", [])
        record_id = recordings[0].get("id") if recordings else None
        return sharing_id, meeting_id, record_id, meeting_title
    except Exception as e:
        logger.error(f"获取会议参数失败: {e}")
        return None, None, None, None

def crawl_meeting_summary_api(share_url, user_cookie: Optional[str] = None):
    """
    使用 API 爬取会议 AI 摘要和待办 (基于 summary.py)
    返回: { title, summary, transcript, todos, personal_todos }
    """
    result = get_meeting_params(share_url, user_cookie)
    if not result or not all(result[:3]):
        return None
    
    share_id, meeting_id, record_id, meeting_title = result

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
        "Content-Type": "application/json",
        "Referer": share_url
    }
    if user_cookie:
        headers["Cookie"] = user_cookie

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        res_json = response.json()
        
        if res_json.get("code") != 0:
            logger.warning(f"API 返回错误: {res_json.get('message')}")
            return None

        data = res_json.get("data", {})
        
        # 解析结果
        summary_parts = []
        todos = []
        
        # 1. DeepSeek 智能总结
        ds_summary = data.get("deepseek_summary", {}).get("topic_summary", {})
        if ds_summary:
            begin = ds_summary.get("begin_summary", "")
            if begin:
                summary_parts.append(f"【AI 智能总览】\n{begin}")
            for point in ds_summary.get("sub_points", []):
                title = point.get('sub_point_title', '')
                summary_parts.append(f"\n# {title}")
                for item in point.get("sub_point_vec_items", []):
                    summary_parts.append(f" • {item.get('point', '')}")
        
        # 2. 章节概览
        chapters = data.get("chapter_summary", {}).get("summary_list", [])
        if chapters:
            chapter_text = "\n【章节内容详情】"
            for idx, c in enumerate(chapters, 1):
                chapter_text += f"\n{idx}. {c.get('title', '')}\n   内容: {c.get('summary', '')}"
            summary_parts.append(chapter_text)
        
        # 3. 发言人总结
        speakers = data.get("speaker_summary", {}).get("speakers_opinions", [])
        if speakers:
            speaker_text = "\n【发言人观点整合】"
            for s in speakers:
                speaker_id = s.get('speaker_id', '未知')
                speaker_text += f"\n发言人: {speaker_id}"
                for sp in s.get("sub_points", []):
                    speaker_text += f"\n  [{sp.get('sub_point_title', '')}]"
                    for item in sp.get("sub_point_vec_items", []):
                        speaker_text += f"\n   - {item.get('point', '')}"
            summary_parts.append(speaker_text)
        
        # 4. 待办事项
        todo_list = data.get("todo", {}).get("todo_list", [])
        for t in todo_list:
            todos.append({
                "title": t.get("todo_name", "待办事项"),
                "description": t.get("todo_name", ""),
                "assignee": "待定",
                "priority": "normal",
                "due_date": ""
            })
        
        summary_text = "\n".join(summary_parts)
        
        logger.info(f"✅ API 爬取成功: 获取摘要 {len(summary_text)} 字符, 待办 {len(todos)} 条")
        
        return {
            "title": meeting_title or "会议纪要",
            "summary": summary_text,
            "transcript": "",  # 摘要 API 不返回完整转写
            "todos": todos,
            "personal_todos": todos  # 兼容旧结构
        }
        
    except Exception as e:
        logger.error(f"爬取摘要异常: {e}")
        return None

def crawl_meeting_api(share_url, user_cookie: Optional[str] = None):
    """
    新的 API 爬虫主入口 - 同时获取摘要和转写
    """
    logger.info(f"🚀 使用 API 爬虫模式爬取: {share_url}")
    
    # 1. 先获取摘要和待办
    summary_result = crawl_meeting_summary_api(share_url, user_cookie)
    
    # 2. 再获取完整转写
    transcript = crawl_meeting_transcript_api(share_url, user_cookie)
    
    # 3. 合并结果
    if summary_result:
        summary_result["transcript"] = transcript
        # 如果 API 没有待办，从转写中提取
        if not summary_result.get("todos") and transcript:
            ai_result = extract_todos_from_text(transcript)
            if ai_result:
                summary_result["summary"] = summary_result.get("summary", "") or ai_result.get("summary", "")
                summary_result["todos"] = ai_result.get("task_list", [])
        # 生成 personal_todos
        if transcript:
            summary_result["personal_todos"] = build_personal_todos(transcript, summary_result.get("todos", []))
        return summary_result
    elif transcript:
        # 只有转写，没有摘要
        ai_result = extract_todos_from_text(transcript)
        return {
            "title": "会议纪要",
            "summary": ai_result.get("summary", "") if ai_result else "",
            "transcript": transcript,
            "todos": ai_result.get("task_list", []) if ai_result else [],
            "personal_todos": build_personal_todos(transcript, ai_result.get("task_list", []) if ai_result else [])
        }
    
    return None

def extract_meeting_url(text: str) -> Optional[str]:
    """
    从文本中提取腾讯会议/企业微信文档的 URL
    """
    # 匹配常见的会议链接格式
    # https://meeting.tencent.com/p/xxx
    # https://meeting.tencent.com/wework/cloud-record/share?id=xxx
    url_pattern = r'(https?://(?:meeting\.tencent\.com|docs\.qq\.com|doc\.weixin\.qq\.com)/[^\s]+)'
    match = re.search(url_pattern, text)
    if match:
        return match.group(1)
    return None

def extract_json_object(text: str, start_index: int) -> Optional[str]:
    """Find the matching closing brace for a JSON object starting at start_index"""
    brace_count = 0
    in_string = False
    escape = False
    
    for i in range(start_index, len(text)):
        char = text[i]
        if in_string:
            if escape:
                escape = False
            elif char == '\\':
                escape = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start_index:i+1]
    return None

def parse_meeting_html(html: str) -> Dict[str, Any]:
    """
    解析腾讯会议 HTML，提取 serverData 中的元数据
    """
    result = {
        "title": "未知会议",
        "meeting_id": "",
        "duration": 0,
        "minutes_text": "",
        "recordings": []
    }
    
    try:
        # 查找 Next.js 的 hydration 数据: self.__next_f.push([1,"..."])
        pushes = re.finditer(r'self\.__next_f\.push\(\[(.*?)\]\)', html)
        
        for match in pushes:
            inner = match.group(1)
            parts = inner.split(',', 1)
            if len(parts) < 2: continue
            
            json_str_raw = parts[1].strip()
            
            # 尝试解析 JSON 字符串
            if json_str_raw.startswith('"') and json_str_raw.endswith('"'):
                try:
                    content = json.loads(json_str_raw)
                    if "serverData" in content:
                        sd_match = re.search(r'"serverData":(\{.*?\})', content)
                        if sd_match:
                            start = content.find('"serverData":') + len('"serverData":')
                            obj_str = extract_json_object(content, start)
                            if obj_str:
                                sd = json.loads(obj_str)
                                
                                # 提取关键信息
                                if "meeting_info" in sd:
                                    subject = sd["meeting_info"].get("subject", "")
                                    # 尝试 Base64 解码标题 (腾讯会议标题常为 Base64)
                                    try:
                                        import base64
                                        decoded_subject = base64.b64decode(subject).decode('utf-8')
                                        result["title"] = decoded_subject
                                    except:
                                        result["title"] = subject
                                    
                                    result["meeting_id"] = sd["meeting_info"].get("meeting_id", "")
                                
                                result["duration"] = sd.get("total_recording_duration", 0)
                                result["recordings"] = sd.get("recordings", [])
                                
                                # 检查是否有纪要文本 (目前通常为空，需要 API)
                                if "smart_minutes" in sd:
                                    result["minutes_text"] = str(sd["smart_minutes"])
                                
                                logger.info(f"✅ 成功提取会议元数据: {result['title']}")
                                return result
                except Exception as e:
                    continue
                    
    except Exception as e:
        logger.error(f"❌ 解析 HTML 失败: {e}")
        
    return result

def extract_json_block(text: str, start_index: int) -> Optional[str]:
    stack = []
    in_string = False
    escape = False
    for i in range(start_index, len(text)):
        char = text[i]
        if in_string:
            if escape:
                escape = False
            elif char == '\\':
                escape = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char in "{[":
                stack.append(char)
            elif char in "}]":
                if not stack:
                    return None
                last = stack.pop()
                if not stack:
                    return text[start_index:i + 1]
    return None

def extract_next_payloads(html: str) -> List[str]:
    payloads = []
    pushes = re.finditer(r'self\.__next_f\.push\(\[(.*?)\]\)', html)
    for match in pushes:
        inner = match.group(1)
        parts = inner.split(',', 1)
        if len(parts) < 2:
            continue
        json_str_raw = parts[1].strip()
        if json_str_raw.startswith('"') and json_str_raw.endswith('"'):
            try:
                payloads.append(json.loads(json_str_raw))
            except Exception:
                continue
    return payloads

def extract_next_data_json(html: str) -> Optional[str]:
    match = re.search(r'__NEXT_DATA__[^>]*>(.*?)</script>', html, re.DOTALL)
    if not match:
        return None
    raw = match.group(1)
    try:
        return json.dumps(json.loads(raw), ensure_ascii=False)
    except Exception:
        return None

def extract_server_data_objects(texts: List[str]) -> List[Dict[str, Any]]:
    server_data_list = []
    for text in texts:
        if not text or "serverData" not in text:
            continue
        idx = text.find('"serverData":')
        while idx != -1:
            start = idx + len('"serverData":')
            obj_str = extract_json_object(text, start)
            if obj_str:
                try:
                    server_data_list.append(json.loads(obj_str))
                except Exception:
                    pass
            idx = text.find('"serverData":', idx + len('"serverData":'))
    return server_data_list

def find_text_by_keys(obj: Any, key_keywords: List[str], min_length: int = 60) -> List[str]:
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                if any(kw in k.lower() for kw in key_keywords) and len(v) >= min_length:
                    results.append(v)
            else:
                results.extend(find_text_by_keys(v, key_keywords, min_length))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(find_text_by_keys(item, key_keywords, min_length))
    return results

def pick_best_text(texts: List[str]) -> str:
    if not texts:
        return ""
    def score(s: str) -> int:
        zh_count = len(re.findall(r'[\u4e00-\u9fa5]', s))
        return len(s) + zh_count * 2
    return max(texts, key=score)

def strip_html_tags(html: str) -> str:
    if "<" not in html:
        return html
    cleaned = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    cleaned = html_lib.unescape(cleaned)
    cleaned = re.sub(r"[ \t\r\f\v]+", " ", cleaned)
    return cleaned.strip()

def extract_title_from_html(html: str) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if match:
        return html_lib.unescape(match.group(1)).strip()
    return ""

def extract_json_values(text: str, key: str) -> List[str]:
    values = []
    pattern = rf'"{re.escape(key)}"\s*:\s*'
    for match in re.finditer(pattern, text):
        idx = match.end()
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            continue
        if text[idx] in "{[":
            block = extract_json_block(text, idx)
            if block:
                values.append(block)
        elif text[idx] == '"':
            i = idx + 1
            escape = False
            while i < len(text):
                char = text[i]
                if escape:
                    escape = False
                elif char == '\\':
                    escape = True
                elif char == '"':
                    values.append(text[idx + 1:i])
                    break
                i += 1
    return values

def normalize_transcript(text: str) -> str:
    if not text:
        return ""
    
    # 1. 基础清洗
    text = text.replace("\u3000", " ").replace("\r", " ").replace("\t", " ")
    
    # 2. 移除常见的 UI 导航词 (尤其是出现在开头或单独一行的)
    ui_words = ["返回", "更多", "分享", "收藏", "搜索", "全部", "只看", "导出", "翻译", "倍速"]
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 跳过极短的 UI 词
        if len(line) <= 4 and line in ui_words:
            continue
        # 跳过纯时间戳 (如果不是跟在名字后面的话，不过这里简单处理)
        # if re.match(r'^\d{1,2}:\d{2}$', line):
        #    continue
            
        cleaned_lines.append(line)
    
    text = " ".join(cleaned_lines)
    
    # 3. 标点符号规范化与分行
    text = re.sub(r"\s{2,}", " ", text)
    text = text.replace("。", "。\n").replace("！", "！\n").replace("？", "？\n")
    text = re.sub(r"\n{2,}", "\n", text)
    
    return text.strip()

def split_speaker_segments(text: str) -> List[Tuple[str, str]]:
    segments = []
    pattern = re.compile(r'([\u4e00-\u9fa5A-Za-z]{1,10})\s*(\d{1,2}:\d{2})')
    matches = list(pattern.finditer(text))
    if not matches:
        return [("", text)]
    for i, match in enumerate(matches):
        speaker = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        segments.append((speaker, content))
    return segments

def normalize_name(name: str) -> str:
    if "Sender" in name or "发送者" in name:
        return "Sender（发送者）"
    name = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", name)
    name = re.sub(r"(先生|女士|总|经理|老师|同学|主任|老板)$", "", name)
    return name.strip()

def cluster_names(names: List[str]) -> Dict[str, str]:
    normalized = []
    mapping = {}
    for name in names:
        norm = normalize_name(name)
        if not norm:
            continue
        matched = None
        for base in normalized:
            ratio = SequenceMatcher(None, norm, base).ratio()
            if ratio >= 0.85 or norm in base or base in norm:
                matched = base
                break
        if not matched:
            normalized.append(norm)
            matched = norm
        mapping[name] = matched
    return mapping

def extract_task_sentences(text: str) -> List[str]:
    keywords = [
        "负责", "跟进", "完成", "提交", "整理", "汇总", "准备", "推进",
        "对接", "安排", "落实", "输出", "复盘", "确认", "测试", "上线",
        "优化", "需求", "修复", "交付", "配合", "支持", "回传"
    ]
    sentences = re.split(r"[。！？\n]", text)
    tasks = []
    for s in sentences:
        s = s.strip()
        if len(s) < 6:
            continue
        if any(k in s for k in keywords):
            tasks.append(s)
    return tasks

def build_personal_todos(transcript: str, meeting_todos: List[dict]) -> List[dict]:
    personal = []
    segments = split_speaker_segments(transcript)
    speaker_names = [s for s, _ in segments if s]
    name_map = cluster_names(speaker_names)

    for t in meeting_todos or []:
        if isinstance(t, str):
            personal.append({
                "title": t,
                "description": t,
                "assignee": "Sender（发送者）",
                "priority": "normal",
                "due_date": ""
            })
            continue
        assignee = t.get("assignee") or "Sender（发送者）"
        assignee = name_map.get(assignee, normalize_name(assignee)) or "Sender（发送者）"
        personal.append({
            "title": t.get("title") or "会议待办",
            "description": t.get("description") or t.get("title") or "",
            "assignee": assignee,
            "priority": t.get("priority") or "normal",
            "due_date": t.get("due_date") or ""
        })

    if personal:
        return personal

    for speaker, content in segments:
        assignee = name_map.get(speaker, normalize_name(speaker)) or "Sender（发送者）"
        for s in extract_task_sentences(content):
            title = s[:32]
            personal.append({
                "title": title,
                "description": s,
                "assignee": assignee,
                "priority": "normal",
                "due_date": ""
            })
    return personal

def parse_meeting_page(html: str) -> Dict[str, Any]:
    candidate_texts = [html]
    candidate_texts.extend([p for p in extract_next_payloads(html) if p])
    next_data = extract_next_data_json(html)
    if next_data:
        candidate_texts.append(next_data)
    server_data_list = extract_server_data_objects(candidate_texts)

    title = ""
    for text in candidate_texts:
        if not title:
            title = extract_title_from_html(text)
        for sd in extract_json_values(text, "serverData"):
            try:
                sd_json = json.loads(sd)
                meeting_info = sd_json.get("meeting_info") or {}
                subject = meeting_info.get("subject") or ""
                if subject:
                    try:
                        import base64
                        title = base64.b64decode(subject).decode("utf-8")
                    except Exception:
                        title = subject
            except Exception:
                continue

    transcript_candidates = []
    for text in candidate_texts:
        for key in ["transcript", "transcription", "asr", "minutes_text", "text"]:
            transcript_candidates.extend(extract_json_values(text, key))
    transcript = ""
    for t in transcript_candidates:
        if isinstance(t, str) and len(t) > len(transcript):
            transcript = t
    if not transcript and server_data_list:
        key_keywords = ["transcript", "transcription", "asr", "subtitle", "minutes", "summary", "text", "content", "speech"]
        text_hits = []
        for sd in server_data_list:
            text_hits.extend(find_text_by_keys(sd, key_keywords))
        transcript = pick_best_text(text_hits)
    if not transcript:
        transcript = strip_html_tags(html)

    transcript = normalize_transcript(transcript)
    ai_result = extract_todos_from_text(transcript) if transcript else None
    summary = ""
    todos = []
    if ai_result:
        summary = ai_result.get("summary", "")
        todos = ai_result.get("task_list", []) or []

    personal_todos = build_personal_todos(transcript, todos)

    return {
        "title": title or "会议纪要",
        "summary": summary or "",
        "transcript": transcript or "",
        "todos": todos or [],
        "personal_todos": personal_todos or []
    }

def crawl_and_parse_meeting_browser(url: str, cookies_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    [备用方法] 使用 Playwright 浏览器爬虫获取会议内容
    """
    if not PLAYWRIGHT_AVAILABLE:
        logger.error("❌ Playwright 未安装，浏览器爬虫不可用。请运行: pip install playwright && playwright install chromium")
        return None
    
    try:
        logger.info(f"🔄 切换到浏览器爬虫模式 (Playwright) 爬取: {url}")
        # 调用基于 pc.py 逻辑的浏览器爬虫
        result = crawl_meeting_minutes(url, cookies_str)
        
        if not result:
            logger.warning("⚠️ 浏览器爬虫未返回结果")
            return None
            
        # 补充 personal_todos 生成逻辑 (复用本文件中的函数)
        # 如果爬虫返回结果中没有 personal_todos，但有转写文本和待办，则自动生成
        if not result.get("personal_todos") and result.get("transcript"):
            logger.info("🔨 正在基于转写内容生成个人待办...")
            result["personal_todos"] = build_personal_todos(result["transcript"], result.get("todos", []))
            
        return result
        
    except Exception as e:
        logger.error(f"❌ 浏览器爬虫失败: {e}")
        return None

def crawl_and_parse_meeting(url: str, cookies_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    主爬虫入口 - 优先使用 API 爬虫，失败时回退到浏览器爬虫
    
    爬取策略：
    1. 首先尝试 API 爬虫 (crawl_meeting_api) - 直接调用腾讯会议 API，速度快
    2. 如果 API 爬虫失败，回退到浏览器爬虫 (crawl_and_parse_meeting_browser) - 使用 Playwright 模拟浏览器
    """
    # 1. 优先尝试 API 爬虫
    # 策略 A: 如果有 cookie，先试带 cookie
    if cookies_str:
        try:
            logger.info("尝试带 Cookie 进行 API 爬取...")
            result = crawl_meeting_api(url, cookies_str)
            if result:
                logger.info("✅ 带 Cookie API 爬虫成功")
                return result
        except Exception as e:
            logger.warning(f"⚠️ 带 Cookie API 爬虫失败: {e}")

    # 策略 B: 尝试无 Cookie API 爬取 (公开链接)
    try:
        logger.info("尝试无 Cookie API 爬取...")
        # 传入 None 作为 cookie，requests 会忽略 None 的 header
        result = crawl_meeting_api(url, None)
        if result:
            logger.info("✅ 无 Cookie API 爬虫成功")
            return result
    except Exception as e:
        logger.warning(f"⚠️ 无 Cookie API 爬虫失败: {e}")
    
    # 2. 回退到浏览器爬虫
    logger.info("🔄 回退到浏览器爬虫模式...")
    return crawl_and_parse_meeting_browser(url, cookies_str)

# 原有的静态爬取逻辑保留但不使用
def crawl_and_parse_meeting_legacy(url: str, cookies_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
    html = fetch_content_with_cookies(url, cookies_str)

def fetch_content_with_cookies(url: str, cookies_str: Optional[str]) -> Optional[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    if cookies_str:
        headers["Cookie"] = cookies_str

    try:
        logger.info(f"🕷️ 正在尝试爬取 URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        content = response.text
        
        # 1. 检测 JavaScript 重定向
        # window.location.replace("...") 或 window.location.href = "..."
        redirect_pattern = r'window\.location\.(?:replace|href)\s*\(?\s*["\']([^"\']+)["\']'
        redirect_match = re.search(redirect_pattern, content)
        if redirect_match:
            new_url = redirect_match.group(1)
            logger.info(f"🔄 检测到 JS 重定向，正在跳转至: {new_url}")
            # 处理相对路径
            if new_url.startswith('/'):
                 # 简单提取域名
                 from urllib.parse import urljoin
                 new_url = urljoin(url, new_url)
            
            # 递归调用 (防止死循环可以加个计数器，这里简单处理)
            return fetch_content_with_cookies(new_url, cookies_str)

        logger.info(f"✅ 爬取成功，获取到 {len(content)} 字符")
        return content
    except Exception as e:
        logger.error(f"❌ 爬取失败: {e}")
        return None
