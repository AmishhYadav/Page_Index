function ResultCard({ result, rank }) {
  if (!result) return null;

  const title = result.title || "Untitled";
  const url = result.url || "#";
  const description = result.description || "No description available.";
  const score = result.score != null ? result.score.toFixed(4) : "N/A";
  const matchedTerms = result.matched_terms || [];

  return (
    <div className="result-card">
      <div className="result-rank">#{rank}</div>
      <div className="result-content">
        <h3 className="result-title">
          <a href={url} target="_blank" rel="noopener noreferrer">
            {title}
          </a>
        </h3>
        <p className="result-url">{url}</p>
        <p className="result-description">{description}</p>
        <div className="result-meta">
          <span className="result-score">Score: {score}</span>
          {result.word_count > 0 && (
            <span className="result-words">{result.word_count} words</span>
          )}
          {matchedTerms.length > 0 && (
            <span className="result-terms">
              Matched: {matchedTerms.join(", ")}
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

export default ResultCard;
