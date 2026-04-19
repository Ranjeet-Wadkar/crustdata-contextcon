# Resa - Research-to-Startup AI Agent Swarm (Crustdata Edition)

Transform research papers into investor-ready pitch decks using a sequential multi-agent pipeline powered by Crustdata APIs, Gemini, and a new sleek Neo-Brutalist Next.js UI!

## 🚀 Overview
The system uses a sequential pipeline of specialized agents. We have migrated from Tavily to Crustdata's Data APIs to find the best market context and venture capital investors. 

### Architecture
- **Frontend** (`/resa/frontend`): A modern, PostHog-inspired Neo-Brutalism React UI built on **Next.js**. It polls our FastAPI agent runner.
- **Backend** (`/resa/backend`): A **FastAPI** Python wrapper encapsulating our multi-agent framework. Uses Crustdata Web Search APIs and Person Search APIs to map deep data about competitors and investors.

## 🏃 Getting Started

### 1. Backend Setup
```bash
cd resa/backend
python -m venv venv
# Activate venv: `source venv/bin/activate` or `.\venv\Scripts\activate` on Windows
pip install -r requirements.txt
```
Make sure you have your `.env` configured inside `resa/backend`:
```env
CRUSTDATA_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```
Run the FastAPI backend:
```bash
uvicorn main:app --port 8000
```

### 2. Frontend Setup
```bash
cd resa/frontend
npm install
npm run dev
```
Visit `http://localhost:3000` (or `3001` if port is taken) to use the UI!

## 🤖 Agents
1. **Research Analysis Agent**: Aggregates scientific literature (`sources=["scholar-articles"]`).
2. **Market Intelligence Agent**: Assesses market trends via Crustdata Web APIs.
3. **Feasibility Assessment Agent**: Analyzes the budget constraint scale.
4. **Stakeholder Matching Agent**: Dynamically parses the Crustdata Person API to pinpoint suitable VCs.
5. **Business Plan Agent**: Wraps insight into a pitch deck with NotebookLM integration!