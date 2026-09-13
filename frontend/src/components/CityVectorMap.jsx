// src/components/CityVectorMap.jsx
import React from 'react';

export default function CityVectorMap({ caseKey }) {
  if (caseKey === 'CASE_B') {
    // Zoomed-in Bengaluru Bellandur Campus Bldg 4 (12.9260° N, 77.6762° E)
    return (
      <svg viewBox="0 0 400 320" width="100%" height="100%" style={{ background: '#1d1d1d', userSelect: 'none' }}>
        <defs>
          <pattern id="grid-b" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(243, 244, 244, 0.04)" strokeWidth="1"/>
          </pattern>
          <radialGradient id="glow-b" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#853953" stopOpacity="0.8"/>
            <stop offset="100%" stopColor="#853953" stopOpacity="0"/>
          </radialGradient>
        </defs>

        <rect width="400" height="320" fill="url(#grid-b)" />
        <path d="M 300 0 C 260 60, 280 120, 400 180 L 400 0 Z" fill="rgba(97, 45, 83, 0.15)" stroke="rgba(97, 45, 83, 0.3)" strokeWidth="1" />
        <text x="320" y="70" fontFamily="var(--font-mono)" fontSize="8" fill="rgba(243, 244, 244, 0.35)">BELLANDUR LAKE</text>

        <path d="M 20 300 L 150 190 L 320 140 L 390 130" stroke="rgba(243, 244, 244, 0.35)" strokeWidth="5" fill="none" />
        <text x="40" y="270" fontFamily="var(--font-mono)" fontSize="8" fill="rgba(243, 244, 244, 0.55)" transform="rotate(-40, 40, 270)">OUTER RING ROAD (ORR)</text>

        {/* Corporate Campus Perimeter */}
        <polygon points="120,60 250,50 270,160 160,180" fill="rgba(243, 244, 244, 0.03)" stroke="rgba(243, 244, 244, 0.2)" strokeWidth="1.5" strokeDasharray="4 2" />
        <rect x="135" y="70" width="30" height="24" fill="rgba(243, 244, 244, 0.05)" stroke="rgba(243, 244, 244, 0.15)" strokeWidth="1" />
        <rect x="180" y="65" width="32" height="26" fill="rgba(243, 244, 244, 0.05)" stroke="rgba(243, 244, 244, 0.15)" strokeWidth="1" />
        
        {/* Adversary Workstation: Building 4 Hardware Lab */}
        <rect x="190" y="110" width="50" height="40" fill="rgba(133, 57, 83, 0.25)" stroke="#853953" strokeWidth="2" />
        <text x="195" y="125" fontFamily="var(--font-mono)" fontSize="7" fontWeight="700" fill="#F3F4F4">BLDG 4 (LAB)</text>
        <text x="195" y="135" fontFamily="var(--font-mono)" fontSize="6" fill="rgba(243, 244, 244, 0.7)">ZONE B // SW-02</text>
        <text x="195" y="145" fontFamily="var(--font-mono)" fontSize="6" fill="rgba(243, 244, 244, 0.7)">PORT Fa0/14</text>

        {/* Radar Pulse */}
        <circle cx="215" cy="130" r="24" fill="url(#glow-b)">
          <animate attributeName="r" values="10;32;10" dur="2s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.8;0.1;0.8" dur="2s" repeatCount="indefinite" />
        </circle>
        <circle cx="215" cy="130" r="4.5" fill="#853953" stroke="#F3F4F4" strokeWidth="1.5" />
      </svg>
    );
  }

  // Zoomed-in Bucharest Pipera District (44.4811° N, 26.1128° E)
  return (
    <svg viewBox="0 0 400 320" width="100%" height="100%" style={{ background: '#1d1d1d', userSelect: 'none' }}>
      <defs>
        <pattern id="grid-a" width="20" height="20" patternUnits="userSpaceOnUse">
          <path d="M 20 0 L 0 0 0 20" fill="none" stroke="rgba(243, 244, 244, 0.04)" strokeWidth="1"/>
        </pattern>
        <radialGradient id="glow-a" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#853953" stopOpacity="0.8"/>
          <stop offset="100%" stopColor="#853953" stopOpacity="0"/>
        </radialGradient>
      </defs>

      <rect width="400" height="320" fill="url(#grid-a)" />
      <path d="M 30 180 L 180 170 L 390 150" stroke="rgba(243, 244, 244, 0.35)" strokeWidth="4" fill="none" />
      <text x="50" y="174" fontFamily="var(--font-mono)" fontSize="8" fill="rgba(243, 244, 244, 0.55)">SOSEAUA PIPERA</text>

      <path d="M 120 100 L 340 290" stroke="rgba(243, 244, 244, 0.3)" strokeWidth="3" fill="none" />
      <text x="210" y="210" fontFamily="var(--font-mono)" fontSize="8" fill="rgba(243, 244, 244, 0.5)" transform="rotate(40, 210, 210)">BD. DIMITRIE POMPEIU</text>

      {/* Adversary Facility (M247 Data Center) */}
      <rect x="235" y="160" width="55" height="42" fill="rgba(133, 57, 83, 0.25)" stroke="#853953" strokeWidth="1.5" />
      <text x="240" y="174" fontFamily="var(--font-mono)" fontSize="7" fontWeight="700" fill="#F3F4F4">M247 DC-BUC</text>
      <text x="240" y="184" fontFamily="var(--font-mono)" fontSize="6" fill="rgba(243, 244, 244, 0.7)">TOR EXIT NODE</text>

      <circle cx="260" cy="180" r="26" fill="url(#glow-a)">
        <animate attributeName="r" values="12;36;12" dur="2.5s" repeatCount="indefinite" />
        <animate attributeName="opacity" values="0.8;0.1;0.8" dur="2.5s" repeatCount="indefinite" />
      </circle>
      <circle cx="260" cy="180" r="5" fill="#853953" stroke="#F3F4F4" strokeWidth="1.5" />
    </svg>
  );
}
