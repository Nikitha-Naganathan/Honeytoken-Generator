// src/services/api.js
import { initialData } from '../data/mockData';

const API_BASE = 'http://localhost:8000/api';
const WS_URL = 'ws://localhost:8000/ws/alerts';

// Helper for HTTP requests with automatic fallback to mockData if backend is not yet started
async function fetchWithFallback(endpoint, fallbackValue, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      }
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn(`[HoneyTrap API] Backend unavailable for ${endpoint}, using local state:`, err.message);
    return fallbackValue;
  }
}

export const api = {
  // Operational Overview
  async getOverview() {
    return fetchWithFallback('/overview', {
      activeThreats: 3,
      containedToday: 14,
      telemetry24h: initialData.telemetry24h,
      priorityThreats: initialData.alerts.slice(0, 3)
    });
  },

  // Live Alerts Feed
  async getAlerts(severity, search) {
    let query = '';
    const params = [];
    if (severity && severity !== 'ALL') params.push(`severity=${encodeURIComponent(severity)}`);
    if (search) params.push(`search=${encodeURIComponent(search)}`);
    if (params.length > 0) query = '?' + params.join('&');

    return fetchWithFallback(`/alerts${query}`, initialData.alerts);
  },

  // Attacker Dossier (Case A vs Case B)
  async getAttackerDossier(caseKey) {
    return fetchWithFallback(`/attacker/${caseKey}`, {
      dossier: initialData.dossiers[caseKey] || initialData.dossiers.CASE_A,
      blockedLedger: initialData.blockedLedger
    });
  },

  // Timeline & Chronology
  async getTimeline() {
    return fetchWithFallback('/timeline', {
      pipeline: initialData.containmentPipeline,
      events: initialData.timelineEvents
    });
  },

  // Fleet Endpoints
  async getEndpoints() {
    return fetchWithFallback('/endpoints', initialData.endpoints);
  },

  // Isolate Endpoint
  async isolateEndpoint(id) {
    return fetchWithFallback(`/endpoints/${id}/isolate`, { success: true }, { method: 'POST' });
  },

  // Restore Endpoint
  async restoreEndpoint(id) {
    return fetchWithFallback(`/endpoints/${id}/restore`, { success: true }, { method: 'POST' });
  },

  // Block Adversary IP
  async blockIp(ip) {
    return fetchWithFallback('/block-ip', { success: true }, {
      method: 'POST',
      body: JSON.stringify({ ip })
    });
  },

  // Reseed Honeytokens on disk
  async reseedHoneytokens() {
    return fetchWithFallback('/honeytokens/generate', { success: true }, { method: 'POST' });
  },

  // WebSocket Live Alert Stream
  subscribeAlerts(onAlert, onConnectionStatus) {
    let ws = null;
    let reconnectTimeout = null;
    let isDisposed = false;

    function connect() {
      if (isDisposed) return;
      try {
        ws = new WebSocket(WS_URL);

        ws.onopen = () => {
          if (onConnectionStatus) onConnectionStatus(true);
          console.log('[HoneyTrap WS] Connected to FastAPI live alerts stream');
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (data.type === 'NEW_ALERT' && data.alert) {
              onAlert(data.alert);
            }
          } catch (e) {
            console.error('[HoneyTrap WS] Failed to parse alert message', e);
          }
        };

        ws.onclose = () => {
          if (onConnectionStatus) onConnectionStatus(false);
          if (!isDisposed) {
            reconnectTimeout = setTimeout(connect, 3000);
          }
        };

        ws.onerror = () => {
          if (ws) ws.close();
        };
      } catch (err) {
        if (!isDisposed) {
          reconnectTimeout = setTimeout(connect, 3000);
        }
      }
    }

    connect();

    return () => {
      isDisposed = true;
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      if (ws) ws.close();
    };
  }
};
