**Q1.** A security analyst configures a system so that no single administrator can both approve and implement changes to production servers. Which security principle is being enforced?

A) Least privilege
B) Separation of duties
C) Defense in depth
D) Need to know

<details><summary>Answer</summary>

**B) Separation of duties**

Separation of duties divides critical tasks between multiple people so no single person can complete a harmful action alone. This prevents fraud and insider threats. Least privilege limits permissions to what is needed; defense in depth uses layered controls; need to know limits access to relevant information only.

</details>

---

**Q2.** A company deploys firewalls, encrypts data at rest, requires MFA for all logins, and conducts quarterly security awareness training. Which security principle does this combination of controls best represent?

A) Least privilege
B) Zero trust
C) Defense in depth
D) Separation of duties

<details><summary>Answer</summary>

**C) Defense in depth**

Defense in depth is a layered security strategy that deploys multiple overlapping controls — technical (firewall, encryption, MFA (Multi-Factor Authentication)) and administrative (training) — so that failure of one control does not compromise the whole system.

</details>

---

**Q3.** An employee is granted only the permissions required to perform their job and nothing more. Which principle does this describe?

A) Separation of duties
B) Least privilege
C) Need to know
D) Job rotation

<details><summary>Answer</summary>

**B) Least privilege**

Least privilege grants users the minimum permissions necessary to perform their role. Need to know is related but specifically refers to limiting access to information; least privilege is the broader principle covering all access rights and permissions.

</details>

---

**Q4.** A security policy states that after three years in the same role, employees in the finance department must switch to a different position for at least six months. Which security principle does this policy implement?

A) Separation of duties
B) Least privilege
C) Job rotation
D) Mandatory vacation

<details><summary>Answer</summary>

**C) Job rotation**

Job rotation periodically moves employees between roles to detect and prevent fraud (since a successor may discover misuse), and to cross-train staff. Mandatory vacation serves a similar anti-fraud purpose for shorter durations. Separation of duties divides a single task between multiple people.

</details>

---

**Q5.** A company's keycard system grants a user access to the building entrance but not to the server room or executive floor. Which access control model is most likely in use?

A) DAC
B) MAC
C) RBAC
D) ABAC

<details><summary>Answer</summary>

**C) RBAC**

RBAC (Role-Based Access Control) assigns permissions to roles, then assigns roles to users. The employee's role grants building access but not server room or executive access. DAC (Discretionary Access Control) lets data owners set permissions; MAC (Mandatory Access Control) uses security labels; ABAC (Attribute-Based Access Control) uses multiple attributes (user, time, location) for policy decisions.

</details>

---

**Q6.** A government agency classifies data using labels such as Top Secret, Secret, and Unclassified, and users can only access data at or below their clearance level. Which access control model is this?

A) RBAC
B) DAC
C) MAC
D) ABAC

<details><summary>Answer</summary>

**C) MAC**

MAC (Mandatory Access Control) assigns security labels to both subjects (users) and objects (data), and access is granted only when the subject's clearance meets or exceeds the object's label. Users cannot change permissions on objects they own. This model is common in government/military environments.

</details>

---

**Q7.** A file server allows the owner of each shared folder to decide who else can read or modify the folder's contents. Which access control model is this?

A) MAC
B) DAC
C) RBAC
D) Rule-based AC

<details><summary>Answer</summary>

**B) DAC**

In DAC (Discretionary Access Control), the resource owner has discretion over who can access their resource. This is the most flexible but least secure model because it relies on individual users making good security decisions. Windows NTFS (New Technology File System) permissions with file ownership are a common real-world example.

</details>

---

**Q8.** An organization's access control policy allows a contractor to access a specific database only during business hours, only from a company-managed device, and only from the corporate network. Which access control model best describes this policy?

A) DAC
B) MAC
C) RBAC
D) ABAC

<details><summary>Answer</summary>

**D) ABAC**

