// src/views/AttackTimeline.jsx
import React, { useState } from 'react';
import ReportModal from '../components/ReportModal';

export default function AttackTimeline({ events, pipeline }) {
  const [showReport, setShowReport] = useState(false);
  const [sevFilter, setSevFilter] = useState('ALL');
  const [catFilter, setCatFilter] = useState('ALL');

  const filtered = events.filter(e => {
    const mSev = sevFilter === 'ALL' || e.severity.toUpperCase() === sevFilter;
    const mCat = catFilter === 'ALL' || e.category.toUpperCase() === catFilter;
    return mSev && mCat;
  });

  return (
    <section className="view-section active">
      <div className="timeline-header-bar">
        <div>
          <div style={{ fontSize: 16, fontWeight: 700, textTransform: 'uppercase' }}>Chronological Forensic Replay</div>
          <div className="font-mono" style={{ fontSize: 12, opacity: 0.6 }}>Target: dc-primary.corp.internal • Microsecond Precision Intercept</div>
        </div>
        <button className="btn btn-primary" onClick={() => setShowReport(true)}>
          Export Incident Report as PDF
        </button>
      </div>

      {/* 4-Stage Containment Pipeline */}
      <div className="containment-pipeline">
        <div className="pipeline-header">
          <div className="pipeline-title">Autonomous Containment Pipeline Execution</div>
          <div className="pipeline-latency">Total containment latency: {pipeline.totalDuration}</div>
        </div>

        <div className="pipeline-steps" style={{ position: 'relative' }}>
          <div className="pipeline-connector"></div>
          {pipeline.stages.map((stage, i) => (
            <div key={i} className="pipeline-step completed">
              <div className="step-node">{i + 1}</div>
              <div className="step-name">{stage.name}</div>
              <div className="step-time">{stage.time}</div>
              <span className="badge-tag accent" style={{ marginTop: 4, fontSize: 10 }}>{stage.note}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Microsecond Timeline Feed */}
      <div className="chronology-feed-wrapper">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20, borderBottom: 'var(--border-subtle)', paddingBottom: 12 }}>
          <div style={{ fontSize: 13, fontWeight: 700, textTransform: 'uppercase' }}>Microsecond Event Stream</div>
          <div style={{ display: 'flex', gap: 12 }}>
            <select className="select-custom font-mono" style={{ fontSize: 11 }} value={sevFilter} onChange={(e) => setSevFilter(e.target.value)}>
              <option value="ALL">ALL SEVERITIES</option>
              <option value="CRITICAL">CRITICAL ONLY</option>
              <option value="HIGH">HIGH ONLY</option>
            </select>
            <select className="select-custom font-mono" style={{ fontSize: 11 }} value={catFilter} onChange={(e) => setCatFilter(e.target.value)}>
              <option value="ALL">ALL CATEGORIES</option>
              <option value="EXECUTION">EXECUTION</option>
              <option value="DETECTION">DETECTION</option>
              <option value="CONTAINMENT">CONTAINMENT</option>
              <option value="EVICTION">EVICTION</option>
              <option value="ISOLATION">ISOLATION</option>
            </select>
          </div>
        </div>

        <div className="timeline-spine">
          {filtered.map(evt => {
            const isCrit = evt.severity === 'critical';
            return (
              <div key={evt.id} className="timeline-event-item">
                <div className={`event-dot ${isCrit ? 'critical' : 'high'}`}></div>
                <div className={`event-content ${isCrit ? 'sev-strip-critical' : 'sev-strip-high'}`}>
                  <div className="event-header">
                    <div className="event-action">
                      <span className={`sev-pill ${evt.severity}`}>{evt.severity}</span>
                      <span className="badge-tag">{evt.category}</span>
                      <span>{evt.action}</span>
                    </div>
                    <div className="event-iso-time font-mono">{evt.isoTimestamp}</div>
                  </div>
                  <div style={{ fontSize: 13, marginBottom: 8, opacity: 0.9 }}>{evt.details}</div>
                  <div className="event-body">
                    <div className="event-detail-item">
                      <span className="event-detail-label">Actor Process</span>
                      <span className="font-mono">{evt.process}</span>
                    </div>
                    <div className="event-detail-item">
                      <span className="event-detail-label">Parent PID</span>
                      <span className="font-mono">{evt.parentPid}</span>
                    </div>
                    <div className="event-detail-item">
                      <span className="event-detail-label">MITRE Technique</span>
                      <span className="badge-tag accent font-mono">{evt.mitre}</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {showReport && <ReportModal onClose={() => setShowReport(false)} />}
    </section>
  );
}
