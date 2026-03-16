**Q1.** An organization implements a policy requiring every access request — even from devices already inside the corporate network — to be verified against identity, device health, and context before being granted. No implicit trust is granted based on network location. Which security model is this?

A) Defense in depth
B) Zero trust architecture
C) NAC
D) Perimeter security model

<details><summary>Answer</summary>

**B) Zero trust architecture**

Zero trust is based on the principle of "never trust, always verify." No entity is trusted by default regardless of network location (inside or outside the perimeter). Every access request is continuously evaluated against identity, device posture, and context. This contrasts with the traditional perimeter (castle-and-moat) model that trusts anything inside the network boundary.

</details>

---

**Q2.** In a zero trust architecture, which component evaluates access requests against policies and decides whether to grant or deny access?

A) PEP
B) PDP
C) IdP
D) CA

<details><summary>Answer</summary>

**B) PDP**

The PDP (Policy Decision Point) — sometimes called the Policy Engine — evaluates access requests against the organization's policies, user identity, device health, and environmental context, then issues an allow or deny decision. The PEP (Policy Enforcement Point) enforces that decision by allowing or blocking the actual traffic/access.

</details>

---

**Q3.** A cloud-native organization deploys software-defined controls that isolate individual workloads from each other, so that a compromised container cannot directly access other containers in the same data center. Which security technique is this?

A) VLANs
B) Air gapping
C) Microsegmentation
D) DMZ placement

<details><summary>Answer</summary>

**C) Microsegmentation**

Microsegmentation uses software-defined networking to enforce fine-grained access controls at the individual workload, container, or VM level. Even workloads on the same physical host are isolated. This limits lateral movement — a compromised workload cannot freely access others. Traditional VLANs (Virtual Local Area Networks) operate at a coarser layer (subnet level).

</details>

---

**Q4.** A company places its public-facing web servers and mail servers in a network segment that is separated from the internal corporate network by a firewall, while another firewall sits between this segment and the internet. What is this network architecture called?

A) Air gap
B) VLAN segmentation
C) Screened subnet (DMZ)
D) Honeynet

<details><summary>Answer</summary>

**C) Screened subnet (DMZ)**

A screened subnet (formerly called DMZ — Demilitarized Zone) is a network segment that sits between the untrusted internet and the trusted internal network, separated by firewalls on both sides. Public-facing servers (web, mail, DNS) are placed here to limit the blast radius of a compromise — attackers cannot reach the internal network directly.

</details>

---

**Q5.** A company uses AWS for its infrastructure. A security audit finds that the company is responsible for patching the guest operating systems on their EC2 instances, while AWS manages the physical data center security and hypervisor layer. Which cloud concept does this describe?

A) CASB
B) Shared responsibility model
C) IaaS
D) CSPM

<details><summary>Answer</summary>

**B) Shared responsibility model**

The shared responsibility model defines which security responsibilities belong to the cloud provider and which belong to the customer. For IaaS (Infrastructure as a Service) (like EC2): AWS secures the physical infrastructure, hypervisor, and networking; the customer secures the OS, middleware, applications, and data. For SaaS (Software as a Service), the provider takes on much more responsibility.

</details>

---

**Q6.** In a Software as a Service (SaaS) deployment, which security control is the customer ALWAYS responsible for, regardless of the shared responsibility model?

A) Physical data center security
B) Network infrastructure patching
C) IAM
D) Application runtime security

<details><summary>Answer</summary>

**C) IAM**

Across all cloud service models (IaaS (Infrastructure as a Service), PaaS, SaaS (Software as a Service)), the customer retains responsibility for managing user identities, access rights, and data. The provider manages the platform, but who can access the customer's data is always the customer's responsibility. This is a critical and frequently tested cloud security concept.

</details>

---

**Q7.** An organization wants visibility into data being uploaded to cloud storage services from corporate devices and the ability to enforce data loss prevention policies for cloud-bound traffic. Which security tool provides this?

A) NGFW
B) WAF
C) CASB
D) SIEM

<details><summary>Answer</summary>

**C) CASB**