ABAC (Attribute-Based Access Control) grants access based on attributes of the user (role: contractor), the resource (specific database), the environment (time of day, network location), and the device (managed device). This multi-attribute evaluation makes ABAC the most granular and flexible model.

</details>

---

**Q9.** Which of the following BEST describes the difference between authentication and authorization?

A) Authentication verifies what resources a user can access; authorization verifies who the user is.
B) Authentication verifies who the user is; authorization determines what resources the user can access.
C) Authentication uses passwords; authorization uses biometrics.
D) Authentication and authorization are interchangeable terms for the same process.

<details><summary>Answer</summary>

**B) Authentication verifies who the user is; authorization determines what resources the user can access.**

Authentication (AuthN) answers "Who are you?" — verifying identity via credentials. Authorization (AuthZ) answers "What are you allowed to do?" — granting or denying access to resources. These are distinct processes that always occur in this order.

</details>

---

**Q10.** A user logs in with a username and password, then receives a push notification on their smartphone that they must approve before access is granted. Which authentication category does the smartphone approval represent?

A) Something you know
B) Something you have
C) Something you are
D) Somewhere you are

<details><summary>Answer</summary>

**B) Something you have**

The smartphone receiving the push notification is a physical possession factor — something you have. The password is something you know. Together they constitute multi-factor authentication (MFA), combining two different factor categories.

</details>

---

**Q11.** A web application uses SAML to allow users to authenticate once with their corporate identity provider and then access multiple SaaS applications without logging in again. Which capability does this describe?

A) Multi-factor authentication
B) SSO
C) OAuth authorization
D) RADIUS authentication

<details><summary>Answer</summary>

**B) SSO**

SSO (Single Sign-On) allows a user to authenticate once and gain access to multiple systems without re-entering credentials. SAML (Security Assertions Markup Language) is the protocol commonly used to implement SSO and identity federation between an identity provider (IdP) and service providers.

</details>

---

**Q12.** A developer needs to allow a third-party fitness app to access a user's calendar data without the user sharing their calendar password with the fitness app. Which protocol is BEST suited for this?

A) SAML
B) LDAP
C) OAuth 2.0
D) RADIUS

<details><summary>Answer</summary>

**C) OAuth 2.0**

OAuth 2.0 is an authorization framework that allows a third-party application to access a user's resources on another service without exposing the user's credentials. The user grants limited delegated access via a token. SAML (Security Assertions Markup Language) is used for authentication/federation; LDAP (Lightweight Directory Access Protocol) is a directory protocol; RADIUS (Remote Authentication Dial-In User Service) is for network access authentication.

</details>

---

**Q13.** An application allows users to log in using their Google account. Google confirms the user's identity and provides the application with the user's name and email address. Which protocol is being used?

A) OAuth 2.0
B) SAML
C) OIDC
D) Kerberos

<details><summary>Answer</summary>

**C) OIDC**

OIDC (OpenID Connect) is an identity layer built on top of OAuth 2.0. While OAuth 2.0 handles authorization, OIDC adds authentication by providing an ID token containing user identity claims (name, email). "Sign in with Google/Apple/Facebook" buttons use OIDC. SAML (Security Assertions Markup Language) is an older federation standard typically used in enterprise contexts.

</details>

---

**Q14.** A security team is evaluating which symmetric encryption algorithm to use for protecting data at rest. They need AES-equivalent security with the shortest possible key length for performance reasons. Which algorithm should they choose?

A) DES with 56-bit keys
B) 3DES with 112-bit keys
C) AES-128
D) AES-256

<details><summary>Answer</summary>

**C) AES-128**

AES-128 provides strong security (currently no practical attack) with a shorter key length (128 bits) than AES-256, offering better performance. DES (56-bit) and 3DES are legacy algorithms considered weak or deprecated. AES-256 is appropriate for highly sensitive data where maximum security outweighs performance.

</details>

---

