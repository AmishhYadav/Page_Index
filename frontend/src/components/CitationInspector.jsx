import React from 'react';
import { X, ExternalLink, ShieldAlert, CheckCircle2, AlertTriangle, FileText } from 'lucide-react';
import './CitationInspector.css';

const CitationInspector = ({ citation, onClose }) => {
    if (!citation) return null;

    const isHighIntegrity = citation.score > 0.9;

    return (
        <div className="citation-inspector">
            <div className="inspector-header">
                <div className="inspector-title">
                    <FileText size={16} className="title-icon" />
                    <span>FORENSIC_INSPECTOR [ID: {citation.filename.split('.')[0]}]</span>
                </div>
                <button className="close-btn" onClick={onClose}>
                    <X size={16} />
                </button>
            </div>

            <div className="inspector-content">
                <div className="evidence-summary">
                    <div className="summary-item">
                        <span className="summary-label">SOURCE_FILE:</span>
                        <span className="summary-value">{citation.filename}</span>
                    </div>
                    <div className="summary-item">
                        <span className="summary-label">PAGE_LOCATION:</span>
                        <span className="summary-value">SECTION {citation.page}</span>
                    </div>
                    <div className="summary-item">
                        <span className="summary-label">VECTOR_SIGNAL:</span>
                        <span className={`summary-value ${isHighIntegrity ? 'emerald' : 'amber'}`}>
                            {(citation.score).toFixed(4)} {isHighIntegrity ? '[VERIFIED]' : '[LOW_CONFIDENCE]'}
                        </span>
                    </div>
                </div>

                <div className="verification-logs">
                    <div className="log-header">VERIFICATION_TRACE</div>
                    <div className="log-entry">
                        <CheckCircle2 size={12} className="emerald" />
                        <span>[03:22:14] HIERARCHY_SYNC_COMPLETE</span>
                    </div>
                    <div className="log-entry">
                        {isHighIntegrity ? (
                            <CheckCircle2 size={12} className="emerald" />
                        ) : (
                            <AlertTriangle size={12} className="amber" />
                        )}
                        <span>[03:22:15] CROSS_ENCODER_SIGNAL_MATCH</span>
                    </div>
                    <div className="log-entry">
                        <CheckCircle2 size={12} className="emerald" />
                        <span>[03:22:15] CITATION_INDEX_ANCHOR_FOUND</span>
                    </div>
                </div>

                <div className="context-preview">
                    <div className="preview-header">
                        <span>RAW_CONTEXT_SNIPPET</span>
                        <button className="action-link">
                            <ExternalLink size={12} />
                            <span>OPEN_VIEWER</span>
                        </button>
                    </div>
                    <div className="preview-box">
                        <p className="preview-text">
                            "...regional sectors show a discrepancy in filing data relating to energy overhead.
                            Volatility in Q3 market indexes contributed to a 12% increase in base operational
                            costs across all monitored expansion zones. Supply chain audits confirm..."
                        </p>
                    </div>
                </div>
            </div>

            <div className="inspector-footer">
                <button className="override-btn">
                    <ShieldAlert size={14} />
                    <span>MANUAL_OVERRIDE</span>
                </button>
            </div>
        </div>
    );
};

export default CitationInspector;
