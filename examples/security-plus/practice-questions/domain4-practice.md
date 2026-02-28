**Q1.** In digital forensics, which of the following represents the correct order of volatility from most to least volatile?

A) Disk → RAM → CPU registers → Remote logs
B) CPU registers → RAM → Disk → Remote logs
C) Remote logs → Disk → RAM → CPU registers
D) RAM → CPU registers → Disk → Remote logs

<details><summary>Answer</summary>

**B) CPU registers → RAM → Disk → Remote logs**

The order of volatility (most to least volatile) is CPU registers/cache → RAM → swap/page file → disk → remote logs → backups. This order ensures that the most volatile data (which can be lost in fractions of a second) is collected first before it disappears. Remote logs and backups are the least volatile because they persist over time.

</details>

---

**Q2.** Which phase of the NIST incident response lifecycle involves identifying that a security breach has occurred?

A) Preparation
B) Detection and Analysis
C) Containment, Eradication, and Recovery
D) Post-Incident Activity

<details><summary>Answer</summary>

**B) Detection and Analysis**

The Detection and Analysis phase is when the incident is discovered and initial analysis occurs to determine what happened and the scope of the incident. Preparation comes first to ensure tools are in place, Containment/Eradication/Recovery involves the active response, and Post-Incident Activity covers lessons learned.

</details>

---

**Q3.** What is the primary purpose of maintaining a chain of custody in a digital forensics investigation?

A) To prove the guilt of the suspect
B) To ensure evidence is admissible in court and integrity is maintained throughout its lifecycle
C) To prevent the suspect from accessing their data
D) To speed up the investigation process

<details><summary>Answer</summary>

**B) To ensure evidence is admissible in court and integrity is maintained throughout its lifecycle**

Chain of custody documents every detail about evidence across its lifecycle: who collected it, when, where, who examined it, who transported it, and when custody changed hands. This documentation is essential for legal admissibility and demonstrating that evidence was not tampered with or corrupted during the investigation.

</details>

---

**Q4.** A SIEM differs from a SOAR platform primarily in that a SOAR platform adds which of the following capabilities?

A) Log collection and centralization
B) Automation, orchestration, and automated response to incidents
C) Event correlation and anomaly detection
D) Real-time threat alerts

<details><summary>Answer</summary>

**B) Automation, orchestration, and automated response to incidents**

SIEM (Security Information and Event Management) collects, centralizes, and analyzes logs. SOAR (Security Orchestration, Automation, and Response) builds on SIEM by automating predefined response playbooks and orchestrating actions across multiple security tools, enabling faster incident response without manual intervention.

</details>

---

**Q5.** Which endpoint security technology monitors endpoint behavior and detects suspicious activities in real-time?

A) Antivirus
B) Endpoint Detection and Response (EDR)
C) Web filter
D) Network firewall

<details><summary>Answer</summary>

**B) Endpoint Detection and Response (EDR)**

EDR uses behavioral analysis, machine learning, and real-time monitoring to detect suspicious activity even if the threat is previously unknown. Traditional antivirus relies on signature-based detection for known malware, making EDR more advanced. Web filters and firewalls operate at different layers than endpoint monitoring.

</details>

---

**Q6.** XDR technology differs from EDR by extending threat detection and response capabilities to which additional layers?

A) Only network segments
B) Multiple security layers including endpoints, networks, servers, email, and cloud environments
C) Only cloud environments
D) Only email and web gateways

<details><summary>Answer</summary>

**B) Multiple security layers including endpoints, networks, servers, email, and cloud environments**

EDR focuses specifically on endpoint data and threats, while XDR (Extended Detection and Response) expands detection and response across multiple layers—endpoints, networks, servers, email, cloud, and other security domains. This provides more comprehensive threat visibility and correlation.

</details>

---

**Q7.** Which principle requires that users be granted only the minimum access necessary to perform their job function?

A) Need to know
B) Separation of duties
C) Least privilege
D) Job rotation

<details><summary>Answer</summary>

**C) Least privilege**

The principle of least privilege states that users should receive the minimum access needed to perform their job function. Need-to-know restricts data access even with system access; separation of duties divides responsibilities; and job rotation moves users between roles to detect fraud.

</details>

---

**Q8.** What is the primary purpose of multi-factor authentication (MFA)?

A) To encrypt user passwords
B) To require multiple forms of identification to verify a user's identity
C) To prevent social engineering attacks
D) To monitor user behavior

<details><summary>Answer</summary>

**B) To require multiple forms of identification to verify a user's identity**

MFA adds an extra layer of security by requiring users to verify their identity through multiple methods, such as a password, biometric scan, one-time code, or hardware token. This makes it much harder for attackers to gain access even if they compromise a password.

</details>

---

**Q9.** Which identity and access management component is responsible for managing access to privileged accounts?

A) Directory services
B) Single Sign-On (SSO)
C) Privileged Access Management (PAM)
D) Multi-factor authentication (MFA)

<details><summary>Answer</summary>

**C) Privileged Access Management (PAM)**

PAM focuses on managing access for privileged users and sensitive accounts, with stronger controls than general IAM. Directory services manage user identities, SSO provides unified authentication, and MFA adds authentication factors, but only PAM specifically addresses privileged account access.

</details>

---

**Q10.** In account management, what is the process of removing user access when an employee leaves the organization called?

A) Provisioning
B) Deprovisioning
C) Recertification
D) Access review

<details><summary>Answer</summary>

**B) Deprovisioning**

Deprovisioning is the process of removing user access, accounts, and resources when employees leave, are terminated, or change roles. Provisioning is the opposite (granting access), recertification involves periodic review of existing access, and access review is a periodic audit process.

</details>

---

**Q11.** Which mobile device management deployment model involves devices purchased by the company but allowing personal use?

A) BYOD (Bring Your Own Device)
B) COPE (Corporate Owned, Personally Enabled)
C) COBO (Corporate Owned, Business Only)
D) MAM (Mobile Application Management)

<details><summary>Answer</summary>

**B) COPE (Corporate Owned, Personally Enabled)**

COPE means the device is company-owned but employees may use it for personal activities like email and social media. BYOD is employee-owned, COBO is company-owned for business only, and MAM is a management approach (not a deployment model).

</details>

---

**Q12.** What is the primary security concern with BYOD (Bring Your Own Device) implementations?

A) Devices are too expensive to manage
B) Company cannot enforce full security controls on personal devices
C) Mobile devices are not supported by any management tools
D) BYOD eliminates the need for endpoint protection

<details><summary>Answer</summary>

**B) Company cannot enforce full security controls on personal devices**

BYOD poses security challenges because the company doesn't own the device and cannot enforce as many security controls as with corporate devices. The company must use MAM to secure applications without intruding on personal content, but full device control is limited compared to COPE or COBO models.

</details>

---

**Q13.** Mobile device management (MDM) can enforce all of the following EXCEPT:

A) Device encryption
B) Strong PIN codes
C) Remote wipe capability
D) Personal application installation restrictions

<details><summary>Answer</summary>

**D) Personal application installation restrictions**

MDM can enforce device encryption, PIN codes, screen locks, and remote wipe. However, on BYOD devices, MDM cannot easily restrict personal application installation without significant privacy concerns. MAM (Mobile Application Management) is used instead to manage specific corporate applications on personal devices.

</details>

---

**Q14.** Which Common Vulnerability Scoring System (CVSS) metric scale ranges from 0 to 10?

A) 0.0 to 5.0
B) 1 to 10
C) 0.0 to 10.0
D) 1 to 100

<details><summary>Answer</summary>

**C) 0.0 to 10.0**

CVSS scores range from 0.0 to 10.0, with higher scores indicating greater severity. A score of 0 means no vulnerability, and 10 is the maximum severity. The scores can be translated to qualitative ratings: low, medium, high, and critical.

</details>

---

**Q15.** In vulnerability management, what is the primary limitation of using CVSS scores alone for prioritization?

A) CVSS scores are not standardized
B) CVSS measures severity but not the likelihood of real-world exploitation
C) CVSS cannot rate vulnerabilities above 8.0
D) CVSS requires CVSS requires access to the vendor's code

<details><summary>Answer</summary>

**B) CVSS measures severity but not the likelihood of real-world exploitation**

CVSS provides a severity rating but does not account for whether a vulnerability is actually being exploited in the wild. Organizations should integrate CVSS with predictive models like EPSS (Exploit Prediction Scoring System) to better prioritize remediation based on real-world threat likelihood.

</details>

---

**Q16.** Which data sanitization method uses an electromagnetic field to destroy data on magnetic media?

A) Shredding
B) Degaussing
C) Purging
D) Overwriting

<details><summary>Answer</summary>

**B) Degaussing**

Degaussing uses a powerful electromagnetic field to erase data stored on magnetic media like hard drives and magnetic tape. Shredding physically destroys media, overwriting (DoD 5220.22-M) writes data multiple times to HDDs, and purging is a general term for data destruction.

</details>

---

**Q17.** What does the "3" in the 3-2-1 backup rule represent?

A) Three backup types (full, differential, incremental)
B) Three identical copies of data
C) Three copies on the same type of media
D) Three days for backup retention

<details><summary>Answer</summary>

**B) Three identical copies of data**

