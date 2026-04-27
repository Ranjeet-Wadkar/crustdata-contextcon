from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
import os
from contextlib import asynccontextmanager

from agents.research_agent import run_research_agent
from agents.market_agent import run_market_agent
from agents.feasibility_agent import run_feasibility_agent
from agents.stakeholder_agent import run_stakeholder_agent
from agents.business_plan_agent import run_business_plan_agent
from utils.llm_client import initialize_llm
from utils.deck_generator import create_pitch_deck, generate_deck_summary
from utils.notebooklm_integration import create_notebooklm_deck
from utils.parser import extract_text_from_pdf, clean_text
from fastapi.responses import FileResponse
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize LLM upon startup
    try:
        initialize_llm()
    except Exception as e:
        print("Failed to init LLM:", e)
    yield

app = FastAPI(title="ContextCon Resa Pipeline", lifespan=lifespan)

# Allow CORS so Next.js frontend can call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchInput(BaseModel):
    text: str

class WorkflowState(BaseModel):
    research_text: str = ""
    agent_outputs: Dict[str, Any] = {}
    logs: List[Dict[str, Any]] = []

state = WorkflowState()

def add_log(agent: str, log_type: str, content: str):
    state.logs.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "agent": agent,
        "type": log_type,
        "content": content
    })

@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)):
    try:
        text = extract_text_from_pdf(file.file)
        text = clean_text(text)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/run/research")
def api_run_research(input_data: ResearchInput):
    state.research_text = input_data.text
    add_log("Research Agent", "call", f"Analyzing research text: {input_data.text[:100]}...")
    result = run_research_agent(input_data.text)
    state.agent_outputs["agent_0"] = result
    add_log("Research Agent", "response", str(result))
    return result

@app.post("/api/run/market")
def api_run_market(override: Optional[Dict[str, Any]] = None):
    if "agent_0" not in state.agent_outputs:
        raise HTTPException(status_code=400, detail="Run research agent first.")
        
    # Handle Overrides
    if override and "topics" in override:
        state.agent_outputs["agent_0"]["output"]["topics"] = override["topics"]
    if override and "product_recommendations" in override:
        state.agent_outputs["agent_0"]["output"]["product_recommendations"] = override["product_recommendations"]
        
    research_data = state.agent_outputs["agent_0"]["output"]
    add_log("Market Agent", "call", f"Analyzing market for innovations: {research_data.get('innovations', [])}")
    result = run_market_agent(research_data)
    state.agent_outputs["agent_1"] = result
    add_log("Market Agent", "response", str(result))
    return result

@app.post("/api/run/feasibility")
def api_run_feasibility():
    if "agent_1" not in state.agent_outputs:
        raise HTTPException(status_code=400, detail="Run market agent first.")
    research_data = state.agent_outputs["agent_0"]["output"]
    market_data = state.agent_outputs["agent_1"]["output"]
    add_log("Feasibility Agent", "call", f"Assessing feasibility for application domain: {research_data.get('application_domains', [])}")
    result = run_feasibility_agent(research_data, market_data)
    state.agent_outputs["agent_2"] = result
    add_log("Feasibility Agent", "response", str(result))
    return result

@app.post("/api/run/stakeholder")
def api_run_stakeholder(override: Optional[Dict[str, Any]] = None):
    if "agent_2" not in state.agent_outputs:
        raise HTTPException(status_code=400, detail="Run feasibility agent first.")
        
    # Handle Overrides
    if override:
        if "resources" not in state.agent_outputs["agent_2"]["output"]:
            state.agent_outputs["agent_2"]["output"]["resources"] = {}
        if "time" in override:
             state.agent_outputs["agent_2"]["output"]["resources"]["time"] = override["time"]
        if "team_size" in override:
             state.agent_outputs["agent_2"]["output"]["resources"]["team_size"] = override["team_size"]
        if "budget" in override:
             state.agent_outputs["agent_2"]["output"]["resources"]["budget"] = override["budget"]
        if "roadmap" in override:
             state.agent_outputs["agent_2"]["output"]["roadmap"] = override["roadmap"]
             
    research_data = state.agent_outputs["agent_0"]["output"]
    market_data = state.agent_outputs["agent_1"]["output"]
    feasibility_data = state.agent_outputs["agent_2"]["output"]
    add_log("Stakeholder Agent", "call", f"Matching stakeholders for domains: {research_data.get('application_domains', [])}")
    result = run_stakeholder_agent(research_data, market_data, feasibility_data)
    state.agent_outputs["agent_3"] = result
    add_log("Stakeholder Agent", "response", str(result))
    return result

@app.post("/api/run/business_plan")
def api_run_business_plan():
    if "agent_3" not in state.agent_outputs:
        raise HTTPException(status_code=400, detail="Run stakeholder agent first.")
    research_data = state.agent_outputs["agent_0"]["output"]
    market_data = state.agent_outputs["agent_1"]["output"]
    feasibility_data = state.agent_outputs["agent_2"]["output"]
    stakeholder_data = state.agent_outputs["agent_3"]["output"]
    add_log("Business Plan Agent", "call", "Generating comprehensive business plan and pitch deck")
    result = run_business_plan_agent(research_data, market_data, feasibility_data, stakeholder_data)
    state.agent_outputs["agent_4"] = result
    add_log("Business Plan Agent", "response", str(result))
    return result

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "ContextCon Resa Pipeline"}

@app.get("/api/state")
def get_state():
    return state.model_dump()

@app.get("/api/logs")
def get_logs():
    return {"logs": state.logs}

@app.post("/api/export/pdf")
def api_export_pdf():
    if "agent_4" not in state.agent_outputs:
        raise HTTPException(status_code=400, detail="Analysis incomplete. Run all agents first.")
    
    # Extract agent outputs properly shaped for deck generation
    all_outputs = {
        'research_agent': state.agent_outputs["agent_0"]["output"],
        'market_agent': state.agent_outputs["agent_1"]["output"],
        'feasibility_agent': state.agent_outputs["agent_2"]["output"],
        'stakeholder_agent': state.agent_outputs["agent_3"]["output"],
        'business_plan_agent': state.agent_outputs["agent_4"]["output"]
    }
    
    html_path = create_pitch_deck(all_outputs)
    return FileResponse(html_path, media_type='text/html', filename='pitch_deck.html')

@app.post("/api/export/notebooklm")
def api_export_notebooklm():
    if "agent_4" not in state.agent_outputs:
        raise HTTPException(status_code=400, detail="Analysis incomplete. Run all agents first.")
    
    all_outputs = {
        'research_agent': state.agent_outputs["agent_0"]["output"],
        'market_agent': state.agent_outputs["agent_1"]["output"],
        'feasibility_agent': state.agent_outputs["agent_2"]["output"],
        'stakeholder_agent': state.agent_outputs["agent_3"]["output"],
        'business_plan_agent': state.agent_outputs["agent_4"]["output"]
    }
    
    deck_summary = generate_deck_summary(all_outputs)
    
    # Using dummy callback since terminal doesn't need to be updated live
    def dummy_callback(msg):
        add_log("NotebookLM Generator", "info", msg)
        
    try:
        pptx_path = create_notebooklm_deck(deck_summary, status_callback=dummy_callback)
        return FileResponse(pptx_path, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', filename='premium_deck.pptx')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NotebookLM Generation Error: {str(e)}")

@app.post("/api/reset")
def reset_state():
    state.research_text = ""
    state.agent_outputs = {}
    state.logs = []
    return {"status": "reset"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
