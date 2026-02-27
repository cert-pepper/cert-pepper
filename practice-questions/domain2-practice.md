# Domain 2 Practice Questions: Threats, Vulnerabilities, and Mitigations

---

**Q1.** An attacker sends a large volume of traffic to a web server from thousands of compromised machines, making it unavailable. What type of attack is this?

A) DoS
B) DDoS
C) Smurf
D) Amplification

<details><summary>Answer</summary>

**B) DDoS**

A Distributed Denial of Service (DDoS) uses multiple compromised machines (botnet) to flood a target. A regular DoS comes from a single source. Smurf is a specific ICMP-based DDoS variant. Amplification uses third-party servers to amplify traffic toward the target.

</details>

---

**Q2.** A threat actor sends a highly personalized email to a CFO, impersonating the CEO and requesting a wire transfer. What type of attack is this?

A) Phishing
B) Vishing
C) Whaling
D) Smishing

<details><summary>Answer</summary>

**C) Whaling**

Whaling is spear phishing targeting high-value executives (C-suite). This is also often called BEC (Business Email Compromise). Generic phishing targets anyone. Vishing uses voice/phone. Smishing uses SMS.

</details>

---

**Q3.** An attacker intercepts and re-sends a previously captured authentication packet to gain unauthorized access. What attack is this?

A) Replay attack
B) MITM attack
C) Session hijacking
D) Credential stuffing

<details><summary>Answer</summary>

**A) Replay attack**

A replay attack captures a valid data transmission and re-sends it to gain access. MITM intercepts ongoing communications. Session hijacking takes over an active session. Credential stuffing uses breached username/password combos.

</details>

---

**Q4.** Which type of malware replicates itself across a network WITHOUT requiring user interaction?

A) Virus
B) Trojan
C) Worm
D) Rootkit

<details><summary>Answer</summary>

**C) Worm**

Worms self-replicate without user action, spreading across networks. Viruses require a user to execute an infected file. Trojans disguise themselves as legitimate software. Rootkits hide deep in the OS.

</details>

---

**Q5.** A penetration tester is given no information about the target organization before the test. Which type of test is this?

A) White box
B) Gray box
C) Black box
D) Passive

<details><summary>Answer</summary>

**C) Black box**

Black box testing simulates an external attacker with no prior knowledge. White box provides full internal knowledge. Gray box provides partial knowledge. Passive testing monitors traffic without active probing.

</details>

---

**Q6.** A vulnerability is discovered in software that the vendor does not yet know about, and no patch exists. What is this called?

A) CVE
B) Zero-day
C) Legacy vulnerability
D) Residual risk

<details><summary>Answer</summary>

**B) Zero-day**

A zero-day vulnerability is unknown to the vendor, with no available patch. CVE is the identifier assigned to known vulnerabilities. Legacy vulnerabilities exist in outdated unsupported software. Residual risk remains after controls are applied.

</details>

---

**Q7.** An attacker compromises a software vendor's update server and inserts malware into a legitimate update. What type of attack is this?

A) Watering hole
B) Supply chain attack
C) Insider threat
D) Trojan

<details><summary>Answer</summary>

**B) Supply chain attack**

A supply chain attack compromises software or hardware before it reaches the target — like poisoning an update mechanism. Watering hole infects a website the target frequently visits. A Trojan disguises itself as legitimate software but is introduced differently.

</details>

---

**Q8.** Which attack attempts to authenticate with many accounts using one common password to avoid lockout policies?

A) Brute force
B) Dictionary attack
C) Password spraying
D) Credential stuffing

<details><summary>Answer</summary>

**C) Password spraying**

Password spraying tries one password against many accounts — intentionally slow to avoid triggering lockouts. Brute force tries all combinations against one account. Dictionary attacks use wordlists. Credential stuffing uses known breached credentials.

</details>

---

**Q9.** A web application allows users to input data into a search field. An attacker enters `'; DROP TABLE users; --` and executes it. What type of attack is this?

A) XSS
B) Buffer overflow
C) SQL injection
D) Directory traversal

<details><summary>Answer</summary>

**C) SQL injection**

SQL injection inserts malicious SQL into input fields that are passed unsanitized to the database. XSS injects scripts into web pages. Buffer overflow writes beyond allocated memory. Directory traversal uses `../` to access restricted files.

</details>

---

**Q10.** Which of the following BEST describes an IOC?

A) A security policy requiring incident response
B) A piece of forensic evidence suggesting a system has been compromised
C) A compliance framework for data handling
D) A tool used to scan for vulnerabilities

<details><summary>Answer</summary>

**B) A piece of forensic evidence suggesting a system has been compromised**

An IOC (Indicator of Compromise) is evidence that a breach has occurred or is occurring — such as malicious IP addresses, suspicious file hashes, unusual outbound traffic, or abnormal login times.

</details>