The 3-2-1 backup rule means: 3 copies of data, 2 on different media types, 1 stored offsite. This ensures protection against data loss from hardware failure, media corruption, or local disasters like fire or flooding.

</details>

---

**Q18.** RTO (Recovery Time Objective) measures which of the following?

A) Maximum time a system can be down before recovery is required
B) Maximum data loss the business can tolerate
C) Time between backup cycles
D) Duration of the recovery process

<details><summary>Answer</summary>

**A) Maximum time a system can be down before recovery is required**

RTO is the maximum acceptable downtime—how fast you must recover. RPO is the maximum data loss acceptable—how much time can pass between backups. These are different concepts; RTO measures time-to-restore while RPO measures acceptable data loss.

</details>

---

**Q19.** Which backup type captures only the changes made since the last full backup, regardless of previous incremental or differential backups?

A) Full backup
B) Incremental backup
C) Differential backup
D) Mirror backup

<details><summary>Answer</summary>

**C) Differential backup**

A differential backup captures all changes since the last full backup (not since the last incremental). An incremental backup captures changes since the last backup of any type (full, differential, or incremental). Differential requires fewer backups to restore (full + latest differential) but uses more storage space.

</details>

---

**Q20.** Which of the following best describes the purpose of system hardening?

A) To increase system performance and speed
B) To reduce potential security vulnerabilities by disabling unnecessary services and features
C) To add more users to the system
D) To increase network bandwidth

<details><summary>Answer</summary>

**B) To reduce potential security vulnerabilities by disabling unnecessary services and features**

Hardening is the process of securing systems against unauthorized access and cyberattacks by removing or disabling unnecessary services, features, and default configurations. It limits the attack surface and potential weaknesses that could be exploited.

</details>

---

**Q21.** What is the primary purpose of a CIS Benchmark?

A) To test network speed and performance
B) To provide standardized security configuration baselines for systems
C) To measure employee productivity
D) To manage user passwords

<details><summary>Answer</summary>

**B) To provide standardized security configuration baselines for systems**

CIS Benchmarks are internationally recognized security standards that provide prescriptive configuration recommendations for securely configuring systems. They are created by industry consensus and cover operating systems, databases, servers, and other technologies across different levels of security hardness.

</details>

---

**Q22.** A honeynet differs from a honeypot in that a honeynet:

A) Only monitors incoming traffic
B) Uses decoy systems that mimic a real network with multiple systems, databases, and servers
C) Can only detect one type of attack
D) Automatically blocks all attacks

<details><summary>Answer</summary>

**B) Uses decoy systems that mimic a real network with multiple systems, databases, and servers**

A honeypot is a single decoy system, while a honeynet is a network of honeypots designed to look like a real network. Honeynets engage attackers longer because they mimic complex networks, allowing security teams to observe attacker behavior across multiple systems and gather more threat intelligence.

</details>

---

**Q23.** Which deception technology creates fake sensitive files designed to alert security teams when accessed?

A) Honeypot
B) Honeynet
C) Honeyfile
D) DNS sinkhole

<details><summary>Answer</summary>

**C) Honeyfile**

Honeyfiles are fake documents with realistic names (like passwords.txt or credit_cards.xlsx) placed in accessible locations. If accessed or exfiltrated, they trigger an alert, helping detect lateral movement and data theft attempts. Honeypots and honeynets are decoy systems, while DNS sinkholes redirect malicious domain traffic.

</details>

---

**Q24.** In the context of incident response, what does the "Containment" phase primarily involve?

A) Collecting evidence and investigating the breach
B) Isolating affected systems to prevent further spread of the incident
C) Removing the attacker and fixing vulnerabilities
D) Conducting a post-mortem review

<details><summary>Answer</summary>

**B) Isolating affected systems to prevent further spread of the incident**

Containment stops the spread of the incident by isolating compromised systems. Eradication removes the threat and fixes vulnerabilities, Recovery restores systems, Detection/Analysis identifies the breach, and Post-Incident Activity covers lessons learned.

</details>

---

**Q25.** Which NIST incident response phase involves reviewing the incident to identify lessons learned and improve future response efforts?

A) Preparation
B) Detection and Analysis
C) Containment, Eradication, and Recovery
D) Post-Incident Activity

<details><summary>Answer</summary>

**D) Post-Incident Activity**

Post-Incident Activity is the final phase where the organization reviews what happened, identifies lessons learned, and implements improvements to prevent similar incidents. This includes updating procedures, tools, and training based on the incident experience.

</details>

---

**Q26.** Which access control model assigns permissions based on job title or role rather than individual users?

A) Discretionary Access Control (DAC)
B) Role-Based Access Control (RBAC)
C) Attribute-Based Access Control (ABAC)
D) Mandatory Access Control (MAC)

<details><summary>Answer</summary>

**B) Role-Based Access Control (RBAC)**

RBAC assigns permissions based on roles (job titles), reducing administrative overhead. DAC relies on data owner decisions, ABAC uses attributes (time, location, device), and MAC is enforced by the system using security labels. RBAC is the most scalable for large organizations.

</details>

---

**Q27.** What is the purpose of separation of duties in access control?

A) To speed up user onboarding
B) To prevent any single individual from having complete control over a critical function
C) To reduce the number of administrators
D) To simplify password management

<details><summary>Answer</summary>

**B) To prevent any single individual from having complete control over a critical function**

Separation of duties divides responsibilities so that no single person can execute a complete sensitive transaction, reducing fraud and errors. For example, one person approves payments while another executes them. This principle enhances security and enforces accountability.

</details>

---

**Q28.** Which job rotation practice is designed to detect fraud or unauthorized activities?

A) Rotating users between different departments weekly
B) Moving users between different roles or positions, typically on a scheduled basis
C) Having users swap security credentials daily
D) Requiring users to change passwords monthly

<details><summary>Answer</summary>

**B) Moving users between different roles or positions, typically on a scheduled basis**

Job rotation moves employees between roles periodically, which can expose unauthorized activities or patterns. When a new person takes a role, they may notice irregularities that the previous occupant hid. This is a detective control that complements preventive controls like separation of duties.

</details>

---

**Q29.** What is account recertification in the context of access control?

A) The process of creating new user accounts
B) A periodic review and verification that user access rights are still appropriate
C) A method to encrypt user credentials
D) The process of changing user passwords

<details><summary>Answer</summary>

**B) A periodic review and verification that user access rights are still appropriate**

Recertification (also called access review) is a periodic audit where managers verify that employees still need their current access rights and that access aligns with job responsibilities. This ensures creep is controlled and unnecessary access is removed, supporting the principle of least privilege.

</details>

---

**Q30.** Which feature of a host-based firewall allows only explicitly approved applications to execute?

A) Port blocking
B) Application whitelisting
C) Network filtering
D) Packet inspection

<details><summary>Answer</summary>

**B) Application whitelisting**

Application whitelisting explicitly allows only approved applications to run, blocking everything else by default. This is more restrictive than a firewall that allows traffic on specific ports. Whitelisting prevents unauthorized software like malware from executing unless explicitly approved.

</details>

---

**Q31.** What is the primary purpose of host intrusion prevention system (HIPS)?

A) To monitor network traffic only
B) To detect and block malicious activities at the host level in real-time
C) To encrypt all host data
D) To back up system files automatically

<details><summary>Answer</summary>

**B) To detect and block malicious activities at the host level in real-time**

HIPS operates on individual hosts to detect and prevent intrusions and malicious behaviors in real-time. It is different from HIDS (which only detects and alerts) because HIPS actively blocks threats. Both operate at the host level, unlike network-based systems.

</details>

---

**Q32.** In endpoint protection, what does sandboxing accomplish?

A) Improves network speed
B) Isolates suspicious applications in a restricted environment to prevent them from affecting the system
C) Encrypts all endpoint data
D) Manages user account permissions

<details><summary>Answer</summary>

**B) Isolates suspicious applications in a restricted environment to prevent them from affecting the system**

Sandboxing runs potentially malicious or unknown applications in an isolated, restricted environment where they cannot access critical system resources or real data. This allows security teams to observe the application's behavior without risk. If the application is malicious, it cannot harm the actual system.

</details>

---

**Q33.** Which monitoring tool collects logs from multiple sources across a network for centralized analysis?

A) NetFlow
B) Packet capture
C) SIEM
D) Protocol analyzer

<details><summary>Answer</summary>

**C) SIEM**

SIEM (Security Information and Event Management) collects, centralizes, and analyzes logs from multiple network sources. NetFlow captures network flow data, packet capture captures packet contents, and protocol analyzers inspect protocols—but only SIEM provides centralized log collection and correlation from diverse sources.

</details>

---

**Q34.** What does NetFlow data provide visibility into?

A) File contents and detailed packet payloads
B) Network traffic patterns and communication flows between systems
C) Operating system log entries
D) Application performance metrics only

<details><summary>Answer</summary>

**B) Network traffic patterns and communication flows between systems**

NetFlow provides information about who is communicating with whom, how much data is being transferred, and traffic patterns—without capturing the actual packet content. This helps detect unusual network behavior and data exfiltration attempts while being less resource-intensive than full packet capture.

</details>

---

**Q35.** What is the primary purpose of syslog in a monitoring and logging strategy?

A) To encrypt all network traffic
B) To centralize the collection of log messages from various devices on a network
C) To prevent unauthorized access
D) To detect viruses automatically

