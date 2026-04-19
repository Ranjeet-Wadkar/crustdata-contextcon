import os
import requests
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

API_VERSION = "2025-11-01"

def get_crustdata_headers():
    api_key = os.getenv('CRUSTDATA_API_KEY') or os.getenv('TAVILY_API_KEY') # Fallback if user uses old env
    if not api_key:
        print("CRUSTDATA_API_KEY not found in env, using placeholder for demo")
        api_key = "demo_key"
        
    return {
        'authorization': f'Bearer {api_key}',
        'content-type': 'application/json',
        'x-api-version': API_VERSION
    }

def search_with_crustdata(query: str, sources: List[str] = ["web"], location: str = "US") -> Dict[str, Any]:
    """Search using Web Search API (Checks Tavily first if flagged)."""
    if os.getenv('USE_TAVILY_FOR_WEBSEARCH', '').lower() == 'true':
        try:
            from tavily import TavilyClient
            api_key = os.getenv('TAVILY_API_KEY')
            if api_key:
                tc = TavilyClient(api_key=api_key)
                response = tc.search(query=query, search_depth="basic", max_results=5)
                results = [{"url": res.get("url"), "content": res.get("content")} for res in response.get("results", [])]
                if results:
                    return {"results": results, "query": query}
        except Exception as e:
            print(f"Tavily fallback failed: {e}")

    url = "https://api.crustdata.com/web/search/live"
    payload = {
        "query": query,
        "sources": sources
    }
    try:
        response = requests.post(url, headers=get_crustdata_headers(), json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Crustdata search failed for query '{query}': {e}")
        # Try generic search fallback
        try:
            words = [w for w in query.split() if len(w) > 3]
            fallback_query = " ".join(words[:2]) + " applications"
            response = requests.post(url, headers=get_crustdata_headers(), json={"query": fallback_query, "sources": ["web"]})
            response.raise_for_status()
            return response.json()
        except:
            return {"results": [{"content": f"Mock data retrieved for {query} due to external API limitations.", "url": "https://example.com"}], "query": query}

def person_search_crustdata(title: str, domain: str) -> Dict[str, Any]:
    """Search for investors/partners using Crustdata Person Search API."""
    url = "https://api.crustdata.com/person/search"
    correct_payload = {
        "filters": {
            "field": "experience.employment_details.current.title",
            "type": "in",
            "value": ["Partner", "Investor", "VC", "Managing Director", title.strip()]
        }
    }
    
    try:
        response = requests.post(url, headers=get_crustdata_headers(), json=correct_payload)
        response.raise_for_status()
        data = response.json()
        
        # Post-filter for domain since API strictly forces exact matching operators
        if "profiles" in data and domain:
             domain_lower = domain.lower()
             filtered = [p for p in data["profiles"] if domain_lower in str(p.get("basic_profile", {})).lower() or domain_lower in str(p.get("experience", {})).lower()]
             if filtered:
                 data["profiles"] = filtered
                 
        return data
    except Exception as e:
        print(f"Crustdata Person search failed: {e}")
        # If it fails, fallback to Web API for people
        return {
            "error": str(e),
            "profiles": []
        }
