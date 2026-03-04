import React, { useState } from 'react';
import { Sliders, Database, Key, Shield, Globe } from 'lucide-react';
import './Settings.css';

const Settings = () => {
    const [config, setConfig] = useState({
        modelTemperature: 0.12,
        topPSampling: 0.95,
        denseRelevanceWeight: 0.85,
        rerankThreshold: 0.65,
        strictVerification: true,
        autoOverride: false
    });

    const handleChange = (key, value) => {
        setConfig(prev => ({ ...prev, [key]: parseFloat(value) }));
    };

    const toggleBoolean = (key) => {
        setConfig(prev => ({ ...prev, [key]: !prev[key] }));
    };

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
                        <input
                            type="range"
                            className="setting-range"
                            min="0" max="1" step="0.01"
                            value={config.modelTemperature}
                            onChange={(e) => handleChange('modelTemperature', e.target.value)}
                        />
                        <span className="setting-value">{config.modelTemperature.toFixed(2)}</span>
                    </div>
                    <div className="setting-item">
                        <span className="setting-label">TOP_P_SAMPLING</span>
                        <input
                            type="range"
                            className="setting-range"
                            min="0" max="1" step="0.01"
                            value={config.topPSampling}
                            onChange={(e) => handleChange('topPSampling', e.target.value)}
                        />
                        <span className="setting-value">{config.topPSampling.toFixed(2)}</span>
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
                        <input
                            type="range"
                            className="setting-range"
                            min="0" max="1" step="0.01"
                            value={config.denseRelevanceWeight}
                            onChange={(e) => handleChange('denseRelevanceWeight', e.target.value)}
                        />
                        <span className="setting-value">{config.denseRelevanceWeight.toFixed(2)}</span>
                    </div>
                    <div className="setting-item">
                        <span className="setting-label">RERANK_THRESHOLD</span>
                        <input
                            type="range"
                            className="setting-range"
                            min="0" max="1" step="0.01"
                            value={config.rerankThreshold}
                            onChange={(e) => handleChange('rerankThreshold', e.target.value)}
                        />
                        <span className="setting-value">{config.rerankThreshold.toFixed(2)}</span>
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
                        <div
                            className={`toggle ${config.strictVerification ? 'active' : ''}`}
                            onClick={() => toggleBoolean('strictVerification')}
                        ></div>
                    </div>
                    <div className="toggle-item">
                        <span>AUTOMATIC_MANUAL_OVERRIDE_FLAG</span>
                        <div
                            className={`toggle ${config.autoOverride ? 'active' : ''}`}
                            onClick={() => toggleBoolean('autoOverride')}
                        ></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