<details><summary>Answer</summary>

**B) To centralize the collection of log messages from various devices on a network**

Syslog is a protocol and service that collects and forwards log messages from multiple devices (servers, routers, firewalls, printers) to a central logging server. This enables centralized log management, analysis, and retention from diverse network sources.

</details>

---

**Q36.** Which of the following is a function of Data Loss Prevention (DLP) systems?

A) Encrypting all user data automatically
B) Detecting and blocking the unauthorized transmission of sensitive data
C) Preventing all network traffic
D) Replacing user authentication

<details><summary>Answer</summary>

**B) Detecting and blocking the unauthorized transmission of sensitive data**

DLP systems identify and prevent sensitive data (credit cards, SSNs, confidential documents) from being transmitted outside the organization through email, cloud services, or other channels. They can alert, block, or quarantine data based on configured policies.

</details>

---

**Q37.** In data classification, what is the primary purpose of assigning sensitivity labels?

A) To improve system performance
B) To provide visibility into the sensitivity level of data and enforce appropriate protection measures
C) To encrypt all data
D) To prevent all data access

<details><summary>Answer</summary>

**B) To provide visibility into the sensitivity level of data and enforce appropriate protection measures**

Data classification with sensitivity labels (public, internal, confidential, restricted) helps organizations understand what data they have, who should access it, and what protection measures are required. This supports data governance, compliance, and appropriate resource allocation for protection.

</details>

---

**Q38.** What does a data retention policy primarily specify?

A) How many copies of data to keep
B) How long data must be retained before destruction
C) Which users can access data
D) How to encrypt data

<details><summary>Answer</summary>

**B) How long data must be retained before destruction**

Retention policies define legal and business requirements for keeping data, including how long to retain records, when to delete them, and special holds for litigation. This supports compliance, reduces storage costs, and manages risk from keeping unnecessary sensitive data.

</details>

---

**Q39.** Which data destruction method is most appropriate for solid-state drives (SSDs)?

A) Degaussing
B) Shredding
C) Overwriting with a validated data sanitization tool
D) Burning

<details><summary>Answer</summary>

**C) Overwriting with a validated data sanitization tool**

Degaussing doesn't work well on SSDs because they use flash memory, not magnetic storage. Physical shredding is ideal but expensive. Overwriting with validated tools specifically designed for SSDs (using TRIM/ATA Secure Erase commands) ensures secure deletion. Burning is not a controlled professional method.

</details>

---

**Q40.** In physical security, what is the primary purpose of a mantrap (also called a manTrap or access control vestibule)?

A) To prevent unauthorized access by forcing individuals into a monitored enclosed space between two doors
B) To lock employees in during a security incident
C) To block all entry to a facility
D) To monitor badge access

<details><summary>Answer</summary>

**A) To prevent unauthorized access by forcing individuals into a monitored enclosed space between two doors**

A mantrap is a small enclosed space with two interlocking doors where only one door can be open at a time. This prevents tailgating (following someone through a door) and allows security personnel to verify credentials before granting access. Only one person at a time can pass through.

</details>

---

**Q41.** What is the primary security benefit of using biometric access control?

A) It is cheaper than badge systems
B) It cannot be shared, forged, or forgotten, providing strong authentication based on individual physical characteristics
C) It never fails or produces errors
D) It eliminates the need for other security controls

<details><summary>Answer</summary>

**B) It cannot be shared, forged, or forgotten, providing strong authentication based on individual physical characteristics**

Biometric controls (fingerprint, iris, facial recognition) are tied to individuals and cannot be stolen, shared, or forgotten like badges or passwords. However, they can have false acceptance/rejection rates and aren't 100% accurate, so they're often combined with other controls.

</details>

---

**Q42.** Which of the following is a primary function of a CMDB (Configuration Management Database)?

A) Storing user passwords
B) Tracking and maintaining information about hardware, software, and configurations
C) Monitoring network traffic
D) Storing backup files

<details><summary>Answer</summary>

**B) Tracking and maintaining information about hardware, software, and configurations**

A CMDB maintains a centralized repository of IT assets, their configurations, relationships, and status. This supports change management by providing visibility into what exists, configuration baselines for comparison, and dependencies between systems.

</details>

---

**Q43.** What is the purpose of a configuration baseline in change management?

A) To encrypt system configurations
B) To provide a known-good reference point for system configuration to detect unauthorized changes
C) To prevent all changes to systems
D) To improve network bandwidth

<details><summary>Answer</summary>

**B) To provide a known-good reference point for system configuration to detect unauthorized changes**

A baseline documents the approved, secure configuration of a system at a point in time. Any deviations from the baseline can be detected and investigated. Baselines support compliance verification, forensics, and incident response by showing what was changed and when.

</details>

---

**Q44.** Which incident response action is performed during the "Eradication" phase?

A) Detecting the security breach
B) Isolating affected systems
C) Removing the threat and fixing underlying vulnerabilities
D) Reviewing lessons learned

<details><summary>Answer</summary>

**C) Removing the threat and fixing underlying vulnerabilities**

Eradication involves removing malware, closing compromised accounts, patching vulnerable software, and fixing configurations that allowed the compromise. This ensures the attacker cannot easily regain access. Containment prevents spread, recovery restores systems, and post-incident reviews lessons.

</details>

---

**Q45.** What does the "Recovery" phase of NIST IR involve?

A) Deleting all evidence of the incident
B) Restoring systems and data to normal operations
C) Identifying the attacker
D) Preventing future incidents

<details><summary>Answer</summary>

**B) Restoring systems and data to normal operations**

The Recovery phase restores affected systems, data, and services to normal operations after the threat has been eradicated. This is done carefully to ensure the system is clean and protected. While preventing future incidents (hardening, patching, policy updates) is part of post-incident activity, recovery focuses on restoration.

</details>

---

**Q46.** In digital forensics, what is a write blocker used for?

A) To block network traffic
B) To prevent accidental modification of evidence during acquisition
C) To encrypt evidence files
D) To delete evidence

<details><summary>Answer</summary>

**B) To prevent accidental modification of evidence during acquisition**

A write blocker is a hardware device or software tool that prevents any writes to a storage device during forensic examination. This maintains the chain of custody and evidence integrity by ensuring that the original media is not modified during the forensic process. This is critical for admissibility in court.

</details>

---

**Q47.** What is the purpose of a legal hold in digital forensics?

A) To approve forensic investigations
B) To preserve evidence relevant to litigation or investigations
C) To prevent all data access
D) To encrypt evidence

<details><summary>Answer</summary>

**B) To preserve evidence relevant to litigation or investigations**

A legal hold (litigation hold) is a notice requiring preservation of specific data and systems relevant to litigation, investigations, or regulatory matters. It prevents automatic deletion of logs, emails, and data that must be retained as evidence, supporting legal discovery requirements.

</details>

---

**Q48.** Which of the following best describes the purpose of threat hunting?

A) To wait for security alerts to respond to incidents
B) To proactively search networks for indicators of compromise and threat activities
C) To prevent all network access
D) To monitor only incoming traffic

<details><summary>Answer</summary>

**B) To proactively search networks for indicators of compromise and threat activities**

Threat hunting is a proactive, continuous process where security teams search for indicators of compromise, malicious activities, and threats that may have evaded automated detection. This differs from reactive incident response and helps find advanced threats before they cause major damage.

</details>

---

**Q49.** In vulnerability scanning, what is the purpose of a credentialed scan?

A) To bypass authentication to test security
B) To scan with user credentials to assess both external and internal vulnerabilities more comprehensively
C) To only scan external vulnerabilities
D) To prevent legitimate users from accessing systems

<details><summary>Answer</summary>

**B) To scan with user credentials to assess both external and internal vulnerabilities more comprehensively**

Credentialed scans use valid user credentials to authenticate and assess internal vulnerabilities, configuration issues, and missing patches that non-authenticated scanners cannot see. This provides deeper visibility into system security than unauthenticated scans, which only test external-facing vulnerabilities.

</details>

---

**Q50.** What is patch management primarily focused on?

A) Creating patches for vulnerabilities
B) Assessing, testing, and deploying security updates and fixes to systems
C) Preventing all software updates
D) Encrypting patches

<details><summary>Answer</summary>

**B) Assessing, testing, and deploying security updates and fixes to systems**

Patch management is the process of identifying, testing, prioritizing, and deploying patches and updates to fix vulnerabilities and bugs. This is critical to reducing the attack surface and keeping systems secure. The process must balance timely patching with testing to avoid breaking systems.

</details>

---

**Q51.** Which of the following is a characteristic of Host-based Intrusion Detection System (HIDS)?

A) It monitors network traffic only
B) It monitors and detects malicious activities on individual host systems
C) It automatically blocks all threats
D) It requires no configuration

<details><summary>Answer</summary>

**B) It monitors and detects malicious activities on individual host systems**

HIDS operates on individual hosts, monitoring system and application activity, file access, process execution, and log entries to detect suspicious behavior. It generates alerts when detected, but does not automatically block (that's HIPS). It complements network-based IDS.

</details>

---

**Q52.** In the context of incident response, what does triage involve?

A) Deleting incident evidence
B) Prioritizing incidents based on severity and business impact
C) Reporting incidents to law enforcement
D) Destroying compromised systems

<details><summary>Answer</summary>

