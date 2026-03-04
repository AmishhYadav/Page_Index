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



function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isLoading, setIsLoading] = useState(false);
  const [activeStage, setActiveStage] = useState(null);
  const [completedStages, setCompletedStages] = useState([]);
  const [result, setResult] = useState(null);
  const [searchError, setSearchError] = useState('');
  const [selectedCitation, setSelectedCitation] = useState(null);

  // Document viewer navigation state (from citations)
  const [viewerFilename, setViewerFilename] = useState('STRAT_FINAL.PDF');
  const [viewerPage, setViewerPage] = useState(14);

  const handleSearch = async (query) => {
    setIsLoading(true);
    setResult(null);
    setSearchError('');
    setCompletedStages([]);
    setSelectedCitation(null);

    // Animate pipeline stages while API call executes
    const stages = ['retrieving', 'fusing', 'reranking', 'packing'];
    const stagePromise = (async () => {
      for (const stage of stages) {
        setActiveStage(stage);
        await new Promise(r => setTimeout(r, 400));
        setCompletedStages(prev => [...prev, stage]);
      }
      setActiveStage(null);
    })();

    try {
      const response = await fetch('/api/v1/ask/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, top_k: 5 }),
      });

      await stagePromise;

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Request failed (${response.status})`);
      }

      const data = await response.json();
      setResult({
        answer: data.answer,
        integrityScore: data.citation_integrity ?? 0,
        citations: (data.citations || []).map(c => ({
          filename: c.document_name,
          page: c.page_number,
          sectionTitle: c.section_title,
          textSnippet: c.text_snippet,
          nodeCount: 1,
          score: 0.9,
        })),
      });
    } catch (err) {
      await stagePromise;
      console.error('Search error:', err);
      setSearchError(err.message || 'Search failed.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNavigate = (tab) => setActiveTab(tab);

  const handleOpenViewer = (citation) => {
    if (citation) {
      setViewerFilename(citation.filename || 'STRAT_FINAL.PDF');
      setViewerPage(citation.page || 1);
    }
    setSelectedCitation(null);
    setActiveTab('viewer');
  };

  const renderModule = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard onNavigate={handleNavigate} />;
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

            {searchError && !isLoading && (
              <div style={{
                padding: '12px 16px',
                margin: '12px 0',
                borderRadius: 'var(--radius)',
                border: '1px solid var(--status-red)',
                color: '#f8d7da',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.75rem',
              }}>
                ⚠ {searchError}
              </div>
            )}

            {selectedCitation && (
              <CitationInspector
                citation={selectedCitation}
                onClose={() => setSelectedCitation(null)}
                onOpenViewer={handleOpenViewer}
              />
            )}
          </div>
        );
      case 'viewer':
        return <DocumentViewer initialPage={viewerPage} filename={viewerFilename} />;
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
