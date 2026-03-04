import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, Download, Maximize2 } from 'lucide-react';
import './DocumentViewer.css';

const DocumentViewer = ({ initialPage = 14, filename = "STRAT_FINAL.PDF" }) => {
    const [page, setPage] = useState(initialPage);
    const [zoom, setZoom] = useState(100);

    const handleZoomIn = () => setZoom(prev => Math.min(prev + 25, 200));
    const handleZoomOut = () => setZoom(prev => Math.max(prev - 25, 50));
    const handleNextPage = () => setPage(prev => Math.min(prev + 1, 32));
    const handlePrevPage = () => setPage(prev => Math.max(prev - 1, 1));

    return (
        <div className="document-viewer">
            <div className="viewer-toolbar">
                <div className="doc-name">{filename.toUpperCase()} [PAGE {page}/32]</div>
                <div className="toolbar-actions">
                    <div className="zoom-controls">
                        <button className="tool-btn" onClick={handleZoomOut}><ZoomOut size={14} /></button>
                        <span className="zoom-level">{zoom}%</span>
                        <button className="tool-btn" onClick={handleZoomIn}><ZoomIn size={14} /></button>
                    </div>
                    <div className="toolbar-divider"></div>
                    <button className="tool-btn"><Download size={14} /></button>
                    <button className="tool-btn"><Maximize2 size={14} /></button>
                </div>
            </div>

            <div className="viewer-workspace">
                <button className="nav-page-btn left" onClick={handlePrevPage}><ChevronLeft size={24} /></button>

                <div
                    className="pdf-page-mock"
                    style={{
                        transform: `scale(${zoom / 100})`,
                        transformOrigin: 'top center',
                        transition: 'transform 0.2s ease'
                    }}
                >
                    <div className="page-content">
                        <h3>{page}.3 REGIONAL ENERGY OVERHEAD ANALYTICS</h3>
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
                        <p>This is dynamic content for page {page}. In a production environment, this would be an actual PDF canvas or SVG render.</p>
                        <div className="skeleton-line large"></div>
                        <div className="skeleton-line"></div>
                        <div className="skeleton-line medium"></div>
                    </div>
                </div>

                <button className="nav-page-btn right" onClick={handleNextPage}><ChevronRight size={24} /></button>
            </div>

            <div className="viewer-footer">
                <div className="metadata-badge">SOURCE_INTEGRITY: 1.0</div>
                <div className="metadata-badge">CASCADE_SYNC: VERIFIED</div>
            </div>
        </div>
    );
};

export default DocumentViewer;