**Q15.** A user's password hash is exposed in a breach. The attacker tries to look up the hash in a precomputed table of hash values but fails because each stored hash in the database is unique despite several users having the same password. Which technique prevented the attack?

A) Key stretching
B) Salting
C) Hashing with SHA-256
D) Encryption with AES

<details><summary>Answer</summary>

**B) Salting**

Salting adds a unique random value to each password before hashing, ensuring that identical passwords produce different hashes. This defeats rainbow table attacks (precomputed hash lookups) because the attacker would need a separate rainbow table for every possible salt value.

</details>

---

**Q16.** A certificate authority (CA) needs to immediately notify clients that a specific TLS certificate should no longer be trusted before its scheduled expiration date. Which mechanism provides real-time revocation status checks?

A) CRL
B) OCSP
C) Certificate pinning
D) Certificate transparency log

<details><summary>Answer</summary>

**B) OCSP**

OCSP (Online Certificate Status Protocol) allows clients to query a CA's OCSP responder in real time to check whether a specific certificate has been revoked. CRLs (Certificate Revocation Lists) are periodically published lists of revoked certificates — they are not real-time and can be large. OCSP stapling is an optimization where the server caches and presents the OCSP response to clients.

</details>

---

**Q17.** A financial institution wants to ensure that transactions cannot be denied by either the sending or receiving party after the fact. Which security property does this require?

A) Confidentiality
B) Integrity
C) Availability
D) Non-repudiation

<details><summary>Answer</summary>

**D) Non-repudiation**

Non-repudiation ensures that a party cannot deny having performed an action. It is achieved through digital signatures: the sender signs with their private key, and the signature can be verified by anyone with the public key. The sender cannot later deny signing because only they possess the private key.

</details>

---

**Q18.** A security control logs all login attempts and sends an alert when more than five failed attempts occur within one minute. Which control type is this?

A) Preventive
B) Detective
C) Corrective
D) Deterrent

<details><summary>Answer</summary>

**B) Detective**

A detective control identifies events that are occurring or have occurred and generates alerts. It does not stop the attack — the failed login attempts are still happening. A preventive control would block the attempts (account lockout); a corrective control would restore a system after harm; a deterrent discourages attacks before they start.

</details>

---

**Q19.** After a security incident, an organization implements account lockout after five failed login attempts. Which control type is an account lockout policy?

A) Detective
B) Corrective
C) Preventive
D) Compensating

<details><summary>Answer</summary>

**C) Preventive**

A preventive control stops a threat before harm occurs. Account lockout prevents further brute-force attempts by locking the account after a threshold of failures. A detective control would only alert on the activity. A corrective control addresses harm after it happens.

</details>

---

**Q20.** An organization cannot upgrade a legacy medical device because the vendor no longer supports it. To reduce risk, they place the device on an isolated VLAN with no internet access and require all connections to go through a bastion host with enhanced logging. This is an example of which control type?

A) Preventive
B) Detective
C) Corrective
D) Compensating

<details><summary>Answer</summary>

**D) Compensating**

A compensating control is an alternative control used when the primary control (e.g., patching the device) is not feasible. Network isolation and enhanced logging compensate for the inability to patch. This is a common scenario with OT (Operational Technology)/ICS (Industrial Control System) and legacy medical devices on Security+ exams.

</details>

---

**Q21.** Which of the following BEST describes the purpose of a Public Key Infrastructure (PKI)?

A) Distributing symmetric encryption keys securely
B) Providing a framework for issuing and managing digital certificates that bind public keys to identities
C) Storing private keys in a centralized hardware security module
D) Enabling users to generate and self-sign certificates without a trusted third party

<details><summary>Answer</summary>

**B) Providing a framework for issuing and managing digital certificates that bind public keys to identities**

PKI (Public Key Infrastructure) is a hierarchy of Certificate Authorities (CAs) that issue digital certificates binding a public key to a specific entity (person, device, or service). This enables trust: any party that trusts the CA can verify the certificate and trust the public key. The CA hierarchy typically includes a root CA and subordinate/intermediate CAs.

