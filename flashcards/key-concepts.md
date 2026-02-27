# Security+ Flashcards: Key Concepts

Format: **Term** → Definition | Memory tip

---

## CIA Triad
**Confidentiality** → Only authorized users can access data | C = Can't see
**Integrity** → Data hasn't been altered | I = Intact
**Availability** → Systems accessible when needed | A = Always up

---

## Attack Types (Quick Reference)
**Phishing** → Mass email impersonating trusted source
**Spear phishing** → Targeted phishing (specific individual)
**Whaling** → Spear phishing targeting C-suite executives
**Vishing** → Voice/phone phishing
**Smishing** → SMS phishing
**Pretexting** → Fabricated scenario to manipulate
**Tailgating** → Following someone through a secure door
**Watering hole** → Infect a website the target frequently visits
**BEC** → Impersonate exec to authorize wire transfer

---

## Malware Quick Reference
**Virus** → Requires user to execute infected file
**Worm** → Self-replicates, no user action needed
**Trojan** → Disguised as legit software
**Ransomware** → Encrypts files, demands payment
**Rootkit** → Hides in OS kernel level
**RAT** → Remote Access Trojan — gives attacker control
**Logic bomb** → Triggers on specific condition/date
**Keylogger** → Records keystrokes
**Fileless malware** → Lives in memory, no file on disk
**Cryptojacker** → Hijacks CPU for crypto mining

---

## Cryptography
**Symmetric** → Same key encrypts and decrypts | AES
**Asymmetric** → Public key encrypts, private key decrypts | RSA, ECC
**Hashing** → One-way, no decryption | SHA-256, MD5 (broken)
**Digital signature** → Private key signs, public key verifies
**Salting** → Random data + password before hashing (defeats rainbow tables)
**PFS (Perfect Forward Secrecy)** → New key per session; past sessions safe even if key leaked

---

## Authentication Factors
**Know** → Password, PIN
**Have** → Smart card, token, phone
**Are** → Biometric (fingerprint, retina)
**Where** → GPS location, IP geolocation
**MFA** → Two or more DIFFERENT factor types

---

## Access Control Models
**DAC** → Owner controls access (NTFS)
**MAC** → Labels control access (military classification)
**RBAC** → Role/job title controls access
**ABAC** → Multiple attributes (dept + time + location)
**Rule-based** → ACL/firewall rules

---

## Network Devices & Tools
**Firewall** → Filters traffic by rules
**IDS** → Detects and alerts (passive, out-of-band)
**IPS** → Detects and blocks (active, inline)
**WAF** → Protects web apps (SQLi, XSS)
**NGFW** → Stateful + DPI + IPS + app awareness
**SIEM** → Log aggregation + correlation + alerting
**NAC** → Checks device compliance before network access
**Honeypot** → Decoy system to attract attackers
**Proxy** → Intermediary between client and server (caching, filtering)
**Reverse proxy** → Intermediary that protects servers

---

## Cloud Models
**IaaS** → You manage OS up | AWS EC2
**PaaS** → You manage apps/data | Heroku
**SaaS** → Provider manages everything | Gmail

## Cloud Deployment
**Public** → Multi-tenant, shared infrastructure
**Private** → Dedicated to one org
**Hybrid** → Mix of public + private
**Community** → Shared among similar orgs

---

## Incident Response (PICERL)
1. **P**reparation
2. **I**dentification
3. **C**ontainment
4. **E**radication
5. **R**ecovery
6. **L**essons Learned

---

## Risk Formulas
**SLE** = Asset Value × Exposure Factor
**ALE** = SLE × ARO
**ARO** = How many times per year an event occurs
**Residual risk** = Risk remaining after controls

## Risk Responses
**Avoid** → Don't do the activity
**Transfer** → Insurance, outsource
**Mitigate** → Add controls to reduce
**Accept** → Document and acknowledge

---

## BCP/DR Terms
**RTO** → Max time before systems must be back online
**RPO** → Max acceptable data loss (measured in time)
**MTTR** → Average time to repair a failure
**MTBF** → Average time between failures

---

## Key Protocols & Ports
| Protocol | Port | Notes |
|----------|------|-------|
| SSH | 22 | Secure shell AND SFTP |
| SMTP | 25 | Email sending |
| DNS | 53 | Domain resolution |
| HTTP | 80 | Insecure web |
| HTTPS | 443 | Secure web |
| LDAP | 389 | Directory (insecure) |
| LDAPS | 636 | Directory (secure) |
| RDP | 3389 | Remote desktop |
| RADIUS | 1812/1813 | Auth/accounting |
| TACACS+ | 49 | Cisco AAA |
| Kerberos | 88 | AD authentication |
| SMB | 445 | Windows file sharing |
| Syslog | 514 UDP / 6514 TLS | Log forwarding |

---

## Compliance Frameworks
**GDPR** → EU personal data; 72-hour breach notification
**HIPAA** → US healthcare (PHI)
**PCI-DSS** → Credit card data
**SOX** → US public company financial integrity
**FISMA** → US federal agencies (NIST-based)

---

## Vendor Agreements
**SLA** → Service performance commitments
**MOU** → Non-binding intent document
**NDA** → Confidentiality agreement
**ISA** → Technical security requirements between connected orgs
**BPA** → Business partnership terms
**MSA** → Master overarching vendor agreement
