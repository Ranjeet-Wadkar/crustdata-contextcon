"""
Shared Tavily API Client Utility.
"""

import os
from typing import Dict, Any, List
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def initialize_tavily_client() -> TavilyClient:
    """Initialize Tavily client with API key."""
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables")
    return TavilyClient(api_key=api_key)

def search_with_tavily(query: str, tavily_client: TavilyClient, depth: str = "advanced", limit: int = 5) -> Dict[str, Any]:
    """
    Search using Tavily API with error handling.
    
    Args:
        query: Search query string
        tavily_client: Initialized Tavily client
        depth: "basic" or "advanced"
        limit: max results to return
    
    Returns:
        Dictionary containing search results
    """
    try:
        response = tavily_client.search(
            query=query,
            search_depth=depth,
            max_results=limit
        )
        return response
    except Exception as e:
        print(f"Tavily search failed for query '{query}': {e}")
        # Fallback to a simpler query if advanced fails
        try:
            fallback_query = f"general trends in {query.split()[-1]} industry"
            response = tavily_client.search(
                query=fallback_query,
                search_depth="basic",
                max_results=3
            )
            return response
        except Exception as e:
            print(f"Fallback search also failed: {e}")
            return {"results": [], "query": query}

def extract_sources_from_results(results: List[Dict]) -> List[str]:
    """
    Extract source URLs from Tavily results.
    """
    sources = []
    for result in results:
        if 'url' in result:
            sources.append(result['url'])
    return sources
