// src/components/ReportModal.jsx
import React from 'react';

export default function ReportModal({ onClose }) {
  return (
    <div className="modal-overlay open">
      <div className="modal-dialog modal-lg">
        <div className="modal-header">
          <div className="modal-title">Executive Incident Containment Summary</div>
          <div className="modal-close" onClick={onClose}>×</div>
        </div>
        <div className="modal-body">
          <div style={{ background: 'rgba(243, 244, 244, 0.02)', border: 'var(--border-subtle)', padding: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '2px solid var(--color-primary-accent)', paddingBottom: 12, marginBottom: 16 }}>
              <div>
                <h2 style={{ fontSize: 18, fontWeight: 800 }}>HONEYTRAP AUTONOMOUS CONTAINMENT REPORT</h2>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'rgba(243, 244, 244, 0.6)' }}>
                  INCIDENT REF: INC-2026-ALT-9042 // DECEPTION TRIPWIRE
                </div>
              </div>
              <span className="sev-pill critical">CRITICAL SEVERITY</span>
            </div>

            <p style={{ fontSize: 13, lineHeight: 1.6, marginBottom: 14 }}>
              On 2026-09-12 at 21:04:12.894210Z, external adversary from <strong>185.220.101.5</strong> executed a reverse shell payload targeting deception bait token <em>aws_secret_key_decoy_prod</em> on <code>dc-primary.corp.internal</code>.
              Autonomous containment quarantined the threat in <strong>412 microseconds</strong> without data compromise.
            </p>

            <div style={{ background: '#1c1c1c', padding: 12, fontFamily: 'var(--font-mono)', fontSize: 11, lineHeight: 1.6, border: 'var(--border-subtle)' }}>
              <div>EVIDENCE_SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</div>
              <div>KERNEL_CONTAINMENT_SIG: ED25519-7F89B210A87C3349D0E1F429A1009941BC88432A99B812</div>
              <div>TOTAL_LATENCY: 412ms</div>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-outline" onClick={onClose}>Close</button>
          <button className="btn btn-primary" onClick={() => window.print()}>Print / Save as PDF</button>
        </div>
      </div>
    </div>
  );
}
