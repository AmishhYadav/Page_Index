import React, { useState, useRef } from 'react';
import { Upload, File as FileIcon, X, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';
import './UploadPanel.css';

const UploadPanel = () => {
    const [files, setFiles] = useState([
        { name: 'Strat_Final.pdf', status: 'completed', progress: 100 },
        { name: 'Infra_Ops.pdf', status: 'completed', progress: 100 },
    ]);
    const fileInputRef = useRef(null);

    const handleFileUpload = async (e) => {
        const selectedFile = e.target.files[0];
        if (!selectedFile) return;

        const newFile = {
            name: selectedFile.name,
            status: 'processing',
            progress: 0
        };

        setFiles(prev => [newFile, ...prev]);

        // Real API Call
        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            // Simulated progress because XHR is needed for real progress, 
            // but we'll use a fetch for simplicity with the backend contract.
            const response = await fetch('/api/v1/documents/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('UPLOAD_FAILED');

            setFiles(prev => prev.map(f =>
                f.name === selectedFile.name ? { ...f, status: 'completed', progress: 100 } : f
            ));
        } catch (error) {
            console.error("Upload Error:", error);
            setFiles(prev => prev.map(f =>
                f.name === selectedFile.name ? { ...f, status: 'error', error: 'SYSTEM_ERROR' } : f
            ));
        }
    };

    return (
        <div className="upload-panel">
            <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept=".pdf"
                onChange={handleFileUpload}
            />
            <div
                className="dropzone"
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                    e.preventDefault();
                    handleFileUpload({ target: { files: e.dataTransfer.files } });
                }}
            >
                <Upload size={32} className="upload-icon" />
                <p className="dropzone-text">DRAG_AND_DROP_PDF_FOR_CASCADE_INDEXING</p>
                <button
                    className="browse-btn"
                    onClick={() => fileInputRef.current.click()}
                >
                    BROWSE_LOCAL_FILES
                </button>
            </div>

            <div className="ingestion-queue">
                <div className="queue-header">INGESTION_QUEUE_STATUS</div>
                <div className="queue-list">
                    {files.map((file, idx) => (
                        <div key={idx} className={`queue-item ${file.status}`}>
                            <FileIcon size={16} className="file-icon" />
                            <div className="file-info">
                                <span className="file-name">{file.name}</span>
                                {file.status === 'processing' && (
                                    <div className="progress-container">
                                        <div className="progress-bar progress-spin"></div>
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