A CASB (Cloud Access Security Broker) sits between the organization and cloud service providers to enforce security policies, provide visibility into cloud usage (shadow IT), apply DLP (Data Loss Prevention) controls, and detect threats in cloud-bound traffic. A WAF (Web Application Firewall) protects web applications from layer 7 attacks; an NGFW (Next-Generation Firewall) operates at the network perimeter; SIEM (Security Information and Event Management) aggregates and correlates logs.

</details>

---

**Q8.** A company needs employees to remotely access internal resources over the internet. The IT team wants to ensure ALL internet traffic from remote workers is routed through the corporate network for inspection, even non-work traffic. Which VPN configuration achieves this?

A) Split tunneling
B) Full tunnel VPN
C) Site-to-site VPN
D) Remote access VPN with split tunneling

<details><summary>Answer</summary>

**B) Full tunnel VPN**

A full tunnel VPN (Virtual Private Network) routes ALL of the client's traffic through the VPN tunnel to the corporate network, including traffic destined for the internet. This allows the corporate security stack to inspect all traffic. Split tunneling only routes traffic destined for corporate resources through the VPN, sending other traffic directly to the internet.

</details>

---

**Q9.** A company has two branch offices that need to communicate securely over the internet as if they were on the same private network. Which VPN type is MOST appropriate?

A) Remote access VPN
B) Site-to-site VPN
C) SSL VPN
D) Split tunnel VPN

<details><summary>Answer</summary>

**B) Site-to-site VPN**

A site-to-site VPN (Virtual Private Network) connects two entire networks (branch offices) over the internet using a persistent, encrypted tunnel between gateway devices. Remote access VPN connects individual users; SSL VPN is a protocol option; split tunneling is a traffic routing configuration, not a VPN type.

</details>

---

**Q10.** A PKI administrator needs to issue a single TLS certificate that will be valid for `www.example.com`, `mail.example.com`, and `api.example.com`. Which certificate type should be used?

A) Wildcard certificate
B) Self-signed certificate
C) SAN certificate
D) EV certificate

<details><summary>Answer</summary>

**C) SAN certificate**

A SAN certificate can cover multiple distinct hostnames in a single certificate by listing them in the Subject Alternative Name extension. A wildcard certificate (`*.example.com`) covers all subdomains at one level but cannot cover different base domains in the same cert. For exactly specified hostnames, a SAN cert is the correct choice.

</details>

---

**Q11.** A web developer needs a single certificate to cover all subdomains of `example.com`, including `www.example.com`, `shop.example.com`, and any future subdomains. Which certificate type is MOST efficient?

A) SAN certificate
B) Wildcard certificate
C) EV certificate
D) Code signing certificate

<details><summary>Answer</summary>

**B) Wildcard certificate**

A wildcard certificate (`*.example.com`) covers all subdomains at one level under the domain automatically, including future subdomains, without needing to specify each one. This is more efficient than a SAN cert when the exact subdomains are not known in advance or when there are many of them.

</details>

---

**Q12.** A browser displays a certificate error warning indicating that a website's certificate was issued by a CA that the browser does not recognize. What is the MOST likely cause?

A) The certificate has expired
B) The certificate has been revoked
C) The certificate chain leads to an untrusted or self-signed root CA
D) The certificate's hostname does not match the URL

<details><summary>Answer</summary>

**C) The certificate chain leads to an untrusted or self-signed root CA**

TLS (Transport Layer Security) certificate trust is established through a chain: the server certificate is signed by an intermediate CA, which is signed by a root CA that the browser/OS trusts. If the root CA is not in the browser's trusted store (e.g., it's self-signed or from an enterprise CA not distributed to the browser), the chain of trust breaks and the browser shows an untrusted CA warning.

</details>

---

**Q13.** A security architect is designing a network for a manufacturing facility that includes industrial control systems (ICS) running proprietary legacy software. The ICS systems cannot be patched. Which design approach BEST reduces risk?

A) Deploy antivirus on the ICS systems
B) Place the ICS systems on the same VLAN as office workstations to simplify monitoring
C) Air-gap the ICS network from all other networks and internet connectivity
D) Connect the ICS systems to the internet so vendors can push remote updates

