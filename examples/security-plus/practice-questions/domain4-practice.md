**Q1.** A SIEM alert fires at 3 AM indicating that a service account has successfully authenticated to 47 different internal servers within 5 minutes — behavior it has never exhibited before. What is the FIRST action a security analyst should take?

A) Delete the service account immediately
B) Ignore the alert — service accounts often have scheduled jobs
C) Investigate the alert to determine if the activity is legitimate or malicious before taking action
D) Shut down all 47 servers to prevent further spread

<details><summary>Answer</summary>

**C) Investigate the alert to determine if the activity is legitimate or malicious before taking action**

The correct first step is investigation to verify the alert before taking disruptive action. Deleting the account or shutting down servers without investigation could disrupt legitimate operations. Ignoring the alert is dangerous. This follows the NIST IR (Incident Response) lifecycle: Detection and Analysis before Containment. CompTIA consistently tests "what do you do FIRST" — the answer is almost always "investigate/verify" before action.

</details>

---

**Q2.** During incident response, a security team confirms that ransomware is actively encrypting files on a file server. In what order should the NEXT three steps be performed?

A) Eradicate → Contain → Recover
B) Contain → Eradicate → Recover
C) Recover → Contain → Eradicate
D) Notify → Eradicate → Contain

<details><summary>Answer</summary>

**B) Contain → Eradicate → Recover**

The NIST incident response lifecycle requires Containment before Eradication. You must stop the spread (containment: isolate the server, disconnect from the network) before attempting to remove the malware (eradication), and only then restore systems (recovery). Attempting eradication without containment allows the threat to spread further.

</details>

---

**Q3.** After containing a ransomware incident, the security team identifies that the malware entered via a phishing email, established persistence via a scheduled task, and encrypted files using the volume shadow copy service. The team removes the malware and restores files from backup. Which phase of the incident response lifecycle comes NEXT?

A) Containment
B) Preparation
C) Post-incident activity / Lessons learned
D) Detection and analysis

<details><summary>Answer</summary>

**C) Post-incident activity / Lessons learned**

After Containment, Eradication, and Recovery, the final NIST phase is Post-Incident Activity (Lessons Learned). The team documents the incident timeline, identifies gaps in detection/response, and updates playbooks and controls. This is often a neglected phase but is critical for improving future response.

</details>

---

**Q4.** A security team collects a forensic image of a compromised server's hard drive. To ensure the image is a perfect, unmodified copy of the original, which of the following steps is MOST important?

A) Store the image in a cloud backup service
B) Compute a cryptographic hash of the original drive and verify the image hash matches
C) Encrypt the image with AES-256 before storage
D) Compress the image to save storage space

<details><summary>Answer</summary>

**B) Compute a cryptographic hash of the original drive and verify the image hash matches**

Hashing (MD5, SHA-1, or SHA-256) before and after imaging verifies forensic integrity — that the copy is bit-for-bit identical to the original. If the hashes match, the image is authentic. This is required to maintain the chain of custody and admissibility of evidence. The forensic process should also use a write blocker to prevent any modification to the original.

</details>

---

**Q5.** A digital forensics investigator arrives at a compromised workstation. Which of the following evidence sources should be captured FIRST to preserve the most volatile data?

A) The contents of the hard drive
B) Backup tapes stored offsite
C) The contents of RAM (memory dump)
D) System log files on the disk

<details><summary>Answer</summary>

**C) The contents of RAM (memory dump)**

The order of volatility prioritizes capture from most volatile (lost on power-off) to least volatile (persists long-term). RAM is the most volatile — it is lost the moment the system is powered off. The order is: CPU registers/cache → RAM → Swap/page file → Disk → Remote logs → Archived media. A memory dump captures running processes, network connections, encryption keys, and credentials.

</details>

---

**Q6.** During a forensic investigation, a chain of custody form documents each person who handled evidence, the date and time, and the reason for access. What is the PRIMARY purpose of maintaining chain of custody?

