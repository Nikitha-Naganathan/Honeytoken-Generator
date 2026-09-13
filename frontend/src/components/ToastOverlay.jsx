// src/components/ToastOverlay.jsx
import React, { useState } from 'react';

export default function ToastOverlay({ toasts, onDismiss, onViewDossier }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const maxVisible = 3;

  const visibleToasts = isExpanded ? toasts : toasts.slice(0, maxVisible);
  const hiddenCount = toasts.length - visibleToasts.length;

  return (
    <div className="toast-container">
      {visibleToasts.map((toast, index) => {
        const isCrit = toast.severity === 'critical' || toast.severity === 'high';
        const offsetStyle = !isExpanded && index > 0 
          ? { transform: `scale(${1 - index * 0.03})`, opacity: 1 - index * 0.15, marginTop: -8 }
          : {};

        return (
          <div
            key={toast.id}
            className={`toast-card ${isCrit ? 'toast-critical' : 'toast-medium'}`}
            style={offsetStyle}
          >
            <div className="toast-content">
              <div className="toast-header">
                <div className="toast-meta">
                  <span className="toast-badge">{toast.severity}</span>
                  <span className="toast-time">{toast.timestamp}</span>
                </div>
                <span className="toast-close" onClick={() => onDismiss(toast.id)}>×</span>
              </div>
              <div className="toast-title">{toast.title}</div>
              <div className="toast-details">
                <div><strong>Target:</strong> <span className="font-mono">{toast.endpoint}</span></div>
                <div><strong>Source:</strong> <span className="font-mono">{toast.sourceIp}</span></div>
                <div style={{ opacity: 0.85, marginTop: 2 }}>{toast.details}</div>
              </div>
              <div className="toast-actions">
                <button
                  className="toast-action-btn"
                  onClick={() => onViewDossier(toast.caseKey)}
                >
                  View Dossier →
                </button>
              </div>
            </div>
            {!isCrit && <div className="toast-progress"></div>}
          </div>
        );
      })}

      {(hiddenCount > 0 || (isExpanded && toasts.length > maxVisible)) && (
        <div
          className="toast-stack-counter"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? 'Collapse Stack ↑' : `+${hiddenCount} more alerts ↓`}
        </div>
      )}
    </div>
  );
}