</details>

---

**Q22.** A security engineer needs to use asymmetric encryption to allow anyone to send encrypted messages to a server while ensuring only the server can decrypt them. What does the sender use to encrypt the message?

A) The sender's private key
B) The server's private key
C) The server's public key
D) A shared symmetric key

<details><summary>Answer</summary>

**C) The server's public key**

In asymmetric encryption, the sender encrypts with the recipient's public key. Only the recipient's private key can decrypt it. This allows anyone with access to the public key to send encrypted messages that only the private key holder can read. (For digital signatures, the sender uses their own private key to sign, and the recipient uses the sender's public key to verify.)

</details>

---

**Q23.** An attacker intercepts encrypted traffic between a client and a server. The attacker cannot decrypt current traffic but stores it hoping to decrypt it later if the server's private key is ever compromised. Which cryptographic property would protect against this threat?

A) Certificate pinning
B) PFS
C) Key escrow
D) OCSP stapling

<details><summary>Answer</summary>

**B) PFS**

PFS (Perfect Forward Secrecy) (achieved via DHE (Diffie-Hellman Ephemeral) or ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) key exchange) generates unique ephemeral session keys for each session. Even if the server's long-term private key is later compromised, past session traffic cannot be decrypted because the ephemeral keys are never stored. This is specifically designed to defeat "harvest now, decrypt later" attacks.

</details>

---

**Q24.** A security team discovers that a web server is using TLS 1.0 for client connections. What is the MOST significant risk of continuing to use TLS 1.0?

A) TLS 1.0 does not support certificate-based authentication
B) TLS 1.0 includes deprecated cipher suites known to have cryptographic weaknesses
C) TLS 1.0 cannot encrypt traffic above 1 Mbps
D) TLS 1.0 requires a certificate from a public CA

<details><summary>Answer</summary>

**B) TLS 1.0 includes deprecated cipher suites known to have cryptographic weaknesses**

TLS (Transport Layer Security) 1.0 supports weak cipher suites including RC4 and CBC-mode ciphers vulnerable to attacks like BEAST (Browser Exploit Against SSL/TLS) and POODLE (Padding Oracle On Downgraded Legacy Encryption). TLS 1.2 and 1.3 are the current standards. TLS 1.3 removed all legacy cipher suites entirely. PCI-DSS (Payment Card Industry Data Security Standard) explicitly prohibits TLS 1.0 for cardholder data environments.

</details>

---

**Q25.** Which encryption algorithm provides the same security strength as RSA-3072 using a significantly shorter key length, making it preferred for resource-constrained environments?

A) AES-256
B) 3DES
C) ECC with a 256-bit key
D) SHA-256

<details><summary>Answer</summary>

**C) ECC with a 256-bit key**

ECC (Elliptic Curve Cryptography) provides equivalent security to RSA with much shorter keys: a 256-bit ECC key provides roughly the same security as a 3072-bit RSA key. This makes ECC preferred for mobile devices, IoT, and TLS (Transport Layer Security) where computational overhead matters. AES-256 is symmetric; SHA-256 is a hash function.

</details>

---

**Q26.** A company policy requires all employees to use a key card to enter secured areas of the office building. What type of security control is being implemented?

A) Technical control
B) Administrative control
C) Physical control
D) Corrective control

<details><summary>Answer</summary>

**C) Physical control**

Physical controls restrict access to facilities, hardware, and physical spaces. A key card system controls who can enter physical areas of a building. Technical controls use technology (firewalls, encryption); administrative controls are policy-based (training, procedures); corrective controls fix issues after an incident has occurred.

</details>

---

**Q27.** Which of the following types of controls decreases the likelihood of a cybersecurity breach occurring?

A) Corrective
B) Transfer
C) Detective
D) Preventive

<details><summary>Answer</summary>

