"""
Research Analysis Agent for the Research-to-Startup AI Agent Swarm.
Analyzes research papers and extracts key innovations, technical readiness, and applications using Gemini AI.
"""

import json
from typing import Dict, List, Any
from utils.llm_client import (
    analyze_research_with_llm,
    extract_research_topics_with_llm,
    analyze_product_links_with_llm
)
from utils.crustdata_client import search_with_crustdata

def analyze_research_paper(text: str) -> Dict[str, Any]:
    """
    Analyze research paper, perform internet search, and extract product ideas.
    
    Args:
        text: Research paper text content
    
    Returns:
        Dictionary containing comprehensive analysis results
    """
    # 1. Base analysis
    gemini_result = analyze_research_with_llm(text)
    
    # 2. Extract topics for search
    topics = extract_research_topics_with_llm(text)
    
    # 3. Search the internet
    similar_papers = []
    try:
        query = f"recent research papers on {' '.join(topics)} applications"
        search_results = search_with_crustdata(query, sources=["scholar-articles", "web"])
        similar_papers = search_results.get('results', [])
    except Exception as e:
        print(f"Failed to use Crustdata in Researcher Agent: {e}")
        
    # 4. Map to product
    product_ideas = analyze_product_links_with_llm(text, similar_papers)

    return {
        "innovations": gemini_result.get("innovations", []),
        "readiness_level": gemini_result.get("readiness_level", 0),
        "application_domains": gemini_result.get("application_domains", []),
        "technical_summary": gemini_result.get("technical_summary", ""),
        "topics": topics,
        "similar_papers": similar_papers[:3], # Only keep top 3
        "product_recommendations": product_ideas.get("product_recommendations", []),
        "analysis_summary": f"This paper introduces {len(gemini_result.get('innovations', []))} key innovations with TRL {gemini_result.get('readiness_level', 0)}, applicable to {len(gemini_result.get('application_domains', []))} domains."
    }

def get_agent_voice_message(analysis_result: Dict[str, Any]) -> str:
    """Generate human-readable voice message for visualization."""
    innovations = analysis_result.get('innovations', [])
    readiness_level = analysis_result.get('readiness_level', 0)
    domains = analysis_result.get('application_domains', [])
    products = analysis_result.get('product_recommendations', [])
    
    message = f"🔬 Research Analysis Complete!\n\n"
    message += f"This paper introduces {len(innovations)} key innovations with Technology Readiness Level {readiness_level}/9. "
    message += f"The research shows strong potential for applications in {', '.join(domains[:3])} industries. "
    
    if products:
        top_product = products[0].get('product_name', 'Unknown')
        message += f"\n💡 Product Idea: {top_product} -> {products[0].get('description', '')}"
        
    return message

def run_research_agent(text: str) -> Dict[str, Any]:
    """
    Main function to run the research analysis agent.
    """
    analysis_result = analyze_research_paper(text)
    voice_message = get_agent_voice_message(analysis_result)
    
    return {
        "agent_name": "Research Analysis Agent",
        "status": "completed",
        "output": analysis_result,
        "voice_message": voice_message,
        "timestamp": "2024-01-01T10:00:00Z"
    }
