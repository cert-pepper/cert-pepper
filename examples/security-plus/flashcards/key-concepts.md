## CIA Triad & Core Principles

**CIA Triad** → Confidentiality (prevent unauthorized disclosure), Integrity (prevent unauthorized modification), Availability (ensure access when needed) | The three foundational security goals; every security control maps to one or more of these

**Non-repudiation** → The ability to prove an action was performed by a specific party — they cannot deny it; achieved via digital signatures | "Non" = cannot, "repudiate" = deny

**Least Privilege** → Grant only the minimum permissions required for a user or process to perform its function | Think: a janitor has keys to the building but not the vault

**Separation of Duties** → Divide critical tasks between multiple people so no single person can complete a harmful action alone | Two keys for a safe deposit box; two people to authorize a wire transfer

**Defense in Depth** → Multiple overlapping layers of security controls so failure of one layer doesn't compromise the whole | Like a castle: moat + walls + guards + inner keep

**Zero Trust** → "Never trust, always verify" — no implicit trust based on network location; every access request is continuously verified | Trust no one inside or outside the perimeter

**Job Rotation** → Periodically moving employees between roles to detect fraud and cross-train | A new person in a role may discover predecessor's misuse

**Need to Know** → Access to information is limited to what is required for the job function — even high-clearance users can be denied access | A Top Secret clearance doesn't mean access to every Top Secret document

## Access Control Models

**DAC — Discretionary Access Control** → Resource owners decide who can access their resources | Most flexible, least secure; Windows file sharing permissions

**MAC — Mandatory Access Control** → Access based on security labels and clearances assigned by the system | Government/military classification systems; users cannot override labels

**RBAC — Role-Based Access Control** → Permissions assigned to roles; users assigned to roles | Most common in enterprise; "HR Analyst" role, "Network Admin" role

**ABAC — Attribute-Based Access Control** → Access decisions based on multiple attributes: user, resource, environment, device | Most granular; "contractor, during business hours, from managed device"

**Rule-Based AC** → Access controlled by administrator-set rules (e.g., firewall ACLs) | Confusingly also called RBAC — context determines which type is meant

## Authentication Factors

**Something you know** → Password, PIN, security question | Weakest factor alone — can be phished, guessed, or stolen

**Something you have** → Smartphone, hardware token, smart card, OTP device | TOTP apps (Google Authenticator), hardware keys (YubiKey)

**Something you are** → Biometric: fingerprint, retinal scan, facial recognition | FAR (False Acceptance Rate) vs FRR (False Rejection Rate); CER is where they meet

**Somewhere you are** → Geolocation, network location | IP address, GPS location

**MFA — Multi-Factor Authentication** → Two or more different factor categories combined | Password + phone push = MFA; two passwords = NOT MFA

**TOTP — Time-based One-Time Password** → OTP generated from a shared secret and current timestamp; valid ~30 seconds | Google Authenticator, Authy

**HOTP — HMAC-based One-Time Password** → OTP generated from a shared secret and a counter; valid until used | YubiKey hardware tokens in HOTP mode

## Authentication Protocols

**SAML — Security Assertions Markup Language** → XML-based protocol for SSO and identity federation between IdP and service providers | Enterprise SSO; "Sign in with corporate account" to SaaS apps

**OAuth 2.0** → Authorization framework allowing third-party access to resources without sharing passwords | "Sign in with Google" to authorize access to your Calendar — OAuth handles the authorization

**OIDC — OpenID Connect** → Identity layer built on OAuth 2.0; adds authentication (who you are) to OAuth's authorization | "Sign in with Google" to verify identity — OIDC provides the ID token with name/email

**Kerberos** → Ticket-based authentication protocol used in Active Directory; uses KDC (Key Distribution Center) and TGTs | Windows domain logins; used internally; vulnerable to Pass-the-Hash, Kerberoasting, Golden Ticket

**RADIUS** → Remote Authentication Dial-In User Service; provides centralized AAA for network access (VPN, 802.1X) | VPN authentication, enterprise Wi-Fi (802.1X), network device authentication