A) To ensure evidence is stored in encrypted form
B) To ensure the integrity and admissibility of evidence in legal proceedings
C) To track the time required for forensic analysis
D) To identify which analyst performed each analysis step

<details><summary>Answer</summary>

**B) To ensure the integrity and admissibility of evidence in legal proceedings**

Chain of custody documentation proves that evidence has not been tampered with, altered, or mishandled from collection through presentation in court. Without a proper chain of custody, evidence may be inadmissible. It is a fundamental requirement in both criminal investigations and civil litigation involving digital evidence.

</details>

---

**Q7.** A vulnerability scan of an organization's network produces 1,200 findings. The security team has limited resources and must prioritize remediation. Which factor should be given the HIGHEST weight when prioritizing?

A) The age of the vulnerability (older vulnerabilities first)
B) The CVSS score combined with whether the vulnerable system is internet-facing and exploited in the wild
C) Alphabetical order of system hostname
D) The cost of the patch

<details><summary>Answer</summary>

**B) The CVSS score combined with whether the vulnerable system is internet-facing and exploited in the wild**

Effective vulnerability prioritization considers CVSS (Common Vulnerability Scoring System) severity, asset criticality (internet-facing vs. internal), and threat intelligence (is this being actively exploited). A Critical CVSS vulnerability on an internet-facing server that is actively exploited is the highest priority. CVSS alone is insufficient because it does not consider whether exploitation is occurring.

</details>

---

**Q8.** A penetration tester is hired to assess a company's security without being given any prior information about the network topology, systems, or credentials. Which type of penetration test is this?

A) White box
B) Gray box
C) Black box
D) Red team

<details><summary>Answer</summary>

**C) Black box**

A black box penetration test provides the tester with no prior knowledge of the target environment, simulating an external attacker's perspective. White box provides full knowledge (source code, architecture, credentials); gray box provides partial knowledge (user-level credentials, general architecture). A red team exercise is a broader, longer-term simulation.

</details>

---

**Q9.** Before conducting a penetration test, the security team and the client agree on which systems are in scope, what techniques are permitted, the test window, and emergency contact procedures. What is this pre-engagement document called?

A) SOW
B) NDA
C) ROE
D) MOU

<details><summary>Answer</summary>

**C) ROE**

ROE (Rules of Engagement) is the formal document that defines the scope, authorized techniques, timing, notification procedures, and limitations for a penetration test. It protects both the tester (authorization to conduct activities that would otherwise be illegal) and the client (limits to prevent disruption). An NDA (Non-Disclosure Agreement) covers confidentiality; an SOW (Statement of Work) describes deliverables; an MOU (Memorandum of Understanding) is a broader agreement.

</details>

---

**Q10.** A threat hunter queries EDR telemetry looking for instances of PowerShell spawned as a child process of Microsoft Word, which is a common technique used by malware delivered via malicious Office macros. Which type of security activity is this?

A) Vulnerability scanning
B) Passive reconnaissance
C) Threat hunting
D) Log review

<details><summary>Answer</summary>

**C) Threat hunting**

Threat hunting is the proactive, analyst-driven search through telemetry and logs to identify threats that have evaded automated detection. The analyst starts with a hypothesis (malicious macros spawn PowerShell from Word) and searches for evidence, rather than waiting for an alert to fire. This is distinct from reactive incident response.

</details>

---

**Q11.** A SIEM correlates logs showing: (1) multiple failed logins to a web application, (2) one successful login from an unusual country, (3) a large data transfer to an external IP within 2 minutes of the successful login. What attack scenario does this sequence MOST likely represent?

A) Insider threat — an employee taking data home
B) Ransomware delivery
C) Credential brute force followed by data exfiltration
D) DDoS attack followed by SQL injection

<details><summary>Answer</summary>

**C) Credential brute force followed by data exfiltration**

The sequence (multiple failed logins → successful login from unusual location → immediate large data transfer) is the classic pattern of a successful brute force attack followed by rapid data exfiltration. SIEMs (Security Information and Event Management systems) are designed to correlate these individual events, which appear innocuous in isolation, into a meaningful attack narrative.

