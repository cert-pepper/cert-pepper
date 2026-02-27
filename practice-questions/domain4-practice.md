# Domain 4 Practice Questions: Security Operations

---

**Q1.** After a ransomware infection is detected, the security team isolates the affected systems. Which incident response phase is this?

A) Identification
B) Containment
C) Eradication
D) Recovery

<details><summary>Answer</summary>

**B) Containment**

Isolating affected systems to prevent further spread is containment. Identification is detecting/confirming the incident. Eradication removes the malware. Recovery restores normal operations.

**Remember PICERL:** Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned

</details>

---

**Q2.** A forensic investigator must collect evidence from a compromised system. In what order should volatile data be collected?

A) Disk, then RAM, then network connections
B) RAM, then disk, then backups
C) CPU cache/registers, then RAM, then disk
D) Backups, then disk, then RAM

<details><summary>Answer</summary>

**C) CPU cache/registers, then RAM, then disk**

Follow the order of volatility — collect the most volatile (temporary) data first before it's lost:
1. CPU registers/cache
2. RAM
3. Swap/page file
4. Disk
5. Remote logs
6. Backups

</details>

---

**Q3.** Which tool would BEST allow a security analyst to aggregate and correlate logs from firewalls, servers, and applications to detect threats?

A) IDS
B) SIEM
C) WAF
D) EDR

<details><summary>Answer</summary>

**B) SIEM**

SIEM (Security Information and Event Management) aggregates logs from multiple sources and correlates events to detect threats and generate alerts. IDS detects network attacks. WAF protects web apps. EDR monitors endpoints specifically.

</details>

---

**Q4.** An employee's laptop is lost. The security team remotely erases all data on the device. What capability enabled this?

A) MDM with remote wipe
B) DLP enforcement
C) FDE with TPM
D) HIDS policy

<details><summary>Answer</summary>

**A) MDM with remote wipe**

MDM (Mobile Device Management) enables remote management of mobile/endpoint devices, including remote wipe to erase data if a device is lost or stolen. DLP prevents data leakage. FDE encrypts the disk. HIDS monitors host activity.

</details>

---

**Q5.** An access control model assigns permissions based on the user's department, clearance level, and time of day. Which model is this?

A) RBAC
B) DAC
C) MAC
D) ABAC

<details><summary>Answer</summary>

**D) ABAC**

ABAC (Attribute-Based Access Control) grants access based on multiple attributes (department, clearance, time, location). RBAC is based on roles/job titles. DAC lets owners control access. MAC uses classification labels.

</details>

---

**Q6.** A security team proactively searches for hidden threats in the network that evaded existing detection tools. What is this activity called?

A) Vulnerability scanning
B) Penetration testing
C) Threat hunting
D) Incident response

<details><summary>Answer</summary>

**C) Threat hunting**

Threat hunting is a proactive, human-led search for threats that may have evaded automated detection. It uses hypotheses from threat intelligence and TTPs. Vulnerability scanning finds known weaknesses. Penetration testing actively exploits them. Incident response reacts to detected events.

</details>

---

**Q7.** Which of the following BEST describes the purpose of a honeynet?

A) To filter malicious traffic before it reaches internal systems
B) To attract and study attacker behavior in a decoy environment
C) To monitor user behavior for anomalies
D) To encrypt network communications

<details><summary>Answer</summary>

**B) To attract and study attacker behavior in a decoy environment**

A honeynet is a network of honeypots designed to attract attackers, observe their techniques, and gather intelligence — without them touching real systems. A firewall filters traffic. UEBA monitors user behavior. TLS encrypts communications.

</details>

---

**Q8.** Replacing a credit card number with a randomly generated token that has no mathematical relationship to the original is called:

A) Encryption
B) Hashing
C) Tokenization
D) Masking

<details><summary>Answer</summary>

**C) Tokenization**

Tokenization substitutes sensitive data with a non-sensitive placeholder (token). The original data is stored securely in a vault and the token has no value to attackers. Encryption is reversible with a key. Hashing is one-way. Masking partially obscures data (e.g., ***-**-1234).

</details>

---

**Q9.** An organization wants to ensure that employees are only accessing systems they are authorized to use. Periodic reviews of who has access to what systems implement which concept?

A) Least privilege
B) Separation of duties
C) Access recertification
D) Account lockout

<details><summary>Answer</summary>

**C) Access recertification**

Access recertification (also called access review or entitlement review) is a periodic review of user permissions to ensure they remain appropriate. Least privilege sets the initial level. Separation of duties splits responsibilities. Account lockout triggers after failed logins.

</details>

---

**Q10.** Which type of endpoint security solution provides real-time monitoring, detection, and automated response capabilities on individual devices?

A) Antivirus
B) HIDS
C) EDR
D) DLP

<details><summary>Answer</summary>

**C) EDR**

EDR (Endpoint Detection and Response) provides continuous monitoring, threat detection, and automated or guided response on endpoints. Traditional antivirus is signature-based only. HIDS detects but doesn't respond. DLP prevents data exfiltration, not malware.

</details>
