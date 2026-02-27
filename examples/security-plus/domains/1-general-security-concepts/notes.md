# Domain 1: General Security Concepts (12%)

## 1.1 Security Controls

### Control Categories
| Category | Description | Example |
|----------|-------------|---------|
| **Technical** | Implemented via technology | Firewall, encryption, MFA |
| **Managerial** | Policies and procedures | Security policy, risk assessment |
| **Operational** | Day-to-day people/process | Security awareness training, guards |
| **Physical** | Physical barriers | Locks, fences, cameras |

### Control Types
| Type | Description | Example |
|------|-------------|---------|
| **Preventive** | Stops attack before it happens | Firewall, access control |
| **Detective** | Identifies attacks in progress | IDS, audit logs |
| **Corrective** | Restores after an attack | Backups, patches |
| **Deterrent** | Discourages attackers | Warning banners, cameras |
| **Compensating** | Alternative when primary fails | Manual review if MFA fails |
| **Directive** | Guides behavior | Policies, procedures |

> **Exam tip:** A control can be multiple types. A camera is both Physical (category) and Detective (type).

---

## 1.2 Fundamental Security Concepts

### CIA Triad
- **Confidentiality** — Only authorized users can access data (encryption, access controls)
- **Integrity** — Data is not altered without authorization (hashing, digital signatures)
- **Availability** — Systems are accessible when needed (redundancy, backups, DDoS protection)

### Additional Concepts
- **Non-repudiation** — Cannot deny performing an action (digital signatures, audit logs)
- **Authentication** — Proving identity
- **Authorization** — What you're allowed to do after authentication
- **Accounting/Auditing** — Tracking what was done (AAA model)

### AAA Framework
- **Authentication** — Who are you? (passwords, MFA)
- **Authorization** — What can you do? (permissions, ACLs)
- **Accounting** — What did you do? (logs, audit trails)

---

## 1.3 Cryptography

### Symmetric Encryption
- Same key for encryption and decryption
- Fast, good for large data
- Key distribution problem
- Examples: **AES**, DES, 3DES, RC4

### Asymmetric Encryption
- Public key encrypts, private key decrypts
- Slower, solves key distribution
- Examples: **RSA**, ECC, Diffie-Hellman

### Common Algorithms
| Algorithm | Type | Use |
|-----------|------|-----|
| AES-256 | Symmetric | File/disk encryption |
| RSA | Asymmetric | Key exchange, digital signatures |
| ECC | Asymmetric | Mobile/IoT (efficient) |
| SHA-256 | Hashing | Integrity verification |
| MD5 | Hashing | **Deprecated** — collision vulnerabilities |
| HMAC | MAC | Message authentication with shared key |
| Diffie-Hellman | Key exchange | Securely exchange keys over insecure channel |

### Hashing
- One-way function — cannot reverse
- Same input always = same output
- Used for: password storage, file integrity, digital signatures
- **SHA-256, SHA-3** are current standards; **MD5 and SHA-1 are broken**

### Digital Signatures
- Created with sender's **private key**
- Verified with sender's **public key**
- Provides: authentication, integrity, non-repudiation

### PKI (Public Key Infrastructure)
- **CA (Certificate Authority)** — Issues and signs digital certificates
- **RA (Registration Authority)** — Verifies identity before CA issues cert
- **CRL (Certificate Revocation List)** — List of revoked certs
- **OCSP (Online Certificate Status Protocol)** — Real-time cert revocation check
- **Certificate chain / Chain of trust** — Root CA → Intermediate CA → End-entity cert

### Key Concepts
- **Key escrow** — Third party holds a copy of the key
- **Perfect Forward Secrecy (PFS)** — New session key per session; past sessions safe if key compromised
- **Salting** — Random data added to password before hashing (prevents rainbow table attacks)
- **Key stretching** — Makes brute force slower (bcrypt, PBKDF2, Argon2)

---

## 1.4 Authentication

### Authentication Factors
| Factor | Type | Example |
|--------|------|---------|
| Something you **know** | Knowledge | Password, PIN |
| Something you **have** | Possession | Smart card, token, phone |
| Something you **are** | Inherence | Fingerprint, retina, voice |
| Somewhere you **are** | Location | GPS location, IP geolocation |
| Something you **do** | Behavior | Typing pattern |

### MFA = 2+ different factor types
- Password + fingerprint = MFA (know + are)
- Password + PIN = NOT MFA (know + know)

### Authentication Protocols
- **RADIUS** — Centralizes authentication for network access (UDP 1812/1813)
- **TACACS+** — Cisco's AAA protocol; encrypts full packet (TCP 49)
- **LDAP** — Directory access protocol; used by AD (TCP 389, LDAPS 636)
- **Kerberos** — Ticket-based authentication; used in Windows AD (UDP/TCP 88)
- **SAML** — XML-based SSO for web apps
- **OAuth** — Authorization framework (not authentication)
- **OpenID Connect** — Identity layer on top of OAuth 2.0
- **802.1X** — Port-based NAC; uses EAP

---

## 1.5 Security Best Practices

### Zero Trust
- "Never trust, always verify"
- Assumes breach — verify every request regardless of location
- Micro-segmentation, least privilege, continuous verification

### Least Privilege
- Grant only permissions needed to perform job function
- Reduce attack surface

### Defense in Depth
- Multiple layers of security controls
- If one fails, others remain

### Separation of Duties
- No single person controls an entire process
- Prevents fraud

### Job Rotation
- Employees rotate roles — detects fraud, reduces single point of failure

### Mandatory Vacation
- Forces others to cover role — uncovers hidden fraud
