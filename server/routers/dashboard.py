from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.search_service import SearchService
from ..services.llm_factory import LLMFactory
import re
import asyncio
import concurrent.futures

router = APIRouter()
search_service = SearchService()

def process_single_query(q: str, meta_info: dict) -> dict:
    """Synchronous function to process a single query: search and summarize."""
    try:
        print(f"Executing dashboard search: {q}")
        search_res = search_service.search(q)
        
        if search_res and "results" in search_res and len(search_res["results"]) > 0:
            # Take the top result for the main display
            top_res = search_res["results"][0] 
            
            # Summarize the content
            original_content = top_res.get("content", "无内容")
            print(f"Summarizing content for {q}...")
            
            # Helper for summarization inside this sync function
            try:
                # Truncate content to avoid token limits or timeouts
                truncated_content = original_content[:15000]
                
                provider = LLMFactory.get_provider("MiniMaxAI/MiniMax-M2.1")
                # Fix: variable names query/content were from outer scope in previous code, need to use args
                messages = [
                    {"role": "user", "content": f"请针对搜索关键词“{q}”，对以下内容进行简要总结，提取核心重点（如政策要点、具体动态等），去除无关信息，保持条理清晰。总结长度控制在300字以内。\n\n原文内容：\n{truncated_content}"}
                ]
                
                summary = ""
                for chunk in provider.chat_stream("MiniMaxAI/MiniMax-M2.1", messages):
                    summary += chunk
                
                if not summary:
                    raise ValueError("Empty summary returned from LLM")

                summary = re.sub(r'<think>.*?</think>', '', summary, flags=re.DOTALL).strip()
                summary_content = summary
            except Exception as e:
                print(f"Summarization failed for {q}: {e}")
                # If summarization fails, still try to be helpful but indicate it's raw
                summary_content = original_content[:500] + "..." if len(original_content) > 500 else original_content

            meta = meta_info.get(q, {})
            
            return {
                "query": q,
                "title": top_res.get("title", "无标题"),
                "content": summary_content,
                "url": top_res.get("url", "#"),
                "subtext": meta.get("subtext", "最新动态"),
                "color": meta.get("color", "blue"),
                "icon_type": meta.get("icon_type", "file")
            }
        else:
            return {
                "query": q,
                "title": "暂无相关数据",
                "content": "未检索到有效信息。",
                "url": "#",
                "subtext": "无数据",
                "color": "slate",
                "icon_type": "alert"
            }
            
    except Exception as e:
        print(f"Error searching for {q}: {e}")
        return {
                "query": q,
                "title": "检索服务异常",
                "content": str(e),
                "url": "#",
                "subtext": "系统错误",
                "color": "red",
                "icon_type": "alert"
        }

@router.post("/api/dashboard/refresh-strategy")
async def refresh_strategy():
    queries = [
        "2024-2025 中国各省旧房改造补贴政策最新汇总",
        "马可波罗、东鹏、恒达、九牧、箭牌财报信息",
        "智能制造",
        "黑灯工厂",
        "中国玉",
        "智能马桶",
        "瓷砖卫浴行业动态"
    ]
    
    # Map queries to UI-friendly subtexts or categories if needed
    meta_info = {
        "2024-2025 中国各省旧房改造补贴政策最新汇总": {
            "subtext": "政策风向标 (POLICY)",
            "icon_type": "policy", 
            "color": "blue"
        },
        "马可波罗、东鹏、恒达、九牧、箭牌财报信息": {
            "subtext": "财务情报 (FINANCE)",
            "icon_type": "finance",
            "color": "emerald"
        },
        "智能制造": {
            "subtext": "技术前沿 (TECH)",
            "icon_type": "tech",
            "color": "indigo"
        },
        "黑灯工厂": {
            "subtext": "生产革新 (MANUFACTURING)",
            "icon_type": "factory",
            "color": "slate"
        },
        "中国玉": {
            "subtext": "文化/产品 (CULTURE)",
            "icon_type": "material",
            "color": "teal"
        },
        "智能马桶": {
            "subtext": "产品创新 (PRODUCT)",
            "icon_type": "product",
            "color": "cyan"
        },
        "瓷砖卫浴行业动态": {
            "subtext": "行业洞察 (INDUSTRY)",
            "icon_type": "industry",
            "color": "orange"
        }
    }

    loop = asyncio.get_running_loop()
    # Use ThreadPoolExecutor to run synchronous search/LLM tasks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(queries)) as executor:
        # Create a list of futures
        futures = [
            loop.run_in_executor(executor, process_single_query, q, meta_info)
            for q in queries
        ]
        # Wait for all futures to complete
        results = await asyncio.gather(*futures)
    
    return {"results": results}

