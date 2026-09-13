// src/views/Overview.jsx
import React from 'react';
import TelemetryChart from '../components/TelemetryChart';

export default function Overview({ data, onInspectDossier, onViewAllAlerts }) {
  return (
    <section className="view-section active">
      {/* Top 2 Metric Cards */}
      <div className="overview-stats-grid">
        <div className="metric-card sev-strip-critical">
          <div className="metric-header">
            <span className="metric-label">Active Threats</span>
            <span className="metric-indicator critical"></span>
          </div>
          <div className="metric-value">3</div>
          <div className="metric-subtext">
            <span className="highlight">2 Critical</span> • 1 High Priority
          </div>
        </div>

        <div className="metric-card sev-strip-medium">
          <div className="metric-header">
            <span className="metric-label">Threats Contained Today</span>
            <span className="metric-indicator nominal"></span>
          </div>
          <div className="metric-value">14</div>
          <div className="metric-subtext">
            <span className="highlight">100% Automated</span> Containment Rate
          </div>
        </div>
      </div>

      {/* 24-Hour Telemetry Chart */}
      <div className="chart-container">
        <div className="chart-header">
          <div className="chart-title-area">
            <div className="chart-title">24-Hour Threat Activity Telemetry</div>
            <span className="badge-tag font-mono">HOURLY INCIDENT FREQUENCY</span>
          </div>
          <div className="chart-legend">
            <div className="legend-item">
              <span className="legend-swatch"></span>
              <span>Autonomous Deception Intercepts (#853953)</span>
            </div>
          </div>
        </div>
        <TelemetryChart data={data.telemetry24h} />
      </div>

      {/* Active Threats Table */}
      <div className="overview-table-section">
        <div className="section-header-row">
          <div className="section-title">Priority Threat Incidents Requiring Analyst Triage</div>
          <button className="btn btn-primary btn-sm" onClick={onViewAllAlerts}>
            View All Live Alerts →
          </button>
        </div>

        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Severity</th>
                <th>Alert ID</th>
                <th>Attack Vector</th>
                <th>Target Host</th>
                <th>Source IP</th>
                <th>Honeytoken Bait Tripped</th>
                <th>Immediate Action</th>
              </tr>
            </thead>
            <tbody>
              {data.alerts.slice(0, 3).map(alert => (
                <tr 
                  key={alert.id} 
                  className={alert.severity === 'critical' ? 'sev-strip-critical' : 'sev-strip-high'}
                  onClick={() => onInspectDossier(alert.caseKey)}
                >
                  <td><span className={`sev-pill ${alert.severity}`}>{alert.severityLabel}</span></td>
                  <td className="font-mono" style={{ fontWeight: 700 }}>{alert.id}</td>
                  <td>{alert.attackType}</td>
                  <td className="font-mono">{alert.hostname}</td>
                  <td className="font-mono">{alert.sourceIp}</td>
                  <td><span className="badge-tag accent font-mono">{alert.baitTrigger}</span></td>
                  <td>
                    <button className="btn btn-primary btn-sm">Inspect Dossier →</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