<details><summary>Answer</summary>

**C) Air-gap the ICS network from all other networks and internet connectivity**

An air gap provides complete physical isolation — the ICS (Industrial Control System) network has no connections to corporate networks or the internet. This is the strongest protection for unpatched legacy OT (Operational Technology) systems where vulnerabilities cannot be fixed. Without network connectivity, remote exploitation is prevented. This is the standard architecture for critical infrastructure.

</details>

---

**Q14.** A security team deploys a system on their network configured to look like a valuable, vulnerable server filled with fake data. The goal is to detect attacks early and study attacker techniques without putting real assets at risk. What is this system called?

A) DMZ server
B) Honeynet
C) Honeypot
D) Canary token

<details><summary>Answer</summary>

**C) Honeypot**

A honeypot is a decoy system intentionally made to appear valuable and vulnerable in order to attract attackers. Any access to a honeypot is inherently suspicious (legitimate users have no reason to access it), making it a high-fidelity early warning system. A honeynet is a network of multiple honeypots.

</details>

---

**Q15.** Security analysts want to monitor attacker behavior across an entire simulated network environment with multiple fake systems representing a realistic corporate infrastructure. Which technology provides this?

A) IDS/IPS
B) Honeypot
C) Honeynet
D) SIEM

<details><summary>Answer</summary>

**C) Honeynet**

A honeynet is a network of interconnected honeypots designed to simulate a realistic corporate environment, allowing security researchers to observe attacker lateral movement, tools, and techniques across multiple systems. A single honeypot is limited to one fake system.

</details>

---

**Q16.** A security team inserts a fake high-privilege Active Directory account with a distinctive name into the directory but never uses it operationally. An alert fires whenever this account is used. What is this technique?

A) Honeypot
B) Honey token
C) DNS sinkhole
D) Canary file

<details><summary>Answer</summary>

**B) Honey token**

A honey token is a fake data item (credential, file, database record, or account) that triggers an alert when accessed or used. Since legitimate operations never touch it, any access indicates unauthorized activity. Honey tokens are low-cost, high-fidelity detection mechanisms. A canary file is a specific type of honey token.

</details>

---

**Q17.** An organization's network security tool intercepts DNS queries for domains known to host malware command-and-control infrastructure and redirects those queries to a controlled internal IP address, preventing malware from reaching its C2 server. What is this technique?

A) DNS cache poisoning
B) DNS sinkhole
C) DNSSEC
D) DNS filtering

<details><summary>Answer</summary>

**B) DNS sinkhole**

A DNS (Domain Name System) sinkhole redirects DNS queries for known malicious domains to a controlled IP (often the sinkhole server itself), preventing malware from communicating with C2 (Command and Control) servers. It also identifies infected hosts on the network (any host querying the malicious domain is potentially compromised).

</details>

---

**Q18.** A security engineer needs to choose between a system that blocks all traffic if it crashes (fail-closed) versus one that allows all traffic through if it crashes (fail-open). Which configuration should be chosen for an IPS protecting an e-commerce payment gateway?

A) Fail-open — to ensure payment transactions are not interrupted
B) Fail-closed — to prevent unfiltered traffic from reaching the payment system
C) Either is acceptable because IPS systems rarely crash
D) Fail-open for business hours; fail-closed for off-hours

<details><summary>Answer</summary>

**B) Fail-closed — to prevent unfiltered traffic from reaching the payment system**

A payment gateway handling cardholder data requires fail-closed (fail-secure) behavior: if the IPS fails, it should block all traffic rather than allow unfiltered traffic through to the payment system. This prioritizes security over availability, which is appropriate for systems handling sensitive financial data under PCI-DSS (Payment Card Industry Data Security Standard) requirements.

</details>

---

**Q19.** Which of the following cryptographic modes of operation provides both confidentiality and authentication (integrity) in a single operation, making it preferred for TLS 1.3?

A) CBC
B) ECB
C) CTR
D) GCM

<details><summary>Answer</summary>

**D) GCM**

