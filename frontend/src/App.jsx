import React, { useState } from 'react';
import AppLayout from './components/AppLayout';
import QueryPanel from './components/QueryPanel';
import AnswerPanel from './components/AnswerPanel';
import PipelineTelemetry from './components/PipelineTelemetry';
import CitationInspector from './components/CitationInspector';
import Dashboard from './components/Dashboard';
import UploadPanel from './components/UploadPanel';
import DocumentViewer from './components/DocumentViewer';
import Settings from './components/Settings';

// Mock data for initial state
const MOCK_RESPONSE = {
  answer: "Analysis of verified filings reveals three critical risk drivers for Q3 expansion: (1) Anticipated 12% increase in regional energy overhead due to market volatility [Doc: Strat_Final.pdf, p14]; (2) Supply chain constraints impacting Phase 2 greenfield materials [Doc: Infra_Ops.pdf, p8]; and (3) Shifting regulatory compliance regarding cross-border data sovereignty [Doc: Compliance_Audit.pdf, p22].",
  integrityScore: 0.982,
  citations: [
    { filename: 'Strat_Final.pdf', page: 14, nodeCount: 4, score: 0.942 },
    { filename: 'Infra_Ops.pdf', page: 8, nodeCount: 2, score: 0.881 },
    { filename: 'Compliance_Audit.pdf', page: 22, nodeCount: 6, score: 0.915 }
  ]
};

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isLoading, setIsLoading] = useState(false);
  const [activeStage, setActiveStage] = useState(null);
  const [completedStages, setCompletedStages] = useState([]);
  const [result, setResult] = useState(null);
  const [selectedCitation, setSelectedCitation] = useState(null);

  const handleSearch = async (query) => {
    setIsLoading(true);
    setResult(null);
    setCompletedStages([]);
    setSelectedCitation(null);

    const stages = ['retrieving', 'fusing', 'reranking', 'packing'];
    for (const stage of stages) {
      setActiveStage(stage);
      await new Promise(r => setTimeout(r, 600));
      setCompletedStages(prev => [...prev, stage]);
    }

    setActiveStage(null);
    setResult(MOCK_RESPONSE);
    setIsLoading(false);
  };

  const renderModule = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'ingest':
        return <UploadPanel />;
      case 'search':
        return (
          <div style={{ maxWidth: '900px', margin: '0 auto', position: 'relative' }}>
            <QueryPanel onSearch={handleSearch} isLoading={isLoading} />

            {(isLoading || activeStage) && (
              <PipelineTelemetry activeStage={activeStage} completedStages={completedStages} />
            )}

            {result && !isLoading && (
              <AnswerPanel
                answer={result.answer}
                citations={result.citations}
                integrityScore={result.integrityScore}
                onSelectCitation={setSelectedCitation}
              />
            )}

            {!isLoading && !result && (
              <div style={{
                height: '200px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '1px dashed var(--border-slate)',
                borderRadius: 'var(--radius)',
                color: 'var(--text-secondary)',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem'
              }}>
                // Awaiting knowledge query...
              </div>
            )}

            {selectedCitation && (
              <CitationInspector
                citation={selectedCitation}
                onClose={() => setSelectedCitation(null)}
              />
            )}
          </div>
        );
      case 'viewer':
        return <DocumentViewer />;
      case 'settings':
        return <Settings />;
      default:
        return <div>Module Under Construction</div>;
    }
  };

  return (
    <AppLayout activeTab={activeTab} onTabChange={setActiveTab}>
      {renderModule()}
    </AppLayout>
  );
}

export default App;