**D) Preventive**

Preventive controls actively reduce the probability of a breach by stopping threats before they succeed. Detective controls identify breaches after they occur. Corrective controls restore systems after an incident. Transfer shifts risk (e.g., insurance) but does not reduce the likelihood of the breach itself.

</details>

---

**Q28.** A systems administrator would like to set up a system that will make it difficult or impossible to deny that someone has performed an action. Which of the following is the administrator trying to accomplish?

A) Non-repudiation
B) Adaptive identity
C) Security zones
D) Deception and disruption

<details><summary>Answer</summary>

**A) Non-repudiation**

Non-repudiation ensures that individuals cannot deny having performed an action. It is typically implemented through digital signatures, audit logs, and timestamps. Adaptive identity adjusts authentication based on risk; security zones segment networks; deception and disruption involve honeypots and similar techniques.

</details>

---

**Q29.** A system administrator implements a regular data backup schedule to ensure that critical business data can be fully restored in the event of a server hardware failure. This action primarily supports which principle of the CIA triad?

A) Confidentiality
B) Integrity
C) Availability
D) Non-repudiation

<details><summary>Answer</summary>

**C) Availability**

Availability ensures that information and systems are accessible to authorized users when needed. Backups allow restoration of data after a failure, directly supporting availability. Confidentiality prevents unauthorized disclosure; integrity prevents unauthorized modification; non-repudiation is not part of the CIA triad.

</details>

---

**Q30.** A network administrator needs to replace Telnet for remotely managing network routers because of its security vulnerabilities. Which of the following protocols would be the most secure replacement?

A) HTTPS
B) SNMP
C) SSH
D) DNSSEC

<details><summary>Answer</summary>

**C) SSH**

Secure Shell (SSH) is the direct encrypted replacement for Telnet, providing encrypted remote command-line access. Telnet transmits credentials in cleartext, making it vulnerable to interception. HTTPS secures web traffic; SNMP manages network devices but is not a remote shell protocol; DNSSEC secures DNS lookups.

</details>

---

**Q31.** Which of the following provides the details about the terms of a test with a third-party penetration tester?

A) Rules of engagement
B) Supply chain analysis
C) Right to audit clause
D) Due diligence

<details><summary>Answer</summary>

**A) Rules of engagement**

Rules of engagement document the scope, limitations, timing, and agreed-upon parameters when conducting third-party security testing. They define what is permitted and what is out of scope. A right to audit clause grants permission to audit a vendor; due diligence is the broader process of investigating before a decision; supply chain analysis evaluates vendor security.

</details>

---

**Q32.** Which of the following is used to add extra complexity before using a one-way data transformation algorithm?

A) Key stretching
B) Data masking
C) Steganography
D) Salting

<details><summary>Answer</summary>

**D) Salting**

Salting adds a random value to a password or input before it is hashed, ensuring that two identical passwords produce different hash outputs. This defeats rainbow table and precomputed hash attacks. Key stretching increases computational cost of hashing (e.g., PBKDF2, bcrypt); data masking obscures data in non-production environments; steganography hides data within other data.

</details>

---

**Q33.** What is the purpose of hashing a patch file before releasing it?

A) Assist in compressing the file
B) Provide a method for customers to verify integrity
C) Encrypt the file for secure transmission
D) Create a unique identifier for record keeping

<details><summary>Answer</summary>

**B) Provide a method for customers to verify integrity**

Hashing creates a fixed-length digest of a file's contents. When the vendor publishes a hash alongside the patch, customers can hash the downloaded file themselves and compare — if the hashes match, the file has not been tampered with or corrupted. Hashing does not compress or encrypt files.

</details>

---

**Q34.** What are the two primary security methods provided by cryptography for email?

A) Firewall and IPS
B) Authentication and Authorization
C) Digital Signatures and Encryption
D) VPN and Proxy servers

<details><summary>Answer</summary>

**C) Digital Signatures and Encryption**

