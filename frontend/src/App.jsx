// src/App.jsx
import React, { useState, useEffect } from 'react';
import { initialData } from './data/mockData';
import { api } from './services/api';

import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import ToastOverlay from './components/ToastOverlay';
import ReleaseModal from './components/ReleaseModal';

import Overview from './views/Overview';
import AlertsFeed from './views/AlertsFeed';
import AttackerInfo from './views/AttackerInfo';
import AttackTimeline from './views/AttackTimeline';
import EndpointsFleet from './views/EndpointsFleet';

export default function App() {
  const [currentView, setCurrentView] = useState('overview');
  const [activeCase, setActiveCase] = useState('CASE_A');
  const [alerts, setAlerts] = useState(initialData.alerts);
  const [endpoints, setEndpoints] = useState(initialData.endpoints);
  const [blockedLedger, setBlockedLedger] = useState(initialData.blockedLedger);
  const [overviewData, setOverviewData] = useState({
    activeThreats: 3,
    containedToday: 14,
    telemetry24h: initialData.telemetry24h,
    priorityThreats: initialData.alerts.slice(0, 3)
  });
  const [toasts, setToasts] = useState([]);
  const [releaseHost, setReleaseHost] = useState(null);
  const [backendOnline, setBackendOnline] = useState(false);

  // 1. Fetch initial data from FastAPI backend
  useEffect(() => {
    async function loadData() {
      const [ov, al, ep] = await Promise.all([
        api.getOverview(),
        api.getAlerts(),
        api.getEndpoints()
      ]);
      if (ov) setOverviewData(ov);
      if (al && al.length) setAlerts(al);
      if (ep && ep.length) setEndpoints(ep);
    }
    loadData();
  }, []);

  // 2. Subscribe to Real-Time WebSocket for Live Deception Alerts from Watchdog
  useEffect(() => {
    const unsubscribe = api.subscribeAlerts(
      (newAlert) => {
        // When a honeytoken on the filesystem is accessed, backend broadcasts alert
        setAlerts(prev => [newAlert, ...prev]);
        addToast({
          title: `Tripwire Triggered: ${newAlert.attackType}`,
          severity: newAlert.severity,
          endpoint: newAlert.hostname,
          sourceIp: newAlert.sourceIp,
          details: newAlert.baitTrigger
        });
      },
      (isOnline) => {
        setBackendOnline(isOnline);
      }
    );

    return () => unsubscribe();
  }, []);

  const addToast = (t) => {
    const newToast = {
      id: 'toast-' + Math.random().toString(36).substring(2, 9),
      title: t.title || 'Canary Threat Tripped',
      severity: t.severity || 'critical',
      endpoint: t.endpoint || 'dc-primary.corp.internal',
      sourceIp: t.sourceIp || '185.220.101.5',
      details: t.details || 'Autonomous deception trigger engaged.',
      timestamp: new Date().toISOString().slice(11, 23) + 'Z',
      caseKey: t.sourceIp?.startsWith('192.168') ? 'CASE_B' : 'CASE_A'
    };
    setToasts(prev => [newToast, ...prev]);
  };

  const handleIsolateHost = async (host) => {
    await api.isolateEndpoint(host);
    setEndpoints(prev => prev.map(e => e.hostname === host ? { ...e, isolated: true, status: 'ISOLATED' } : e));
    setAlerts(prev => prev.map(a => a.hostname === host ? { ...a, hostIsolated: true } : a));
    addToast({ title: `Host Quarantined: ${host}`, severity: 'critical', endpoint: host });
  };

  const handleReleaseHost = (host) => {
    setReleaseHost(host);
  };

  const confirmReleaseHost = async () => {
    if (!releaseHost) return;
    await api.restoreEndpoint(releaseHost);
    setEndpoints(prev => prev.map(e => e.hostname === releaseHost ? { ...e, isolated: false, status: 'HEALTHY' } : e));
    setAlerts(prev => prev.map(a => a.hostname === releaseHost ? { ...a, hostIsolated: false } : a));
    addToast({ title: `Host Rejoined Fleet: ${releaseHost}`, severity: 'medium', endpoint: releaseHost });
    setReleaseHost(null);
  };

  const handleBlockIp = async (ip) => {
    await api.blockIp(ip);
    const newItem = {
      timestamp: new Date().toISOString(),
      ip,
      cidr: `${ip}/32`,
      triggerRule: 'Manual Analyst Action (SOC-ANALYST)',
      status: 'PERIMETER DROP ENFORCED'
    };
    setBlockedLedger(prev => [newItem, ...prev]);
    addToast({ title: 'Perimeter Rule Deployed', severity: 'critical', sourceIp: ip });
  };

  const handleReseed = async () => {
    await api.reseedHoneytokens();
    addToast({
      title: 'Honeytokens Reseeded on Disk',
      severity: 'medium',
      details: 'Rotated deception secrets in honeytokens/ directory.'
    });
  };

  return (
    <div className="app-container">
      <Sidebar currentView={currentView} onNavigate={setCurrentView} />

      <div className="main-wrapper">
        <Topbar
          pageTitle={
            currentView === 'overview' ? 'Security Operations Overview' :
            currentView === 'alerts' ? 'Live Alerts Feed' :
            currentView === 'attacker' ? 'Attacker Dossier & Vector Map' :
            currentView === 'timeline' ? 'Attack Timeline & Microsecond Replay' :
            'Endpoints & Fleet Deception Posture'
          }
          pageSubtitle={
            backendOnline 
              ? 'FastAPI Backend: CONNECTED (Live WebSocket Active)' 
              : 'Autonomous Deception & Telemetry Triage'
          }
          onTriggerToast={() => addToast({ title: 'Canary AWS Secret Accessed', severity: 'critical' })}
          onTriggerStack={() => {
            addToast({ title: 'Fake SAM Dump Attempt', severity: 'high' });
            setTimeout(() => addToast({ title: 'Port 445 Probe', severity: 'medium', sourceIp: '192.168.1.27' }), 150);
          }}
        />

        <main className="viewport">
          {currentView === 'overview' && (
            <Overview
              data={{
                telemetry24h: overviewData.telemetry24h,
                alerts: alerts
              }}
              onInspectDossier={(c) => { setActiveCase(c); setCurrentView('attacker'); }}
              onViewAllAlerts={() => setCurrentView('alerts')}
            />
          )}

          {currentView === 'alerts' && (
            <AlertsFeed
              alerts={alerts}
              onInspectDossier={(c) => { setActiveCase(c); setCurrentView('attacker'); }}
              onIsolateHost={handleIsolateHost}
              onReleaseHost={handleReleaseHost}
              onBlockIp={handleBlockIp}
            />
          )}

          {currentView === 'attacker' && (
            <AttackerInfo
              dossiers={initialData.dossiers}
              activeCase={activeCase}
              onCaseChange={setActiveCase}
              blockedLedger={blockedLedger}
              onBlockIp={handleBlockIp}
              onSeverSubnet={() => addToast({ title: 'Subnet Severed', severity: 'critical' })}
              onReseed={handleReseed}
            />
          )}

          {currentView === 'timeline' && (
            <AttackTimeline
              events={initialData.timelineEvents}
              pipeline={initialData.containmentPipeline}
            />
          )}

          {currentView === 'endpoints' && (
            <EndpointsFleet
              endpoints={endpoints}
              onIsolate={handleIsolateHost}
              onRestore={handleReleaseHost}
            />
          )}
        </main>
      </div>

      <ToastOverlay
        toasts={toasts}
        onDismiss={(id) => setToasts(prev => prev.filter(t => t.id !== id))}
        onViewDossier={(c) => { setActiveCase(c); setCurrentView('attacker'); }}
      />

      {releaseHost && (
        <ReleaseModal
          hostname={releaseHost}
          onClose={() => setReleaseHost(null)}
          onConfirm={confirmReleaseHost}
        />
      )}
    </div>
  );
}