</details>

---

**Q12.** A SOC analyst receives an alert from the SIEM about a potential intrusion. After investigation, the analyst determines the alert was generated by legitimate scheduled backup software and not an attack. What is this called?

A) True positive
B) False positive
C) True negative
D) False negative

<details><summary>Answer</summary>

**B) False positive**

A false positive is an alert that fires for benign activity (the backup software) that is incorrectly flagged as malicious. False positives cause alert fatigue. A true positive is a real attack correctly detected; a false negative is a real attack that was missed; a true negative is legitimate activity correctly not flagged.

</details>

---

**Q13.** Which type of scan provides the MOST comprehensive vulnerability information including missing patches, misconfigurations, and weak passwords by logging into target systems with valid credentials?

A) Unauthenticated (credentialless) scan
B) Authenticated scan
C) External scan
D) Network discovery scan

<details><summary>Answer</summary>

**B) Authenticated scan**

An authenticated scan uses valid credentials to log into target systems and inspect them from the inside — checking installed software versions, registry settings, configuration files, and password policies. Unauthenticated scans can only see what is exposed externally (open ports, service banners) and produce more false positives and negatives.

</details>

---

**Q14.** A security analyst is reviewing logs and notices a host on the internal network sending DNS queries for `abc123def456.evil-c2.com` — a domain with a randomly generated subdomain — at regular 60-second intervals. No user is logged into the host. What is the MOST likely explanation?

A) A user is using a DNS-based VPN
B) The host is infected with malware using DNS for command-and-control (C2) communication
C) The DNS server is performing routine health checks
D) A developer is testing a DNS application

<details><summary>Answer</summary>

**B) The host is infected with malware using DNS for command-and-control (C2) communication**

Regular, automated DNS (Domain Name System) queries to randomly-generated subdomains (domain generation algorithm / DGA (Domain Generation Algorithm) behavior) from a host with no active user session is a strong indicator of malware C2 (Command and Control) communication using DNS tunneling or DGA-based C2. DNS is often allowed through firewalls, making it a common covert channel for malware. DNS sinkholes and behavioral analysis catch this pattern.

</details>

---

**Q15.** An organization discovers that an attacker had persistent access to their environment for 8 months before detection. During this time, the attacker conducted reconnaissance, moved laterally, and exfiltrated data in small amounts to avoid detection thresholds. What is the term for the duration of attacker access before detection?

A) RPO
B) MTTR
C) Dwell time
D) RTO

<details><summary>Answer</summary>

**C) Dwell time**

Dwell time is the duration from initial compromise to detection. The industry average is measured in months. Long dwell times indicate gaps in detection capabilities. Nation-state APTs (Advanced Persistent Threats) deliberately minimize their footprint to extend dwell time. Reducing dwell time is a primary goal of threat hunting and advanced detection programs.

</details>

---

**Q16.** A mobile device management (MDM) policy requires that all employee smartphones use a 6-digit PIN and have remote wipe enabled. An employee refuses to install the MDM profile on their personal iPhone that they use for work email. Which BYOD policy enforcement approach should the organization apply?

A) Force the employee to install MDM using their IT administrator credentials
B) Allow the exception since it is the employee's personal device
C) Prohibit the device from accessing corporate resources until it complies with MDM enrollment
D) Issue the employee a company-owned device as a replacement

<details><summary>Answer</summary>

**C) Prohibit the device from accessing corporate resources until it complies with MDM enrollment**

NAC (Network Access Control) enforces compliance: non-compliant devices should be blocked from accessing corporate resources. The MDM (Mobile Device Management) policy protects corporate data on the device. Allowing exceptions undermines the policy. Issuing a company device is a separate decision. The security principle is: compliance is required for access — full stop.

</details>

---

**Q17.** A security operations team deploys a tool that automatically quarantines endpoints showing suspicious behavior, sends alert notifications to analysts, and opens tickets in the ITSM system — all without human intervention. Which technology is this?

