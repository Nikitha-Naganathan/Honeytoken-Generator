// src/views/AttackerInfo.jsx
import React, { useState } from 'react';
import CityVectorMap from '../components/CityVectorMap';

export default function AttackerInfo({ dossiers, activeCase, onCaseChange, blockedLedger, onBlockIp, onSeverSubnet, onReseed }) {
  const [copied, setCopied] = useState(false);
  const d = dossiers[activeCase];

  const handleCopy = () => {
    navigator.clipboard.writeText(d.sourceIp);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <section className="view-section active">
      {/* Case Switcher Tabs */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, background: 'var(--surface-panel)', border: 'var(--border-subtle)', padding: '12px 18px' }}>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
          <span style={{ fontSize: 12, fontWeight: 700, color: 'rgba(243, 244, 244, 0.6)' }}>INVESTIGATION DOSSIER:</span>
          <div className="tab-group">
            <button className={`tab-btn ${activeCase === 'CASE_A' ? 'active' : ''}`} onClick={() => onCaseChange('CASE_A')}>
              CASE A: Public IP Adversary (185.220.101.5)
            </button>
            <button className={`tab-btn ${activeCase === 'CASE_B' ? 'active' : ''}`} onClick={() => onCaseChange('CASE_B')}>
              CASE B: Internal RFC 1918 Lateral (192.168.1.27)
            </button>
          </div>
        </div>
        <span className={`badge-tag ${d.isPublic ? 'accent' : 'secondary'}`}>
          {d.isPublic ? 'CASE A: PUBLIC THREAT INTEL' : 'CASE B: INTERNAL RFC 1918 LATERAL'}
        </span>
      </div>

      {/* 68% / 32% Asymmetric Layout */}
      <div className="attacker-layout">
        {/* Left 68% Panel */}
        <div className="attacker-dossier-panel">
          <div className="dossier-header-bar">
            <div>
              <div className="dossier-title">Adversary Intelligence Dossier</div>
              <span className="font-mono" style={{ fontSize: 12, opacity: 0.7 }}>{d.type}</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span className="font-mono" style={{ fontSize: 16, fontWeight: 700 }}>{d.sourceIp}</span>
              <button className="copy-btn" onClick={handleCopy}>
                {copied ? '✓ COPIED' : 'COPY'}
              </button>
            </div>
          </div>

          <div className="dossier-grid">
            <div className="dossier-card">
              <div className="dossier-card-title">Attribution & Threat Actor</div>
              <div className="dossier-rows">
                <div className="dossier-row"><span className="dossier-k">Actor Group</span><span className="dossier-v">{d.threatGroup}</span></div>
                <div className="dossier-row"><span className="dossier-k">Confidence</span><span className="dossier-v font-mono">{d.confidenceScore}</span></div>
                <div className="dossier-row"><span className="dossier-k">MITRE ID</span><span className="badge-tag accent font-mono">{d.mitreTechnique}</span></div>
              </div>
            </div>

            <div className="dossier-card">
              <div className="dossier-card-title">Network Infrastructure</div>
              <div className="dossier-rows">
                <div className="dossier-row"><span className="dossier-k">Autonomous System / Net</span><span className="dossier-v font-mono">{d.isPublic ? d.asn : `MAC: ${d.macAddress}`}</span></div>
                <div className="dossier-row"><span className="dossier-k">Provider / VLAN</span><span className="dossier-v">{d.isPublic ? d.isp : d.vlanId}</span></div>
                <div className="dossier-row"><span className="dossier-k">Coordinates</span><span className="dossier-v font-mono">{d.coordinates}</span></div>
              </div>
            </div>

            <div className="dossier-card" style={{ gridColumn: 'span 2' }}>
              <div className="dossier-card-title">Targeted Deception Bait & Physical Location</div>
              <div className="dossier-rows">
                <div className="dossier-row"><span className="dossier-k">Target Asset</span><span className="dossier-v font-mono">{d.targetedAsset}</span></div>
                <div className="dossier-row"><span className="dossier-k">Honeytoken</span><span className="badge-tag accent font-mono">{d.baitTriggered}</span></div>
                <div className="dossier-row"><span className="dossier-k">Location</span><span className="dossier-v">{d.isPublic ? d.geolocation : d.physicalLocation}</span></div>
              </div>
            </div>
          </div>

          <div className="attacker-action-bar">
            <button className="btn btn-primary" onClick={() => onBlockIp(d.sourceIp)}>Block IP at Perimeter Firewall</button>
            <button className="btn btn-secondary" onClick={onSeverSubnet}>Sever Subnet Routing</button>
            <button className="btn btn-outline" onClick={onReseed}>Trigger Decoy Reseed</button>
          </div>
        </div>

        {/* Right 32% Map Panel */}
        <div className="attacker-map-panel">
          <div className="map-header">
            <div className="map-title">{d.mapCity}</div>
            <div className="map-coords font-mono">{d.coordinates}</div>
          </div>
          <div className="map-canvas-container">
            <div className="map-hud-overlay font-mono">PRECISION SATELLITE VECTOR MESH</div>
            <CityVectorMap caseKey={activeCase} />
          </div>
        </div>
      </div>

      {/* Blocked Ledger Table */}
      <div className="blocked-ledger-panel">
        <div className="section-title" style={{ marginBottom: 14 }}>Recently Blocked Adversary IPs</div>
        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Timestamp (UTC)</th>
                <th>Source IP</th>
                <th>CIDR</th>
                <th>Rule</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {blockedLedger.map((item, i) => (
                <tr key={i} className="sev-strip-critical">
                  <td className="font-mono" style={{ fontSize: 11 }}>{item.timestamp}</td>
                  <td className="font-mono" style={{ fontWeight: 700 }}>{item.ip}</td>
                  <td className="font-mono">{item.cidr}</td>
                  <td style={{ fontSize: 12 }}>{item.triggerRule}</td>
                  <td><span className="badge-tag accent font-mono" style={{ fontSize: 10 }}>{item.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