GCM (Galois/Counter Mode) is an authenticated encryption mode that provides both confidentiality (via CTR (Counter Mode) encryption) and message authentication (via GHASH). TLS (Transport Layer Security) 1.3 mandates authenticated encryption (AEAD (Authenticated Encryption with Associated Data)) cipher suites like AES-128-GCM and AES-256-GCM. ECB (Electronic Code Book) is insecure; CBC (Cipher Block Chaining) requires a separate MAC; CTR provides encryption but not authentication alone.

</details>

---

**Q20.** A system stores sensitive encryption keys in a dedicated tamper-resistant hardware device that never exports the keys in plaintext. Cryptographic operations are performed inside the device. What is this device called?

A) TPM
B) HSM
C) SED
D) Smart card

<details><summary>Answer</summary>

**B) HSM**

An HSM (Hardware Security Module) is a dedicated, tamper-resistant hardware appliance for secure key generation, storage, and cryptographic operations. Keys are never exposed in plaintext outside the HSM boundary. HSMs are used in PKI (Public Key Infrastructure), payment card processing (PCI-DSS (Payment Card Industry Data Security Standard)), and code signing. A TPM (Trusted Platform Module) is an embedded chip in a PC motherboard for device attestation; it serves a similar but more limited purpose.

</details>

---

**Q21.** An organization wants to protect laptop hard drives so that if a laptop is stolen, the data cannot be accessed even if the drive is removed and connected to another system. Which technology should be deployed?

A) Bitlocker TPM-based full disk encryption
B) File-level encryption with EFS
C) RAID-1 mirroring
D) VDI

<details><summary>Answer</summary>

**A) Bitlocker TPM-based full disk encryption**

FDE (Full Disk Encryption) via BitLocker with TPM (Trusted Platform Module) protects all data on the drive. If the drive is removed and placed in another system, it cannot be decrypted because the TPM binding prevents decryption outside the original hardware configuration. EFS (Encrypting File System) only encrypts individual files; RAID provides redundancy, not confidentiality; VDI (Virtual Desktop Infrastructure) stores data server-side.

</details>

---

**Q22.** Which of the following represents a data state that is the most difficult to protect with encryption and is the primary target during a live memory forensics investigation?

A) Data at rest
B) Data in transit
C) Data in use
D) Data in archive

<details><summary>Answer</summary>

**C) Data in use**

Data in use (data being processed in CPU registers and RAM) is the hardest to protect because it must be decrypted to be processed. It is the primary target for memory forensics (capturing encryption keys, credentials, and sensitive data from RAM). TEEs (Trusted Execution Environments) like Intel SGX are emerging mitigations.

</details>

---

**Q23.** A healthcare organization needs to share patient datasets with a research partner for analysis but must ensure that individual patients cannot be identified from the dataset. Which data protection technique should be applied?

A) Tokenization
B) Encryption
C) Data masking
D) Anonymization

<details><summary>Answer</summary>

**D) Anonymization**

Anonymization permanently removes all identifying information from the dataset so that individuals cannot be identified, even with additional external data. Unlike pseudonymization, anonymization cannot be reversed. This is the appropriate technique when data is shared externally for research. GDPR (General Data Protection Regulation) recognizes truly anonymized data as outside its scope.

</details>

---

**Q24.** A payment processor replaces stored credit card numbers with random tokens in their application database. The actual card numbers are stored in a separate, highly secured vault. Which data protection technique is this?

A) Encryption
B) Tokenization
C) Anonymization
D) Data masking

<details><summary>Answer</summary>

**B) Tokenization**

Tokenization replaces sensitive data (credit card numbers) with non-sensitive substitutes (tokens) that have no exploitable value. The original data is stored in a secure token vault and can be retrieved by authorized systems. PCI-DSS (Payment Card Industry Data Security Standard) explicitly recognizes tokenization as a method to reduce the scope of cardholder data environments.

</details>

---

**Q25.** An attacker discovers that an IDS uses only signature-based detection. They slightly modify a known exploit to change its byte pattern while preserving its function. The modified exploit bypasses the IDS. What is this technique called?

A) Zero-day exploit
B) Evasion / obfuscation
C) Polymorphic malware
D) Living off the land

