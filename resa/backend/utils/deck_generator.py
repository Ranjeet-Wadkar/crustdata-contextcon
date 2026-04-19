"""
Pitch deck generation utilities for the Research-to-Startup AI Agent Swarm.
"""

def create_pitch_deck(agent_outputs: Dict[str, Any], output_path: str = "pitch_deck.html") -> str:
    """Generate an HTML pitch deck styled with Neo-Brutalism."""
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    feasibility_data = agent_outputs.get('feasibility_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  :root {{ --primary: #f26222; --bg: #fffbf5; --text: #000; --border: #000; }}
  body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); padding: 2rem; }}
  .slide {{ border: 4px solid var(--border); box-shadow: 8px 8px 0px var(--text); background: white; padding: 2rem; margin-bottom: 3rem; border-radius: 8px; }}
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
    <h2>1. Core Innovations</h2>
    <ul>
      {''.join(f'<li>{i}</li>' for i in research_data.get('innovations', [])[:3])}
    </ul>
    <p>TRL Score: {research_data.get('readiness_level', 0)}/9</p>
  </div>
  
  <div class="slide">
    <h2>2. Market Opportunity</h2>
    <p>TAM: {market_data.get('TAM', 'N/A')} | SAM: {market_data.get('SAM', 'N/A')} | SOM: {market_data.get('SOM', 'N/A')}</p>
    <h3>Competitors</h3>
    <ul>
      {''.join(f'<li>{c}</li>' for c in market_data.get('competitors', [])[:3])}
    </ul>
  </div>
  
  <div class="slide">
    <h2>3. Feasibility & Roadmap</h2>
    <p>Budget: {feasibility_data.get('resources', {}).get('budget', 'Unknown')} | Time: {feasibility_data.get('resources', {}).get('time', 'Unknown')}</p>
    <ol>
      {''.join(f'<li>{m}</li>' for m in feasibility_data.get('roadmap', []))}
    </ol>
  </div>

  <div class="slide">
    <h2>4. Matching Investors</h2>
    <ul>
      {''.join(f"<li>{inv.get('name', 'Unknown')} ({(inv.get('match_score', 0)*100):.0f}% Match) - {inv.get('ticket_size', 'N/A')}</li>" for inv in stakeholder_data.get('investor_matches', [])[:3])}
    </ul>
  </div>
</body>
</html>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return output_path

def generate_deck_summary(agent_outputs: Dict[str, Any]) -> str:
    """
    Generate a text summary of the pitch deck for preview.
    
    Args:
        agent_outputs: Dictionary containing outputs from all agents
    
    Returns:
        Text summary of the pitch deck
    """
    research_data = agent_outputs.get('research_agent', {})
    market_data = agent_outputs.get('market_agent', {})
    stakeholder_data = agent_outputs.get('stakeholder_agent', {})
    
    summary = "## Pitch Deck Summary\n\n"
    
    # Key innovations
    innovations = research_data.get('innovations', [])
    if innovations:
        summary += f"**Key Innovation:** {innovations[0]}\n\n"
    
    # Market size
    tam = market_data.get('TAM', 'N/A')
    summary += f"**Market Size:** {tam}\n\n"
    
    # Top investor match
    investor_matches = stakeholder_data.get('investor_matches', [])
    if investor_matches:
        top_investor = investor_matches[0]
        summary += f"**Top Investor Match:** {top_investor.get('name', 'Unknown')} ({top_investor.get('match_score', 0)*100:.0f}% match)\n\n"
    
    # Team recommendations
    team_roles = stakeholder_data.get('team_roles', [])
    if team_roles:
        summary += f"**Recommended Team:** {', '.join(team_roles)}\n\n"
    
    return summary