A) SIEM
B) EDR
C) SOAR
D) UEBA

<details><summary>Answer</summary>

**C) SOAR**

SOAR (Security Orchestration, Automation, and Response) platforms automate and orchestrate incident response workflows (playbooks). When a threat is detected, SOAR can automatically execute response actions (quarantine, notify, ticket) without waiting for analyst action, dramatically reducing mean time to respond (MTTR (Mean Time to Recover)). SIEM (Security Information and Event Management) collects and correlates logs; EDR (Endpoint Detection and Response) monitors and responds at the endpoint level; UEBA (User and Entity Behavior Analytics) analyzes behavioral anomalies.

</details>

---

**Q18.** Which tool combines endpoint telemetry across the entire organization — including network, email, cloud, and identity data — to detect attacks that span multiple vectors in a single correlated view?

A) EDR
B) SIEM
C) XDR
D) CASB

<details><summary>Answer</summary>

**C) XDR**

XDR (Extended Detection and Response) extends beyond EDR (Endpoint Detection and Response) by integrating telemetry from endpoints, network, email, cloud workloads, and identity systems into a unified detection and response platform. This cross-domain visibility allows detection of attacks that pivot between environments (e.g., a phishing email → endpoint compromise → lateral movement to cloud). EDR is limited to endpoint telemetry.

</details>

---

**Q19.** A security analyst uses a tool to analyze network packet captures and identifies an HTTP POST request containing `admin'--` in the username field and a blank password. The server responded with HTTP 200 OK. What should the analyst conclude?

A) The server successfully blocked a SQL injection attempt
B) A SQL injection attempt likely succeeded and the attacker may have bypassed authentication
C) The user entered an invalid username and was rejected
D) This is normal application health check traffic

<details><summary>Answer</summary>

**B) A SQL injection attempt likely succeeded and the attacker may have bypassed authentication**

`admin'--` is a SQL injection payload that comments out the password check in the SQL query (the `--` sequence is a SQL comment). A 200 OK response suggests the query succeeded and the attacker may have been authenticated as admin. This requires immediate investigation — verify whether the admin session was used for malicious activity.

</details>

---

**Q20.** A security team uses Nmap to scan a target network. The scan returns "filtered" for port 443 on a specific host. What does this mean?

A) Port 443 is open and accepting connections
B) Port 443 is closed — the service is not running
C) A firewall or packet filter is blocking probe packets to port 443 — the state cannot be determined
D) Port 443 is open but the service did not respond within the timeout

<details><summary>Answer</summary>

**C) A firewall or packet filter is blocking probe packets to port 443 — the state cannot be determined**

Nmap reports three states: open (accepting connections), closed (port reachable but no service listening), and filtered (a firewall/ACL (Access Control List) is dropping probe packets without responding). Filtered does not mean the port is closed — a service may be running but protected by a packet filter.

</details>

---

**Q21.** An organization's security policy requires that all software changes go through a formal review and approval process before being deployed to production. Which security process does this represent?

A) Vulnerability management
B) Change management
C) Incident response
D) Configuration management

<details><summary>Answer</summary>

**B) Change management**

Change management is the formal process for requesting, reviewing, approving, testing, and implementing changes to IT systems. It reduces the risk of unauthorized or poorly tested changes causing security incidents or outages. Change management is a key control for preventing both accidental and malicious modifications to production systems.

</details>

---

**Q22.** After a data breach, investigators discover that the attacker moved laterally through the network for three weeks by exploiting the same unpatched vulnerability on multiple servers. The patch had been available for six months. Which security process failure does this represent?

A) Incident response failure
B) Access control failure
C) Patch management failure
D) Change management failure

<details><summary>Answer</summary>

**C) Patch management failure**

Patch management is the process of applying available security updates in a timely manner. A six-month-old available patch that was not applied represents a patch management failure. This is one of the most common root causes of breaches — the vast majority of exploits target known vulnerabilities with available patches.

</details>

