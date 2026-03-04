import React, { useState } from 'react';
import { Command, Search, Filter } from 'lucide-react';
import './QueryPanel.css';

const QueryPanel = ({ onSearch, isLoading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            onSearch(query);
        }
    };

    return (
        <div className="query-panel">
            <form className="query-form" onSubmit={handleSubmit}>
                <div className="query-input-wrapper">
                    <Command size={16} className="terminal-icon" />
                    <input
                        type="text"
                        className="query-input"
                        placeholder="Query knowledge corpus..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        disabled={isLoading}
                        autoFocus
                    />
                    <div className="shortcut-badge">⌘K</div>
                </div>

                <div className="query-actions">
                    <button type="button" className="action-btn">
                        <Filter size={14} />
                        <span>FILTERS</span>
                    </button>
                    <div className="action-divider"></div>
                    <button type="submit" className="search-btn" disabled={isLoading || !query.trim()}>
                        <Search size={14} />
                        <span>EXECUTE</span>
                    </button>
                </div>
            </form>
        </div>
    );
};

export default QueryPanel;
