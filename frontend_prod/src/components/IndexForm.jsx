import { useState } from "react";

function IndexForm({ onIndex, loading }) {
  const [url, setUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim() && !loading) {
      onIndex(url);
    }
  };

  return (
    <form className="index-form" onSubmit={handleSubmit}>
      <h2>Index a New Page</h2>
      <p>Enter a URL to scrape and add to the search index.</p>
      <div className="form-row">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          disabled={loading}
          maxLength={2000}
        />
        <button type="submit" disabled={loading || !url.trim()}>
          {loading ? "Indexing..." : "Index"}
        </button>
      </div>
    </form>
  );
}

export default IndexForm;