Cryptography provides two core email security benefits: encryption ensures confidentiality (only the intended recipient can read the message), and digital signatures provide authentication, integrity, and non-repudiation (the recipient can verify who sent the message and that it was not altered).

</details>

---

**Q35.** Which key is used to encrypt an email digital signature?

A) Sender's public key
B) Recipient's public key
C) Sender's private key
D) Recipient's private key

<details><summary>Answer</summary>

**C) Sender's private key**

A digital signature is created by hashing the message and then encrypting that hash with the sender's private key. The recipient decrypts the hash using the sender's public key to verify the signature. This proves that only the holder of the private key could have created the signature, providing authentication and non-repudiation.

</details>

---

**Q36.** What are the two primary encryption methods?

A) Symmetric and Asymmetric
B) Algorithmic and Key-based
C) Plaintext and Ciphertext
D) Cleartext and Encoded

<details><summary>Answer</summary>

**A) Symmetric and Asymmetric**

Symmetric encryption uses the same key for both encryption and decryption (fast, efficient, good for bulk data). Asymmetric encryption uses a mathematically related key pair — a public key and a private key — and is used for key exchange and digital signatures. HTTPS combines both: asymmetric to exchange a session key, then symmetric for the data transfer.

</details>

---

**Q37.** How do email applications use asymmetric and symmetric encryption together?

A) Symmetric to share session key; asymmetric to encrypt data
B) Asymmetric to share session key; symmetric to encrypt data
C) Exclusively symmetric encryption
D) Exclusively asymmetric encryption

<details><summary>Answer</summary>

**B) Asymmetric to share session key; symmetric to encrypt data**

Asymmetric encryption is used in a hybrid scheme: the sender uses the recipient's public key to securely exchange a symmetric session key. The bulk of the message is then encrypted using the faster symmetric session key. This combines the security of asymmetric key exchange with the performance of symmetric encryption.

</details>

---

**Q38.** What is a Certificate Revocation List (CRL)?

A) A list of serial numbers for unissued certificates
B) A list of revoked certificates sorted by issue dates
C) A version 2 certificate listing revoked certs by serial numbers
D) A list of expired certificates sorted by serial numbers

<details><summary>Answer</summary>

**C) A version 2 certificate listing revoked certs by serial numbers**

A CRL is published by a Certificate Authority and lists the serial numbers of certificates that have been revoked before their expiration date (e.g., due to compromise or key exposure). It is an X.509 v2 structure. The Online Certificate Status Protocol (OCSP) is the more modern, real-time alternative to CRL polling.

</details>

---

**Q39.** What is the main characteristic of symmetric encryption?

A) Uses two keys as a matched pair
B) Hides data within other files
C) Validates identity using certificates
D) Uses the same key to encrypt and decrypt data

<details><summary>Answer</summary>

**D) Uses the same key to encrypt and decrypt data**

Symmetric encryption uses a single shared key for both encryption and decryption. The major challenge is key distribution — securely sharing the key with the other party. Common symmetric algorithms include AES, DES, 3DES, Blowfish, and RC4.

</details>

---

**Q40.** What does "data in processing" (data in use) refer to?

A) Encrypted data waiting for decryption on a server
B) Encrypted data sent over a network
C) Data being actively used by a computer that is not encrypted
D) Encrypted data stored on storage media

<details><summary>Answer</summary>

**C) Data being actively used by a computer that is not encrypted**

Data in use refers to data currently being processed in RAM or CPU registers. It is typically unencrypted during this phase, making it a high-value target for memory scraping attacks. Data in transit is encrypted on the network (e.g., TLS); data at rest is stored on disk (e.g., encrypted volumes).

</details>

---

**Q41.** What is the main advantage of Elliptic Curve Cryptography (ECC)?

A) It uses larger keys for better security
B) It is mainly used for signing emails only
C) It provides less security for low-power devices
D) It takes less processing power than other methods

