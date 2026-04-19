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
    """Search using Crustdata Web Search API."""
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
    payload = {
        "filters": [
            {
                "filter_type": "CURRENT_TITLE",
                "type": "in",
                "value": [title]
            },
            {
                 "filter_type": "CURRENT_COMPANY",
                 "type": "in",
                 "value": [domain]
            }
        ],
        "page": 1
    }
    
    # We will try a different approach if specific filtering fails, 
    # we can use Web APIs to search for LinkedIn profiles instead as an alternative if needed.
    # We are following the format from person.md: { "field": "dotpath", "type": "op", "value": ... }
    correct_payload = {
        "filters": [
            {
                "field": "experience.employment_details.current.title",
                "type": "in",
                "value": ["Partner", "Investor", "VC", "Managing Director"]
            },
            {
                 "field": "basic_profile.headline",
                 "type": "contains",
                 "value": domain
            }
        ],
        "page": 1
    }
    
    try:
        response = requests.post(url, headers=get_crustdata_headers(), json=correct_payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Crustdata Person search failed: {e}")
        # If it fails, fallback to Web API for people
        return {
            "error": str(e),
            "profiles": []
        }