**B) Prioritizing incidents based on severity and business impact**

Triage is the process of assessing and prioritizing incidents based on severity, affected systems, business impact, and required response time. Critical incidents affecting core systems receive higher priority than lower-impact incidents. This ensures resources are allocated to the most important incidents first.

</details>

---

**Q53.** What is the primary purpose of role-based access control (RBAC) recertification?

A) To change user passwords
B) To verify that assigned roles and permissions remain appropriate for job functions
C) To delete inactive users
D) To encrypt access logs

<details><summary>Answer</summary>

**B) To verify that assigned roles and permissions remain appropriate for job functions**

RBAC recertification is a periodic review where managers verify that users still need their assigned roles and that role permissions align with current responsibilities. This prevents access creep where users accumulate unnecessary permissions over time.

</details>

---

**Q54.** Which access control concept requires that users need authorization not just to access systems, but specifically to access the data within them?

A) Least privilege
B) Need-to-know
C) Separation of duties
D) Due diligence

<details><summary>Answer</summary>

**B) Need-to-know**

Need-to-know is the principle that even if a user has access to a system, they should only be able to view or use the specific data required for their job. This is more restrictive than just system access and ensures data is accessible only to those who truly require it.

</details>

---

**Q55.** What is the primary difference between LDAP and Active Directory?

A) LDAP is only for passwords, Active Directory is for all identities
B) LDAP is a protocol for directory services, Active Directory is a Microsoft implementation that includes LDAP
C) Active Directory is older than LDAP
D) They are the same technology

<details><summary>Answer</summary>

**B) LDAP is a protocol for directory services, Active Directory is a Microsoft implementation that includes LDAP**

LDAP (Lightweight Directory Access Protocol) is a standardized protocol for accessing and maintaining directory services. Active Directory is Microsoft's directory service implementation that uses LDAP (along with other protocols). LDAP is the protocol, Active Directory is a specific product using that protocol.

</details>

---

**Q56.** What is the purpose of Single Sign-On (SSO) in identity management?

A) To prevent all access to systems
B) To allow users to authenticate once and access multiple systems without re-authenticating
C) To eliminate the need for passwords
D) To restrict all user access

<details><summary>Answer</summary>

**B) To allow users to authenticate once and access multiple systems without re-authenticating**

SSO enables users to log in once and gain access to multiple related systems or applications without entering credentials again. This improves user experience and reduces password fatigue while still maintaining security. Federation extends this across different organizations.

</details>

---

**Q57.** What does federation in identity management primarily enable?

A) Forcing users to memorize multiple passwords
B) Allowing users from one organization to access resources in another organization using their own credentials
C) Preventing all cross-organization access
D) Eliminating authentication

<details><summary>Answer</summary>

**B) Allowing users from one organization to access resources in another organization using their own credentials**

Federation enables trusted relationships between organizations' identity systems, allowing users to authenticate with their home organization and access resources in partner organizations. This is used for B2B access, cloud services, and partner integrations without managing separate accounts.

</details>

---

**Q58.** Which type of account is typically used for service delivery and automation rather than human users?

A) Standard user account
B) Guest account
C) Service account
D) Administrator account

<details><summary>Answer</summary>

**C) Service account**

Service accounts are used by applications, services, and automation tools to run scheduled tasks and access resources without human intervention. They often have higher privileges and extended password lifecycles. Proper management of service accounts is critical because they often have broad permissions and can be targets for privilege escalation.

</details>

---

**Q59.** What should happen to user accounts that belong to terminated employees?

A) Leave them active in case the employee returns
B) Change the password but keep the account
C) Disable or delete them as part of deprovisioning
D) Transfer them to other employees

<details><summary>Answer</summary>

**C) Disable or delete them as part of deprovisioning**

When employees leave, their accounts should be disabled (or deleted after a retention period) to prevent unauthorized access. This is part of the deprovisioning process. Leaving accounts active creates security risks and potential compliance violations. Accounts should be fully deprovisioned within a defined timeframe.

</details>

---

**Q60.** Which of the following best describes time-based access in account management?

A) Restricting access based on geographic location
B) Granting access only during specified hours or periods
C) Requiring users to access systems in a specific order
D) Limiting access duration to prevent long sessions

<details><summary>Answer</summary>

**B) Granting access only during specified hours or periods**

Time-based access controls restrict when users or accounts can authenticate and access resources. For example, access might be limited to business hours only, or contractor access might be valid only for specific project duration. This is a detective control that complements other security measures.

</details>

---

**Q61.** What is geofencing in the context of access control?

A) Building physical fences to prevent access
B) Restricting access based on geographic location or GPS coordinates
C) Preventing all remote access
D) Encrypting geographic data

<details><summary>Answer</summary>

**B) Restricting access based on geographic location or GPS coordinates**

Geofencing enforces access restrictions based on geographic location. For example, access to sensitive applications might be blocked from outside a facility or country. This is particularly useful for mobile device management, preventing access from unauthorized locations while enabling legitimate access from expected locations.

</details>

---

**Q62.** Which of the following is an example of a preventive access control?

A) Reviewing access logs for unauthorized activity
B) Implementing multi-factor authentication to prevent unauthorized access
C) Detecting and alerting on suspicious login attempts
D) Investigating access violations after they occur

<details><summary>Answer</summary>

**B) Implementing multi-factor authentication to prevent unauthorized access**

Preventive controls stop unauthorized activities before they happen (MFA, locks, encryption). Preventive controls stop unauthorized activities before they happen. Detective controls (logs, audits, alerts) identify unauthorized activities after the fact. Corrective controls remediate unauthorized activities. Only MFA is preventive among the options.

</details>

---

**Q63.** What is the primary security advantage of implementing application whitelisting?

A) It allows all applications to run by default
B) It explicitly allows only approved applications, blocking everything else by default
C) It requires more administrative overhead than blacklisting
D) It improves system performance significantly

<details><summary>Answer</summary>

**B) It explicitly allows only approved applications, blocking everything else by default**

Whitelisting uses an "allow-list" approach, more secure than blacklisting's "block-list" approach. All applications are blocked unless explicitly approved, preventing unauthorized or malicious software from executing. This requires administrative effort but provides strong protection against unknown threats.

</details>

---

**Q64.** What is the primary function of a host firewall?

A) Monitoring all network traffic
B) Controlling inbound and outbound connections on individual hosts
C) Encrypting all network traffic
D) Preventing all external access

<details><summary>Answer</summary>

**B) Controlling inbound and outbound connections on individual hosts**

A host-based firewall operates on individual systems to control what network traffic is allowed in and out. Unlike a network firewall that protects many systems, a host firewall provides granular control at the individual system level. This complements network firewalls for defense in depth.

</details>

---

**Q65.** Which endpoint security technology is specifically designed for behavioral analysis of processes and activities?

A) Antivirus
B) Data loss prevention
C) Endpoint Detection and Response (EDR)
D) Firewall

<details><summary>Answer</summary>

**C) Endpoint Detection and Response (EDR)**

EDR specifically uses behavioral analysis and machine learning to detect suspicious process activities, command-line execution, memory access patterns, and other behaviors that indicate compromise. This is more advanced than signature-based antivirus and can detect unknown threats based on anomalous behavior.

</details>

---

**Q66.** What is the purpose of email filtering in endpoint and network security?

A) To improve email delivery speed
B) To detect and block malicious emails, spam, and phishing attempts
C) To read all user emails
D) To prevent all external emails

<details><summary>Answer</summary>

**B) To detect and block malicious emails, spam, and phishing attempts**

Email filtering examines email content, attachments, and sender information to block malware, phishing attempts, spam, and unwanted emails. Filters can be deployed at the gateway or on individual endpoints. This is a critical defense against email-based attacks.

</details>

---

**Q67.** Which of the following is NOT a typical function of a SIEM platform?

A) Collecting logs from multiple sources
B) Correlating events to detect anomalies
C) Automatically executing pre-defined remediation actions
D) Alerting on suspicious patterns

<details><summary>Answer</summary>

**C) Automatically executing pre-defined remediation actions**

SIEM focuses on log collection, centralization, correlation, analysis, and alerting. Automatic remediation is a SOAR (Security Orchestration, Automation, and Response) function. SOAR builds on SIEM by adding automation and orchestration capabilities.

</details>

---

**Q68.** What is the primary purpose of application whitelisting on endpoints?

A) To improve application loading speed
B) To prevent unauthorized or malicious applications from executing
C) To remove all applications from the system
D) To manage user access to applications

<details><summary>Answer</summary>

**B) To prevent unauthorized or malicious applications from executing**

Application whitelisting explicitly allows only pre-approved applications to run, blocking everything else. This prevents malware and unauthorized software from executing, reducing the attack surface significantly. It's more secure than blacklisting but requires more administrative maintenance.

</details>

---

**Q69.** Which incident response activity involves collecting evidence and understanding what happened during an incident?

A) Preparation
B) Detection and Analysis
C) Containment
D) Post-Incident Activity

<details><summary>Answer</summary>

**B) Detection and Analysis**

Detection and Analysis is when the security team discovers the incident, collects evidence, investigates, and analyzes the scope, impact, and cause. Preparation is pre-incident planning, Containment is during active response, and Post-Incident Activity is lessons learned afterward.

</details>

---

