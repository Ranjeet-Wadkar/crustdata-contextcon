"use client";
import React, { useState, useEffect } from 'react';
import NeoButton from '@/components/NeoButton';

export default function Home() {
  const [text, setText] = useState('');
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [showLogs, setShowLogs] = useState(false);
  const [activeTab, setActiveTab] = useState('research');

  // Human-in-loop states
  const [researchOverride, setResearchOverride] = useState({ topics: '', products: '' });
  const [feasibilityOverride, setFeasibilityOverride] = useState({ time: '', team_size: '', budget: '', roadmap: ''});

  const fetchLogs = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/logs');
      if (res.ok) {
        const data = await res.json();
        setLogs(data.logs || []);
      }
    } catch (e) {}
  };

  useEffect(() => {
    let interval: any;
    if (activeStep > 0 && activeStep < 6) {
      interval = setInterval(fetchLogs, 1000);
    }
    return () => clearInterval(interval);
  }, [activeStep]);

  const agents = ['Research', 'Market Insight', 'Feasibility', 'Stakeholder', 'Business Plan'];

  const startAnalysis = async () => {
    if (!text) return;
    setLoading(true);
    await fetch('http://localhost:8000/api/reset', { method: 'POST' });
    
    // Step 1: Research
    setActiveStep(1);
    const r1 = await fetch('http://localhost:8000/api/run/research', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text})
    });
    const d1 = await r1.json();
    setResults([d1]);
    
    setResearchOverride({
      topics: d1.output?.topics?.join(', ') || '',
      products: d1.output?.product_recommendations?.map((p: any) => `${p.product_name}: ${p.description}`).join('\n') || ''
    });
    
    // Pause for Human-in-loop (Wait before moving to Market)
    setLoading(false);
  };

  const continueMarketFeasibility = async () => {
    setLoading(true);
    
    // Run Market (passing overrides)
    setActiveStep(2);
    const mPayload = {
      topics: researchOverride.topics.split(',').map(t => t.trim()),
      product_recommendations: [{ product_name: "Refined Output", description: researchOverride.products, relevance: "High" }]
    };
    const r2 = await fetch('http://localhost:8000/api/run/market', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(mPayload)
    });
    const d2 = await r2.json();
    setResults(prev => [...prev.slice(0,1), d2]); // Ensures length is 2

    // Run Feasibility
    setActiveStep(3);
    const r3 = await fetch('http://localhost:8000/api/run/feasibility', { method: 'POST' });
    const d3 = await r3.json();
    setResults(prev => [...prev.slice(0,2), d3]);
    
    setFeasibilityOverride({
      time: d3.output?.resources?.time || '',
      team_size: d3.output?.resources?.team_size || '',
      budget: d3.output?.resources?.budget || '',
      roadmap: d3.output?.roadmap?.join('\n') || ''
    });

    setLoading(false);
  };

  const continueStakeholderBusiness = async () => {
    setLoading(true);
    
    // Run Stakeholder
    setActiveStep(4);
    const fPayload = {
      time: feasibilityOverride.time,
      team_size: feasibilityOverride.team_size,
      budget: feasibilityOverride.budget,
      roadmap: feasibilityOverride.roadmap.split('\n').filter(l => l.trim())
    };
    const r4 = await fetch('http://localhost:8000/api/run/stakeholder', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(fPayload)
    });
    const d4 = await r4.json();
    setResults(prev => [...prev.slice(0,3), d4]);

    // Run Business Plan
    setActiveStep(5);
    const r5 = await fetch('http://localhost:8000/api/run/business_plan', { method: 'POST' });
    const d5 = await r5.json();
    setResults(prev => [...prev.slice(0,4), d5]);

    setActiveStep(6);
    setLoading(false);
    fetchLogs();
  };

  const downloadFile = async (url: string, filename: string) => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/export/${url}`, { method: 'POST' });
      if (!res.ok) throw new Error("Export failed");
      const blob = await res.blob();
      const objUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = objUrl;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch(e) {
      alert("Error generating file!");
    }
    setLoading(false);
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      if (data.text) {
        setText(data.text);
      } else {
        alert(data.detail || "Error extracting text");
      }
    } catch(e) {
      alert("Error uploading file");
    }
    setLoading(false);
  };

  return (
    <main style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      
      {activeStep === 0 && (
      <div className="neo-card" style={{ padding: '2rem' }}>
        <h2 style={{ marginTop: 0, fontSize: '1.5rem', fontWeight: 800 }}>Start your Analysis</h2>
        <p style={{ opacity: 0.8, marginBottom: '2rem' }}>
          Paste your research abstract or key concepts, or upload a PDF.
        </p>
        
        <input 
           type="file" 
           accept="application/pdf" 
           onChange={handleFileUpload} 
           style={{ marginBottom: '1rem', display: 'block' }}
           disabled={loading}
        />

        <textarea
          className="neo-input"
          rows={8}
          placeholder="...or paste research paper text here"
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{ marginBottom: '1.5rem', minHeight: '150px' }}
          disabled={loading}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
          <NeoButton onClick={startAnalysis} disabled={loading || !text}>
            {loading ? 'Processing...' : 'Start Agent Swarm 🚀'}
          </NeoButton>
        </div>
      </div>
      )}

      {activeStep > 0 && activeStep < 6 && (
        <div className="neo-card">
          <h2 style={{ marginTop: 0 }}>Agent Swarm Progress</h2>
          <div style={{ display: 'flex', gap: '1rem', flexDirection: 'column', marginBottom: '2rem' }}>
            {agents.map((agent, index) => (
              <div key={agent} style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{ 
                  width: '30px', height: '30px', borderRadius: '50%', border: '2px solid var(--border-color)', 
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  background: activeStep > index + 1 ? '#4ade80' : (activeStep === index + 1 ? '#facc15' : 'transparent'),
                  color: '#000', fontWeight: 'bold'
                }}>
                  {activeStep > index + 1 ? '✓' : index + 1}
                </div>
                <div style={{ fontWeight: 'bold' }}>{agent} Agent</div>
                {results[index] && (
                  <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>
                    - {results[index].voice_message?.substring(0, 80)}...
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Human IN LOOP FORMs */}
          {activeStep === 1 && !loading && (
            <div style={{ padding: '1rem', border: '2px solid var(--primary)', borderRadius: '8px', background: 'rgba(242, 98, 34, 0.1)' }}>
               <h3 style={{marginTop: 0}}>⚠️ Review Research & Mappings</h3>
               <p>The Research Agent has found similar papers and derived initial product ideas. Refine them before we figure out the market size!</p>
               <input className="neo-input" value={researchOverride.topics} onChange={e => setResearchOverride({...researchOverride, topics: e.target.value})} style={{marginBottom:'1rem'}} placeholder="Topics" />
               <textarea className="neo-input" value={researchOverride.products} onChange={e => setResearchOverride({...researchOverride, products: e.target.value})} rows={4} style={{marginBottom:'1rem'}} placeholder="Products" />
               <NeoButton onClick={continueMarketFeasibility} fullWidth={true}>Approve & Run Market Evaluation</NeoButton>
            </div>
          )}

          {activeStep === 3 && !loading && (
            <div style={{ padding: '1rem', border: '2px solid var(--primary)', borderRadius: '8px', background: 'rgba(242, 98, 34, 0.1)' }}>
               <h3 style={{marginTop: 0}}>⚠️ Review Feasibility & Scale</h3>
               <p>The Feasibility Agent has assessed the project scale and roadmap. Refine the budgeting and timeline assumptions:</p>
               <div style={{display:'flex', gap:'1rem', marginBottom:'1rem'}}>
                 <input className="neo-input" value={feasibilityOverride.time} onChange={e => setFeasibilityOverride({...feasibilityOverride, time: e.target.value})} placeholder="Timeline" />
                 <input className="neo-input" value={feasibilityOverride.team_size} onChange={e => setFeasibilityOverride({...feasibilityOverride, team_size: e.target.value})} placeholder="Team Size" />
                 <input className="neo-input" value={feasibilityOverride.budget} onChange={e => setFeasibilityOverride({...feasibilityOverride, budget: e.target.value})} placeholder="Budget" />
               </div>
               <textarea className="neo-input" value={feasibilityOverride.roadmap} onChange={e => setFeasibilityOverride({...feasibilityOverride, roadmap: e.target.value})} rows={4} style={{marginBottom:'1rem'}} placeholder="Development Roadmap" />
               <NeoButton onClick={continueStakeholderBusiness} fullWidth={true}>Approve & Finalize Complete Pitch Deck</NeoButton>
            </div>
          )}

        </div>
      )}
      
      {activeStep === 6 && (
        <div className="neo-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap' }}>
            <h2 style={{ marginTop: 0 }}>Analysis Complete!</h2>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <NeoButton onClick={() => downloadFile('pdf', 'pitch_deck.pdf')}>📥 Download PDF Deck</NeoButton>
              <NeoButton onClick={() => downloadFile('notebooklm', 'notebookLM_premium.pptx')}>🚀 Premium PPTX (NotebookLM)</NeoButton>
              <NeoButton onClick={() => { setActiveStep(0); setResults([]); setText(''); }}>🔄 New Analysis</NeoButton>
            </div>
          </div>
          
          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem', borderBottom: '2px solid var(--border-color)', paddingBottom: '1rem' }}>
            <button className="neo-input" style={{ width: 'auto', background: activeTab === 'research' ? 'var(--primary)' : 'transparent', fontWeight: 'bold' }} onClick={() => setActiveTab('research')}>🔬 Research</button>
            <button className="neo-input" style={{ width: 'auto', background: activeTab === 'market' ? 'var(--primary)' : 'transparent', fontWeight: 'bold' }} onClick={() => setActiveTab('market')}>📊 Market</button>
            <button className="neo-input" style={{ width: 'auto', background: activeTab === 'feasibility' ? 'var(--primary)' : 'transparent', fontWeight: 'bold' }} onClick={() => setActiveTab('feasibility')}>⚙️ Feasibility</button>
            <button className="neo-input" style={{ width: 'auto', background: activeTab === 'stakeholders' ? 'var(--primary)' : 'transparent', fontWeight: 'bold' }} onClick={() => setActiveTab('stakeholders')}>🤝 Stakeholders</button>
            <button className="neo-input" style={{ width: 'auto', background: activeTab === 'pitch' ? 'var(--primary)' : 'transparent', fontWeight: 'bold' }} onClick={() => setActiveTab('pitch')}>📋 Pitch Summary</button>
          </div>

          <div style={{ marginTop: '2rem' }}>
            {activeTab === 'research' && results[0]?.output && (
              <div>
                <h3>Key Innovations</h3>
                <ul>{results[0].output.innovations?.map((i: string, idx: number) => <li key={idx}>{i}</li>)}</ul>
                <p><strong>TRL Score:</strong> {results[0].output.readiness_level}/9</p>
                <p><strong>Domains:</strong> {results[0].output.application_domains?.join(', ')}</p>
              </div>
            )}
            {activeTab === 'market' && results[1]?.output && (
              <div>
                <p><strong>TAM:</strong> {results[1].output.TAM}</p>
                <p><strong>SAM:</strong> {results[1].output.SAM}</p>
                <p><strong>SOM:</strong> {results[1].output.SOM}</p>
                <h3>Market Trends</h3>
                <ul>{results[1].output.trends?.map((t: any, idx: number) => <li key={idx}>{typeof t === 'string' ? t : (t.trend || t.name || JSON.stringify(t))}</li>)}</ul>
                <h3>Competitors</h3>
                <ul>{results[1].output.competitors?.map((c: any, idx: number) => <li key={idx}>{typeof c === 'string' ? c : (c.competitor || c.name || JSON.stringify(c))}</li>)}</ul>
              </div>
            )}
            {activeTab === 'feasibility' && results[2]?.output && (
              <div>
                <p><strong>Feasibility Score:</strong> {results[2].output.feasibility_score}/10</p>
                <p><strong>Timeline:</strong> {results[2].output.resources?.time}</p>
                <p><strong>Budget:</strong> {results[2].output.resources?.budget}</p>
                <h3>Roadmap</h3>
                <ol>{results[2].output.roadmap?.map((r: string, idx: number) => <li key={idx}>{r}</li>)}</ol>
                <h3>Risks</h3>
                <ul>{results[2].output.risks?.map((r: string, idx: number) => <li key={idx}>{r}</li>)}</ul>
              </div>
            )}
            {activeTab === 'stakeholders' && results[3]?.output && (
              <div>
                <h3>Recommended Team</h3>
                <ul>{results[3].output.team_roles?.map((r: string, idx: number) => <li key={idx}>{r}</li>)}</ul>
                <h3>Investor Matches</h3>
                <ol>
                  {results[3].output.investor_matches?.map((inv: any, idx: number) => (
                     <li key={idx}><strong>{inv.name}</strong> - Match: {(inv.match_score*100).toFixed(0)}% ({inv.geo}) Focusing on {inv.focus?.join(', ')}</li>
                  ))}
                </ol>
              </div>
            )}
            {activeTab === 'pitch' && results[4]?.output && (
              <div>
                <h3>Slides Generated</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {results[4].output.slides?.map((slide: any, idx: number) => (
                    <div key={idx} style={{ padding: '1rem', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
                      <h4 style={{marginTop:0}}>{slide.title}</h4>
                      <p style={{whiteSpace: 'pre-wrap'}}>{slide.content}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* API Logs Viewer */}
      {logs.length > 0 && (
        <div className="neo-card" style={{ marginTop: 'auto', background: 'var(--surface)' }}>
          <div 
             style={{ display: 'flex', justifyContent: 'space-between', cursor: 'pointer', alignItems: 'center' }} 
             onClick={() => setShowLogs(!showLogs)}
          >
            <h3 style={{ margin: 0 }}>🤖 Processing Logs ({logs.length})</h3>
            <span>{showLogs ? '▲ Collapse' : '▼ Expand'}</span>
          </div>
          
          {showLogs && (
            <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '300px', overflowY: 'auto' }}>
              {logs.map((log, i) => (
                <div key={i} style={{ padding: '0.5rem', background: 'var(--bg-color)', border: '1px solid var(--border-color)', borderRadius: '4px', fontSize: '0.85rem' }}>
                  <strong>[{log.timestamp}] {log.agent} </strong>
                  <span style={{ color: log.type === 'call' ? 'var(--primary)' : 'inherit' }}>({log.type})</span>
                  <pre style={{ margin: '0.5rem 0 0 0', whiteSpace: 'pre-wrap', wordBreak: 'break-word', maxHeight:'100px', overflow:'auto' }}>{log.content}</pre>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </main>
  );
}
