import requests
import logging
import re
import json
import html as html_lib
from difflib import SequenceMatcher
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urljoin
from backend.ai_handler import extract_todos_from_text

logger = logging.getLogger("URLCrawler")

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
                "priority": "medium",
                "due_date": ""
            })
            continue
        assignee = t.get("assignee") or "Sender（发送者）"
        assignee = name_map.get(assignee, normalize_name(assignee)) or "Sender（发送者）"
        personal.append({
            "title": t.get("title") or "会议待办",
            "description": t.get("description") or t.get("title") or "",
            "assignee": assignee,
            "priority": t.get("priority") or "medium",
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
                "priority": "medium",
                "due_date": ""
            })
    return personal

def parse_meeting_page(html: str) -> Dict[str, Any]:
    candidate_texts = [html]
    candidate_texts.extend([p for p in extract_next_payloads(html) if p])
    next_data = extract_next_data_json(html)
    if next_data:
        candidate_texts.append(next_data)

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

def crawl_and_parse_meeting(url: str, cookies_str: Optional[str] = None) -> Optional[Dict[str, Any]]:
    html = fetch_content_with_cookies(url, cookies_str)
    if not html:
        return None
    parsed = parse_meeting_page(html)
    
    # 只要 summary 或 todos 为空，就尝试 fallback，但不要覆盖已有的值
    if not parsed.get("summary") or not parsed.get("todos"):
        fallback = parse_meeting_html(html)
        if fallback.get("minutes_text") and not parsed.get("summary"):
            parsed["summary"] = fallback.get("minutes_text", "")
        if fallback.get("title") and (not parsed.get("title") or parsed.get("title") == "会议纪要"):
            parsed["title"] = fallback.get("title")
            
    return parsed

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