**802.1X** → Port-based Network Access Control; uses RADIUS for enterprise authentication | Prevents unauthorized devices from connecting to wired/wireless networks; pairs with EAP

## Cryptography Fundamentals

**Symmetric encryption** → Same key encrypts and decrypts; fast but key distribution is the challenge | AES (current standard), 3DES (deprecated), DES (broken)

**Asymmetric encryption** → Key pair: public key (encrypt/verify), private key (decrypt/sign); solves key distribution but slower | RSA, ECC; used for key exchange and digital signatures

**Hashing** → One-way function producing a fixed-length digest; used for integrity verification and password storage | SHA-256, SHA-3 (current); MD5, SHA-1 (deprecated/broken)

**Digital signature** → Hash of message encrypted with sender's private key; provides authentication, integrity, and non-repudiation | Verify with sender's public key; if valid: message is from them and unaltered

**Salting** → Adding a random unique value to a password before hashing | Defeats rainbow table attacks; ensures identical passwords produce different hashes

**Key stretching** → Applying hashing many times (PBKDF2, bcrypt, scrypt) to slow brute force | bcrypt is the gold standard for password storage

**Perfect Forward Secrecy (PFS)** → Ephemeral session keys ensure past sessions can't be decrypted even if long-term key is compromised | Uses DHE or ECDHE; defeats "harvest now, decrypt later"

**AES** → Advanced Encryption Standard; symmetric block cipher; current gold standard | AES-128 (good), AES-256 (highest security); used for data at rest and in transit

**ECC — Elliptic Curve Cryptography** → Asymmetric crypto; 256-bit ECC ≈ 3072-bit RSA in security; preferred for mobile/IoT | Shorter keys = less computation; used in TLS 1.3, mobile devices

**RSA** → Rivest-Shamir-Adleman; asymmetric; based on difficulty of factoring large primes | 2048-bit minimum; 3072-bit recommended; being replaced by ECC in modern systems

## PKI & Certificates

**PKI — Public Key Infrastructure** → Hierarchy of CAs that issue certificates binding public keys to identities | Root CA → Intermediate CA → End-entity certificate

**CA — Certificate Authority** → Issues, manages, and revokes digital certificates | Root CAs self-sign; intermediate CAs signed by root; end-entity certs signed by intermediate

**CRL — Certificate Revocation List** → Published list of revoked certificates; checked by clients | Periodic publication; can be stale; large and slow for high-volume environments

**OCSP — Online Certificate Status Protocol** → Real-time query to check if a specific certificate is revoked | Faster than CRL; OCSP stapling caches the response at the server to reduce latency

**Certificate pinning** → Hardcoding expected cert/public key in client app; rejects any other cert even from trusted CA | Prevents MITM via rogue CA; used in mobile apps

**Wildcard certificate** → Covers all subdomains at one level: *.example.com | Efficient for many subdomains; doesn't cover root domain or multi-level subdomains (*.*.example.com)

**SAN certificate** → Subject Alternative Name; covers multiple specific hostnames in one cert | More precise than wildcard; explicitly lists each covered hostname

**Self-signed certificate** → Cert signed by its own private key rather than a CA; not trusted by default | Used internally; browsers show warning for public-facing use

## Network Security

**Firewall** → Filters traffic based on rules (ACLs); first line of defense | Stateless (packet filter) vs. stateful (tracks connections) vs. NGFW (layer 7 inspection)

**IDS — Intrusion Detection System** → Monitors traffic/activity for suspicious patterns; generates alerts | Passive — detects and alerts but does NOT block; NIDS (network), HIDS (host)

**IPS — Intrusion Prevention System** → Monitors AND actively blocks malicious traffic | Inline — must be placed in the traffic path; false positives can disrupt traffic

**WAF — Web Application Firewall** → Filters HTTP/HTTPS traffic to protect web apps from OWASP Top 10 | SQLi, XSS, CSRF, OWASP Top 10; operates at Layer 7

