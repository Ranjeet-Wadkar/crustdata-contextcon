"use client";
import React, { useState, useEffect } from 'react';
import NeoButton from '@/components/NeoButton';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const SAMPLE_TEXT = `© 2019 JETIR March 2019, Volume 6, Issue 3 www.jetir.org (ISSN-2349-5162)
JETIREO06150 Journal of Emerging Technologies and Innovative Research (JETIR) www.jetir.org 657
A Research Paper on Solid Waste Management
Shweta Choudhary
Department of General Science
Vivekananda Global University, Jaipur
Email ID: shweta.choudhary@vgu.ac.in
ABSTRACT: Solid garbage is the unwanted, harmful, and wasted substance arising from day-to-day civic events. Management
of the solid wastes can be described as the methodology of managing solid waste generation, storage, collection, transport,
treatment and disposal. A country's growth status can be defined in several forms. As regards its effect on solid waste
management, the growth status of this publication is classified according to the availability of economic capital and the degree
of industrialization development. Economic growth status is more a function of the new economic environment than of the
current economic situation (recession vs prosperity). The degree of industrialization is expressed in terms of the extent to which
technical tools are mechanized and usable. The words "developed" and "industrialization" are often used interchangeably,
justifiably or not. In so far as solid waste management is concerned, it is difficult to impose a specific structural definition due
to regional shifts in the degree of growth within each region. For example, in a developed country, a large metropolitan
population (typically the provincial capital and surrounding area) might be at a level of growth well above that of the rest of the
nation. On the other hand, such groups are not absolutely resistant to the restrictions enforced by the nation's position. It is
important to remember that while the material provided in this paper refers specifically to developing nations, some of it can
even refer to a transforming country, or even to an advanced or developed world. The human-environmental relationships are
a dynamic phenomenon. The ability of the Planet to sustain human beings is determined not only by the specific food needs, but
also by our resource use rates, the volume of waste production, the technology employed in various applications. With the
population growth and the growing trend of resource use, we have in effect exceeded the planet's carrying power.
KEYWORDS: Industrialization, prosperity, recession, solid garbage, waste management, landfill, Environment.
INTRODUCTION
The natural reserves of the Planet are not enough now to support human demands and economic activities.
Global warming has demonstrated the risk of overstepping the ability of the Planet to consume our waste
goods. However, the implications of increasing the sufficient availability of vital materials and the degree to
which we have already advanced in this chain are not well known, and are instead viewed with an economic
and manufacturing perspective. The ability of the Planet to consume our waste is a significant factor that
drives the development of waste management technologies [1].
Land-filling is perhaps the oldest method in coordinated waste management. Until the 1970s, land-filling was
practiced as an unceremonious waste disposal in any convenient location without taking into account health,
welfare, environmental conservation or cost efficiency. Yet now the situation has shifted not because of the
understanding and value of the handling of waste, but also other matters [2]. Availability of landfill capacity
in urban environments is getting frightening and a very bad problem. The problem causes political incentive
to redirect waste to many other methods for treatment. Currently, the trend of sophisticated waste management
schemes of countries is to reduce waste that ends up in landfills. In Hong Kong, for example, the initiative's
driving force was the lack of landfill capacity, instead of resource use.
In relation to recycling, the growing waste-to-energy systems and advances in technologies and emissions
reduction tools further decreased the volumes entering landfills primarily in Europe, while in the future it may
be a model for other nations. It refers in particular to those regions where seeking suitable landfill capacity is
a problem and those regions where these solutions are still not completely applied. This should also be
anticipated that in the near future, better and environmentally efficient product design will be possible and
will transform the face of energy harvesting systems. Given risks, land-filling is unavoidable and the final
inert fraction always has to be buried. The construction, maintenance and management of landfills is being
constantly investigated and new methods are being implemented to reduce air and water emissions [3].
© 2019 JETIR March 2019, Volume 6, Issue 3 www.jetir.org (ISSN-2349-5162)
JETIREO06150 Journal of Emerging Technologies and Innovative Research (JETIR) www.jetir.org 658
The accumulation of landfill gas offers room for green-house gas (GHG) reduction. Yet the economics of
extracting waste and recycling electricity remain to be convincingly illustrated. Since, due to partial oxidation
in the landfill, the average methane content of landfill gas is around fifty percentage and most of the gas
produced in landfills is lost to the environment, even with an efficient gas collection system [4]. This low
methane level in the landfill gas necessitates vital upgrade activities that jeopardize the advantages of
collecting landfill gas.
Solid waste management is a term that refers to the storage and disposal process for solid wastes. This also
provides recycled options for things that don't belong to trash or waste. As long as humans have lived in
villages and rural areas, the problem has been trash or solid waste. The solid waste management used in solid,
liquid, and gaseous waste disposal [5]. It is known as a realistic method of disposal of certain toxic waste
products (such as medical organic waste). Incineration is a controversial waste disposal process, owing to
concerns including gaseous pollutant pollution. The most significant justification for recycling waste is to
protect the environment and the public health. Garbage and waste can pollute the air and water. It is also
recognized that decaying garbage releases poisonous gases that interact with the atmospheric air and can cause
respiratory issues in people.
Categorization and comparison of solid industrial waste based on the thermo-chemical properties. Municipal
solid waste (MSW) has usually been divided into six categories: food residues, wood waste, pulp, textiles,
plastics, and rubber. Products may be further divided into subgroups within each grouping [6]. Properly
regulated waste will support the society economically and socially through recycling and, where possible,
reusing waste. Solid waste treatment main elements include on-site managing, processing and storing; garbage
collection; waste management transfer and transport, reduction and final disposal. Solid waste involves trash,
building rubble, industrial refuse, sewage or waste disposal sludge or air quality control plants, among the
other recycled items [7].
The practices related to urban solid waste management from the point of generation before final disposal can
be divided into the six functional components.
• Generation of waste
• Storage of waste
• Collection of waste
• Transportation of waste
• Process of segregation
• Disposal of waste
© 2019 JETIR March 2019, Volume 6, Issue 3 www.jetir.org (ISSN-2349-5162)
JETIREO06150 Journal of Emerging Technologies and Innovative Research (JETIR) www.jetir.org 659
Solid Waste Collection:
Integration of waste management:
Integrated waste management is a framework for the design and development of modern waste management
and disposal systems and the study and optimization of current waste disposal systems. Within this definition
it is important to examine all technological and non-technical elements of management schemes together [8].
Currently, with the introduction of new legislation, laws, and waste management sector as an enterprise, nontechnical elements like public involvement and awareness are necessary and essential to the successful
adoption of many recycling and recovery schemes. A classic example is the general resistance to incineration
services around the world largely due to the perception that incinerators are the origin to dioxins, which also
underlines the efficiency of incinerators in reducing waste quantity and waste disposal levels. Therefore, in
managing pollutants reaching the atmosphere, advances in emissions abatement mechanisms and gasification
techniques [9].
More critically, for the effective implementation of the new waste treatment systems, engaging the public in
such reviews and informing them about the needs and concerns of waste treatment and disposal in a specific
region or country. Today, cooperation between the state, business, and informal sectors is apparent, and it is
optimal to coordinate environmental education and public participation for successful implementation through
one of these networks [10][11]. As stated earlier, the Planet's carrying capacity is continuously threatened as
the environmental protection is paying the price for economic activities. Therefore, resources are rising while
© 2019 JETIR March 2019, Volume 6, Issue 3 www.jetir.org (ISSN-2349-5162)
JETIREO06150 Journal of Emerging Technologies and Innovative Research (JETIR) www.jetir.org 660
competition is growing with the environment and consumption being changed. As the new waste management
elite maintains, the first step to achieving waste reduction is citizen engagement and improving their view,
whereas recycling and reuse often need technical assistance. Energy and nutrient regeneration are focused on
science though their adoption may be a target of NIMBY syndrome if not properly tackled [12-14].
Modern integrated waste disposal is thus the need for time, whereas sustainability needs to be incorporated
into all materials, taking into account the material supply and demand. It's unavoidable that waste is tool now
and it's the duty of people if people use it. As is obvious from past experience, if people really find the Planet
as "our home" it is not convenient, but not difficult.
The waste management hierarchy witnessed changes in the recent decade and currently recycling and recovery
is focused more than the landfilling [15]. Sustainable use of Resources and management of solid waste is
clearly depicted in Figure 2.
© 2019 JETIR March 2019, Volume 6, Issue 3 www.jetir.org (ISSN-2349-5162)
JETIREO06150 Journal of Emerging Technologies and Innovative Research (JETIR) www.jetir.org 661
Both the figures mentioned above, i.e. Figure 3 and 4 depicts the composition of the municipal solid waste
in India and typical Indian state(s) respectively.
Disposal of solid wastes:
• COMPOSTING: It is done by vermin composting of any type of biodegradable wastes such as hotel
refuge, biodegradable portion from residence and commercial market, vegetable waste, leaf litter, etc.
Size of each vermin composting rack is 6.21 m X 1.56 m X 0.62 m made up of steel. It requires two
month.
• LAND FILLING:-Waste is stored on the top of the hill in almost bout five acres area. All inorganic
material is used for the land filling and dumping.
CONCLUSION
Despite the numerous emerging techniques that arise for solid waste management, landfilling is still the most
prevalent approach in the northeastern area of Illinois. Creation and closure of landfills may present potential
groundwater threat due to leachate intake, and air quality due to released gases. Although proper care and
monitoring is sustained for a relatively long period of time (30 years), this may result in a danger to public
health. Such administration, if inaccurate, is inefficient and potentially risky.
• The statistics gathered indicate that the overall proportion of refuse induced by food and vegetable
scraps, the percentage of the reuse caused by food and vegetable scraps, the second highest was paper
and the third highest was inert material. There was a higher proportion of disposable carry bags, where
glass, ceramics and metals were nearly equal to one another.
• Since there is a manual separation plate type of solid waste at the dumping site in villages, it is the
most effective way to obtain the recovery and reuse of materials such as metal, plastic, glass and rubber
etc. Framework should be based on rules on environmental protection (reduction, recycling, reuse, and
recovery).
• Annual report of addition of the strategies for collection of solid waste shall have to be formulated.
• Provision of litter bins at public places shall be made and there will compulsory segregation at all the
sources.
© 2019 JETIR March 2019, Volume 6, Issue 3 www.jetir.org (ISSN-2349-5162)
JETIREO06150 Journal of Emerging Technologies and Innovative Research (JETIR) www.jetir.org 662
• Community knowledge, political commitment and civic participation are key to the effective
application of the regulatory regulations and to an comprehensive approach to efficient disposal of
solid urban waste.
• There should be sufficient health and safety provisions for workers at all stages of waste handling.
• As the dump site is several kilometers away and smaller trucks are used for solid waste transportation,
it would be ideal to set up recycling plant and save on transportation expenses.
REFERENCES
[1] T. J. Sin, G. K. Chen, K. S. Long, I. Goh, and H. Hwang, “Current practice of waste management
system in Malaysia : Towards sustainable waste management,” 1st FPTP Postgrad. Semin. "Towards
Sustain. Manag., 2013.
[2] A. Khalid, M. Arshad, M. Anjum, T. Mahmood, and L. Dawson, “The anaerobic digestion of solid
organic waste,” Waste Management. 2011.
[3] L. Matsakas, Q. Gao, S. Jansson, U. Rova, and P. Christakopoulos, “Green conversion of municipal
solid wastes into fuels and chemicals,” Electronic Journal of Biotechnology. 2017.
[4] H. I. Abdel-Shafy and M. S. M. Mansour, “Solid waste issue: Sources, composition, disposal,
recycling, and valorization,” Egyptian Journal of Petroleum. 2018.
[5] Senate Economic Planning Office, “Philippine Solid Wastes,” Philipp. Solid Wastes A Glance, 2017.
[6] A. Johari, H. Alkali, H. Hashim, S. I. Ahmed, and R. Mat, “Municipal solid waste management and
potential revenue from recycling in Malaysia,” Mod. Appl. Sci., 2014.
[7] M. D. M. Samsudin and M. M. Don, “Municipal solid waste management in Malaysia: Current
practices, challenges and prospect,” J. Teknol. (Sciences Eng., 2013.
[8] U. Arena, “Process and technological aspects of municipal solid waste gasification. A review,” Waste
Manag., 2012.
[9] J. chun Lee and B. D. Pandey, “Bio-processing of solid wastes and secondary resources for metal
extraction - A review,” Waste Management. 2012.
[10] A. Pires, G. Martinho, and N. Bin Chang, “Solid waste management in European countries: A review
of systems analysis techniques,” Journal of Environmental Management. 2011.
[11] A. Fercoq, S. Lamouri, and V. Carbone, “Lean/Green integration focused on waste reduction
techniques,” J. Clean. Prod., 2016.
[12] C. Ezeah, J. A. Fazakerley, and C. L. Roberts, “Emerging trends in informal sector recycling in
developing and transition countries,” Waste Management. 2013.
[13] J. G. Paul, J. Arce-Jaque, N. Ravena, and S. P. Villamor, “Integration of the informal sector into
municipal solid waste management in the Philippines - What does it need?,” Waste Manag., 2012.
[14] P. S. Murthy and M. Madhava Naidu, “Sustainable management of coffee industry by-products and
value addition - A review,” Resources, Conservation and Recycling. 2012.
[15] D. Victor and P. Agamuthu, “Strategic environmental assessment policy integration model for solid
waste management in Malaysia,” Environ. Sci. Policy, 2013.`;