<details><summary>Answer</summary>

**C) Polymorphic malware**

Polymorphic malware changes its code signature (byte pattern) with each iteration while maintaining the same malicious functionality, evading signature-based detection. Metamorphic malware goes further by rewriting its entire codebase. This is why behavior-based and heuristic detection are important complements to signature-based AV.

</details>

---

**Q26.** An organization's mobile device management (MDM) policy enforces screen lock, remote wipe capability, and prevents users from installing apps from unknown sources. A remote wipe is triggered when an employee reports their company phone stolen. This scenario primarily addresses which data state security concern?

A) Data in transit
B) Data in use
C) Data at rest on a lost/stolen endpoint
D) Data processed in cloud applications

<details><summary>Answer</summary>

**C) Data at rest on a lost/stolen endpoint**

MDM (Mobile Device Management) remote wipe protects data at rest on a lost or stolen device. If the device falls into the wrong hands, the MDM can wipe the device before an attacker can bypass local encryption or access controls. This is a key mobile device security control.

</details>

---

**Q27.** A security architect needs to deploy a security solution that can detect and block attacks targeting a specific web application, including SQL injection, XSS, and OWASP Top 10 vulnerabilities, without affecting network-level traffic. Which tool is MOST appropriate?

A) Network-based IPS
B) NGFW
C) WAF
D) UTM

<details><summary>Answer</summary>

**C) WAF**

A WAF (Web Application Firewall) operates at Layer 7 (application layer) and is specifically designed to detect and block web application attacks including SQLi (SQL Injection), XSS (Cross-Site Scripting), CSRF (Cross-Site Request Forgery), and other OWASP Top 10 vulnerabilities by inspecting HTTP/HTTPS traffic. A network IPS operates at lower layers and lacks application-context awareness; an NGFW (Next-Generation Firewall) provides some layer 7 inspection but is not specialized for web application attacks.

</details>

---

**Q28.** An organization is leveraging a VPN between its headquarters and a branch location. Which of the following is the VPN protecting?

A) Data in use
B) Data in transit
C) Geographic restrictions
D) Data sovereignty

<details><summary>Answer</summary>

**B) Data in transit**

VPNs encrypt data as it travels across an untrusted network (such as the public internet), protecting data in transit. Data in use refers to data being actively processed in memory; data at rest is data stored on disk. Geographic restrictions and data sovereignty are legal/regulatory concepts, not VPN functions.

</details>

---

**Q29.** Configuring a VPN to preserve bandwidth requires which of the following settings?

A) Point-to-Point Tunneling
B) Secure Socket Tunneling
C) Full tunnel
D) Split tunnel

<details><summary>Answer</summary>

**D) Split tunnel**

Split tunneling sends only traffic destined for the corporate network through the VPN tunnel, while all other internet traffic travels directly to the destination without going through the corporate gateway. This preserves bandwidth at the corporate end. Full tunneling routes all traffic through the VPN, maximizing security but consuming more bandwidth.

</details>

---

**Q30.** Which PKI trust model uses a single master CA called the root that signs all other certificate authorities?

A) Distributed trust model
B) Bridge trust model
C) Hierarchical trust model
D) Centralized trust model

<details><summary>Answer</summary>

**C) Hierarchical trust model**

The hierarchical trust model uses a single root CA at the top of a chain of trust. The root CA signs intermediate CAs, which in turn sign end-entity certificates. This creates a predictable chain of trust. The bridge model connects separate PKI hierarchies; the distributed model has multiple equally trusted CAs; there is no standard "centralized" model per se.

</details>

---

**Q31.** A certificate is needed to cover the domains .domain.com and .domain.org plus all of their subdomains. Which type of certificate should be used?

A) Domain validation certificate
B) Wildcard certificate
C) SAN certificate
D) Extended validation certificate

<details><summary>Answer</summary>

**C) SAN (Subject Alternative Name) certificate**

A SAN certificate allows a single certificate to cover multiple different domain names and hostnames in a single certificate. A wildcard certificate covers first-level subdomains of a single domain (e.g., *.domain.com) but cannot cover multiple different base domains. A domain validation certificate only confirms domain control; an EV certificate requires additional identity verification.

