# Domain 3: Security Architecture (18%)

## 3.1 Network Security Architecture

### Network Zones
- **DMZ (Demilitarized Zone)** — Semi-trusted zone hosting public-facing servers (web, email, DNS)
- **Intranet** — Internal private network
- **Extranet** — Controlled access for partners/vendors
- **Air gap** — Physically isolated network (no internet connection)

### Firewalls
| Type | Description |
|------|-------------|
| **Packet filtering** | Inspects headers (IP, port, protocol); stateless |
| **Stateful** | Tracks connection state; knows if packet is part of established session |
| **Application (Layer 7)** | Deep packet inspection; understands app protocols |
| **WAF (Web App Firewall)** | Protects web apps from OWASP attacks (SQLi, XSS) |
| **NGFW (Next-Gen Firewall)** | Combines stateful + DPI + IPS + application awareness |

### IDS vs IPS
| | IDS | IPS |
|--|-----|-----|
| **Action** | Detects and alerts | Detects and blocks |
| **Placement** | Out-of-band (passive) | Inline (active) |
| **Risk** | False negatives miss attacks | False positives block legit traffic |

### Detection Methods
- **Signature-based** — Matches known attack patterns; misses zero-days
- **Anomaly-based (behavior-based)** — Baseline deviation; detects unknowns but more false positives
- **Heuristic** — Rule-based logic to identify suspicious behavior

### VPN Types
| Type | Use |
|------|-----|
| **Site-to-site VPN** | Connect two networks (HQ to branch) |
| **Remote access VPN** | Individual user to corporate network |
| **SSL/TLS VPN** | Browser-based, no client needed (port 443) |
| **IPsec VPN** | Protocol suite for secure IP communication |
| **Split tunneling** | Only VPN traffic goes through tunnel; rest goes direct |
| **Full tunnel** | All traffic through VPN |

### IPsec Modes
- **Transport mode** — Encrypts payload only; original IP header intact
- **Tunnel mode** — Encrypts entire packet; new IP header added
- **AH (Authentication Header)** — Integrity and authentication; no encryption
- **ESP (Encapsulating Security Payload)** — Encryption + integrity

### Network Protocols (Secure vs Insecure)
| Insecure | Secure | Port |
|----------|--------|------|
| HTTP | HTTPS | 443 |
| Telnet | SSH | 22 |
| FTP | SFTP / FTPS | 22 / 990 |
| SNMP v1/v2 | SNMPv3 | 161/162 |
| LDAP | LDAPS | 636 |
| DNS (plain) | DNSSEC | 53 |

---

## 3.2 Cloud Security

### Cloud Service Models
| Model | Provider Manages | Customer Manages | Example |
|-------|-----------------|-----------------|---------|
| **IaaS** | Physical, hypervisor | OS, apps, data | AWS EC2, Azure VMs |
| **PaaS** | Physical to runtime | Apps, data | Heroku, Google App Engine |
| **SaaS** | Everything | Data configuration | Office 365, Salesforce |

### Cloud Deployment Models
- **Public cloud** — Shared infrastructure, multi-tenant (AWS, Azure, GCP)
- **Private cloud** — Dedicated infrastructure for one org
- **Hybrid cloud** — Mix of public and private
- **Community cloud** — Shared among orgs with similar requirements

### Cloud Security Concepts
- **Shared responsibility model** — Security responsibilities split between CSP and customer
- **CASB (Cloud Access Security Broker)** — Enforces security policies between cloud users and providers
- **CSPM (Cloud Security Posture Management)** — Monitors cloud config for misconfigurations
- **SWG (Secure Web Gateway)** — Filters web traffic for cloud users
- **SASE (Secure Access Service Edge)** — Network security delivered from the cloud (SD-WAN + security)

### Virtualization Security
- **Hypervisor types:**
  - Type 1 (bare metal): runs directly on hardware (VMware ESXi, Hyper-V)
  - Type 2 (hosted): runs on OS (VirtualBox, VMware Workstation)
- **VM escape** — Attacker breaks out of VM to hypervisor/host
- **VM sprawl** — Unmanaged proliferation of VMs
- **Snapshot** — Point-in-time VM state; can be used for recovery

### Container Security
- **Containers** share host OS kernel (unlike VMs which have separate kernels)
- **Docker** — Container platform
- **Kubernetes** — Container orchestration
- Risks: container escape, insecure images, privilege escalation

---

## 3.3 Infrastructure Security

### Secure Network Design
- **NAC (Network Access Control)** — Ensures devices meet security policy before network access
- **802.1X** — Standard for port-based NAC using EAP
- **VLAN** — Logical network segmentation at Layer 2
- **Port security** — Limits MAC addresses per switch port

### Load Balancing
- Distributes traffic across multiple servers
- Improves availability and performance
- **Active-active** — Both nodes handle traffic
- **Active-passive** — Secondary takes over only on failure

### High Availability Concepts
- **MTTR (Mean Time to Repair)** — Average time to fix a failure
- **MTBF (Mean Time Between Failures)** — Average time between failures
- **RTO (Recovery Time Objective)** — Max acceptable downtime
- **RPO (Recovery Point Objective)** — Max acceptable data loss (time)

### Redundancy
- **RAID** (Redundant Array of Independent Disks)
  - RAID 0: Striping — speed, no redundancy
  - RAID 1: Mirroring — full redundancy
  - RAID 5: Striping + parity — 1 disk failure tolerance
  - RAID 6: Striping + double parity — 2 disk failure tolerance
  - RAID 10: Mirror + stripe — performance + redundancy
- **UPS** — Uninterruptible power supply
- **Geographic redundancy** — Sites in different locations

### Secure Protocols and Ports (Key List)
| Protocol | Port | Use |
|----------|------|-----|
| SSH | 22 | Secure remote shell |
| SMTP | 25 | Email sending |
| DNS | 53 | Domain resolution |
| DHCP | 67/68 | IP assignment |
| HTTP | 80 | Web (insecure) |
| HTTPS | 443 | Web (secure) |
| SMB | 445 | File sharing (Windows) |
| LDAP | 389 | Directory services |
| LDAPS | 636 | LDAP over SSL |
| RDP | 3389 | Remote desktop |
| SFTP | 22 | Secure file transfer |
| FTPS | 990 | FTP over SSL |

---

## 3.4 Identity Architecture

### IAM (Identity and Access Management)
- **Directory services** — Centralized user/resource management (Active Directory, LDAP)
- **SSO (Single Sign-On)** — One login for multiple systems
- **Federation** — Trust relationship between identity providers (cross-org SSO)
- **SAML** — XML-based SSO standard
- **OAuth 2.0** — Authorization delegation
- **OpenID Connect** — Authentication on top of OAuth

### Privileged Access
- **PAM (Privileged Access Management)** — Controls admin/privileged accounts
- **Just-in-time access** — Temporary elevated privileges on demand
- **Privileged accounts** should use separate credentials from daily accounts
