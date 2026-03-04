import React from 'react';
import {
    BarChart3,
    Activity,
    Database,
    Cpu,
    Clock,
    ShieldCheck,
    TrendingUp,
    AlertTriangle
} from 'lucide-react';
import './Dashboard.css';

const Dashboard = () => {
    return (
        <div className="dashboard-view">
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-header">
                        <Database size={14} className="blue" />
                        <span>TOTAL_KNOWLEDGE_NODES</span>
                    </div>
                    <div className="stat-value">12,482</div>
                    <div className="stat-footer">
                        <TrendingUp size={12} className="emerald" />
                        <span className="emerald">+12.4%</span>
                        <span className="footer-label">vs LAST_WEEK</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-header">
                        <Activity size={14} className="blue" />
                        <span>AVG_RETRIEVAL_LATENCY</span>
                    </div>
                    <div className="stat-value">342ms</div>
                    <div className="stat-footer">
                        <Clock size={12} />
                        <span className="footer-label">P99: 412ms</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-header">
                        <ShieldCheck size={14} className="emerald" />
                        <span>MEAN_CITATION_INTEGRITY</span>
                    </div>
                    <div className="stat-value">99.4%</div>
                    <div className="stat-footer">
                        <span className="emerald">HIGH_PRECISION</span>
                    </div>
                </div>

                <div className="stat-card">
                    <div className="stat-header">
                        <Cpu size={14} className="blue" />
                        <span>TOKEN_ROI_EFFICIENCY</span>
                    </div>
                    <div className="stat-value">0.84</div>
                    <div className="stat-footer">
                        <span className="footer-label">THRESHOLD: 0.70</span>
                    </div>
                </div>
            </div>

            <div className="charts-area">
                <div className="chart-panel">
                    <div className="panel-header">KNOWLEDGE_DISTRIBUTION_TRENDS</div>
                    <div className="chart-mock">
                        <div className="bar" style={{ height: '40%' }}></div>
                        <div className="bar" style={{ height: '60%' }}></div>
                        <div className="bar" style={{ height: '45%' }}></div>
                        <div className="bar" style={{ height: '70%' }}></div>
                        <div className="bar active" style={{ height: '90%' }}></div>
                        <div className="bar" style={{ height: '65%' }}></div>
                        <div className="bar" style={{ height: '50%' }}></div>
                    </div>
                </div>

                <div className="chart-panel">
                    <div className="panel-header">ANOMALY_DETECTION_LOG</div>
                    <div className="anomaly-list">
                        <div className="anomaly-item">
                            <AlertTriangle size={14} className="amber" />
                            <div className="anomaly-info">
                                <span className="anomaly-id">Q-842</span>
                                <span className="anomaly-desc">Low integrity signal (0.64) detected in Finance_v2</span>
                            </div>
                        </div>
                        <div className="anomaly-item">
                            <AlertTriangle size={14} className="amber" />
                            <div className="anomaly-info">
                                <span className="anomaly-id">Q-838</span>
                                <span className="anomaly-desc">Cross-encoder validation failed for Citation #4</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
