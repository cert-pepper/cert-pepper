# Domain 2: Threats, Vulnerabilities, and Mitigations (22%)

## 2.1 Threat Actors

| Actor Type | Motivation | Sophistication | Resources |
|------------|-----------|----------------|-----------|
| **Nation-state** | Espionage, disruption | Very high (APT) | Government-funded |
| **Organized crime** | Financial gain | High | Well-funded |
| **Hacktivist** | Political/social cause | Moderate | Variable |
| **Script kiddie** | Recognition, curiosity | Low | Low — uses existing tools |
| **Insider threat** | Revenge, financial gain | Varies | Has internal access |
| **Shadow IT** | Convenience | Low | Internal, unsanctioned |

### APT (Advanced Persistent Threat)
- Long-term, stealthy attack campaign
- Typically nation-state sponsored
- Goal: persistent access, not quick destruction

---

## 2.2 Attack Types

### Social Engineering
| Attack | Description |
|--------|-------------|
| **Phishing** | Mass email impersonating trusted source |
| **Spear phishing** | Targeted phishing at specific individual |
| **Whaling** | Spear phishing targeting executives |
| **Vishing** | Voice/phone phishing |
| **Smishing** | SMS phishing |
| **Pretexting** | Fabricated scenario to gain info |
| **Baiting** | Leaving infected USB drives, etc. |
| **Tailgating/Piggybacking** | Following authorized person through door |
| **Watering hole** | Infect site target frequently visits |
| **Business Email Compromise (BEC)** | Impersonate exec to authorize wire transfer |

### Network Attacks
| Attack | Description |
|--------|-------------|
| **MITM (Man-in-the-Middle)** | Intercepts communication between two parties |
| **Replay attack** | Captures and re-sends valid data |
| **DoS (Denial of Service)** | Overwhelms resource from one source |
| **DDoS** | DoS from many sources (botnet) |
| **Smurf attack** | ICMP flood using spoofed source IP |
| **DNS poisoning** | Corrupts DNS cache to redirect traffic |
| **ARP spoofing** | Associates attacker MAC with victim IP (enables MITM) |
| **VLAN hopping** | Switch spoofing or double tagging to reach other VLANs |
| **Evil twin** | Rogue WAP mimics legitimate AP |
| **Deauthentication attack** | Forces client off WiFi (used in WPA handshake capture) |
| **On-path attack** | Modern term for MITM |

### Application Attacks
| Attack | Description |
|--------|-------------|
| **SQL injection** | Inserts SQL into input fields |
| **XSS (Cross-site scripting)** | Injects malicious scripts into web pages |
| **CSRF (Cross-site request forgery)** | Tricks browser into making unauthorized request |
| **Directory traversal** | `../` to access files outside web root |
| **Command injection** | Executes OS commands via app input |
| **Buffer overflow** | Overflows memory to execute arbitrary code |
| **Integer overflow** | Value exceeds integer max, wraps around |
| **Race condition / TOCTOU** | Time-of-check vs time-of-use vulnerability |
| **Clickjacking** | Invisible overlay tricks user into clicking |
| **API attacks** | Exploiting insecure API endpoints |

### Password Attacks
| Attack | Description |
|--------|-------------|
| **Brute force** | Try every combination |
| **Dictionary attack** | Try common words/passwords |
| **Credential stuffing** | Use breached username/password pairs |
| **Password spraying** | One password tried against many accounts (avoids lockout) |
| **Rainbow table** | Pre-computed hash lookup (defeated by salting) |

### Malware Types
| Type | Description |
|------|-------------|
| **Virus** | Attaches to files, spreads when executed |
| **Worm** | Self-replicates without user action |
| **Trojan** | Disguised as legitimate software |
| **Ransomware** | Encrypts files, demands payment |
| **Spyware** | Silently monitors and reports activity |
| **Adware** | Displays unwanted ads |
| **Rootkit** | Hides itself deep in OS (kernel level) |
| **Keylogger** | Records keystrokes |
| **Botnet/bot** | Compromised system in attacker's network |
| **RAT (Remote Access Trojan)** | Gives remote control to attacker |
| **Logic bomb** | Triggers malicious code on condition |
| **Fileless malware** | Runs in memory, no file on disk |
| **Cryptojacker** | Uses victim's CPU to mine crypto |

---

## 2.3 Vulnerabilities

### Vulnerability Categories
- **Zero-day** — Vulnerability unknown to vendor, no patch available
- **Legacy systems** — Outdated OS/software no longer patched
- **Misconfigurations** — Default credentials, open ports, weak settings
- **Unpatched software** — Known CVE with available patch not applied
- **Weak credentials** — Default/simple passwords
- **Insecure protocols** — Telnet, FTP, HTTP, SNMPv1

### CVE and CVSS
- **CVE (Common Vulnerabilities and Exposures)** — Unique ID for known vulnerabilities
- **CVSS (Common Vulnerability Scoring System)** — 0-10 score for severity
  - Critical: 9.0-10.0 | High: 7.0-8.9 | Medium: 4.0-6.9 | Low: 0.1-3.9

### Supply Chain Attacks
- Compromise software/hardware before it reaches target
- Examples: SolarWinds, XZ Utils backdoor
- Mitigations: vendor vetting, code signing, SBOMs

---

## 2.4 Vulnerability Management

### Scanning Types
| Type | Description |
|------|-------------|
| **Vulnerability scan** | Identifies known vulnerabilities; non-exploiting |
| **Penetration test** | Actively exploits vulnerabilities |
| **Authenticated scan** | Uses credentials; finds more vulnerabilities |
| **Unauthenticated scan** | External attacker perspective |
| **Agent-based scan** | Software installed on host |
| **Passive scan** | Monitors traffic without sending probes |

### Penetration Testing Phases
1. **Planning/Reconnaissance** — Define scope, gather intel
2. **Scanning/Enumeration** — Identify open ports, services, vulnerabilities
3. **Exploitation** — Actively exploit vulnerabilities
4. **Post-exploitation** — Maintain access, pivot, exfiltrate
5. **Reporting** — Document findings and recommendations

### Pen Test Types by Knowledge
| Type | Attacker Knowledge |
|------|--------------------|
| **Black box** | No internal knowledge (external attacker sim) |
| **White box** | Full knowledge (internal audit sim) |
| **Gray box** | Partial knowledge |

### Threat Intelligence
- **OSINT** — Open Source Intelligence (public info)
- **ISAC** — Information Sharing and Analysis Center (sector-specific threat sharing)
- **IOC (Indicator of Compromise)** — Evidence of a breach (malicious IP, hash, domain)
- **TTPs** — Tactics, Techniques, and Procedures (how attackers operate)
- **STIX/TAXII** — Standards for sharing threat intelligence

---

## 2.5 Mitigations

### Hardening
- Remove unnecessary services, software, accounts
- Change default credentials
- Enable host-based firewall
- Apply patches promptly
- **CIS Benchmarks** — Security configuration guides
- **STIG (Security Technical Implementation Guide)** — DoD hardening guides

### Network Mitigations
- **Network segmentation** — Isolate sensitive systems
- **Microsegmentation** — Granular, software-defined isolation
- **Jump server/bastion host** — Controlled gateway to sensitive networks
- **Honeypot** — Decoy system to attract and study attackers
- **Honeynet** — Network of honeypots
- **Port security** — Limits MACs per switch port

### Patch Management
- Test patches before deployment
- Emergency patches for critical vulnerabilities
- Maintain patch inventory/tracking
