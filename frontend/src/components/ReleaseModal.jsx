// src/components/ReleaseModal.jsx
import React from 'react';

export default function ReleaseModal({ hostname, onClose, onConfirm }) {
  return (
    <div className="modal-overlay open">
      <div className="modal-dialog">
        <div className="modal-header">
          <div className="modal-title">Confirm Host De-Isolation</div>
          <div className="modal-close" onClick={onClose}>×</div>
        </div>
        <div className="modal-body">
          <p style={{ marginBottom: 12 }}>
            You are about to release quarantined host <strong className="font-mono">{hostname}</strong> back into the fleet.
          </p>
          <div style={{ background: 'rgba(133, 57, 83, 0.15)', border: '1px solid var(--color-primary-accent)', padding: 12, borderRadius: 'var(--radius-sm)' }}>
            <strong>CRITICAL SAFETY WARNING:</strong> Verify that rogue parent processes have been terminated and decoy honeytokens recycled before rejoining.
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-outline" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" onClick={onConfirm}>Confirm & Release Host</button>
        </div>
      </div>
    </div>
  );
}
