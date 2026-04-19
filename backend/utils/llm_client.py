"""
LLM client for the Research-to-Startup AI Agent Swarm.
Handles all interactions with Gemini and OpenAI APIs, with fallback routing and comprehensive logging.
"""

import google.generativeai as genai
import openai
import json
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Any, List
from datetime import datetime

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to track if we're in demo mode
DEMO_MODE = False

# Global state for clients
GENAI_INITIALIZED = False
OPENAI_INITIALIZED = False

def initialize_llm():
    """Initialize LLM clients with API keys."""
    global DEMO_MODE, GENAI_INITIALIZED, OPENAI_INITIALIZED
    
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    default_llm = os.getenv('DEFAULT_LLM', 'gemini').lower()
    
    GENAI_INITIALIZED = False
    OPENAI_INITIALIZED = False
    
    if gemini_api_key and gemini_api_key != 'demo-key-placeholder':
        try:
            genai.configure(api_key=gemini_api_key)
            # Test model initialization
            genai.GenerativeModel('models/gemini-2.5-flash-lite')
            logger.info("✅ Gemini API initialized successfully")
            GENAI_INITIALIZED = True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini: {str(e)}")

    if openai_api_key and openai_api_key != 'your_openai_api_key_here':
        try:
            openai.api_key = openai_api_key
            logger.info("✅ OpenAI API initialized successfully")
            OPENAI_INITIALIZED = True
        except Exception as e:
            logger.error(f"❌ Failed to initialize OpenAI: {str(e)}")
            
    if not GENAI_INITIALIZED and not OPENAI_INITIALIZED:
        DEMO_MODE = True
        logger.warning("⚠️ Using demo mode. Set GEMINI_API_KEY or OPENAI_API_KEY in .env for real AI access.")
        return None
        
    DEMO_MODE = False
    
    # Return info about what was initialized
    return {
        "gemini": GENAI_INITIALIZED,
        "openai": OPENAI_INITIALIZED,
        "default": default_llm
    }

def call_gemini_api(prompt: str, model_name: str = 'gemini-2.5-flash-lite') -> str:
    """Call Gemini API."""
    if not GENAI_INITIALIZED:
        raise Exception("Gemini not initialized")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    if response.text:
        return response.text
    raise Exception("Empty response from Gemini")

def call_openai_api(prompt: str, model_name: str = 'gpt-4o-mini') -> str:
    """Call OpenAI API."""
    if not OPENAI_INITIALIZED:
        raise Exception("OpenAI not initialized")
    response = openai.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}]
    )
    if response.choices and response.choices[0].message.content:
        return response.choices[0].message.content
    raise Exception("Empty response from OpenAI")

def call_llm(prompt: str) -> str:
    """
    Call LLM API with fallback mechanism.
    """
    global DEMO_MODE
    
    logger.info(f"📝 Prompt: {prompt[:200]}...")
    
    if DEMO_MODE:
        logger.warning("⚠️ DEMO MODE - Returning mock response")
        return generate_mock_response(prompt)
        
    default_llm = os.getenv('DEFAULT_LLM', 'gemini').lower()
    
    # Prioritized selection based on default_llm and initialized state
    primary = None
    secondary = None
    
    if default_llm == "openai":
        if OPENAI_INITIALIZED: primary = ("openai", call_openai_api)
        if GENAI_INITIALIZED: secondary = ("gemini", call_gemini_api)
    else:
        if GENAI_INITIALIZED: primary = ("gemini", call_gemini_api)
        if OPENAI_INITIALIZED: secondary = ("openai", call_openai_api)
        
    if not primary and secondary:
        primary = secondary
        secondary = None
        
    if not primary:
        logger.warning("⚠️ No LLM initialized - Returning mock response")
        return generate_mock_response(prompt)

    # Try Primary
    provider_name, call_func = primary
    logger.info(f"🤖 Calling {provider_name.upper()} API as Primary")
    try:
        response = call_func(prompt)
        logger.info(f"✅ {provider_name.upper()} API Response received")
        return response
    except Exception as e:
        logger.error(f"❌ {provider_name.upper()} API Error: {str(e)}")
        
        # Try Secondary
        if secondary:
            sec_provider_name, sec_call_func = secondary
            logger.info(f"🔄 Falling back to {sec_provider_name.upper()} API")
            try:
                response = sec_call_func(prompt)
                logger.info(f"✅ {sec_provider_name.upper()} API Response received on fallback")
                return response
            except Exception as e2:
                logger.error(f"❌ {sec_provider_name.upper()} API Error (Fallback): {str(e2)}")
                
    logger.warning("⚠️ All LLMs failed - Falling back to mock response")
    return generate_mock_response(prompt)