<details><summary>Answer</summary>

**D) It takes less processing power than other methods**

ECC achieves equivalent security to RSA with significantly smaller key sizes. For example, a 256-bit ECC key provides roughly the same security as a 3072-bit RSA key. This makes ECC ideal for resource-constrained environments such as mobile devices, IoT sensors, and smart cards where CPU cycles and battery life are limited.

</details>

---

**Q42.** What is the important characteristic of ephemeral keys?

A) They use a deterministic algorithm
B) They have the same lifetime as a certificate
C) They are only valid for a single session and are then discarded
D) They are validated by a certificate authority

<details><summary>Answer</summary>

**C) They are only valid for a single session and are then discarded**

Ephemeral keys are temporary keys generated fresh for each session. Once the session ends, the key is destroyed and never reused. This property provides Perfect Forward Secrecy (PFS): even if a long-term private key is compromised in the future, past sessions cannot be decrypted because the ephemeral session keys no longer exist.

</details>

---

**Q43.** What is the benefit of Perfect Forward Secrecy?

A) It increases certificate validation speed
B) It allows a deterministic algorithm for public key generation
C) It ensures a compromised long-term key does not affect past session security
D) It extends the lifetime of a certificate

<details><summary>Answer</summary>

**C) It ensures a compromised long-term key does not affect past session security**

Perfect Forward Secrecy (PFS) is achieved by using ephemeral key exchange algorithms (e.g., ECDHE or DHE). Because unique session keys are generated for each connection and immediately discarded, a future compromise of the server's private key cannot be used to decrypt previously captured traffic.

</details>

---

**Q44.** What security benefits are provided when a digital signature is successfully decrypted?

A) Confidentiality, Integrity, and Availability
B) Non-repudiation, Availability, and Authentication
C) Integrity, Confidentiality, and Authentication
D) Authentication, Non-repudiation, and Integrity

<details><summary>Answer</summary>

**D) Authentication, Non-repudiation, and Integrity**

When a recipient decrypts a digital signature using the sender's public key and the result matches the message hash, three things are confirmed: Authentication (the message came from the holder of that private key), Non-repudiation (the sender cannot deny sending it), and Integrity (the message was not altered in transit). Digital signatures do not provide confidentiality — the message body must be separately encrypted for that.

</details>

---

**Q45.** What does a hash function in cryptography ensure?

A) Confidentiality of data
B) Non-repudiation of an action
C) Integrity of data
D) Authentication of identity

<details><summary>Answer</summary>

**C) Integrity of data**

Hash functions produce a fixed-length digest from input data. Any change to the input, no matter how small, produces a completely different hash output. This property makes hashes useful for verifying that data has not been altered. Common hashing algorithms include MD5 (128-bit, deprecated for security), SHA-1 (deprecated), SHA-256, and SHA-3.

</details>

---

**Q46.** What is the primary purpose of steganography?

A) Encrypt data so it cannot be read
B) Create symmetric or asymmetric keys
C) Hide data inside other data
D) Create different hash values

<details><summary>Answer</summary>

**C) Hide data inside other data**

Steganography is the practice of concealing a message within another non-secret message or medium so that the existence of the hidden message is not apparent to observers. Common methods include hiding data in the least significant bits of image, audio, or video files. Unlike encryption, steganography does not scramble the message — it hides the fact that a message exists at all.

</details>

---

**Q47.** A data administrator is configuring authentication for a SaaS application and would like to reduce the number of credentials employees need to maintain. Which of the following should the administrator implement?

A) SSO
B) LEAP
C) MFA
D) PEAP

<details><summary>Answer</summary>

**A) SSO**

Single Sign-On (SSO) allows users to authenticate once and then access multiple applications without re-entering credentials. This reduces credential fatigue and the number of passwords users must remember. MFA adds additional authentication factors but does not reduce the number of credential sets. LEAP and PEAP are wireless authentication protocols.

</details>

---