</details>

---

**Q32.** Which technology is most effective in segmenting and isolating different workloads within a cloud environment?

A) VLANs
B) Zero Trust Architecture
C) Firewalls
D) Microsegmentation

<details><summary>Answer</summary>

**D) Microsegmentation**

Microsegmentation divides a network or cloud environment into very small, isolated segments and applies granular security policies to each. In cloud/virtualized environments, it is more flexible and granular than traditional VLANs. Zero Trust Architecture is a broader security philosophy; VLANs are effective in on-premises environments but less granular for cloud workloads; firewalls provide perimeter control but not workload-level isolation.

</details>

---

**Q33.** In an asymmetric server cluster, what does the standby server do?

A) Performs useful work plus provides failover support
B) Performs no useful work — it only waits on standby
C) Launches virtual machine copies when load increases
D) Increases the total number of cluster nodes needed

<details><summary>Answer</summary>

**B) Performs no useful work — it only waits on standby**

In an asymmetric cluster (active-passive), the standby server remains idle until the active server fails, at which point it takes over. This differs from a symmetric (active-active) cluster, where all nodes perform useful work simultaneously. Asymmetric clustering is simpler but wastes the standby server's capacity under normal operation.

</details>

---

**Q34.** What is the significant difference between block ciphers and stream ciphers?

A) Block ciphers are more efficient for continuous data streams
B) Stream ciphers divide data into fixed-size blocks
C) They use different numbers of keys
D) Block ciphers encrypt in fixed-size blocks; stream ciphers encrypt one bit or byte at a time

<details><summary>Answer</summary>

**D) Block ciphers encrypt in fixed-size blocks; stream ciphers encrypt one bit or byte at a time**

Block ciphers (e.g., AES) process data in fixed-size chunks (typically 128 bits). Stream ciphers (e.g., RC4, ChaCha20) encrypt data one bit or byte at a time, making them suitable for real-time data streams. Stream ciphers are often faster for continuous streams; block ciphers are widely used in file and disk encryption.

</details>

---

**Q35.** What is the critical difference between SSL and TLS?

A) SSL is still commonly used for securing internet data
B) TLS and SSL are exactly the same
C) TLS requires certificates while SSL does not
D) SSL combined encryption with authentication; TLS does not

<details><summary>Answer</summary>

**C) TLS requires certificates**

TLS (Transport Layer Security) is the modern replacement for SSL (Secure Sockets Layer), which has been deprecated due to numerous vulnerabilities. TLS requires both parties to use certificates for authentication and requires certificate validation. SSL has known weaknesses (POODLE, DROWN) and should not be used. When you see "SSL certificate" in modern usage, it is technically a TLS certificate.

</details>

---

**Q36.** What does the primary use of a Subject Alternative Name (SAN) certificate allow?

A) Identify a specific computer within a domain
B) Serve as evidence of organizational trustworthiness
C) Used for multiple different-named domains owned by the same organization
D) Indicate control over a specific DNS domain

<details><summary>Answer</summary>

**C) Used for multiple different-named domains owned by the same organization**

SAN certificates allow organizations to secure multiple different domain names (e.g., example.com, example.org, mail.example.net) under a single certificate. This is more flexible than wildcard certificates, which only cover subdomains of a single base domain. SAN is defined in RFC 5280 and is the standard for modern multi-domain certificates.

</details>

---

**Q37.** What is public key pinning used for?

A) Timestamp and sign OCSP responses
B) Reduce OCSP traffic to the CA
C) Prevent attackers from impersonating a website using fraudulent certificates
D) Specify how long client browsers should cache data

<details><summary>Answer</summary>

**C) Prevent attackers from impersonating a website using fraudulent certificates**

Public key pinning (HTTP Public Key Pinning, or HPKP) is a security mechanism that allows a website to specify which CA or certificate should be trusted for that domain. This prevents man-in-the-middle attacks where an attacker uses a fraudulently issued but technically valid certificate from a different CA to impersonate the site.

</details>

---