**SIEM** → Security Information and Event Management; aggregates, normalizes, and correlates logs; generates alerts | Splunk, QRadar; provides single pane of glass for security events

**SOAR** → Security Orchestration, Automation, and Response; automates IR playbooks | SIEM detects; SOAR responds automatically (quarantine, notify, ticket)

**EDR** → Endpoint Detection and Response; monitors endpoint for threats, enables investigation and response | CrowdStrike Falcon, Carbon Black, Microsoft Defender for Endpoint

**XDR** → Extended Detection and Response; cross-domain (endpoint + network + cloud + email) | Correlates attacks spanning multiple vectors in one view

**UEBA** → User and Entity Behavior Analytics; ML-based anomaly detection for users and devices | Detects compromised accounts, insider threats based on behavioral deviations

**NAC — Network Access Control** → Checks device compliance (patches, AV) before granting network access | 802.1X with health checks; quarantine VLAN for non-compliant devices

**DMZ — Demilitarized Zone / Screened Subnet** → Network segment between internet and internal network; hosts public-facing services | Web servers, mail servers, DNS; firewalls on both sides

**VLAN — Virtual LAN** → Logical network segmentation at Layer 2; limits broadcast domains and lateral movement | Separate VLANs for servers, workstations, IoT, guests

**VPN — Virtual Private Network** → Encrypted tunnel over public network | Remote access VPN (user to network) vs site-to-site VPN (network to network)

**CASB — Cloud Access Security Broker** → Sits between org and cloud services; enforces DLP, visibility, and policy | Discovers shadow IT; controls cloud app access; applies DLP to cloud-bound data

## Attack Types — Know These Cold

**Phishing** → Fraudulent email to steal credentials or deliver malware | Broad, non-targeted; most common initial access vector

**Spear phishing** → Targeted phishing using personalized info from OSINT | Researched target; higher success rate; precursor to APT attacks

**Whaling** → Spear phishing targeting executives (CEO, CFO) | High-value target; often combined with BEC

**Vishing** → Voice/phone phishing | "IT support" calling for your password; pretexting over the phone

**Smishing** → SMS phishing | Text message with malicious link or credential request

**BEC — Business Email Compromise** → Impersonating executive via email to authorize fraudulent transfers | Attacker impersonates CEO/CFO to trick finance employee into wire transfer

**Pretexting** → Fabricating a scenario (pretext) to manipulate a target | Foundation of most social engineering attacks; "I'm from IT, I need your password"

**Watering hole** → Compromising a website the target group visits; waiting for them | Like a predator at a watering hole; targets a group not an individual

**Typosquatting** → Registering misspelled/look-alike domains | paypa1.com, gooogle.com; captures mistyped URL traffic

**Baiting** → Luring victim with something enticing (USB drive, download) | Curiosity kills the cat; "Payroll Q4 - Confidential" USB in parking lot

**Tailgating/Piggybacking** → Following authorized person through secured door | Social courtesy exploit; mitigated by mantraps and security culture

**SQL injection** → Inserting malicious SQL in input fields to manipulate database | `' OR '1'='1`; most critical web vulnerability; mitigated by parameterized queries

**XSS — Cross-Site Scripting** → Injecting malicious scripts into web pages | Stored (persistent) vs Reflected; steals session cookies; mitigated by output encoding

**CSRF — Cross-Site Request Forgery** → Tricks browser into making unauthorized request using active session | User must be logged in; mitigated by CSRF tokens

**SSRF — Server-Side Request Forgery** → Tricks server into making requests to internal resources | Cloud metadata endpoints (169.254.169.254); Capital One breach used SSRF

**IDOR — Insecure Direct Object Reference** → Accessing another user's data by manipulating object identifiers | Change `?id=12345` to `?id=12346` to see someone else's account

**Pass-the-hash** → Using captured NTLM hash to authenticate without knowing the plaintext password | Windows lateral movement; mitigated by Credential Guard, local admin password randomization

