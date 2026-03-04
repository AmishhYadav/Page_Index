import React, { useState, useCallback } from 'react';
import AppLayout from './components/AppLayout';
import QueryPanel from './components/QueryPanel';
import AnswerPanel from './components/AnswerPanel';
import PipelineTelemetry from './components/PipelineTelemetry';
import CitationInspector from './components/CitationInspector';
import Dashboard from './components/Dashboard';
import UploadPanel from './components/UploadPanel';
import DocumentViewer from './components/DocumentViewer';
import Settings from './components/Settings';
import SearchBar from "./components/SearchBar";
import ResultCard from "./components/ResultCard";
import IndexForm from "./components/IndexForm";
import "./App.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searchInfo, setSearchInfo] = useState(null);
  const [indexMessage, setIndexMessage] = useState("");
  const [indexError, setIndexError] = useState("");
  const [indexLoading, setIndexLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("search");
  const [isLoading, setIsLoading] = useState(false);
  const [activeStage, setActiveStage] = useState(null);
  const [completedStages, setCompletedStages] = useState([]);
  const [result, setResult] = useState(null);
  const [selectedCitation, setSelectedCitation] = useState(null);

  // Viewer state for cross-link navigation
  const [viewerContext, setViewerContext] = useState({
    filename: 'STRAT_FINAL.PDF',
    page: 1
  });

  const handleSearch = useCallback(async (query) => {
    if (!query.trim()) {
      setError("Please enter a search query");
      setResults([]);
      setSearchInfo(null);
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);
    setSearchInfo(null);

    try {
      const response = await fetch(
        `${API_BASE}/search?q=${encodeURIComponent(query.trim())}`
      );
      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Search failed");
        return;
      }

      setResults(data.results || []);
      setSearchInfo({
        total: data.total_results || 0,
        query: data.query || query,
      });

      if ((data.results || []).length === 0) {
        setError("No results found. Try different keywords or index more pages.");
      }
    } catch (err) {
      if (err.name === "TypeError" && err.message.includes("fetch")) {
        setError("Cannot connect to server. Make sure the backend is running on port 5000.");
      } else {
        setError("Search failed. Please try again.");
      }
      console.error("Search error:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleIndex = useCallback(async (url) => {
    if (!url.trim()) {
      setIndexError("Please enter a URL");
      return;
    }

    setIndexLoading(true);
    setIndexMessage("");
    setIndexError("");

    try {
      const response = await fetch(`${API_BASE}/index`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url.trim() }),
      });
      const data = await response.json();

      if (!response.ok) {
        setIndexError(data.error || "Indexing failed");
        return;
      }

      setIndexMessage(
        `✅ ${data.message}${data.title ? ` — "${data.title}"` : ""}${data.word_count ? ` (${data.word_count} words)` : ""}`
      );
    } catch (err) {
      if (err.name === "TypeError" && err.message.includes("fetch")) {
        setIndexError("Cannot connect to server. Make sure the backend is running.");
      } else {
        setIndexError("Indexing failed. Please try again.");
      }
      console.error("Index error:", err);
    } finally {
      setIndexLoading(false);
    }
  }, []);

  const handleOpenViewer = (citation) => {
    setViewerContext({
      filename: citation.filename,
      page: citation.page
    });
    setActiveTab('viewer');
    setSelectedCitation(null);
  };

  const renderModule = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard onNavigate={setActiveTab} />;
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
                onOpenViewer={handleOpenViewer}
              />
            )}
          </div>
        );
      case 'viewer':
        return <DocumentViewer initialPage={viewerContext.page} filename={viewerContext.filename} />;
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
