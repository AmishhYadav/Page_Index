import React from 'react';
import { Sliders, Database, Key, Shield, Globe } from 'lucide-react';
import './Settings.css';

const Settings = () => {
    return (
        <div className="settings-view">
            <div className="settings-section">
                <div className="section-header">
                    <Sliders size={14} className="blue" />
                    <span>INFERENCE_PARAMETERS</span>
                </div>
                <div className="settings-grid">
                    <div className="setting-item">
                        <span className="setting-label">MODEL_TEMPERATURE</span>
                        <input type="range" className="setting-range" />
                        <span className="setting-value">0.12</span>
                    </div>
                    <div className="setting-item">
                        <span className="setting-label">TOP_P_SAMPLING</span>
                        <input type="range" className="setting-range" />
                        <span className="setting-value">0.95</span>
                    </div>
                </div>
            </div>

            <div className="settings-section">
                <div className="section-header">
                    <Database size={14} className="blue" />
                    <span>ALGORITHM_CONFIGURATION</span>
                </div>
                <div className="settings-grid">
                    <div className="setting-item">
                        <span className="setting-label">DENSE_RELEVANCE_WEIGHT</span>
                        <input type="range" className="setting-range" />
                        <span className="setting-value">0.85</span>
                    </div>
                    <div className="setting-item">
                        <span className="setting-label">RERANK_THRESHOLD</span>
                        <input type="range" className="setting-range" />
                        <span className="setting-value">0.65</span>
                    </div>
                </div>
            </div>

            <div className="settings-section">
                <div className="section-header">
                    <Shield size={14} className="emerald" />
                    <span>INTEGRITY_ENFORCEMENT</span>
                </div>
                <div className="toggle-group">
                    <div className="toggle-item">
                        <span>STRICT_CITATION_VERIFICATION</span>
                        <div className="toggle active"></div>
                    </div>
                    <div className="toggle-item">
                        <span>AUTOMATIC_MANUAL_OVERRIDE_FLAG</span>
                        <div className="toggle"></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
