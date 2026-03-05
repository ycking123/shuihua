from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..services.search_service import SearchService
from ..services.llm_factory import LLMFactory
from ..database import get_db
from ..models import StrategyDaily
from sqlalchemy.orm import Session
from datetime import datetime, date
import re
import asyncio
import concurrent.futures
import uuid

router = APIRouter()
search_service = SearchService()

def process_single_query(query_config: dict) -> dict:
    """Synchronous function to process a single query: search and summarize."""
    q = query_config["query"]
    meta = query_config["meta"]
    fallback = query_config.get("fallback")
    
    try:
        print(f"Executing dashboard search: {q}")
        search_res = search_service.search(q)
        
        # If no results and fallback exists, try fallback
        if (not search_res or "results" not in search_res or len(search_res["results"]) == 0) and fallback:
            print(f"Primary query '{q}' returned no results. Trying fallback: '{fallback}'")
            q = fallback # Update q to fallback for display purposes (or keep original title?)
            # Let's use the fallback result but maybe keep the original category intent
            search_res = search_service.search(fallback)

        if search_res and "results" in search_res and len(search_res["results"]) > 0:
            # Use all results (up to 10)
            all_results = search_res["results"]
            top_res = all_results[0]
            
            # Prepare content for summarization (combine snippets/summaries of top 5 to save tokens)
            combined_content = ""
            for i, res in enumerate(all_results[:5]):
                combined_content += f"[{i+1}] {res.get('title', '')}: {res.get('content', '')}\n"
            
            print(f"Summarizing content for {q}...")
            
            try:
                truncated_content = combined_content[:15000]
                
                provider = LLMFactory.get_provider("MiniMaxAI/MiniMax-M2.1")
                messages = [
                    {"role": "user", "content": f"请针对搜索关键词“{q}”，根据以下搜索结果进行简要总结，提取核心重点（如政策要点、具体动态等），去除无关信息。要求总结精炼，长度控制在100字以内。\n\n搜索结果：\n{truncated_content}"}
                ]
                
                summary = ""
                for chunk in provider.chat_stream("MiniMaxAI/MiniMax-M2.1", messages):
                    summary += chunk
                
                if not summary:
                    summary = "无法生成总结。"

                summary = re.sub(r'<think>.*?</think>', '', summary, flags=re.DOTALL).strip()
            except Exception as e:
                print(f"Summarization failed for {q}: {e}")
                summary = top_res.get("content", "")[:200] + "..."

            # Construct the final content string as requested:
            # Line 1: LLM Summary
            # Line 2: Original URL (of the top result)
            # Line 3+: List of 10 items
            
            final_content = f"**核心摘要**: {summary}\n\n"
            final_content += f"**主要来源**: [{top_res.get('url', '#')}]({top_res.get('url', '#')})\n\n"
            final_content += "**相关资讯**:\n"
            
            for i, res in enumerate(all_results):
                title = res.get('title', '无标题')
                url = res.get('url', '#')
                final_content += f"- [{title}]({url})\n"
            
            return {
                "query": q,
                "title": q,  # Title is now the keyword
                "content": final_content,
                "url": top_res.get("url", "#"),
                "subtext": meta.get("subtext", "最新动态"),
                "color": meta.get("color", "blue"),
                "icon_type": meta.get("icon_type", "file")
            }
        else:
            # Return None to indicate failure, so we can filter it out
            return None
            
    except Exception as e:
        print(f"Error searching for {q}: {e}")
        return None