**Q70.** What is the purpose of a forensic image in digital forensics?

A) To create visual representations of incidents
B) To create an exact, bit-for-bit copy of storage media for analysis
C) To compress evidence files
D) To encrypt evidence data

<details><summary>Answer</summary>

**B) To create an exact, bit-for-bit copy of storage media for analysis**

A forensic image is a complete, byte-for-byte copy of a storage device (hard drive, USB, phone) that preserves all data including deleted files and metadata. Forensic analysis is performed on the image copy, not the original, preserving the chain of custody and allowing repeated analysis without modifying original evidence.

</details>

---

**Q71.** Which CVSS metric component measures the privileges required to exploit a vulnerability?

A) Attack Vector
B) Privileges Required
C) User Interaction
D) Scope

<details><summary>Answer</summary>

**B) Privileges Required**

The Privileges Required metric indicates whether exploitation requires low, high, or no privileges. Attack Vector measures network/local/physical accessibility, User Interaction measures if user interaction is needed, and Scope measures if impact extends beyond the vulnerable component. Each affects the overall CVSS score.

</details>

---

**Q72.** What is the primary security risk of weak password policies?

A) Increased storage requirements
B) Systems become vulnerable to brute force and dictionary attacks
C) Users forget their passwords
D) Compliance becomes harder

<details><summary>Answer</summary>

**B) Systems become vulnerable to brute force and dictionary attacks**

Weak password policies (short passwords, limited character sets, no expiration) make accounts vulnerable to attack. Strong policies require sufficient length, complexity, and regular changes. MFA further strengthens security beyond password-only protection.

</details>

---

**Q73.** Which of the following is a characteristic of a privileged user account?

A) Limited to read-only access
B) Can execute all or most system commands and access sensitive data
C) Cannot access the internet
D) Used only for backup purposes

<details><summary>Answer</summary>

**B) Can execute all or most system commands and access sensitive data**

Privileged accounts (administrative, root, service accounts with elevated permissions) have broad system and data access. These accounts require strict controls including PAM, MFA, logging, and regular audits because they pose significant security risk if compromised.

</details>

---

**Q74.** What does the principle of "need-to-know" imply in data access?

A) All employees should have access to all data
B) Users should only access the specific data required for their job
C) Managers should have access to all employee data
D) Sensitive data should never be accessed

<details><summary>Answer</summary>

**B) Users should only access the specific data required for their job**

Need-to-know restricts data access to only what is necessary for job function, even if users have system access. This is more restrictive than role-based access and supports data protection and compliance. Combined with least privilege, it minimizes exposure of sensitive data.

</details>

---

**Q75.** In vulnerability management, what is patch prioritization primarily based on?

A) Alphabetical order of patches
B) Release date of patches
C) CVSS severity score, exploitability, and business impact
D) Random selection

<details><summary>Answer</summary>

**C) CVSS severity score, exploitability, and business impact**

Patches should be prioritized based on severity (CVSS), whether exploits exist in the wild (exploitability), and impact on critical business systems. This allows organizations to allocate limited resources effectively, patching the most critical vulnerabilities first while managing the risk of patch deployment failures.

</details>

---

**Q76.** Which of the following best describes the purpose of a honeypot?

A) To encrypt network traffic
B) To serve as a decoy system to attract and monitor attacker activities
C) To block all attacks
D) To monitor legitimate user activity

<details><summary>Answer</summary>

**B) To serve as a decoy system to attract and monitor attacker activities**

Honeypots are intentionally vulnerable or valuable-looking systems designed to attract attackers. They provide no production value but allow security teams to observe attack techniques, malware samples, and attacker behaviors. This intelligence improves overall security posture.

</details>

---

**Q77.** What is the primary advantage of centralized logging through syslog?

A) It eliminates the need for firewalls
B) It allows administrators to monitor and analyze logs from all devices in one location
C) It prevents all security incidents
D) It improves network speed

<details><summary>Answer</summary>

**B) It allows administrators to monitor and analyze logs from all devices in one location**

Centralized logging via syslog aggregates logs from routers, servers, firewalls, and other devices into a central repository. This enables efficient log analysis, long-term retention, forensic investigation, and compliance reporting. Without centralization, logs are difficult to manage and security events may be missed.

</details>

---

**Q78.** What is the primary limitation of signature-based antivirus detection?

A) It is too slow
B) It can only detect known malware with existing signatures, missing zero-days and variants
C) It uses too much disk space
D) It blocks legitimate applications

<details><summary>Answer</summary>

**B) It can only detect known malware with existing signatures, missing zero-days and variants**

Signature-based detection relies on patterns of known malware. Unknown malware (zero-days), polymorphic malware, and variants without known signatures evade detection. EDR and behavioral analysis address this limitation by detecting suspicious behavior regardless of signatures.

</details>

---

**Q79.** In the context of data classification, what does "confidential" typically mean?

A) The data is public and can be shared widely
B) The data should only be accessed by authorized personnel and could cause harm if disclosed
C) The data can only be accessed by IT personnel
D) The data should be shared with all employees

<details><summary>Answer</summary>

**B) The data should only be accessed by authorized personnel and could cause harm if disclosed**

Confidential data classification indicates sensitive information that requires strong protection. Access should be strictly limited, encryption required, and unauthorized disclosure could cause significant harm. This is typically the second-highest classification (after "restricted").

</details>

---

**Q80.** What is the purpose of data retention policies?

A) To store all data indefinitely
B) To specify how long different types of data should be kept before secure destruction
C) To prevent all data access
D) To encrypt all data

<details><summary>Answer</summary>

**B) To specify how long different types of data should be kept before secure destruction**

Retention policies define how long to keep different data types based on legal, regulatory, and business requirements. Proper retention reduces storage, cost, risk from old data breaches, and legal liability. Data should be destroyed according to policy when its retention period expires.

</details>

---

**Q81.** Which of the following is a primary security function of access control lists (ACLs)?

A) Improving network speed
B) Defining which users or systems can access specific resources
C) Encrypting network traffic
D) Monitoring network bandwidth

<details><summary>Answer</summary>

**B) Defining which users or systems can access specific resources**

ACLs specify who or what has permission to access files, systems, or network resources. They are fundamental to implementing least privilege and access control policies. ACLs can be configured at the file system, directory, application, or network level.

</details>

---

**Q82.** What should be the primary focus of a post-incident activity in incident response?

A) Punishing the people involved
B) Identifying lessons learned and improving response procedures and systems
C) Deleting all evidence
D) Keeping the incident confidential

<details><summary>Answer</summary>

**B) Identifying lessons learned and improving response procedures and systems**

Post-incident reviews analyze what happened, identify root causes, document lessons learned, and implement improvements to processes, tools, training, and controls. This prevents similar incidents and strengthens the security posture for future incidents.

</details>

---

**Q83.** Which mobile device management capability prevents an employee from accessing company data on a stolen device?

A) Device encryption
B) Remote wipe
C) Application whitelisting
D) Screen lock enforcement

<details><summary>Answer</summary>

**B) Remote wipe**

Remote wipe allows administrators to erase all data on a lost or stolen device remotely, preventing unauthorized access to company data. Device encryption prevents data access if physical controls fail, but remote wipe is the capability specifically designed to address stolen device scenarios.

</details>

---

**Q84.** What is the primary difference between MDM and MAM?

A) MDM is more expensive than MAM
B) MDM manages entire devices; MAM manages applications on devices
C) MAM manages entire devices; MDM manages applications
D) They are identical technologies

<details><summary>Answer</summary>

**B) MDM manages entire devices; MAM manages applications on devices**

MDM (Mobile Device Management) manages the entire device, enforcing security policies, device settings, and full data control. MAM (Mobile Application Management) manages only specific applications and their data without controlling the full device. BYOD scenarios often use MAM to control corporate apps while leaving personal data private.

</details>

---

**Q85.** Which of the following best describes the purpose of configuration management in security?

A) To increase system complexity
B) To maintain known-good system configurations and detect unauthorized changes
C) To prevent all software updates
D) To manage user passwords

<details><summary>Answer</summary>

**B) To maintain known-good system configurations and detect unauthorized changes**

Configuration management ensures systems are configured to security baselines, tracks changes, and detects deviations. This supports compliance, incident response, and prevents unauthorized modifications. Tools like CMDB help track what should be configured on each system.

</details>

---

**Q86.** What is a primary security benefit of the 3-2-1 backup rule?

A) It reduces backup costs significantly
B) It ensures data can be recovered even if primary backups are compromised or destroyed
C) It improves system performance
D) It eliminates the need for encryption

<details><summary>Answer</summary>

**B) It ensures data can be recovered even if primary backups are compromised or destroyed**

The 3-2-1 rule (3 copies, 2 different media, 1 offsite) protects against multiple failure scenarios: media failure, ransomware, natural disasters. If two copies are destroyed, one still exists. If on-site copies are compromised, the offsite copy remains clean for recovery.

</details>

---

**Q87.** What does RPO measure in backup and disaster recovery?

A) Maximum system downtime acceptable
B) Maximum data loss acceptable (time since last backup)
C) Duration of the recovery process
D) Cost of the backup solution

<details><summary>Answer</summary>

**B) Maximum data loss acceptable (time since last backup)**

