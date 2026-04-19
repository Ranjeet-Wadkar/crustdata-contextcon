"""
Investor matching algorithm for the Research-to-Startup AI Agent Swarm.
Scores investors based on project attributes and returns ranked matches.
"""

import json
from typing import List, Dict, Any
from utils.crustdata_client import person_search_crustdata

def load_investors() -> List[Dict[str, Any]]:
    # Instead of loading local file, we will interact dynamically in find_investor_matches
    pass

def calculate_match_score(project_attributes: Dict[str, Any], investor: Dict[str, Any]) -> float:
    """
    Calculate match score between project and investor.
    
    Scoring criteria:
    - +0.4 if focus matches project domain
    - +0.3 if stage fits roadmap
    - +0.2 if geo matches
    - +0.1 if ticket covers funding needs
    """
    score = 0.0
    
    # Focus matching (0.4 points)
    project_domains = project_attributes.get('application_domains', [])
    investor_focus = investor.get('focus', [])
    
    focus_matches = set(project_domains) & set(investor_focus)
    if focus_matches:
        score += 0.4 * (len(focus_matches) / len(investor_focus))
    
    # Stage matching (0.3 points)
    # Stage matching (0.3 points)
    try:
        val = str(project_attributes.get('readiness_level', 0))
        digits = "".join(filter(str.isdigit, val))
        project_stage = int(digits) if digits else 0
    except Exception:
        project_stage = 0
        
    investor_stage = investor.get('stage', '')
    
    # Map TRL levels to funding stages
    if project_stage <= 3 and investor_stage == 'Seed':
        score += 0.3
    elif 4 <= project_stage <= 6 and investor_stage in ['Seed', 'Series A']:
        score += 0.3
    elif project_stage >= 7 and investor_stage in ['Series A', 'Series B']:
        score += 0.3
    
    # Geographic matching (0.2 points)
    project_geo = project_attributes.get('geo', 'Global')
    investor_geo = investor.get('geo', 'Global')
    
    if investor_geo == 'Global' or project_geo == investor_geo:
        score += 0.2
    
    # Ticket size matching (0.1 points)
    project_funding_needs = project_attributes.get('funding_needs', 0)
    investor_ticket = investor.get('ticket_size', '')
    
    if investor_ticket and project_funding_needs > 0:
        # Parse ticket size range
        ticket_range = parse_ticket_size(investor_ticket)
        if ticket_range and ticket_range[0] <= project_funding_needs <= ticket_range[1]:
            score += 0.1
    
    return min(score, 1.0)  # Cap at 1.0

def parse_ticket_size(ticket_str: str) -> tuple:
    """Parse ticket size string to get min/max values."""
    try:
        # Remove $ and k/M suffixes, convert to numbers
        clean_str = ticket_str.replace('$', '').replace('k', '000').replace('M', '000000')
        if '-' in clean_str:
            min_val, max_val = clean_str.split('-')
            return (int(min_val), int(max_val))
        else:
            val = int(clean_str)
            return (val, val)
    except:
        return None

def find_investor_matches(project_attributes: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    """
    Find top investor matches for a project using Crustdata APIs.
    """
    domains = project_attributes.get('application_domains', [])
    domain = domains[0] if domains else "Technology"
    
    # Call Crustdata
    results = person_search_crustdata(title="Partner", domain=domain)
    
    scored_investors = []
    
    profiles = results.get("profiles", [])
    if profiles:
        for profile in profiles:
            basic_profile = profile.get("basic_profile", {})
            name = basic_profile.get("name", "Unknown Investor")
            headline = basic_profile.get("headline", "")
            location = basic_profile.get("location", "Global")
            
            # Simple scoring based on relevance in headline or title
            score = 0.5 
            if domain.lower() in headline.lower():
                score += 0.3
                
            scored_investors.append({
                "name": name,
                "focus": [domain],
                "stage": "Seed/Series A", # Inferred default
                "geo": location,
                "ticket_size": "$500k-$2M",
                "match_score": min(score, 1.0)
            })
    else:
        # Fallback dummy logic if Crustdata API limit/error occurs
        scored_investors = [
            {
                "name": "Jane Venture (Fallback)",
                "focus": [domain],
                "stage": "Seed",
                "geo": "Global",
                "ticket_size": "$1M",
                "match_score": 0.85
            }
        ]
        
    scored_investors.sort(key=lambda x: x['match_score'], reverse=True)
    return scored_investors[:top_n]

def get_team_recommendations(project_attributes: Dict[str, Any]) -> List[str]:
    """
    Suggest optimal team composition based on project attributes.
    
    Args:
        project_attributes: Dictionary containing project information
    
    Returns:
        List of recommended team roles
    """
    base_roles = ["Technical Founder", "Business Strategist"]
    
    # Add domain-specific roles based on application domains
    domains = project_attributes.get('application_domains', [])
    
    if any(domain in ['Healthcare', 'Biotech', 'Pharma'] for domain in domains):
        base_roles.append("Domain Expert (Healthcare)")
    elif any(domain in ['Sustainability', 'CleanTech', 'Energy'] for domain in domains):
        base_roles.append("Domain Expert (Climate)")
    elif any(domain in ['FinTech', 'Blockchain'] for domain in domains):
        base_roles.append("Domain Expert (Finance)")
    elif any(domain in ['EdTech', 'Education'] for domain in domains):
        base_roles.append("Domain Expert (Education)")
    else:
        base_roles.append("Domain Expert")
    
    # Add roles based on technical complexity
    # Add roles based on technical complexity
    try:
        val = str(project_attributes.get('readiness_level', 0))
        digits = "".join(filter(str.isdigit, val))
        readiness_level = int(digits) if digits else 0
    except Exception:
        readiness_level = 0
    if readiness_level <= 3:
        base_roles.append("Research Scientist")
    elif readiness_level <= 6:
        base_roles.append("Product Manager")
    else:
        base_roles.append("Operations Manager")
    
    return base_roles
