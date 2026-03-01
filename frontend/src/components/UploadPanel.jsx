import React, { useState } from 'react';
import { Upload, File, X, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import './UploadPanel.css';

const UploadPanel = () => {
    const [files, setFiles] = useState([
        { name: 'Strat_Final.pdf', status: 'completed', progress: 100 },
        { name: 'Infra_Ops.pdf', status: 'completed', progress: 100 },
        { name: 'Q1_Forecast_Draft.pdf', status: 'processing', progress: 45 },
        { name: 'Internal_Audit.xlsx', status: 'error', progress: 0, error: 'FILE_TYPE_NOT_SUPPORTED' },
    ]);

    return (
        <div className="upload-panel">
            <div className="dropzone">
                <Upload size={32} className="upload-icon" />
                <p className="dropzone-text">DRAG_AND_DROP_PDF_FOR_CASCADE_INDEXING</p>
                <button className="browse-btn">BROWSE_LOCAL_FILES</button>
            </div>

            <div className="ingestion-queue">
                <div className="queue-header">INGESTION_QUEUE_STATUS</div>
                <div className="queue-list">
                    {files.map((file, idx) => (
                        <div key={idx} className={`queue-item ${file.status}`}>
                            <File size={16} className="file-icon" />
                            <div className="file-info">
                                <span className="file-name">{file.name}</span>
                                {file.status === 'processing' && (
                                    <div className="progress-container">
                                        <div className="progress-bar" style={{ width: `${file.progress}%` }}></div>
                                    </div>
                                )}
                            </div>
                            <div className="file-status">
                                {file.status === 'completed' && <CheckCircle2 size={16} className="emerald" />}
                                {file.status === 'processing' && <Loader2 size={16} className="spin blue" />}
                                {file.status === 'error' && <AlertCircle size={16} className="amber" />}
                                <span className="status-label">{file.status.toUpperCase()}</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default UploadPanel;