RPO (Recovery Point Objective) defines how much data loss is acceptable. An RPO of 4 hours means losing up to 4 hours of data is acceptable; backups should occur more frequently than that. RTO measures downtime, not data loss. Organizations must balance RPO/RTO requirements with costs.

</details>

---

**Q88.** Which of the following is a primary function of Data Loss Prevention (DLP)?

A) Encrypting email messages
B) Monitoring and blocking unauthorized transmission of sensitive data
C) Preventing all email transmission
D) Managing email accounts

<details><summary>Answer</summary>

**B) Monitoring and blocking unauthorized transmission of sensitive data**

DLP systems detect sensitive data (credit card numbers, SSNs, confidential documents) and prevent transmission through email, cloud storage, USB, or messaging. They can block, quarantine, alert, or track data depending on configuration, protecting sensitive data from unauthorized disclosure.

</details>

---

**Q89.** What is the primary security purpose of requiring strong passwords combined with MFA?

A) To prevent all access
B) To provide layered protection against credential compromise
C) To simplify password management
D) To speed up authentication

<details><summary>Answer</summary>

**B) To provide layered protection against credential compromise**

Combining strong passwords with MFA implements defense in depth. Even if an attacker obtains a password through phishing or credential stuffing, they cannot access the account without the second factor. This significantly reduces account compromise risk.

</details>

---

**Q90.** In incident response, what is the primary purpose of the Preparation phase?

A) Investigating the incident
B) Isolating affected systems
C) Ensuring tools, procedures, training, and teams are ready to respond to incidents
D) Recovering from the incident

<details><summary>Answer</summary>

**C) Ensuring tools, procedures, training, and teams are ready to respond to incidents**

Preparation involves establishing IR procedures, acquiring tools, training staff, building incident response teams, and establishing relationships with external organizations. Good preparation significantly reduces response time and effectiveness when incidents occur.

</details>

---

**Q91.** Which access control model is most flexible for complex authorization requirements involving multiple attributes?

A) Discretionary Access Control (DAC)
B) Role-Based Access Control (RBAC)
C) Attribute-Based Access Control (ABAC)
D) Mandatory Access Control (MAC)

<details><summary>Answer</summary>

**C) Attribute-Based Access Control (ABAC)**

ABAC makes access decisions based on multiple attributes (user attributes, resource attributes, environment attributes, action). This allows complex policies like "allow access to files if user is in engineering AND has security clearance AND accessing from office AND accessing before 6 PM". RBAC can't handle this complexity.

</details>

---

**Q92.** What is the primary purpose of hardening operating systems?

A) To improve operating system speed
B) To reduce security vulnerabilities by disabling unnecessary services and changing default configurations
C) To increase disk storage
D) To enable all features by default

<details><summary>Answer</summary>

**B) To reduce security vulnerabilities by disabling unnecessary services and changing default configurations**

OS hardening removes unnecessary services, applies patches, changes insecure defaults, disables unused protocols, and configures security settings. This reduces the attack surface and potential entry points for attackers.

</details>

---

**Q93.** Which of the following is a benefit of implementing least privilege access control?

A) Simplifying user access management
B) Reducing the damage potential if a user account is compromised
C) Eliminating the need for other security controls
D) Improving application performance

<details><summary>Answer</summary>

**B) Reducing the damage potential if a user account is compromised**

Least privilege limits what an attacker can do if they compromise a user account. If a user has only the access needed for their job, attackers inheriting that access are similarly limited. This is a key principle for reducing blast radius and supporting defense in depth.

</details>

---

**Q94.** What is a honeyfile primarily designed to detect?

A) Network intrusions only
B) Data exfiltration and lateral movement attempts
C) Operating system vulnerabilities
D) Configuration errors

<details><summary>Answer</summary>

**B) Data exfiltration and lateral movement attempts**

Honeyfiles are fake sensitive documents placed in accessible locations. When accessed or exfiltrated, they trigger alerts, helping detect when attackers are moving laterally or attempting data theft. This is more specific than honeypots which are entire decoy systems.

</details>

---

**Q95.** In security operations, what is the primary purpose of vulnerability scanning?

A) To eliminate all vulnerabilities
B) To discover vulnerabilities in systems and applications
C) To prevent all security incidents
D) To manage user access

<details><summary>Answer</summary>

**B) To discover vulnerabilities in systems and applications**

Vulnerability scanners automatically probe systems for known security weaknesses, missing patches, weak configurations, and default credentials. The scan results guide patching and hardening efforts. Scans are typically credentialed (with authentication) or uncredentialed (external probing).

</details>

---

**Q96.** What is a DNS sinkhole used for in deception and defense?

A) Improving DNS performance
B) Redirecting malicious domain traffic to a controlled system for analysis
C) Blocking all DNS queries
D) Encrypting DNS traffic

<details><summary>Answer</summary>

**B) Redirecting malicious domain traffic to a controlled system for analysis**

A DNS sinkhole intercepts DNS requests for known malicious domains and redirects them to a controlled server instead of the attacker's server. This prevents connections to malware C&C servers and allows analysis of infected systems without them communicating with attackers.

</details>

---

**Q97.** Which of the following is a disadvantage of database activity monitoring?

A) It provides too little security information
B) It can generate significant performance overhead and large volumes of log data
C) It cannot detect SQL injection
D) It prevents all database access

<details><summary>Answer</summary>

**B) It can generate significant performance overhead and large volumes of log data**

Database activity monitoring logs all database transactions and accesses, which can create very large log volumes and impact database performance. Organizations must carefully configure monitoring to capture important activities while managing performance impact and storage requirements.

</details>

---

**Q98.** What is the primary security purpose of disabling unnecessary services and ports?

A) To improve network speed
B) To reduce the attack surface by eliminating potential entry points
C) To prevent all network traffic
D) To simplify administration

<details><summary>Answer</summary>

**B) To reduce the attack surface by eliminating potential entry points**

Every open port and running service is a potential attack vector. Disabling unnecessary services and ports reduces the number of targets attackers can target, supporting the principle of defense in depth and hardening strategy.

</details>

---

**Q99.** In digital forensics, what is the order of volatility used for?

A) To determine who committed a crime
B) To guide the sequence of evidence collection, starting with most volatile data
C) To encrypt evidence files
D) To prevent evidence tampering

<details><summary>Answer</summary>

**B) To guide the sequence of evidence collection, starting with most volatile data**

Order of volatility ensures that the most volatile data (CPU registers, RAM) is captured first before it disappears. This maximizes the amount of evidence preserved and follows established forensic best practices to maintain chain of custody.

</details>

---

**Q100.** What is the primary purpose of incident response tabletop exercises?

A) To waste time during security meetings
B) To practice incident response procedures, identify gaps, and train teams in a low-risk environment
C) To document all security incidents
D) To prevent all incidents

<details><summary>Answer</summary>

**B) To practice incident response procedures, identify gaps, and train teams in a low-risk environment**

Tabletop exercises simulate incidents in a controlled, discussion-based setting where teams work through response procedures without actual system impact. This identifies process gaps, tests communication, trains staff, and improves readiness before real incidents occur.

</details>

---

**Q101.** Which of the following best describes privilege escalation?

A) Promoting a user to manager
B) An attacker gaining higher-level access than originally granted
C) Increasing the number of users
D) Adding more security controls

<details><summary>Answer</summary>

**B) An attacker gaining higher-level access than originally granted**

Privilege escalation occurs when an attacker exploits vulnerabilities to gain higher-level access (from user to admin, for example). Vertical escalation increases privilege level; horizontal escalation accesses other users' data at the same level. Preventing escalation requires patch management and proper access control.

</details>

---

**Q102.** What is the primary security benefit of certificate pinning in application development?

A) It improves application speed
B) It prevents man-in-the-middle attacks by binding applications to specific SSL/TLS certificates
C) It reduces storage requirements
D) It enables all SSL certificates

<details><summary>Answer</summary>

**B) It prevents man-in-the-middle attacks by binding applications to specific SSL/TLS certificates**

Certificate pinning binds an application to a specific certificate or public key, preventing MITM attacks even if an attacker compromises a Certificate Authority. Mobile apps commonly use pinning to protect against SSL stripping and certificate spoofing attacks.

</details>

---

**Q103.** In identity and access management, what does provisioning involve?

A) Removing user access
B) Creating user accounts and granting appropriate access rights
C) Changing user passwords
D) Disabling user accounts

<details><summary>Answer</summary>

**B) Creating user accounts and granting appropriate access rights**

Provisioning is the process of creating user accounts, assigning roles, granting access permissions, and setting up resources for new users. This is part of the IAM lifecycle. Deprovisioning is the opposite (removing access). Provisioning should align with least privilege principles.

</details>

---

**Q104.** What is the primary purpose of endpoint hardening?

A) To improve endpoint speed
B) To reduce security vulnerabilities on individual systems by removing unnecessary software and changing insecure defaults
C) To prevent all endpoint access
D) To increase endpoint storage

<details><summary>Answer</summary>

**B) To reduce security vulnerabilities on individual systems by removing unnecessary software and changing insecure defaults**

Endpoint hardening secures individual systems (workstations, servers) by disabling unnecessary services, applying patches, configuring security settings, and enforcing strong authentication. This reduces the risk of endpoints being compromised or serving as attack vectors.

</details>

---

**Q105.** Which of the following is a typical function of a unified threat management (UTM) device?