**Kerberoasting** → Extracting Kerberos service ticket hashes from AD for offline cracking | Targets service accounts with SPNs; cracked offline with Hashcat

**Golden ticket attack** → Using KRBTGT hash to forge arbitrary Kerberos tickets | Full AD compromise; requires domain controller access; mitigated by regularly rotating KRBTGT

**Pass-the-ticket** → Stealing and reusing Kerberos tickets without cracking them | Related to pass-the-hash but for Kerberos environments

**Replay attack** → Capturing valid auth data and retransmitting it later | Mitigated by timestamps, nonces, and session tokens

**Evil twin** → Rogue AP mimicking a legitimate SSID | Deauthentication + evil twin; intercepts traffic; mitigated by 802.1X and WIDS

**DNS poisoning** → Injecting false DNS records into resolver cache | Redirects users to attacker-controlled IPs; mitigated by DNSSEC

**Ransomware** → Encrypts victim's data; demands payment for decryption key | WannaCry, REvil; response: isolate → preserve evidence → restore from clean backups

**Supply chain attack** → Compromising a vendor/update to reach downstream targets | SolarWinds SUNBURST; XZ Utils backdoor; very high impact per attack

**Living off the Land (LotL)** → Using legitimate OS tools (PowerShell, WMI, cmd) to avoid detection | No new malware binaries; defeats signature-based AV; detected by behavioral analysis

## Incident Response

**NIST IR Phases** → Preparation → Detection & Analysis → Containment, Eradication & Recovery → Post-Incident Activity | PICERL mnemonic: Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned

**Containment** → FIRST action after confirming an incident — stop the spread before eradication | Isolate affected systems; don't eradicate before containing

**Order of volatility** → CPU/cache → RAM → Swap/page file → Disk → Remote logs → Archives | Most volatile first; RAM is lost on power-off; capture it first in forensics

**Chain of custody** → Documentation of who handled evidence, when, and how | Required for legal admissibility; any gap can invalidate evidence

**Write blocker** → Hardware device that prevents writes to forensic evidence media | Ensures imaging doesn't alter the original drive; required for admissible forensics

**Forensic image hash** → Cryptographic hash (SHA-256) computed before and after imaging to verify integrity | If hashes match, the copy is bit-for-bit identical to the original

**Tabletop exercise** → Discussion-based simulation; no live systems touched | Cheapest, least disruptive; identifies process and communication gaps

**True positive** → Real attack, alert fired | What security teams want
**False positive** → No real attack, alert fired | Alert fatigue; tune detection rules
**False negative** → Real attack, no alert | Most dangerous; missed detection
**True negative** → No attack, no alert | Good; no action needed

## Risk Management

**Risk formula** → Risk = Threat × Vulnerability × Impact | Reduce any component to reduce overall risk

**SLE** → Single Loss Expectancy = Asset Value × Exposure Factor | One-time financial loss from a single incident

**ARO** → Annualized Rate of Occurrence = how often a threat occurs per year | Once in 10 years = ARO of 0.1

**ALE** → Annualized Loss Expectancy = SLE × ARO | Expected annual loss; cost of controls should be less than ALE

**Risk avoidance** → Eliminate the activity creating the risk entirely | Stop using FTP entirely instead of securing it

**Risk transference** → Shift financial impact to a third party | Cyber insurance; indemnification clauses in vendor contracts

**Risk mitigation** → Reduce likelihood or impact through controls | Patching, MFA, backups, encryption

**Risk acceptance** → Document and accept the residual risk | When mitigation cost exceeds potential loss; must be formally documented

**Residual risk** → Risk remaining after controls are applied | What you're left with after mitigation; can be accepted or transferred

**RTO — Recovery Time Objective** → Maximum acceptable downtime | Drives DR design: how fast must we recover?

**RPO — Recovery Point Objective** → Maximum acceptable data loss measured in time | Drives backup frequency: how old can recovered data be?

**MTTR — Mean Time to Recover** → Average actual time to restore a system after failure | Lower is better; actual performance vs. RTO goal

