from tavily import TavilyClient
import os

class SearchService:
    def __init__(self):
        # Prefer env var, fallback to hardcoded (from user's test file) if needed, 
        # but better to rely on env.
        # User's test file had: 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
        # We saw it in .env.local as LOCAL_TAVILY_KEY
        api_key = os.getenv("LOCAL_TAVILY_KEY")
        if not api_key:
             print("Warning: LOCAL_TAVILY_KEY not found in environment variables.")
        
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str):
        """
        Executes a search query using Tavily API.
        Returns the search results context.
        """
        try:
            print(f"Searching for: {query}")
            response = self.client.search(query, search_depth="basic")
            # response is typically a dict with 'results' list
            return response
        except Exception as e:
            print(f"Tavily Search Error: {e}")
            return {"error": str(e)}

    def get_search_context(self, query: str) -> str:
        """
        Helper to get a string context from search results.
        """
        results = self.search(query)
        if not results or "results" not in results:
            return ""
        
        context = "Search Results:\n"
        for res in results.get("results", []):
            context += f"- Title: {res.get('title')}\n  Content: {res.get('content')}\n  URL: {res.get('url')}\n\n"
        
        return context

    def get_cleaned_search_content(self, query: str) -> str:
        """
        Executes search and returns only the content of the results, cleaned.
        """
        results = self.search(query)
        if not results or "results" not in results:
            return ""
        
        # Extract only the content (body) from each result
        contents = [res.get('content', '') for res in results.get("results", [])]
        
        # Join them with newlines
        return "\n\n".join(filter(None, contents))