---

**Q23.** A security team wants to securely dispose of hard drives from decommissioned servers that contained classified data. Which method provides the HIGHEST assurance that data cannot be recovered?

A) Formatting the drives with a standard format command
B) Overwriting the drives with zeros using a software tool
C) Physical destruction (shredding or incineration)
D) Degaussing

<details><summary>Answer</summary>

**C) Physical destruction (shredding or incineration)**

Physical destruction provides the highest assurance of data sanitization — the media is destroyed and no data recovery is possible. Degaussing is effective for magnetic media but does not work on SSDs. Software overwriting may leave recoverable data on SSDs due to wear leveling. For classified data, physical destruction or NIST 800-88 purging is required.

</details>

---

**Q24.** A security analyst discovers an executable file in a user's temp directory. Before taking any action, the analyst wants to determine if the file is known malware without executing it in the live environment. What is the FIRST step the analyst should take?

A) Delete the file immediately
B) Submit the file hash to a threat intelligence platform like VirusTotal
C) Execute the file in the live environment to observe its behavior
D) Email the file to the vendor for analysis

<details><summary>Answer</summary>

**B) Submit the file hash to a threat intelligence platform like VirusTotal**

Submitting the file hash (MD5, SHA-256) to a threat intelligence platform allows instant identification of known malware without executing the file. This is fast, safe, and non-destructive. Executing the file in a live environment risks spreading infection; deleting destroys evidence; emailing the file is a security violation.

</details>

---

**Q25.** An organization conducts a security exercise where key stakeholders gather in a conference room and verbally walk through their response to a simulated ransomware scenario, discussing roles and decisions without touching live systems. What type of exercise is this?

A) Full-scale exercise
B) Functional exercise
C) Red team exercise
D) Tabletop exercise

<details><summary>Answer</summary>

**D) Tabletop exercise**

A tabletop exercise is a discussion-based simulation where participants talk through their responses to a hypothetical scenario. No systems are touched. It is the least disruptive and least expensive exercise type but still valuable for identifying process gaps and clarifying roles. A functional exercise involves actual systems/tools; a full-scale exercise simulates a real incident comprehensively.

</details>

---

**Q26.** A user reports that their Active Directory account is locked out. Security logs show 500 failed authentication attempts from an IP address outside the corporate network within 10 minutes. What type of attack is MOST likely occurring?

A) Password spraying
B) Brute force attack against a single account
C) Credential stuffing
D) Pass-the-hash

<details><summary>Answer</summary>

**B) Brute force attack against a single account**

500 failed attempts against a single account (causing lockout) within a short time window from a single external IP is the classic signature of a brute force attack — systematically trying many passwords against one target account. Password spraying tries few passwords across many accounts; credential stuffing uses known breached pairs; pass-the-hash uses NTLM (New Technology LAN Manager) hashes.

</details>

---

**Q27.** A developer checks source code into a repository using their credentials from a home computer late on a Friday night. The next day, production systems are compromised via a backdoor in that code. What type of threat does this scenario MOST likely represent?

A) Nation-state APT
B) External hacker
C) Insider threat (malicious)
D) Supply chain attack

<details><summary>Answer</summary>

**C) Insider threat (malicious)**

A developer using their authorized credentials to push malicious code to a production repository is a malicious insider threat. The attacker is an employee or contractor with legitimate access who abuses it for malicious purposes. Insider threats are particularly dangerous because they bypass perimeter controls.

</details>

---

**Q28.** A SOC receives threat intelligence indicating that a known threat actor is actively scanning for organizations using a specific version of a VPN appliance with an unpatched CVE. The organization uses this exact VPN model. What is the MOST appropriate immediate response?

A) Wait for the CVE to be assigned a severity rating before acting
B) Apply the vendor patch immediately and review VPN access logs for signs of compromise
C) Purchase a new VPN appliance from a different vendor
D) Block all VPN access until the threat subsides

<details><summary>Answer</summary>

**B) Apply the vendor patch immediately and review VPN access logs for signs of compromise**