@router.post("/api/dashboard/refresh-strategy")
async def refresh_strategy(db: Session = Depends(get_db)):
    today_str = date.today().strftime("%Y-%m-%d")
    
    # Check DB cache first
    cached_records = db.query(StrategyDaily).filter(StrategyDaily.report_date == today_str).all()
    
    # Define queries with metadata and fallbacks
    query_configs = [
        {
            "query": "2024年建材家居以旧换新政策",
            "fallback": "2024年房地产利好政策",
            "meta": { "subtext": "政策风向标 (POLICY)", "icon_type": "policy", "color": "blue" }
        },
        {
            "query": "2024年陶瓷卫浴上市公司业绩分析",
            "fallback": "建材行业2024年财务报告",
            "meta": { "subtext": "财务情报 (FINANCE)", "icon_type": "finance", "color": "emerald" }
        },
        {
            "query": "陶瓷行业数字化转型案例",
            "fallback": "制造业数字化转型案例",
            "meta": { "subtext": "技术前沿 (TECH)", "icon_type": "tech", "color": "indigo" }
        },
        {
            "query": "建材行业绿色工厂黑灯工厂",
            "fallback": "智能制造黑灯工厂",
            "meta": { "subtext": "生产革新 (MANUFACTURING)", "icon_type": "factory", "color": "slate" }
        },
        {
            "query": "中国玉文化与现代设计",
            "fallback": "新中式建材设计趋势",
            "meta": { "subtext": "文化/产品 (CULTURE)", "icon_type": "material", "color": "teal" }
        },
        {
            "query": "2025年智能卫浴产品趋势",
            "fallback": "智能家居行业动态",
            "meta": { "subtext": "产品创新 (PRODUCT)", "icon_type": "product", "color": "cyan" }
        },
        {
            "query": "2024年中国建筑陶瓷行业发展报告",
            "fallback": "2024年建材行业市场分析",
            "meta": { "subtext": "行业洞察 (INDUSTRY)", "icon_type": "industry", "color": "orange" }
        }
    ]

    # Map configs by query key for easy access
    config_map = {cfg["query"]: cfg for cfg in query_configs}
    
    # If we have cached records and they match the number of queries (or at least some), return them
    # For stricter consistency, we might want to ensure all queries are present, but for now, if we have data for today, return it.
    if cached_records and len(cached_records) > 0:
        print(f"Returning cached strategy reports for {today_str}")
        results = []
        for record in cached_records:
            # Reconstruct result object
            # Find meta from config_map if possible, otherwise use stored values
            # Note: The stored record has subtext/color/icon_type, so we can use those directly.
            results.append({
                "query": record.query_key,
                "title": record.title,
                "content": record.content,
                "url": record.url,
                "subtext": record.subtext,
                "color": record.color,
                "icon_type": record.icon_type,
                "date": record.report_date
            })
            
        # Optional: Check if we are missing any queries and fetch them? 
        # For simplicity, if we have cache, we assume it's the daily batch.
        # But if the user added a NEW query to the code, it won't be in cache.
        # Let's simple check: if cache count < query_configs count, maybe we should fetch the missing ones?
        # Let's keep it simple: If cache exists, use it. To force refresh, user might need a different endpoint or parameter (not requested yet).
        
        # Sort results to match query_configs order if important, or just return.
        # Let's try to maintain order based on query_configs
        ordered_results = []
        cache_map = {r["query"]: r for r in results}
        
        for cfg in query_configs:
            q = cfg["query"]
            if q in cache_map:
                ordered_results.append(cache_map[q])
            # Else: missing from cache, ignore or fetch? 
            # If we strictly want to avoid API calls, we ignore.
        
        if len(ordered_results) > 0:
             return {"results": ordered_results}

    # Cache miss or empty: Fetch from API
    print(f"Cache miss for {today_str}, fetching from API...")
    
    loop = asyncio.get_running_loop()
    # Use ThreadPoolExecutor to run synchronous search/LLM tasks in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(query_configs)) as executor:
        # Create a list of futures
        futures = [
            loop.run_in_executor(executor, process_single_query, config)
            for config in query_configs
        ]
        # Wait for all futures to complete
        results = await asyncio.gather(*futures)
    
    # Filter out None results (failed searches)
    valid_results = [r for r in results if r is not None]
    
    # Save to DB
    try:
        for res in valid_results:
            new_record = StrategyDaily(
                id=str(uuid.uuid4()),
                report_date=today_str,
                query_key=res["query"],
                title=res["title"],
                content=res["content"],
                url=res["url"],
                subtext=res["subtext"],
                color=res["color"],
                icon_type=res["icon_type"]
            )
            db.add(new_record)
        db.commit()
        print(f"Saved {len(valid_results)} strategy reports to DB.")
    except Exception as e:
        print(f"Failed to save strategy reports to DB: {e}")
        db.rollback()
    
    return {"results": valid_results}


