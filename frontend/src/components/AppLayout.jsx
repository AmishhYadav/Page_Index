import React from 'react';
import {
    BarChart3,
    Upload,
    Search,
    FileText,
    Settings,
    Terminal,
    Activity,
    ShieldCheck
} from 'lucide-react';
import './AppLayout.css';

const navItems = [
    { id: 'dashboard', label: 'DASHBOARD', icon: BarChart3 },
    { id: 'ingest', label: 'INGEST DOCUMENTS', icon: Upload },
    { id: 'search', label: 'KNOWLEDGE SEARCH', icon: Search },
    { id: 'viewer', label: 'DOCUMENT VIEWER', icon: FileText },
];

const AppLayout = ({ children, activeTab, onTabChange }) => {
    return (
        <div className="app-layout">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="sidebar-header">
                    <Terminal size={20} className="logo-icon" />
                    <span className="logo-text">PAGEINDEX</span>
                </div>

                <nav className="nav-group">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        return (
                            <button
                                key={item.id}
                                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                                onClick={() => onTabChange(item.id)}
                            >
                                <Icon size={18} />
                                <span>{item.label}</span>
                            </button>
                        );
                    })}
                </nav>

                <div className="sidebar-footer">
                    <button
                        className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
                        onClick={() => onTabChange('settings')}
                    >
                        <Settings size={18} />
                        <span>SETTINGS</span>
                    </button>
                </div>
            </aside>

            {/* Main Workspace */}
            <main className="workspace">
                {/* Header Telemetry */}
                <header className="header">
                    <div className="telemetry-item">
                        <span className="telemetry-label">DOCS</span>
                        <span className="telemetry-value">842.00</span>
                    </div>
                    <div className="telemetry-divider"></div>
                    <div className="telemetry-item">
                        <span className="telemetry-label">INDEX_NODES</span>
                        <span className="telemetry-value">12.4K</span>
                    </div>
                    <div className="telemetry-divider"></div>
                    <div className="telemetry-item">
                        <span className="telemetry-label">INTEGRITY</span>
                        <span className="telemetry-value emerald">99.85%</span>
                    </div>
                    <div className="telemetry-divider"></div>
                    <div className="telemetry-item">
                        <span className="telemetry-label">LATENCY_P99</span>
                        <span className="telemetry-value">412ms</span>
                    </div>

                    <div className="header-spacer"></div>

                    <div className="status-indicator">
                        <Activity size={14} className="status-icon" />
                        <span>SYSTEM_READY</span>
                    </div>
                </header>

                {/* Content Area */}
                <div className="content">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default AppLayout;
