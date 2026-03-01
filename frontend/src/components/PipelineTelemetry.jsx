import React from 'react';
import { Search, Share2, Layers, Cpu, CheckCircle2 } from 'lucide-react';
import './PipelineTelemetry.css';

const stages = [
    { id: 'retrieving', label: 'HYBRID_RETRIEVAL', icon: Search },
    { id: 'fusing', label: 'RRF_FUSION', icon: Share2 },
    { id: 'reranking', label: 'CROSS_ENCODER_RERANK', icon: Layers },
    { id: 'packing', label: 'CONTEXT_PACKING', icon: Cpu },
];

const PipelineTelemetry = ({ activeStage, completedStages = [] }) => {
    return (
        <div className="pipeline-telemetry">
            <div className="telemetry-header">
                <span className="telemetry-title">RETR_PIPELINE_TRACE</span>
            </div>
            <div className="stages-container">
                {stages.map((stage, index) => {
                    const Icon = stage.icon;
                    const isActive = activeStage === stage.id;
                    const isCompleted = completedStages.includes(stage.id);

                    return (
                        <React.Fragment key={stage.id}>
                            <div className={`stage-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                                <div className="stage-icon-wrapper">
                                    {isCompleted ? <CheckCircle2 size={12} className="emerald" /> : <Icon size={12} />}
                                </div>
                                <span className="stage-label">{stage.label}</span>
                            </div>
                            {index < stages.length - 1 && <div className="stage-divider"></div>}
                        </React.Fragment>
                    );
                })}
            </div>
        </div>
    );
};

export default PipelineTelemetry;