When threat intelligence confirms active exploitation of a known vulnerability affecting your infrastructure, the immediate response is to patch AND investigate for existing compromise. Active exploitation means the window for patching before attack is narrow. Waiting for severity ratings wastes critical time when the threat is actively targeting your specific asset.

</details>

---

**Q29.** A security engineer configures an email gateway rule to quarantine any message containing attachments with .exe, .bat, or .ps1 extensions. Which security operations function does this implement?

A) Vulnerability management
B) Threat hunting
C) Preventive email security control
D) Incident response

<details><summary>Answer</summary>

**C) Preventive email security control**

Blocking or quarantining email attachments with executable or script extensions is a preventive control that stops malware delivery via email before it reaches users. This is a standard email security configuration that addresses one of the most common initial access vectors (malicious attachments in phishing emails).

</details>

---

**Q30.** During a post-incident review, the team finds that the attacker maintained persistence on the network for 11 months by creating a scheduled task that re-installed a backdoor if it was removed. What should the team add to their incident response checklist to prevent this in the future?

A) Check for unusual scheduled tasks, startup items, and services as part of the eradication phase
B) Format all hard drives immediately upon detecting any malware
C) Disable all scheduled tasks on all systems permanently
D) Change all user passwords and consider the incident closed

<details><summary>Answer</summary>

**A) Check for unusual scheduled tasks, startup items, and services as part of the eradication phase**

Persistence mechanisms (scheduled tasks, registry run keys, WMI subscriptions, startup items, rogue services) must be hunted and removed as part of eradication. Removing just the primary malware payload while leaving the persistence mechanism allows re-infection. This is a critical lessons-learned finding that should update IR playbooks.

</details>

---

**Q31.** An IDS generates an alert when a threat is actually present and an attack is occurring. What is this classification called?

A) False positive
B) False negative
C) True positive
D) True negative

<details><summary>Answer</summary>

**C) True positive**

A true positive is a correct alert: the IDS detected a real attack. True negative = no alert, no attack (correct). False positive = alert fires but no real attack (wrong alarm). False negative = real attack but no alert (missed detection, the most dangerous outcome).

</details>

---

**Q32.** After a security incident, an organization wants to determine exactly what commands the attacker ran, what files were accessed, and in what order. Which log sources would be MOST valuable for this reconstruction? (Select the best answer)

A) DHCP server logs
B) DNS query logs
C) Endpoint EDR telemetry, Windows event logs (Security, PowerShell), and firewall logs
D) SMTP mail server logs

<details><summary>Answer</summary>

**C) Endpoint EDR telemetry, Windows event logs (Security, PowerShell), and firewall logs**

Reconstructing attacker activity requires endpoint-level logging. EDR (Endpoint Detection and Response) telemetry captures process execution, command lines, and file activity. Windows Security event logs record authentication events; PowerShell logging (Script Block logging) captures commands run. Firewall logs provide network context. DHCP, DNS (Domain Name System), and SMTP logs provide supporting context but not command-level detail.

</details>

---

**Q33.** During a security incident, the security operations team identified sustained network traffic from a malicious IP address: 10.1.4.9. A security analyst is creating an inbound firewall rule to block the IP address from accessing the organization's network. Which of the following fulfills this request?

A) access-list inbound deny ip source 0.0.0.0/0 destination 10.1.4.9/32
B) access-list inbound deny ip source 10.1.4.9/32 destination 0.0.0.0/0
C) access-list inbound permit ip source 10.1.4.9/32 destination 0.0.0.0/0
D) access-list inbound permit ip source 0.0.0.0/0 destination 10.1.4.9/32

<details><summary>Answer</summary>

**B) access-list inbound deny ip source 10.1.4.9/32 destination 0.0.0.0/0**

An inbound firewall rule must DENY traffic with the malicious IP (10.1.4.9) as the SOURCE attempting to reach any destination (0.0.0.0/0) inside the network. Option A incorrectly has the malicious IP as the destination. Options C and D use "permit" instead of "deny." The rule reads: on the inbound interface, deny all IP traffic where the source is 10.1.4.9 going to any destination.

