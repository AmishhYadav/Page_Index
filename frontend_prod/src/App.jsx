import { useState, useCallback } from "react";
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

  return (
    <div className="app">
      <header className="app-header">
        <h1>📄 Page Index</h1>
        <p>Index and search web pages</p>
        <nav className="tabs">
          <button
            className={activeTab === "search" ? "active" : ""}
            onClick={() => setActiveTab("search")}
          >
            🔍 Search
          </button>
          <button
            className={activeTab === "index" ? "active" : ""}
            onClick={() => setActiveTab("index")}
          >
            ➕ Index Page
          </button>
        </nav>
      </header>

      <main className="app-main">
        {activeTab === "search" && (
          <section className="search-section">
            <SearchBar onSearch={handleSearch} loading={loading} />

            {loading && <div className="loading">🔄 Searching...</div>}

            {error && !loading && <div className="error-message">{error}</div>}

            {searchInfo && !loading && !error && (
              <div className="search-info">
                Found {searchInfo.total} result{searchInfo.total !== 1 ? "s" : ""} for &ldquo;{searchInfo.query}&rdquo;
              </div>
            )}

            <div className="results">
              {results.map((result, index) => (
                <ResultCard key={result.url || index} result={result} rank={index + 1} />
              ))}
            </div>
          </section>
        )}

        {activeTab === "index" && (
          <section className="index-section">
            <IndexForm onIndex={handleIndex} loading={indexLoading} />
            {indexLoading && <div className="loading">🔄 Indexing page...</div>}
            {indexMessage && <div className="success-message">{indexMessage}</div>}
            {indexError && <div className="error-message">{indexError}</div>}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