A) Only monitoring network traffic
B) Providing multiple security functions (firewall, antivirus, DLP, IDS/IPS) in one device
C) Encrypting all network traffic
D) Blocking all external access

<details><summary>Answer</summary>

**B) Providing multiple security functions (firewall, antivirus, DLP, IDS/IPS) in one device**

A UTM appliance consolidates multiple security functions into a single device, simplifying management and reducing costs compared to maintaining separate devices. However, this consolidation can create a single point of failure if not properly configured with redundancy.

</details>

---

**Q106.** What is the primary security purpose of database encryption?

A) To improve database performance
B) To protect data confidentiality if the database is stolen or compromised
C) To speed up database queries
D) To prevent all database access

<details><summary>Answer</summary>

**B) To protect data confidentiality if the database is stolen or compromised**

Encrypting databases protects sensitive data at rest, ensuring that if the physical storage is stolen or databases accessed through unauthorized means, the data remains unreadable without encryption keys. This is a critical control for protecting confidential information.

</details>

---

**Q107.** In vulnerability management, what is the purpose of a vulnerability remediation plan?

A) To ignore vulnerabilities
B) To document how and when specific vulnerabilities will be fixed based on priority and risk
C) To prevent all software updates
D) To eliminate all system access

<details><summary>Answer</summary>

**B) To document how and when specific vulnerabilities will be fixed based on priority and risk**

A remediation plan prioritizes vulnerabilities based on CVSS score, exploitability, and business impact, then schedules patching or mitigation. This ensures consistent, tracked remediation and prevents security drift. Plans should include testing procedures and rollback procedures.

</details>

---

**Q108.** What is the primary difference between a full backup and an incremental backup?

A) Full is faster than incremental
B) Full backs up everything; incremental backs up only changes since the last backup of any type
C) Incremental backs up everything; full backs up changes
D) They are identical

<details><summary>Answer</summary>

**B) Full backs up everything; incremental backs up only changes since the last backup of any type**

Full backups capture all data. Incremental backups capture only changes since the last backup (any type). Differential backups capture changes since the last full backup. Incremental requires fewer backups but requires full + all incremental backups to restore; differential requires full + latest differential.

</details>

---

**Q109.** What is a primary security consideration for service accounts?

A) Service accounts should have user-friendly passwords
B) Service accounts typically have elevated privileges and require strong controls including monitoring and regular credential rotation
C) Service accounts should not be monitored
D) Service accounts rarely need security controls

<details><summary>Answer</summary>

**B) Service accounts typically have elevated privileges and require strong controls including monitoring and regular credential rotation**

Service accounts often run with high privileges and must be carefully protected. They should have strong, complex passwords, regular credential rotation, restricted access, and detailed logging. Compromised service accounts can provide attackers with broad system access.

</details>

---

**Q110.** In security operations, what does EDR telemetry provide visibility into?

A) Only network traffic patterns
B) Process execution, memory access, file operations, and other endpoint activities
C) Only user login attempts
D) Only application performance

<details><summary>Answer</summary>

**B) Process execution, memory access, file operations, and other endpoint activities**

EDR telemetry captures detailed endpoint activities including process execution chains, registry access, network connections, file operations, and memory activities. This deep visibility enables detection of sophisticated attacks and supports forensic investigations.

</details>

---

**Q111.** What is the primary security purpose of an air gap network?

A) To improve network speed
B) To isolate critical systems from networks by physically preventing direct connections
C) To prevent all network access
D) To increase network bandwidth

<details><summary>Answer</summary>

**B) To isolate critical systems from networks by physically preventing direct connections**

Air gaps physically separate critical systems from other networks, preventing direct cyber attacks from reaching them. Even a sophisticated compromise on connected networks cannot spread across the air gap. Critical infrastructure and classified systems commonly use air gaps.

</details>

---

**Q112.** In access control, what is a credential?

A) A job title
B) Something that proves identity (password, certificate, biometric, badge)
C) A security clearance level
D) A manager approval

<details><summary>Answer</summary>

**B) Something that proves identity (password, certificate, biometric, badge)**

Credentials are factors used to authenticate identity: something you know (password), something you have (certificate, badge, token), something you are (biometric), somewhere you are (location), or something you do (behavior). MFA combines multiple credential types for stronger authentication.

</details>

---

**Q113.** What is the primary security benefit of implementing network segmentation?

A) It improves network speed dramatically
B) It isolates network segments to limit lateral movement and contain breaches
C) It prevents all external access
D) It eliminates the need for firewalls

<details><summary>Answer</summary>

**B) It isolates network segments to limit lateral movement and contain breaches**

Network segmentation divides the network into isolated zones with controlled traffic between them. If one segment is compromised, attackers cannot easily move to other segments, containing the breach. This supports defense in depth and reduces blast radius.

</details>

---

**Q114.** What is the primary purpose of a web application firewall (WAF)?

A) Monitoring network traffic only
B) Protecting web applications from attacks like SQL injection, XSS, and DDoS
C) Encrypting all web traffic
D) Blocking all external web access

<details><summary>Answer</summary>

**B) Protecting web applications from attacks like SQL injection, XSS, and DDoS**

A WAF sits between users and web applications to inspect HTTP/HTTPS traffic and block malicious requests including SQL injection, cross-site scripting, command injection, and DDoS attacks. WAFs understand application protocols better than network firewalls.

</details>

---

**Q115.** In incident response, what should be included in an incident report?

A) Only the attack details
B) Timeline of events, impact, root cause, response actions, and recommendations for prevention
C) Only the names of people involved
D) Only technical details

<details><summary>Answer</summary>

**B) Timeline of events, impact, root cause, response actions, and recommendations for prevention**

Incident reports should comprehensively document what happened (timeline), what systems were affected (impact), why it happened (root cause), how it was responded to (actions), and how to prevent recurrence (recommendations). This supports post-incident activity and organizational learning.

</details>

---

**Q116.** What is the primary security purpose of enforcing strong password policies?

A) To annoy users with complex requirements
B) To make accounts resistant to brute force and dictionary attacks
C) To prevent all access
D) To improve system performance

<details><summary>Answer</summary>

**B) To make accounts resistant to brute force and dictionary attacks**

Strong password policies (minimum length, complexity, expiration, history) make passwords harder to crack through brute force or dictionary attacks. Combined with MFA, they significantly reduce account compromise risk. Users should be trained on password management best practices.

</details>

---

**Q117.** What does the "2" in the 3-2-1 backup rule represent?

A) Two backup types
B) Two different storage media types
C) Two copies on site
D) Two weeks retention

<details><summary>Answer</summary>

**B) Two different storage media types**

The "2" in 3-2-1 means the backup copies should be stored on two different media types (e.g., one on disk, one on tape). This protects against media-specific failures. If both copies were on the same media type, a media failure could lose both.

</details>

---

**Q118.** In mobile device management, what is a geofence primarily used for?

A) Improving mobile device performance
B) Restricting access based on geographic location
C) Preventing all mobile device access
D) Monitoring user location exclusively

<details><summary>Answer</summary>

**B) Restricting access based on geographic location**

Geofences allow organizations to restrict sensitive app access to authorized locations (office building) and block access from other locations. This prevents access from lost/stolen devices or employees outside approved locations, protecting sensitive corporate data on mobile devices.

</details>

---

**Q119.** What is the primary difference between detection and analysis in incident response?

A) They are the same process
B) Detection identifies that an incident occurred; Analysis determines what happened, scope, and impact
C) Analysis happens before detection
D) Detection involves fixing the incident

<details><summary>Answer</summary>

**B) Detection identifies that an incident occurred; Analysis determines what happened, scope, and impact**

Detection discovers that an incident has occurred (alert triggered, anomaly detected). Analysis investigates the incident to understand what happened, how many systems are affected, what data was accessed, and the scope of impact. Both are critical for effective response.

</details>

---

**Q120.** What is the primary security benefit of code signing?

A) It improves code performance
B) It ensures code integrity and authenticity by cryptographically signing code so tampering is detectable
C) It prevents all software updates
D) It encrypts source code

<details><summary>Answer</summary>

**B) It ensures code integrity and authenticity by cryptographically signing code so tampering is detectable**

Code signing uses digital signatures to verify that software hasn't been modified since signing and came from the claimed source. This prevents execution of malicious or tampered code. Operating systems and browsers increasingly require code signing for trust.

</details>

---

**Q121.** In security operations, what is a false positive in intrusion detection?

A) An actual attack that was missed
B) A legitimate activity that was incorrectly identified as malicious
C) A successful intrusion
D) An undetected vulnerability

<details><summary>Answer</summary>

**B) A legitimate activity that was incorrectly identified as malicious**

False positives are alerts triggered for benign activities (legitimate user behavior flagged as attack). High false positive rates lead to alert fatigue and missed real threats. Tuning IDS/SIEM to balance sensitivity and false positives is a constant challenge in security operations.

</details>

---

**Q122.** What is the primary purpose of a security baseline?

A) To document all security incidents
B) To establish a known-good configuration of systems for comparison and detecting changes
C) To prevent all software installation
D) To track employee behavior

<details><summary>Answer</summary>

**B) To establish a known-good configuration of systems for comparison and detecting changes**

