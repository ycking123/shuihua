# `/backend` 模块文档

## 模块职责
后端服务层，负责会议爬虫、AI 处理、业务逻辑。

## 成员清单

| 文件 | 主要函数/类 | 职责 |
|-----|------------|------|
| `url_crawler.py` | `crawl_meeting_url()` | 会议 URL 爬取主逻辑 |
| `ai_handler.py` | `extract_todos_from_text()` | AI 文本分析，提取待办事项 |
| `crawl_with_browser.py` | `crawl_meeting_minutes()` | Playwright 浏览器爬虫（可选依赖） |
| `server_receive.py` | - | 服务接收处理（待补充） |

## 接口说明

### `url_crawler.py`
```python
def crawl_meeting_url(share_url: str, user_cookie: str = None) -> Dict:
    """
    爬取会议 URL，提取会议信息

    Args:
        share_url: 会议分享链接
        user_cookie: 用户认证 Cookie（可选）

    Returns:
        Dict: 会议信息字典
    """
```

### `ai_handler.py`
```python
def extract_todos_from_text(text: str) -> List[Dict]:
    """
    从会议文本中提取待办事项

    Args:
        text: 会议纪要/录音转写文本

    Returns:
        List[Dict]: 待办事项列表
    """
```

### 依赖关系
```python
from backend.ai_handler import extract_todos_from_text
```

### 可选依赖
- Playwright（浏览器爬虫）：`PLAYWRIGHT_AVAILABLE` 标志位控制

---

**最后更新**: 2026-02-25
