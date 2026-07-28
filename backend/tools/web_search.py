"""
Web Search Tool - Tavily free-tier wrapper
Owner: Faiza
"""
import os
from tavily import TavilyClient

class WebSearchTool:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not set in .env")
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5) -> list:
        """Run a web search and return list of {title, url, content}."""
        response = self.client.search(query=query, max_results=max_results)
        return response.get("results", [])