A security baseline documents the approved configuration of a system at a reference point. Deviations from the baseline indicate configuration drift or unauthorized changes, triggering investigation. Baselines support compliance, forensics, and change management.

</details>

---

**Q123.** In data security, what does data purging involve?

A) Encrypting data
B) Permanently removing data that is no longer needed
C) Backing up data
D) Restricting access to data

<details><summary>Answer</summary>

**B) Permanently removing data that is no longer needed**

Data purging is the permanent deletion of data after its retention period expires or when no longer needed. This reduces storage costs, risk from old data breaches, and privacy/compliance liability. Purging should verify that data is securely destroyed, not just deleted.

</details>

---

**Q124.** What is the primary security risk of public WiFi networks?

A) They are slow
B) Lack of encryption allows eavesdropping and MITM attacks
C) They use too much bandwidth
D) They prevent internet access

<details><summary>Answer</summary>

**B) Lack of encryption allows eavesdropping and MITM attacks**

Public WiFi is unencrypted, allowing attackers to intercept traffic, eavesdrop on communications, and perform man-in-the-middle attacks. Users should use VPNs on public WiFi to encrypt traffic and protect credentials and sensitive data from interception.

</details>

---

**Q125.** In vulnerability management, what is the purpose of a vulnerability assessment?

A) To prevent all vulnerabilities
B) To systematically identify and document vulnerabilities in systems and applications
C) To eliminate a specific vulnerability
D) To monitor all user activity

<details><summary>Answer</summary>

**B) To systematically identify and document vulnerabilities in systems and applications**

Vulnerability assessments use scanning tools and manual testing to discover security weaknesses. The results prioritize remediation efforts and guide patching strategies. Regular assessments help maintain security posture by identifying new vulnerabilities as systems change.

</details>

---

**Q126.** What is the primary security purpose of antivirus software?

A) To improve system performance
B) To detect and remove known malware and viruses
C) To prevent all security incidents
D) To encrypt all files

<details><summary>Answer</summary>

**B) To detect and remove known malware and viruses**

Antivirus software uses signature-based detection to identify and remove known malware. While not sufficient against advanced threats, antivirus is a foundational endpoint protection control that prevents infection from common malware. EDR complements antivirus with behavioral detection.

</details>

---

**Q127.** In incident response, what is containment primarily focused on?

A) Investigating the attack
B) Stopping the attack and limiting damage
C) Removing all evidence
D) Prosecuting the attacker

<details><summary>Answer</summary>

**B) Stopping the attack and limiting damage**

Containment aims to stop ongoing attacks and limit damage spread. Tactics include isolating systems, disabling compromised accounts, blocking command and control traffic, and patching exploited vulnerabilities. The goal is to stop the bleeding before eradication and recovery.

</details>

---

**Q128.** What does the "1" in the 3-2-1 backup rule represent?

A) One backup type
B) One copy stored offsite
C) One day retention
D) One backup device

<details><summary>Answer</summary>

**B) One copy stored offsite**

The "1" in 3-2-1 means one copy should be stored offsite or in a geographically different location. This protects against local disasters (fire, flooding, theft) that could destroy on-site backups. Offsite backups are critical for business continuity.

</details>

---

**Q129.** In security operations, what is a security baseline used for?

A) Tracking user activities
B) Establishing known-good system configurations for comparison and audit
C) Preventing all system changes
D) Managing user passwords

<details><summary>Answer</summary>

**B) Establishing known-good system configurations for comparison and audit**

Security baselines define how systems should be configured based on security standards (CIS Benchmarks, vendor recommendations). Configurations are compared against baselines to detect drift, verify compliance, and guide remediation of configuration weaknesses.

</details>

---

**Q130.** What is the primary purpose of event correlation in SIEM?

A) To delete security logs
B) To find relationships between events from multiple sources to detect attack patterns
C) To prevent all security incidents
D) To monitor user productivity

<details><summary>Answer</summary>

**B) To find relationships between events from multiple sources to detect attack patterns**

Event correlation analyzes logs from multiple sources to find relationships and patterns that indicate attacks. For example, multiple failed logins followed by successful login from unusual location might indicate a brute force attack. Correlation detects multi-step attacks that individual logs wouldn't.

</details>

---

**Q131.** In digital forensics, what is a logical investigation?

A) Using only common sense to determine guilt
B) Examining file systems and data within storage devices
C) Analyzing physical evidence
D) Interviewing suspects

<details><summary>Answer</summary>

**B) Examining file systems and data within storage devices**

Logical investigation examines file systems, deleted files, and data within storage to understand what occurred. Physical investigation examines hardware components. Logical forensics typically begins with forensic images and analyzes file systems, registry, logs, and data files.

</details>

---

**Q132.** What is the primary security benefit of implementing role-based access control?

A) It is easier than manual access management
B) It reduces administrative overhead and ensures consistent access based on job role
C) It prevents all access
D) It improves system speed

<details><summary>Answer</summary>

**B) It reduces administrative overhead and ensures consistent access based on job role**

RBAC assigns permissions to roles rather than individuals. When users change jobs, they switch roles and automatically get appropriate access. This reduces manual management, ensures consistency, and supports least privilege better than DAC where individual access is difficult to manage at scale.

</details>

---

**Q133.** In vulnerability scanning, what is a credentialed scan primarily designed to detect?

A) External vulnerabilities only
B) Internal vulnerabilities like missing patches and configuration issues
C) Only network vulnerabilities
D) Only application vulnerabilities

<details><summary>Answer</summary>

**B) Internal vulnerabilities like missing patches and configuration issues**

Credentialed scans authenticate and scan systems from inside, detecting vulnerabilities not visible from outside: missing patches, weak configurations, disabled security controls, and policy violations. These can only be discovered by authenticated access to system internals.

</details>

---

**Q134.** What is the primary purpose of an incident response plan?

A) To document all security incidents after they occur
B) To establish procedures, roles, and communication protocols for responding to incidents
C) To prevent all security incidents
D) To punish security failures

<details><summary>Answer</summary>

**B) To establish procedures, roles, and communication protocols for responding to incidents**

An IR plan documents how the organization will respond to security incidents: what teams are involved, communication procedures, escalation paths, incident classification, and detailed response steps. Having a plan before an incident occurs significantly improves response effectiveness.

</details>

---

**Q135.** In access control, what does "deny by default" mean?

A) All access should be denied
B) Access is denied unless explicitly allowed
C) Users must prove innocence
D) Access is allowed unless explicitly denied

<details><summary>Answer</summary>

**B) Access is denied unless explicitly allowed**

Deny by default (whitelist approach) explicitly allows only approved access; everything else is blocked. This is more secure than allow by default (blacklist) where everything is allowed except explicitly blocked items. Deny by default reduces risk from new threats and misconfiguration.

</details>

---

**Q136.** What is the primary security purpose of network access control (NAC)?

A) To prevent all network access
B) To enforce security policies and compliance before devices can connect to the network
C) To improve network speed
D) To monitor user productivity

<details><summary>Answer</summary>

**B) To enforce security policies and compliance before devices can connect to the network**

NAC systems verify that devices meet security requirements (antivirus updated, patches applied, firewall enabled) before granting network access. Non-compliant devices are quarantined or restricted to remediation networks, protecting the network from compromised or vulnerable devices.

</details>

---

**Q137.** In endpoint security, what is a rootkit?

A) A toolkit for system administration
B) Malware that operates with root/administrative privileges, hiding its presence on the system
C) A software update tool
D) A network monitoring tool

<details><summary>Answer</summary>

**B) Malware that operates with root/administrative privileges, hiding its presence on the system**

Rootkits are sophisticated malware that runs with high privileges while hiding themselves from detection. They can intercept system calls, hide files/processes, and enable persistent access. Rootkits are difficult to detect and remove, requiring forensic analysis and often system rebuilding.

</details>

---

**Q138.** What is the primary security purpose of using a bastion host?

A) To allow all external access
B) To serve as a hardened, monitored entry point to an internal network
C) To prevent all external access
D) To speed up internet connections

<details><summary>Answer</summary>

**B) To serve as a hardened, monitored entry point to an internal network**

A bastion host is a highly-hardened, monitored system that serves as the only public-facing access point to an internal network (jump box). All external access goes through the bastion, which enforces logging and security policies. This protects internal systems from direct exposure.

</details>

---

**Q139.** In vulnerability management, what does CVSS stand for?

A) Common Vulnerability Scanning System
B) Common Vulnerability Scoring System
C) Comprehensive Vulnerability Security Standard
D) Critical Vulnerability Source System

<details><summary>Answer</summary>

**B) Common Vulnerability Scoring System**

CVSS is a standardized framework for rating vulnerability severity on a 0-10 scale. It provides a common language for communicating vulnerability severity across organizations and tools, supporting consistent prioritization of remediation efforts.

</details>

---

**Q140.** What is the primary security objective of the NIST incident response framework?

A) To punish security failures
B) To establish a structured approach for detecting, responding to, and recovering from security incidents
C) To prevent all security incidents
D) To document user behavior

<details><summary>Answer</summary>

**B) To establish a structured approach for detecting, responding to, and recovering from security incidents**

The NIST IR framework provides a systematic approach to incident response across four phases: Preparation, Detection and Analysis, Containment/Eradication/Recovery, and Post-Incident Activity. This framework helps organizations respond effectively and consistently to security incidents.

</details>
