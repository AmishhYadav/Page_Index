import React from 'react';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, Download, Maximize2 } from 'lucide-react';
import './DocumentViewer.css';

const DocumentViewer = () => {
    return (
        <div className="document-viewer">
            <div className="viewer-toolbar">
                <div className="doc-name">STRAT_FINAL.PDF [PAGE 14/32]</div>
                <div className="toolbar-actions">
                    <div className="zoom-controls">
                        <button className="tool-btn"><ZoomOut size={14} /></button>
                        <span className="zoom-level">100%</span>
                        <button className="tool-btn"><ZoomIn size={14} /></button>
                    </div>
                    <div className="toolbar-divider"></div>
                    <button className="tool-btn"><Download size={14} /></button>
                    <button className="tool-btn"><Maximize2 size={14} /></button>
                </div>
            </div>

            <div className="viewer-workspace">
                <button className="nav-page-btn left"><ChevronLeft size={24} /></button>

                <div className="pdf-page-mock">
                    <div className="page-content">
                        <h3>3.3 REGIONAL ENERGY OVERHEAD ANALYTICS</h3>
                        <p>
                            Analysis of verified filings reveals three critical risk drivers for Q3 expansion.
                            The <mark className="highlight">anticipated 12% increase in regional energy overhead</mark> due
                            to market volatility is a primary concern. Infrastructure operations in Phase 2
                            greenfield zones are specifically sensitive to these cost fluctuations.
                        </p>
                        <p>
                            Operational baseline indicates that the current energy grid integrity score remains
                            at 0.94, suggesting a need for redundant backup systems in the southern sector.
                        </p>
                        <div className="skeleton-line large"></div>
                        <div className="skeleton-line"></div>
                        <div className="skeleton-line medium"></div>
                    </div>
                </div>

                <button className="nav-page-btn right"><ChevronRight size={24} /></button>
            </div>

            <div className="viewer-footer">
                <div className="metadata-badge">SOURCE_INTEGRITY: 1.0</div>
                <div className="metadata-badge">CASCADE_SYNC: VERIFIED</div>
            </div>
        </div>
    );
};

export default DocumentViewer;
