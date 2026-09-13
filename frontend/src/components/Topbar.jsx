// src/components/Topbar.jsx
import React, { useState, useEffect } from 'react';

export default function Topbar({ pageTitle, pageSubtitle, onTriggerToast, onTriggerStack }) {
  const [utcTime, setUtcTime] = useState('');

  useEffect(() => {
    const update = () => {
      const now = new Date();
      const year = now.getUTCFullYear();
      const month = String(now.getUTCMonth() + 1).padStart(2, '0');
      const day = String(now.getUTCDate()).padStart(2, '0');
      const hours = String(now.getUTCHours()).padStart(2, '0');
      const minutes = String(now.getUTCMinutes()).padStart(2, '0');
      const seconds = String(now.getUTCSeconds()).padStart(2, '0');
      const millis = String(now.getUTCMilliseconds()).padStart(3, '0');
      const micros = String(Math.floor((performance.now() * 100) % 1000)).padStart(3, '0');

      setUtcTime(`${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${millis}${micros}Z`);
    };

    update();
    const interval = setInterval(update, 65);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="topbar">
      <div className="topbar-left">
        <div className="page-title">{pageTitle}</div>
        <div className="page-subtitle">{pageSubtitle}</div>
      </div>

      <div className="topbar-right">
        <div className="system-status-pill">
          <span className="status-beacon"></span>
          <span>3 Active Agents Online</span>
        </div>

        <div className="utc-clock">
          <span className="utc-label">UTC</span>
          <span>{utcTime}</span>
        </div>

        <div className="topbar-actions">
          <button className="topbar-btn" onClick={onTriggerToast} title="Simulate real-time high priority intrusion alert">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            Simulate Inbound Alert
          </button>
          <button className="topbar-btn" onClick={onTriggerStack} title="Simulate alert burst to test toast stacking">
            Simulate Alert Stack
          </button>
        </div>
      </div>
    </header>
  );
}
