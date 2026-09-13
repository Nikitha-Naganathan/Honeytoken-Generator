// src/views/AlertsFeed.jsx
import React, { useState } from 'react';

export default function AlertsFeed({ alerts, onInspectDossier, onIsolateHost, onReleaseHost, onBlockIp }) {
  const [search, setSearch] = useState('');
  const [sevFilter, setSevFilter] = useState('ALL');
  const [sort, setSort] = useState('newest');
  const [expandedAlerts, setExpandedAlerts] = useState(new Set());

  const toggleExpand = (id) => {
    setExpandedAlerts(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const filtered = alerts.filter(a => {
    const matchSev = sevFilter === 'ALL' || a.severity.toUpperCase() === sevFilter;
    const q = search.toLowerCase();
    const matchSearch = !q || a.id.toLowerCase().includes(q) || a.hostname.toLowerCase().includes(q) || a.sourceIp.includes(q) || a.attackType.toLowerCase().includes(q);
    return matchSev && matchSearch;
  });

  return (
    <section className="view-section active">
      {/* Search & Filter Bar */}
      <div className="alerts-controls-bar">
        <div className="alerts-filter-left">
          <div className="search-wrapper" style={{ flex: 1 }}>
            <input 
              type="text" 
              className="input-search font-mono" 
              placeholder="Search by IP, hash, hostname, attack vector..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="tab-group">
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM'].map(s => (
              <button
                key={s}
                className={`tab-btn ${sevFilter === s ? 'active' : ''}`}
                onClick={() => setSevFilter(s)}
              >
                {s}
              </button>
            ))}
          </div>
        </div>

        <div className="alerts-filter-right">
          <select className="select-custom font-mono" value={sort} onChange={(e) => setSort(e.target.value)}>
            <option value="newest">Newest First</option>
            <option value="severity">Highest Severity</option>
          </select>
        </div>
      </div>

      {/* Alert Cards */}
      <div className="alerts-feed">
        {filtered.map(a => {
          const isExp = expandedAlerts.has(a.id);
          const isCrit = a.severity === 'critical';

          return (
            <div key={a.id} className={`alert-card ${isCrit ? 'sev-strip-critical' : 'sev-strip-high'} ${isExp ? 'expanded' : ''}`}>
              <div className="alert-card-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className={`sev-pill ${a.severity}`}>{a.severityLabel}</span>
                  <span className="alert-id">{a.id}</span>
                </div>
                <div className="font-mono alert-time" style={{ fontSize: 11, color: 'rgba(243, 244, 244, 0.65)' }}>
                  {a.timestamp.slice(11, 23)} UTC
                </div>
                <div>
                  <div className="alert-type">{a.attackType}</div>
                  <div className="alert-bait font-mono" style={{ fontSize: 11, opacity: 0.7 }}>
                    {a.baitTrigger}
                  </div>
                </div>
                <div className="font-mono">{a.hostname}</div>
                <div className="font-mono">{a.sourceIp}</div>
                <div className="alert-card-actions">
                  <button className="btn btn-outline btn-sm" onClick={() => toggleExpand(a.id)}>
                    {isExp ? 'Hide Forensics ↑' : 'View Forensics ↓'}
                  </button>
                  {a.hostIsolated ? (
                    <button className="btn btn-outline btn-sm" onClick={() => onReleaseHost(a.hostname)}>Release Host</button>
                  ) : (
                    <button className="btn btn-primary btn-sm" onClick={() => onIsolateHost(a.hostname)}>Isolate Host</button>
                  )}
                  <button className="btn btn-secondary btn-sm" onClick={() => onInspectDossier(a.caseKey)}>
                    Attacker Info →
                  </button>
                </div>
              </div>

              {/* Sliding Forensics Drawer */}
              <div className="forensics-drawer">
                <div className="forensics-grid">
                  <div>
                    <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'rgba(243, 244, 244, 0.5)', marginBottom: 8 }}>
                      Process Execution Hierarchy
                    </div>
                    <div className="tree-view">
                      {a.forensics.processTree.map((n, i) => (
                        <div key={i} className="tree-node">
                          {'    '.repeat(n.level)}
                          {n.level > 0 && <span className="tree-branch">└── </span>}
                          <span style={n.critical ? { color: '#F3F4F4', fontWeight: 700 } : {}}>{n.name}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="forensic-field-list">
                    <div className="field-row">
                      <span className="field-label">Parent PID</span>
                      <span className="field-val font-mono">{a.forensics.parentPid} ({a.forensics.parentProcess})</span>
                    </div>
                    <div className="field-row">
                      <span className="field-label">Binary Path</span>
                      <span className="field-val font-mono" style={{ fontSize: 11 }}>{a.forensics.fullPath}</span>
                    </div>
                    <div className="field-row">
                      <span className="field-label">SHA-256</span>
                      <span className="field-val font-mono" style={{ fontSize: 11 }}>{a.forensics.sha256}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
