// src/components/TelemetryChart.jsx
import React, { useState, useRef } from 'react';

export default function TelemetryChart({ data }) {
  const [activePoint, setActivePoint] = useState(null);
  const wrapperRef = useRef(null);

  const width = 800;
  const height = 220;
  const pad = { top: 20, right: 30, bottom: 35, left: 45 };
  const plotW = width - pad.left - pad.right;
  const plotH = height - pad.top - pad.bottom;

  const maxVal = Math.max(...data.map(d => d.count), 25);
  const points = data.map((d, i) => ({
    x: pad.left + (i / (data.length - 1)) * plotW,
    y: pad.top + plotH - (d.count / maxVal) * plotH,
    data: d
  }));

  const lineD = points.reduce((acc, pt, i) => (
    i === 0 ? `M ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}` : `${acc} L ${pt.x.toFixed(1)} ${pt.y.toFixed(1)}`
  ), '');

  const areaD = `${lineD} L ${points[points.length - 1].x.toFixed(1)} ${pad.top + plotH} L ${points[0].x.toFixed(1)} ${pad.top + plotH} Z`;

  const handleMouseMove = (e) => {
    if (!wrapperRef.current) return;
    const rect = wrapperRef.current.getBoundingClientRect();
    const mouseX = ((e.clientX - rect.left) / rect.width) * width;
    
    let closest = points[0];
    let minDiff = Math.abs(mouseX - closest.x);
    for (const p of points) {
      const diff = Math.abs(mouseX - p.x);
      if (diff < minDiff) {
        minDiff = diff;
        closest = p;
      }
    }
    setActivePoint(closest);
  };

  return (
    <div 
      className="svg-chart-wrapper" 
      ref={wrapperRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={() => setActivePoint(null)}
      style={{ position: 'relative' }}
    >
      <svg className="svg-chart" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="none">
        <defs>
          <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#853953" stopOpacity="0.45" />
            <stop offset="60%" stopColor="#612D53" stopOpacity="0.15" />
            <stop offset="100%" stopColor="#2C2C2C" stopOpacity="0.0" />
          </linearGradient>
        </defs>

        {/* Horizontal grid lines */}
        {[0, 5, 10, 15, 20, 25].map(v => {
          const y = pad.top + plotH - (v / maxVal) * plotH;
          return (
            <g key={v}>
              <line x1={pad.left} y1={y} x2={width - pad.right} y2={y} stroke="rgba(243, 244, 244, 0.07)" strokeDasharray="3 3" />
              <text x={pad.left - 10} y={y + 4} fontFamily="var(--font-mono)" fontSize="10" fill="rgba(243, 244, 244, 0.45)" textAnchor="end">{v}</text>
            </g>
          );
        })}

        {/* X-axis time ticks */}
        {points.map((pt, i) => (i % 3 === 0 || i === points.length - 1) && (
          <g key={pt.data.hour}>
            <line x1={pt.x} y1={pad.top + plotH} x2={pt.x} y2={pad.top + plotH + 5} stroke="rgba(243, 244, 244, 0.2)" />
            <text x={pt.x} y={pad.top + plotH + 18} fontFamily="var(--font-mono)" fontSize="10" fill="rgba(243, 244, 244, 0.55)" textAnchor="middle">{pt.data.hour}</text>
          </g>
        ))}

        {/* Gradient area under trendline */}
        <path d={areaD} fill="url(#chartGrad)" />

        {/* Solid #853953 Trendline */}
        <path d={lineD} fill="none" stroke="#853953" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />

        {/* Vertical crosshair */}
        {activePoint && (
          <line x1={activePoint.x} y1={pad.top} x2={activePoint.x} y2={pad.top + plotH} stroke="rgba(243, 244, 244, 0.25)" strokeDasharray="2 2" />
        )}

        {/* Data points */}
        {points.map((pt, i) => (
          <circle
            key={i}
            cx={pt.x}
            cy={pt.y}
            r={activePoint === pt ? 7 : 4}
            fill={activePoint === pt ? "#853953" : "#2C2C2C"}
            stroke="#853953"
            strokeWidth="2"
          />
        ))}
      </svg>

      {/* Floating tooltip */}
      {activePoint && (
        <div
          className="chart-tooltip"
          style={{
            display: 'block',
            left: `${Math.min(Math.max(activePoint.x - 120, 10), width - 250)}px`,
            top: `${activePoint.y - 65 < 5 ? activePoint.y + 15 : activePoint.y - 65}px`
          }}
        >
          <div className="tooltip-time">{activePoint.data.hour} UTC • 24H WINDOW</div>
          <div className="tooltip-value">{activePoint.data.count} Intrusion Traps Tripped</div>
          <div className="tooltip-trigger">Top Trigger: {activePoint.data.trigger}</div>
        </div>
      )}
    </div>
  );
}
