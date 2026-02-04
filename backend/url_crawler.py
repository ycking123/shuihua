import requests
import logging
import re
import json
from typing import Optional, Dict, Any
from urllib.parse import urljoin

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

def crawl_and_parse_meeting(url: str, cookies_str: str) -> Optional[Dict[str, Any]]:
    """
    爬取并解析会议内容 (入口函数)
    """
    html = fetch_content_with_cookies(url, cookies_str)
    if not html:
        return None
    
    return parse_meeting_html(html)

def fetch_content_with_cookies(url: str, cookies_str: str) -> Optional[str]:
    """
    使用用户提供的 Cookie 爬取页面内容
    """
    if not cookies_str:
        logger.warning("⚠️ 未提供 Cookie，无法爬取受保护的会议页面")
        return None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": cookies_str
    }

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
