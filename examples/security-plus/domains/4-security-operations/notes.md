# Domain 4: Security Operations (28%) — HIGHEST WEIGHT

## 4.1 Identity and Access Management

### Account Types
- **User accounts** — Standard employee accounts
- **Admin/privileged accounts** — Elevated permissions; should be separate from daily-use accounts
- **Service accounts** — Used by applications/services
- **Guest accounts** — Temporary, limited access
- **Shared accounts** — Avoid! Hard to audit

### Access Control Models
| Model | Description | Example |
|-------|-------------|---------|
| **DAC (Discretionary)** | Owner controls access | NTFS permissions |
| **MAC (Mandatory)** | Labels determine access (gov/military) | Top Secret clearance |
| **RBAC (Role-Based)** | Access based on job role | Admin role, user role |
| **ABAC (Attribute-Based)** | Access based on attributes (dept, time, location) | Policy engine |
| **Rule-Based** | Access based on rules/ACLs | Firewall rules |

### Account Management
- **Least privilege** — Minimum permissions needed
- **Account lockout** — Lock after N failed attempts
- **Password expiration** — Force periodic changes
- **Disabling vs deleting** — Disable first, delete after retention period
- **Recertification/access review** — Periodic review of who has what access
- **Provisioning/deprovisioning** — Onboarding/offboarding workflows

---

## 4.2 Endpoint Security

### Endpoint Protection
- **EDR (Endpoint Detection and Response)** — Real-time monitoring, threat detection, response on endpoints
- **XDR (Extended Detection and Response)** — EDR + network + cloud (broader scope)
- **Antivirus/Anti-malware** — Signature and heuristic detection
- **HIDS (Host-based IDS)** — Monitors activity on individual host
- **HIPS (Host-based IPS)** — Blocks on individual host

### Mobile Device Management
- **MDM (Mobile Device Management)** — Centrally manage mobile devices
- **MAM (Mobile Application Management)** — Manage only apps, not full device
- **BYOD (Bring Your Own Device)** — Employee-owned devices accessing corporate resources
  - Risks: data mixing, lost device, malware
- **COPE (Company Owned, Personally Enabled)** — Company owns device, personal use allowed
- **Remote wipe** — Erase device data remotely
- **Containerization** — Separate work and personal data on device

### Patch Management
1. Identify — scan for missing patches
2. Test — validate in non-production
3. Deploy — staged rollout
4. Verify — confirm successful application

---

## 4.3 Network Security Monitoring

### SIEM (Security Information and Event Management)
- Aggregates and correlates logs from multiple sources
- Generates alerts based on rules/correlation
- Used for: incident detection, compliance, forensics
- Examples: Splunk, IBM QRadar, Microsoft Sentinel

### Log Sources
- **Firewall logs** — Allowed/blocked traffic
- **IDS/IPS logs** — Attack signatures detected
- **Authentication logs** — Login success/failure
- **System logs** — OS events
- **Application logs** — App-specific events
- **DNS logs** — DNS queries (useful for detecting C2 traffic)

### Network Monitoring Tools
- **Wireshark** — Packet capture and analysis
- **Nmap** — Network scanner (open ports, services, OS detection)
- **Netflow** — Traffic flow data (not full packets)
- **SNMP** — Network device monitoring (v3 is secure)
- **Syslog** — Log aggregation (UDP 514, TCP 6514 for TLS)

### Baseline and Anomaly Detection
- Establish normal behavior baseline
- Alert on deviations
- **UBA/UEBA (User/Entity Behavior Analytics)** — ML-based anomaly detection

---

## 4.4 Incident Response

### Incident Response Phases (PICERL)
1. **Preparation** — Policies, team, tools, training
2. **Identification** — Detect and confirm incident
3. **Containment** — Limit spread (short-term + long-term containment)
4. **Eradication** — Remove threat (malware, accounts, vulnerabilities)
5. **Recovery** — Restore systems to normal operation
6. **Lessons Learned** — Post-incident review, improve processes

> **Exam tip:** Memorize PICERL order. Order matters on exam questions.

### Containment Strategies
- **Short-term** — Isolate affected systems immediately
- **Long-term** — Fix root cause before reconnecting
- **Evidence preservation** — Don't destroy evidence during containment

### Digital Forensics
- **Chain of custody** — Document who handled evidence and when
- **Order of volatility** — Collect most volatile data first:
  1. CPU registers/cache
  2. RAM
  3. Swap/pagefile
  4. Disk
  5. Remote logs
  6. Backups
- **Write blocker** — Prevents writing to evidence drive
- **Forensic image** — Bit-for-bit copy of storage media
- **Legal hold** — Preserve data relevant to litigation

### Threat Hunting
- Proactive search for threats that evaded detection
- Based on hypotheses from threat intelligence
- Uses TTPs and IOCs

---

## 4.5 Data Security

### Data Classifications
| Level | Description | Example |
|-------|-------------|---------|
| **Public** | No restriction | Marketing materials |
| **Internal/Private** | Internal use only | Employee directory |
| **Confidential** | Need-to-know | Business plans |
| **Restricted/Secret** | Highly sensitive | PII, financial data |

### Data States
- **Data at rest** — Stored data (encrypt with AES-256, BitLocker, FileVault)
- **Data in transit** — Moving over network (TLS, VPN)
- **Data in use/processing** — Actively being processed (memory encryption, secure enclaves)

### Data Loss Prevention (DLP)
- Monitors and controls data movement
- **Network DLP** — Inspects traffic for sensitive data
- **Endpoint DLP** — Controls USB, email, printing on endpoints
- **Cloud DLP** — Monitors cloud-stored data

### Data Handling
- **Tokenization** — Replace sensitive data with non-sensitive token
- **Masking** — Obscure data (show only last 4 digits of SSN)
- **Anonymization** — Remove all identifying info (irreversible)
- **Pseudonymization** — Replace identifying info with pseudonym (reversible with key)

---

## 4.6 Security Tools

### Vulnerability Scanners
- **Nessus** — Popular vulnerability scanner
- **OpenVAS** — Open-source vulnerability scanner
- **Qualys** — Cloud-based vulnerability management

### Penetration Testing Tools
- **Metasploit** — Exploitation framework
- **Burp Suite** — Web app testing
- **Kali Linux** — Pentesting distro

### Password Tools
- **Hashcat** — Password cracking (GPU-accelerated)
- **John the Ripper** — Password cracking

### Network Tools
- **Nmap** — Port scanning
- **Wireshark** — Packet analysis
- **Tcpdump** — CLI packet capture
- **Netcat** — Network utility (banner grabbing, port scanning)