def generate_mock_response(prompt: str) -> str:
    """Generate intelligent mock responses based on prompt content."""
    prompt_lower = prompt.lower()
    
    if "innovations" in prompt_lower and "research" in prompt_lower:
        return json.dumps({
            "innovations": [
                "Novel machine learning algorithm for pattern recognition",
                "Advanced materials with enhanced properties", 
                "Innovative computational approach to optimization"
            ],
            "readiness_level": 6,
            "application_domains": ["AI/ML", "Healthcare", "Manufacturing"],
            "technical_summary": "Breakthrough research with strong commercial potential"
        })
    elif "market" in prompt_lower and "tam" in prompt_lower:
        return json.dumps({
            "TAM": "$500B",
            "SAM": "$50B",
            "SOM": "$5B", 
            "trends": [
                "Rapid digital transformation across industries",
                "Increased focus on AI-powered solutions",
                "Growing demand for automation"
            ],
            "competitors": ["Google", "Microsoft", "Amazon", "IBM", "OpenAI"]
        })
    elif "feasibility" in prompt_lower and "roadmap" in prompt_lower:
        return json.dumps({
            "roadmap": [
                "Complete technical validation",
                "Develop MVP prototype", 
                "Conduct market validation",
                "Refine product based on feedback",
                "Scale manufacturing",
                "Launch commercial product"
            ],
            "resources": {
                "time": "18 months",
                "team_size": "8 people", 
                "budget": "$1.5M"
            },
            "risks": [
                "Technical complexity challenges",
                "Market competition",
                "Regulatory requirements",
                "Funding constraints",
                "Talent acquisition"
            ],
            "feasibility_score": 7
        })
    elif "business plan" in prompt_lower and "slides" in prompt_lower:
        return json.dumps({
            "slides": [
                {
                    "title": "Problem & Opportunity",
                    "content": "Addressing critical challenges in target market with innovative solutions."
                },
                {
                    "title": "Core Innovation",
                    "content": "Breakthrough technology with clear competitive advantages."
                },
                {
                    "title": "Market Landscape", 
                    "content": "Large addressable market with strong growth potential."
                },
                {
                    "title": "Competitive Advantage",
                    "content": "Unique positioning with sustainable competitive moats."
                },
                {
                    "title": "Feasibility & Roadmap",
                    "content": "Clear development path with realistic resource requirements."
                },
                {
                    "title": "Business Potential",
                    "content": "Strong revenue potential with clear monetization strategy."
                },
                {
                    "title": "Next Steps & Investor Recommendations",
                    "content": "Ready for funding with identified investor matches."
                }
            ]
        })
    elif "topics" in prompt_lower and "research" in prompt_lower:
        return json.dumps({
            "topics": ["Artificial Intelligence", "Neural Networks", "Deep Learning"]
        })
    elif "product" in prompt_lower and "analogous" in prompt_lower:
        return json.dumps({
            "product_recommendations": [
                {
                    "product_name": "Titanium Smartphone Casing",
                    "description": "Using high-strength, lightweight materials for premium consumer electronics, similar to how recent aerospace papers describe novel titanium alloys.",
                    "relevance": "High"
                }
            ]
        })
    else:
        return f"Mock LLM response for: {prompt[:100]}..."


def analyze_research_with_llm(text: str) -> Dict[str, Any]:
    prompt = f"""
    Analyze this research paper and extract the following information in JSON format:
    
    {text[:2000]}...
    
    Please provide:
    1. Key innovations (list of 3-5 main innovations)
    2. Technology readiness level (TRL 1-9)
    3. Application domains (list of relevant industries/domains)
    4. Technical summary (brief description of the technology)
    
    Return as JSON with keys: innovations, readiness_level, application_domains, technical_summary
    """
    
    response = call_llm(prompt)
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        result = json.loads(json_str)
        return result
    except:
        return {
            "innovations": [
                "Novel machine learning algorithm for pattern recognition",
                "Advanced materials with enhanced properties",
                "Innovative computational approach to optimization"
            ],
            "readiness_level": 5,
            "application_domains": ["AI/ML", "Healthcare", "Manufacturing"],
            "technical_summary": "Breakthrough research with strong commercial potential"
        }

def extract_research_topics_with_llm(text: str) -> List[str]:
    prompt = f"""
    Analyze this research paper excerpt and extract 2-3 specific technical topics or keywords that would be perfect for searching the internet to find similar research papers.
    
    Excerpt: {text[:2000]}...
    
    Return as JSON with a key "topics" containing a list of strings!
    """
    response = call_llm(prompt)
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        result = json.loads(json_str)
        return result.get("topics", [])
    except:
        return ["Advanced Materials", "Technology Innovations"]