</details>

---

**Q34.** An enterprise is limiting outbound DNS traffic to a single authorized DNS server at IP 10.50.10.25. Which firewall ACL best accomplishes this?

A) Permit UDP source any destination 10.50.10.25 port 53; deny UDP source any destination any port 53
B) Deny UDP source any destination any port 53; permit UDP source any destination 10.50.10.25 port 53
C) Permit TCP source any destination 10.50.10.25 port 53; deny all
D) Deny UDP source any destination 10.50.10.25 port 53; permit all

<details><summary>Answer</summary>

**A) Permit UDP source any destination 10.50.10.25 port 53; deny UDP source any destination any port 53**

Firewall rules are processed top-to-bottom and stop at the first match. The correct approach is: (1) explicitly permit DNS to the authorized server, then (2) deny all other DNS traffic. This allows only the authorized DNS server while blocking all other outbound DNS. Option B would deny all DNS first, blocking everything including the authorized server.

</details>

---

**Q35.** Which of the following is the final step of the incident response process?

A) Containment
B) Lessons learned
C) Eradication
D) Detection

<details><summary>Answer</summary>

**B) Lessons learned**

The NIST incident response lifecycle consists of: Preparation → Detection and Analysis → Containment, Eradication, and Recovery → Post-Incident Activity (Lessons Learned). The lessons learned phase is the final step, where the team reviews what occurred, documents findings, identifies gaps in processes, and implements improvements to prevent recurrence.

</details>

---

**Q36.** A company is implementing a policy to allow employees to use their personal equipment for work. The company wants to ensure that only company-approved applications can be installed. Which of the following addresses this concern?

A) MDM
B) Containerization
C) DLP
D) FIM

<details><summary>Answer</summary>

**A) MDM**

Mobile Device Management (MDM) allows organizations to enforce security policies on both corporate and employee-owned (BYOD) devices, including restricting app installation to an approved app catalog, enforcing encryption, requiring screen locks, and remotely wiping devices. Containerization separates work and personal data; DLP prevents data exfiltration; FIM monitors file integrity changes.

</details>

---

**Q37.** Which of the following would help ensure a security analyst is able to accurately measure the overall risk to an organization when a new vulnerability is disclosed?

A) A full inventory of all hardware and software
B) Documentation of system classifications
C) A list of system owners and their departments
D) Third-party risk assessment documentation

<details><summary>Answer</summary>

**A) A full inventory of all hardware and software**

When a new vulnerability is disclosed, the first step is determining which systems are affected. A comprehensive asset inventory (hardware and software) allows analysts to immediately identify all potentially vulnerable systems, prioritize remediation by criticality, and measure exposure. Without it, the analyst cannot determine the full scope of risk.

</details>

---

**Q38.** A company receives an alert that a widely used network device vendor has been banned by the government. Which concern will the general counsel most likely raise during a hardware refresh of these devices?

A) Sanctions
B) Data sovereignty
C) Cost of replacement
D) Loss of license

<details><summary>Answer</summary>

**A) Sanctions**

Sanctions are legal restrictions that prohibit the purchase, use, import, or continued operation of products from specific entities or countries. When a government bans a vendor, continuing to use or procure those products may constitute a sanctions violation. General counsel's primary concern in this scenario is legal compliance, not cost or technical factors.

</details>

---

**Q39.** Which of the following security concepts is being followed when implementing a product that offers protection against DDoS attacks?

A) Availability
B) Non-repudiation
C) Integrity
D) Confidentiality

<details><summary>Answer</summary>

**A) Availability**

DDoS (Distributed Denial of Service) attacks target the availability of systems by overwhelming them with traffic, making them inaccessible to legitimate users. Implementing DDoS protection directly addresses the availability component of the CIA triad. Non-repudiation involves proving actions; integrity involves preventing unauthorized modification; confidentiality involves preventing unauthorized disclosure.

