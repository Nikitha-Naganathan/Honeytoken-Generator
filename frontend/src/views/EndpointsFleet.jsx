// src/views/EndpointsFleet.jsx
import React, { useState } from 'react';

export default function EndpointsFleet({ endpoints, onIsolate, onRestore }) {
  const [filter, setFilter] = useState('ALL');

  const total = endpoints.length;
  const healthy = endpoints.filter(e => e.status === 'HEALTHY').length;
  const isolated = endpoints.filter(e => e.isolated).length;
  const tokens = endpoints.reduce((acc, e) => acc + e.honeytokenCount, 0);

  const filtered = endpoints.filter(e => filter === 'ALL' || e.status === filter);

  return (
    <section className="view-section active">
      {/* Top Summary Pills */}
      <div className="fleet-summary-grid">
        <div className="fleet-stat-pill sev-strip-critical">
          <div className="stat-pill-info">
            <span className="stat-pill-title">Total Agents</span>
            <span className="stat-pill-num">{total}</span>
          </div>
        </div>
        <div className="fleet-stat-pill sev-strip-low">
          <div className="stat-pill-info">
            <span className="stat-pill-title">Healthy Agents</span>
            <span className="stat-pill-num">{healthy}</span>
          </div>
        </div>
        <div className="fleet-stat-pill sev-strip-high">
          <div className="stat-pill-info">
            <span className="stat-pill-title">Isolated Endpoints</span>
            <span className="stat-pill-num">{isolated}</span>
          </div>
        </div>
        <div className="fleet-stat-pill sev-strip-medium">
          <div className="stat-pill-info">
            <span className="stat-pill-title">Deployed Honeytokens</span>
            <span className="stat-pill-num">{tokens}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ marginBottom: 16 }}>
        <div className="tab-group">
          {['ALL', 'COMPROMISED', 'CONTAINED', 'HEALTHY'].map(s => (
            <button key={s} className={`tab-btn ${filter === s ? 'active' : ''}`} onClick={() => setFilter(s)}>
              {s}
            </button>
          ))}
        </div>
      </div>

      {/* Fleet Table */}
      <div className="fleet-table-panel">
        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Endpoint & ID</th>
                <th>OS / Arch</th>
                <th>IP & MAC</th>
                <th>Agent Version</th>
                <th>Deployed Honeytokens</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(ep => {
                const isCrit = ep.status === 'COMPROMISED';
                const isCont = ep.status === 'CONTAINED' || ep.status === 'ISOLATED';
                return (
                  <tr key={ep.id} className={isCrit ? 'sev-strip-critical' : isCont ? 'sev-strip-high' : 'sev-strip-low'}>
                    <td>
                      <div style={{ fontWeight: 700 }}>{ep.hostname}</div>
                      <div style={{ fontSize: 11, opacity: 0.5 }}>{ep.id}</div>
                    </td>
                    <td style={{ fontSize: 12 }}>{ep.os}</td>
                    <td className="font-mono">
                      <div>{ep.ip}</div>
                      <div style={{ fontSize: 10, opacity: 0.5 }}>{ep.mac}</div>
                    </td>
                    <td><span className="badge-tag font-mono">{ep.agentVersion}</span></td>
                    <td>
                      <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                        {ep.honeytokens.map((tok, i) => (
                          <span key={i} className="badge-tag accent font-mono" style={{ fontSize: 10 }}>{tok}</span>
                        ))}
                      </div>
                    </td>
                    <td>
                      <span className={`sev-pill ${isCrit ? 'critical' : isCont ? 'high' : 'low'}`}>{ep.status}</span>
                    </td>
                    <td>
                      {ep.isolated ? (
                        <button className="btn btn-outline btn-sm" onClick={() => onRestore(ep.hostname)}>Restore Host</button>
                      ) : (
                        <button className="btn btn-primary btn-sm" onClick={() => onIsolate(ep.id)}>Isolate</button>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
