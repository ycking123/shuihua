import requests
import json
import os

class SearchService:
    def __init__(self):
        # Bocha API Key provided by user (from test_bocha_fastapi.py)
        self.api_key = "sk-b324513f33f84c90adc017d5dbe55858"
        self.api_url = "https://api.bocha.cn/v1/web-search"

    def search(self, query: str):
        """
        Executes a search query using Bocha API.
        Returns the search results in a format compatible with the previous Tavily implementation.
        """
        try:
            print(f"Searching for: {query}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "query": query,
                "summary": True,
                "freshness": "noLimit",
                "count": 10
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                print(f"Bocha Search Error: {response.status_code} - {response.text}")
                return {"error": f"API Error: {response.status_code}", "results": []}
                
            resp_json = response.json()
            
            # Bocha response structure: {"code": 200, "data": {"webPages": {"value": [...]}}}
            data = resp_json.get("data", {})
            
            results = []
            if "webPages" in data and "value" in data["webPages"]:
                for item in data["webPages"]["value"]:
                    content = item.get("summary") or item.get("snippet") or ""
                    results.append({
                        "title": item.get("name"),
                        "url": item.get("url"),
                        "content": content
                    })
            
            return {"results": results}
            
        except Exception as e:
            print(f"Bocha Search Exception: {e}")
            return {"error": str(e), "results": []}

    def get_search_context(self, query: str) -> str:
        """
        Helper to get a string context from search results.
        """
        search_res = self.search(query)
        if not search_res or "results" not in search_res:
            return ""
        
        context = "Search Results:\n"
        for res in search_res.get("results", []):
            context += f"- Title: {res.get('title')}\n  Content: {res.get('content')}\n  URL: {res.get('url')}\n\n"
        
        return context

    def get_cleaned_search_content(self, query: str) -> str:
        """
        Executes search and returns only the content of the results, cleaned.
        """
        search_res = self.search(query)
        if not search_res or "results" not in search_res:
            return ""
        
        # Extract only the content (body) from each result
        contents = [res.get('content', '') for res in search_res.get("results", [])]
        
        # Join them with newlines
        return "\n\n".join(filter(None, contents))