</details>

---

**Q40.** Which IT asset typically justifies the most security effort due to its highest value to the organization?

A) Operating systems
B) Custom order fulfillment systems
C) Servers and hardware
D) Proprietary databases containing sales, marketing, production, and finance data

<details><summary>Answer</summary>

**D) Proprietary databases**

Proprietary organizational databases are often the hardest assets to replace and contain unique, irreplaceable data that represents years of accumulated business value. While servers and OS platforms can be rebuilt from standard builds, proprietary data cannot be re-created. Data security should focus highest effort on protecting the data itself, not just the systems that store it.

</details>

---

**Q41.** What is the primary indicator of an online password attack observed in system logs?

A) Cryptographic attack signatures
B) A captured password database
C) Repeated failed password guess attempts
D) Evidence of offline brute force

<details><summary>Answer</summary>

**C) Repeated failed password guess attempts in system logs**

Online password attacks involve directly attempting authentication against a live system, generating Event ID 4625 (Windows) or authentication failure log entries for each failed attempt. The key indicator is a high volume of authentication failures, often from a single source IP or targeting a single account. Offline attacks work against captured password hashes without generating authentication events.

</details>

---

**Q42.** What is the first step in the certificate validation process when a client connects to a server?

A) The client queries the CA for a copy of the CRL
B) The server responds with a certificate including the public key
C) The client ensures the certificate is not expired
D) The client checks whether the certificate was issued by a trusted CA

<details><summary>Answer</summary>

**C) Ensure the certificate is not expired**

Certificate validation follows a sequence: (1) Check that the certificate has not expired (validity period), (2) Check that it was issued by a trusted CA, (3) Verify the chain of trust up to a root CA, (4) Check revocation status via CRL or OCSP. Expiry is checked first as it is the most computationally simple check and immediately invalidates the certificate if it fails.

</details>

---

**Q43.** What is the purpose of the Certificate Authority (CA) in a PKI?

A) Issues driver's licenses for identity verification
B) Sells software products related to encryption
C) Issues, manages, validates, and revokes digital certificates
D) Develops new encryption algorithms

<details><summary>Answer</summary>

**C) Issues, manages, validates, and revokes digital certificates**

The CA is the cornerstone of PKI. It is a trusted third party that verifies the identity of certificate requesters, issues signed digital certificates, maintains revocation information (via CRL or OCSP), and may operate sub-CAs in a hierarchy. Root CAs are typically kept offline to protect the ultimate trust anchor.

</details>

---

**Q44.** What is the notable weakness of PBKDF2 as a password hashing function?

A) It does not use a salt when generating hashes
B) It can only generate hashes up to 512 bits in length
C) It can be configured with lower iteration counts, reducing computational cost
D) It cannot be used with HMAC

<details><summary>Answer</summary>

**C) It can be configured for less computing time and RAM usage**

PBKDF2 (Password-Based Key Derivation Function 2) is a key stretching algorithm that makes brute-force attacks more expensive by iterating a hash function many times. However, it has a weakness: the iteration count is configurable, meaning administrators may set it too low for performance reasons, undermining its security. Additionally, PBKDF2 can be efficiently parallelized on GPUs, giving it a disadvantage compared to memory-hard functions like bcrypt, scrypt, or Argon2.

</details>

---

**Q45.** A security analyst needs to investigate an email security incident. The target user opened an attachment containing a worm. The worm has begun spreading to other systems on the network. Which of the following should the analyst do FIRST?

A) Reimage all affected systems
B) Identify and isolate all affected systems
C) Update anti-malware signatures on all systems
D) Notify senior management of the breach

<details><summary>Answer</summary>

**B) Identify and isolate all affected systems**

In the incident response process, after detection, the immediate priority is containment. Isolating affected systems stops the worm from spreading further. Reimaging is part of eradication and recovery, which comes after containment. Updating signatures is a useful step but does not stop ongoing propagation. Notification is important but should not delay active containment.

</details>

---