def analyze_product_links_with_llm(original_text: str, similar_papers: List[Dict]) -> Dict[str, Any]:
    papers_summary = ""
    for idx, paper in enumerate(similar_papers[:3]):
        papers_summary += f"{idx+1}. {paper.get('title', 'Unknown')} - {paper.get('content', '')}\n"

    prompt = f"""
    You are an expert product strategist. I will provide you with a newly uploaded research paper and a list of existing similar research papers found online.
    Your goal is to cross-reference these to identify a tangible, commercially existing product use-case.
    For example, if the research is about 'novel titanium alloys' and similar papers mention aerospace applications, you could draw parallels to a 'Titanium Smartphone Casing' (like the iPhone 15 Pro). 
    
    ORIGINAL RESEARCH:
    {original_text[:2000]}...

    SIMILAR PAPERS FOUND ONLINE:
    {papers_summary}
    
    Return a JSON containing an array of 2 'product_recommendations'. 
    Each object should have: 'product_name', 'description' (explaining the analogous link), and 'relevance' (High/Medium).
    Return format strictly as JSON, e.g. {{"product_recommendations": [...]}}
    """
    response = call_llm(prompt)
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        result = json.loads(json_str)
        return result
    except:
        return {
            "product_recommendations": [
                {
                    "product_name": "Titanium Smartphone Casing",
                    "description": "Using high-strength materials for premium consumer electronics, derived from aerospace advancements.",
                    "relevance": "High"
                }
            ]
        }

def analyze_market_with_llm(innovations: List[str], domains: List[str]) -> Dict[str, Any]:
    prompt = f"""
    Analyze the market potential for these innovations: {', '.join(innovations)}
    in these domains: {', '.join(domains)}
    
    Provide market analysis in JSON format with:
    1. Total Addressable Market (TAM) - estimated market size
    2. Serviceable Addressable Market (SAM) - realistic target market
    3. Serviceable Obtainable Market (SOM) - achievable market share
    4. Key market trends (list of 3-5 trends)
    5. Major competitors (list of 3-5 competitors)
    
    Return as JSON with keys: TAM, SAM, SOM, trends, competitors
    """
    
    response = call_llm(prompt)
    
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        return {
            "TAM": "$500B",
            "SAM": "$50B", 
            "SOM": "$5B",
            "trends": [
                "Rapid digital transformation across industries",
                "Increased focus on AI-powered solutions",
                "Growing demand for automation"
            ],
            "competitors": ["Google", "Microsoft", "Amazon", "IBM", "OpenAI"]
        }

def assess_feasibility_with_llm(research_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
    Assess the commercial feasibility for this technology:
    
    Innovations: {research_data.get('innovations', [])}
    TRL Level: {research_data.get('readiness_level', 0)}
    Domains: {research_data.get('application_domains', [])}
    Market Size: {market_data.get('TAM', 'N/A')}
    
    Provide feasibility analysis in JSON format with:
    1. Development roadmap (list of 5-7 key milestones)
    2. Resource requirements (time, team size, budget)
    3. Key risks (list of 5-7 risks)
    4. Feasibility score (1-10)
    
    Return as JSON with keys: roadmap, resources, risks, feasibility_score
    """
    
    response = call_llm(prompt)
    
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        return {
            "roadmap": [
                "Complete technical validation",
                "Develop MVP prototype",
                "Conduct market validation",
                "Refine product based on feedback",
                "Scale manufacturing",
                "Launch commercial product"
            ],
            "resources": {
                "time": "18 months",
                "team_size": "8 people",
                "budget": "$1.5M"
            },
            "risks": [
                "Technical complexity challenges",
                "Market competition",
                "Regulatory requirements",
                "Funding constraints",
                "Talent acquisition"
            ],
            "feasibility_score": 7
        }

def generate_business_plan_with_llm(all_agent_outputs: Dict[str, Any]) -> Dict[str, Any]:
    prompt = f"""
    Generate a comprehensive business plan and pitch deck based on this analysis:
    
    Research: {all_agent_outputs.get('research_agent', {})}
    Market: {all_agent_outputs.get('market_agent', {})}
    Feasibility: {all_agent_outputs.get('feasibility_agent', {})}
    Stakeholders: {all_agent_outputs.get('stakeholder_agent', {})}
    
    Create a pitch deck with 7 slides in JSON format:
    1. Problem & Opportunity
    2. Core Innovation
    3. Market Landscape
    4. Competitive Advantage
    5. Feasibility & Roadmap
    6. Business Potential
    7. Next Steps & Investor Recommendations
    
    Return as JSON with key "slides" containing array of slide objects with "title" and "content" fields.
    """
    
    response = call_llm(prompt)
    
    try:
        if "```json" in response:
            json_start = response.find("```json") + 7
            json_end = response.find("```", json_start)
            json_str = response[json_start:json_end].strip()
        else:
            json_str = response
        
        result = json.loads(json_str)
        return result
    except:
        return {
            "slides": [
                {
                    "title": "Problem & Opportunity",
                    "content": "Addressing critical challenges in target market with innovative solutions."
                },
                {
                    "title": "Core Innovation", 
                    "content": "Breakthrough technology with clear competitive advantages."
                },
                {
                    "title": "Market Landscape",
                    "content": "Large addressable market with strong growth potential."
                },
                {
                    "title": "Competitive Advantage",
                    "content": "Unique positioning with sustainable competitive moats."
                },
                {
                    "title": "Feasibility & Roadmap",
                    "content": "Clear development path with realistic resource requirements."
                },
                {
                    "title": "Business Potential",
                    "content": "Strong revenue potential with clear monetization strategy."
                },
                {
                    "title": "Next Steps & Investor Recommendations",
                    "content": "Ready for funding with identified investor matches."
                }
            ]
        }
