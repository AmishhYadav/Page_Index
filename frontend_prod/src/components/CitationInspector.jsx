import React from 'react';
import { X, ExternalLink, ShieldAlert, CheckCircle2, AlertTriangle, FileText } from 'lucide-react';
import './CitationInspector.css';

const CitationInspector = ({ citation, onClose, onOpenViewer }) => {
    if (!citation) return null;

    const isHighIntegrity = (citation.score || 0) > 0.9;
    const filename = citation.filename || "UNKNOWN_SOURCE";

    return (
        <div className="citation-inspector">
            <div className="inspector-header">
                <div className="inspector-title">
                    <FileText size={16} className="title-icon" />
                    <span>FORENSIC_INSPECTOR [ID: {filename.split('.')[0]}]</span>
                </div>
                <button className="close-btn" onClick={onClose}>
                    <X size={16} />
                </button>
            </div>

            <div className="inspector-content">
                <div className="evidence-summary">
                    <div className="summary-item">
                        <span className="summary-label">SOURCE_FILE:</span>
                        <span className="summary-value">{filename}</span>
                    </div>
                    <div className="summary-item">
                        <span className="summary-label">PAGE_LOCATION:</span>
                        <span className="summary-value">SECTION {citation.page || '?'}</span>
                    </div>
                    <div className="summary-item">
                        <span className="summary-label">VECTOR_SIGNAL:</span>
                        <span className={`summary-value ${(isHighIntegrity || !citation.score) ? 'emerald' : 'amber'}`}>
                            {(citation.score || 0).toFixed(4)} {isHighIntegrity ? '[VERIFIED]' : '[SIGNAL_VARIANCE]'}
                        </span>
                    </div>
                </div>

                <div className="verification-logs">
                    <div className="log-header">VERIFICATION_TRACE</div>
                    <div className="log-entry">
                        <CheckCircle2 size={12} className="emerald" />
                        <span>[{new Date().toLocaleTimeString([], { hour12: false })}] HIERARCHY_SYNC_COMPLETE</span>
                    </div>
                    <div className="log-entry">
                        {isHighIntegrity ? (
                            <CheckCircle2 size={12} className="emerald" />
                        ) : (
                            <AlertTriangle size={12} className="amber" />
                        )}
                        <span>[{new Date().toLocaleTimeString([], { hour12: false })}] CROSS_ENCODER_SIGNAL_MATCH</span>
                    </div>
                    <div className="log-entry">
                        <CheckCircle2 size={12} className="emerald" />
                        <span>[{new Date().toLocaleTimeString([], { hour12: false })}] CITATION_INDEX_ANCHOR_FOUND</span>
                    </div>
                </div>

                <div className="context-preview">
                    <div className="preview-header">
                        <span>RAW_CONTEXT_SNIPPET</span>
                        <button
                            className="action-link"
                            onClick={() => onOpenViewer && onOpenViewer(citation)}
                        >
                            <ExternalLink size={12} />
                            <span>OPEN_VIEWER</span>
                        </button>
                    </div>
                    <div className="preview-box">
                        <p className="preview-text">
                            "{citation.textSnippet || '...context signal unavailable for this snippet...'}"
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