**MTBF — Mean Time Between Failures** → Average time a system operates between failures | Higher is better; measure of reliability

**BIA — Business Impact Analysis** → Identifies critical functions and impact of their disruption | Produces RTO/RPO requirements; prioritizes recovery order

## Compliance Frameworks

**NIST CSF** → Identify, Protect, Detect, Respond, Recover | Voluntary U.S. framework; widely adopted; risk-based

**NIST RMF (SP 800-37)** → Categorize, Select, Implement, Assess, Authorize, Monitor | Mandatory for federal systems under FISMA; structured 6-step process

**NIST SP 800-53** → Security and privacy controls catalog for federal systems | Used with RMF; hundreds of specific controls organized by family

**ISO 27001** → International ISMS standard; formal certification available | Used by global organizations; certifiable by third-party auditors

**HIPAA** → U.S. healthcare: protects PHI (Protected Health Information) | Applies to covered entities and business associates; breach notification within 60 days

**GDPR** → EU: protects personal data of EU/EEA residents | 72-hour breach notification; right to erasure; applies globally to EU data subjects

**PCI-DSS** → Payment card data security; 12 requirements | Required for any org storing/processing/transmitting card data; annual assessment

**SOX** → Sarbanes-Oxley: financial reporting integrity for U.S. public companies | IT controls supporting financial reporting; audit trails required

## Data Classification & Handling

**Data at rest** → Stored data; protect with encryption (AES, FDE, BitLocker) | Highest volume of sensitive data; SED, FDE, database encryption

**Data in transit** → Data moving across networks; protect with TLS, IPSec, VPN | HTTPS, SFTP, encrypted email (S/MIME, TLS)

**Data in use** → Data being processed in memory; hardest to protect | Memory forensics captures this; Trusted Execution Environments (TEEs) help

**Tokenization** → Replace sensitive data with non-sensitive token; original in secure vault | PCI-DSS recognized; reduces cardholder data environment scope

**Anonymization** → Permanently remove all identifying information | Cannot be reversed; GDPR considers truly anonymized data out of scope

**Pseudonymization** → Replace identifiers with pseudonyms; reversible with key | GDPR recognizes this but it's still personal data; better than nothing

**Data masking** → Replace real data with realistic fake data for testing | Dev/test environments; "555-1234" phone numbers in test databases

## Wireless Security

**WEP** → Broken; uses RC4; do not use | Crackable in minutes with aircrack-ng

**WPA2** → Uses CCMP/AES; secure with strong passphrase; enterprise mode uses 802.1X | Current standard for most deployments; KRACK attack possible in PSK mode

**WPA3** → Uses SAE (Simultaneous Authentication of Equals); no PSK offline dictionary attacks | Current best; resistant to offline cracking even with captured handshake

**WPS (Wi-Fi Protected Setup)** → Disable immediately; 8-digit PIN is brute-forceable in ~4 hours | CVE-2011-5053; known vulnerability; universally recommended to disable

**SSID hiding** → Minimal security; easily discovered by passive scanning | Not a security control; just inconvenience

**MAC filtering** → Minimal security; MACs are trivially spoofed | Not a security control; not a substitute for WPA3/802.1X

**Evil twin** → Rogue AP with same SSID; users connect thinking it's legitimate | Use 802.1X (certificate-based auth) to prevent; WIDS to detect

## Email Security

**SPF** → DNS TXT record listing authorized sending IPs for a domain | Checks: is this IP allowed to send for this domain? Does not sign message body

**DKIM** → Cryptographic signature added to email headers; verified via DNS public key | Signs the message; if signature invalid, message was tampered or forged

**DMARC** → Policy layer; tells receivers what to do when SPF/DKIM fails (none/quarantine/reject) | Reports back to domain owner; builds on SPF + DKIM

**S/MIME** → End-to-end email encryption and signing; requires cert on each user's email client | Gold standard for email confidentiality; rarely deployed due to complexity