export default function Home() {
  const [text, setText] = useState('');
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [logs, setLogs] = useState<any[]>([]);
  const [showLogs, setShowLogs] = useState(false);
  const [activeTab, setActiveTab] = useState('research');
  const [notebookLoading, setNotebookLoading] = useState(false);

  // Human-in-loop states
  const [researchOverride, setResearchOverride] = useState({ topics: '', products: '' });
  const [feasibilityOverride, setFeasibilityOverride] = useState({ time: '', team_size: '', budget: '', roadmap: ''});

  const fetchLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/logs`);
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
    await fetch(`${API_BASE}/api/reset`, { method: 'POST' });
    
    // Step 1: Research
    setActiveStep(1);
    const r1 = await fetch(`${API_BASE}/api/run/research`, {
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
    const r2 = await fetch(`${API_BASE}/api/run/market`, {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(mPayload)
    });
    const d2 = await r2.json();
    setResults(prev => [...prev.slice(0,1), d2]); // Ensures length is 2

    // Run Feasibility
    setActiveStep(3);
    const r3 = await fetch(`${API_BASE}/api/run/feasibility`, { method: 'POST' });
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
    const r4 = await fetch(`${API_BASE}/api/run/stakeholder`, {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(fPayload)
    });
    const d4 = await r4.json();
    setResults(prev => [...prev.slice(0,3), d4]);

    // Run Business Plan
    setActiveStep(5);
    const r5 = await fetch(`${API_BASE}/api/run/business_plan`, { method: 'POST' });
    const d5 = await r5.json();
    setResults(prev => [...prev.slice(0,4), d5]);

    setActiveStep(6);
    setLoading(false);
    fetchLogs();
  };

  const downloadFile = async (url: string, filename: string) => {
    if (url === 'notebooklm') setNotebookLoading(true);
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/export/${url}`, { method: 'POST' });
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
    } finally {
      setLoading(false);
      setNotebookLoading(false);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await fetch(`${API_BASE}/api/upload`, {
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
          <NeoButton onClick={() => setText(SAMPLE_TEXT)} disabled={loading}>
            📄 Try Sample Paper
          </NeoButton>
          <NeoButton onClick={startAnalysis} disabled={loading || !text}>
            {loading ? 'Processing...' : 'Start Agent Swarm 🚀'}
          </NeoButton>
        </div>
      </div>
      )}

      {activeStep > 0 && activeStep < 6 && (
        <div className="neo-card">
          <h2 style={{ marginTop: 0, marginBottom: '0.5rem' }}>Agent Swarm Progress</h2>
          <p style={{ fontSize: '0.85rem', opacity: 0.6, marginBottom: '2rem', fontStyle: 'italic' }}>
            ⏱️ Total analysis takes approx. 80s with 2 human-in-the-loop validation checkpoints.
          </p>
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
                    - {results[index].voice_message ? String(results[index].voice_message).substring(0, 80) : 'Processing...'}...
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
              <NeoButton onClick={() => downloadFile('pdf', 'pitch_deck.html')}>📥 Download HTML Deck</NeoButton>
              <NeoButton onClick={() => downloadFile('notebooklm', 'notebookLM_premium.pptx')} disabled={loading}>
                {notebookLoading ? '⏳ Generating...' : '🚀 Premium PPTX (NotebookLM)'}
              </NeoButton>
              <NeoButton onClick={() => { setActiveStep(0); setResults([]); setText(''); }}>🔄 New Analysis</NeoButton>
            </div>
          </div>
          
          {notebookLoading && (
            <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(242, 98, 34, 0.1)', border: '2px dashed var(--primary)', borderRadius: '8px' }}>
              <p style={{ margin: 0, fontWeight: 'bold' }}>
                🚀 Generating Investor-Grade PPTX via NotebookLM Swarm...
              </p>
              <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.9rem', opacity: 0.8 }}>
                May return an error incase there is a rate limit hit, since I am using a free trial account. This process involves AI agents logging into NotebookLM and generating formatted slides. This usually takes 3-4 mins. <strong>Please do not refresh the page. </strong>
              </p>
            </div>
          )}
          
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
                <ul>{results[3].output.team_roles?.map((r: any, idx: number) => <li key={idx}>{String(r)}</li>)}</ul>
                <h3>Investor Matches</h3>
                <ol>
                  {(results[3].output.investor_matches || []).map((inv: any, idx: number) => (
                     <li key={idx}>
                       <strong>{inv?.name || 'Unknown Investor'}</strong> 
                       {inv?.match_score != null && ` - Match: ${(inv.match_score*100).toFixed(0)}%`}
                       {inv?.geo && ` (${inv.geo})`}
                       {inv?.focus && ` Focusing on ${Array.isArray(inv.focus) ? inv.focus.join(', ') : inv.focus}`}
                     </li>
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
