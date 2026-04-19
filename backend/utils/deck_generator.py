"""
Pitch deck generation utilities for the Research-to-Startup AI Agent Swarm.
"""
from typing import Dict, Any

def create_pitch_deck(agent_outputs: Dict[str, Any], output_path: str = "pitch_deck.html") -> str:
    """Generate an HTML pitch deck styled with Neo-Brutalism, containing 10 structured slides."""
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    feasibility_data = agent_outputs.get('feasibility_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    bp_data = agent_outputs.get('business_plan_agent', {})
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  :root {{ --primary: #f26222; --bg: #fffbf5; --text: #000; --border: #000; }}
  body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }}
  .slide {{ border: 4px solid var(--border); box-shadow: 8px 8px 0px var(--text); background: white; padding: 2rem; margin-bottom: 3rem; border-radius: 8px; page-break-after: always; }}
  h1, h2 {{ font-weight: 900; text-transform: uppercase; color: var(--primary); text-shadow: 2px 2px 0px var(--text); margin-top: 0; }}
  h1 {{ font-size: 3rem; border-bottom: 4px solid var(--border); padding-bottom: 1rem; }}
  h2 {{ font-size: 2rem; margin-bottom: 1.5rem; }}
  ul, ol {{ font-size: 1.2rem; font-weight: bold; line-height: 1.6; margin-left: 1rem; }}
  p {{ font-size: 1.2rem; font-weight: 600; line-height: 1.6; }}
</style>
</head>
<body>
  <div class="slide">
    <h1>Research-to-Startup</h1>
    <p>Transforming Core Technical Research into Viable Commercial Scale Pitch Decks.</p>
  </div>
  
  <div class="slide">
    <h2>1. Executive Summary</h2>
    <p>A high-tech approach targeting: {", ".join(research_data.get('application_domains', [])[:3])}</p>
    <p>We are translating scientific breakthroughs directly into commercially viable products to resolve critical bottlenecks in modern infrastructure.</p>
  </div>

  <div class="slide">
    <h2>2. The Problem</h2>
    <p>Current solutions fail to integrate modern research constraints, leaving a gap for specialized high-TRL methodologies.</p>
    <ul>
      {''.join(f'<li>Trend validating demand: {t}</li>' for t in market_data.get('trends', [])[:3])}
    </ul>
  </div>
  
  <div class="slide">
    <h2>3. The Solution / Core Innovation</h2>
    <ul>
      {''.join(f'<li>{i}</li>' for i in research_data.get('innovations', [])[:3])}
    </ul>
    <p><strong>Competitive Technology Readiness Level (TRL):</strong> {research_data.get('readiness_level', 0)}/9</p>
  </div>
  
  <div class="slide">
    <h2>4. Market Opportunity</h2>
    <p>Total Addressable Market (TAM): {market_data.get('TAM', 'N/A')} <br>
       Serviceable Addressable Market (SAM): {market_data.get('SAM', 'N/A')} <br>
       Serviceable Obtainable Market (SOM): {market_data.get('SOM', 'N/A')}</p>
  </div>
  
  <div class="slide">
    <h2>5. Business Model</h2>
    <p>Our revenue generation strategies rely on direct IP integration, software pipelines, and enterprise B2B licensing across our target domains.</p>
  </div>
  
  <div class="slide">
    <h2>6. Go-To-Market Strategy</h2>
    <p>Our primary strategy is establishing joint ventures and pilot programs to cross the "Valley of Death" in early-stage deep tech commercialization.</p>
    <ul>
      {'<li>Conduct technical validation and regulatory compliance tests.</li>' if research_data.get('readiness_level', 0) < 6 else '<li>Immediate scaling and commercial deployment.</li>'}
    </ul>
  </div>
  
  <div class="slide">
    <h2>7. Competitive Landscape</h2>
    <h3>Known Industry Incumbents & Competitors</h3>
    <ul>
      {''.join(f"<li>{c.get('name', str(c))} - {c.get('focus', '')}</li>" if isinstance(c, dict) else f"<li>{c}</li>" for c in market_data.get('competitors', [])[:5])}
    </ul>
  </div>
  
  <div class="slide">
    <h2>8. Feasibility & Development Roadmap</h2>
    <p>Estimated Development Timeline: {feasibility_data.get('resources', {}).get('time', 'Unknown')}</p>
    <ol>
      {''.join(f'<li>{m}</li>' for m in feasibility_data.get('roadmap', []))}
    </ol>
  </div>

  <div class="slide">
    <h2>9. The Ask (Funding Requirements)</h2>
    <p>Required Capital: {feasibility_data.get('resources', {}).get('budget', 'Unknown')}</p>
    <p>Capital will be allocated strictly towards reaching our mapped technical milestones, acquiring necessary engineering headcount ({feasibility_data.get('resources', {}).get('team_size', 'Unknown')}), and achieving our operational roadmap over the calculated runway.</p>
  </div>

  <div class="slide">
    <h2>10. Target Stakeholders & Investors</h2>
    <ul>
      {''.join(f"<li>{inv.get('name', 'Unknown')} ({(inv.get('match_score', 0)*100):.0f}% Portfolio Match) - Preferred Stage: {inv.get('stage', 'N/A')} | Ticket Size: {inv.get('ticket_size', 'N/A')}</li>" for inv in stakeholder_data.get('investor_matches', [])[:5])}
    </ul>
  </div>
</body>
</html>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path

def generate_deck_summary(agent_outputs: Dict[str, Any]) -> str:
    """Generate a formal 10-slide markdown presentation to feed to NotebookLM."""
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    feasibility_data = agent_outputs.get('feasibility_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    
    summary = "# Pitch Deck: Deep Tech Commercialization\n\n"
    
    summary += "## 1. Executive Summary\n"
    summary += f"Target Domains: {', '.join(research_data.get('application_domains', []))}\n\n"
    
    summary += "## 2. The Problem\n"
    summary += "Current solutions fail to integrate modern research constraints, leaving a gap for specialized high-TRL methodologies.\n"
    for t in market_data.get('trends', []):
        summary += f"- {t}\n"
    summary += "\n"
        
    summary += "## 3. The Solution / Core Innovation\n"
    for i in research_data.get('innovations', []):
        summary += f"- {i}\n"
    summary += f"\nTechnology Readiness Level: {research_data.get('readiness_level', 0)}/9\n\n"
    
    summary += "## 4. Market Opportunity\n"
    summary += f"- **TAM:** {market_data.get('TAM', 'N/A')}\n"
    summary += f"- **SAM:** {market_data.get('SAM', 'N/A')}\n"
    summary += f"- **SOM:** {market_data.get('SOM', 'N/A')}\n\n"
    
    summary += "## 5. Business Model\n"
    summary += "Revenue generation primarily through B2B Licensing, enterprise software integration pipelines, and specialized joint ventures.\n\n"
    
    summary += "## 6. Go-To-Market Strategy\n"
    summary += "Begin with paid pilot programs across target domains to validate technical integration. Scale into recurring licensing models once product-market fit secures ROI.\n\n"
    
    summary += "## 7. Competitive Landscape\n"
    for c in market_data.get('competitors', []):
        if isinstance(c, dict):
            summary += f"- **{c.get('name', 'Unknown')}**: {c.get('focus', 'Competitor')}\n"
        else:
            summary += f"- {c}\n"
    summary += "\n"
    
    summary += "## 8. Feasibility & Roadmap\n"
    for m in feasibility_data.get('roadmap', []):
        summary += f"1. {m}\n"
    summary += "\n"
    
    summary += "## 9. The Ask (Funding)\n"
    summary += f"- **Budget Required:** {feasibility_data.get('resources', {}).get('budget', 'Unknown')}\n"
    summary += f"- **Development Time:** {feasibility_data.get('resources', {}).get('time', 'Unknown')}\n"
    summary += f"- **Team Size Needed:** {feasibility_data.get('resources', {}).get('team_size', 'Unknown')}\n\n"
    
    summary += "## 10. Target Stakeholders\n"
    for inv in stakeholder_data.get('investor_matches', []):
        summary += f"- **{inv.get('name', 'Unknown')}**: {inv.get('stage', 'Unknown')} Stage | Ticket: {inv.get('ticket_size', 'Unknown')} | Match: {(inv.get('match_score', 0)*100):.0f}%\n"
    summary += "\n"
    
    return summary
