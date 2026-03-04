import React from 'react';
import { ShieldCheck, FileText, ChevronRight } from 'lucide-react';
import './AnswerPanel.css';

const AnswerPanel = ({ answer, citations = [], integrityScore = 0, onSelectCitation }) => {
    if (!answer) return null;

    return (
        <div className="answer-panel">
            <div className="integrity-banner">
                <ShieldCheck size={14} className="emerald" />
                <span className="integrity-label">CITATION_INTEGRITY:</span>
                <span className={`integrity-value ${integrityScore > 0.9 ? 'emerald' : 'amber'}`}>
                    {(integrityScore * 100).toFixed(1)}% {integrityScore > 0.9 ? 'VERIFIED' : 'WARNING'}
                </span>
            </div>

            <div className="answer-content">
                <p className="answer-text">
                    {answer}
                </p>
            </div>

            <div className="citations-header">
                <span className="citations-label">METADATA_SOURCES [{citations.length}]</span>
            </div>

            <div className="citations-list">
                {citations.map((cite, idx) => (
                    <div
                        key={idx}
                        className="citation-card"
                        onClick={() => onSelectCitation && onSelectCitation(cite)}
                    >
                        <div className="citation-icon">
                            <FileText size={14} />
                        </div>
                        <div className="citation-info">
                            <span className="citation-filename">{cite.filename || 'UNKNOWN_FILE'}</span>
                            <span className="citation-meta">PAGE {cite.page || '?'} | NODES {cite.nodeCount || 0}</span>
                        </div>
                        <div className="citation-score">
                            <span className="score-label">RELEVANCE</span>
                            <span className="score-value">{(cite.score || 0).toFixed(3)}</span>
                        </div>
                        <ChevronRight size={14} className="citation-arrow" />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AnswerPanel;
