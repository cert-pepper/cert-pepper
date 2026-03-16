**Q1.** A user receives an email appearing to come from their company's CEO asking them to urgently wire $47,000 to a vendor account. The CEO's actual email address differs by one character. What type of attack is this?

A) Phishing
B) Spear phishing
C) BEC
D) Whaling

<details><summary>Answer</summary>

**C) BEC**

BEC (Business Email Compromise) is a sophisticated attack where the attacker impersonates an executive or trusted partner via email to authorize fraudulent financial transactions. The scenario involves a spoofed executive email requesting a wire transfer — the defining characteristics of BEC. Whaling targets executives as victims; BEC uses executives as the impersonated sender to manipulate employees.

</details>

---

**Q2.** An attacker calls an employee claiming to be from the IT help desk and asks the employee to provide their password to resolve an urgent account issue. What type of attack is this?

A) Phishing
B) Smishing
C) Vishing
D) Pretexting

<details><summary>Answer</summary>

**C) Vishing**

Vishing (voice phishing) is social engineering conducted over telephone calls. The attacker uses a fabricated scenario ("IT help desk") to manipulate the victim into providing credentials. Phishing uses email; smishing uses SMS; pretexting is the act of creating a false scenario (vishing is a type of pretexting, but vishing is the more specific answer here).

</details>

---

**Q3.** An attacker sends a text message to employees of a bank pretending to be the bank's fraud department, asking recipients to click a link to verify their account. What type of attack is this?

A) Vishing
B) Phishing
C) Smishing
D) Spear phishing

<details><summary>Answer</summary>

**C) Smishing**

Smishing is phishing conducted via SMS (text messages). The delivery mechanism (text message) is what distinguishes smishing from phishing (email) and vishing (phone call).

</details>

---

**Q4.** An attacker researches a target executive on LinkedIn, then sends a personalized email referencing the executive's recent conference presentation and asking them to review an attached document. What type of attack is this?

A) Phishing
B) Spear phishing
C) Whaling
D) Business email compromise

<details><summary>Answer</summary>

**B) Spear phishing**

Spear phishing is a targeted phishing attack directed at a specific individual using personalized information gathered through research (OSINT (Open Source Intelligence)). The use of LinkedIn research and personal details distinguishes it from generic phishing. Whaling is spear phishing specifically targeting high-profile individuals like executives — while the target here is an executive, the key detail is the targeting methodology; whaling would be the answer if the question emphasized their high-profile status as the reason for targeting.

</details>

---

**Q5.** An attacker registers the domain "paypa1.com" (with the number one instead of the letter l) and creates a fake login page identical to the real site. What type of attack is this?

A) Pharming
B) Watering hole
C) Typosquatting
D) Homograph attack

<details><summary>Answer</summary>

**C) Typosquatting**

Typosquatting (also called URL hijacking) involves registering a domain that is a common misspelling or character substitution of a legitimate domain to capture traffic from users who mistype the URL. A homograph attack uses Unicode characters that visually resemble ASCII characters; pharming redirects via DNS (Domain Name System) poisoning; a watering hole compromises a legitimate site frequented by the target.

</details>

---

**Q6.** A threat actor compromises a popular developer blog that is frequently visited by employees of a software company they are targeting. The attacker embeds malware that infects visitors. What type of attack is this?

A) Typosquatting
B) Spear phishing
C) Watering hole attack
D) Supply chain attack

<details><summary>Answer</summary>

**C) Watering hole attack**

A watering hole attack compromises a website known to be frequented by the target group, then waits for victims to visit and be infected — like a predator waiting at a watering hole. The attacker did not target the software company directly; they targeted a site their employees visit.

</details>

---

**Q7.** A penetration tester drops several USB drives labeled "Q3 Payroll - Confidential" in the parking lot of the target organization. This technique is known as what?

A) Pretexting
B) Tailgating
C) Baiting
D) Shoulder surfing

<details><summary>Answer</summary>

**C) Baiting**

Baiting lures a victim with something enticing (the curiosity of finding a "confidential payroll" USB). If a victim plugs in the drive, it executes malware. The physical delivery mechanism and the lure of curiosity/reward are the defining characteristics of baiting.

</details>

---

**Q8.** An employee follows closely behind an authorized person through a badge-access door without presenting their own credentials. What is this physical social engineering technique called?

A) Baiting
B) Tailgating
C) Shoulder surfing
D) Dumpster diving

<details><summary>Answer</summary>

**B) Tailgating**

Tailgating (also called piggybacking) involves physically following an authorized person through a secured entry point without independent authentication. The attacker exploits social courtesy — people typically hold doors open for those behind them.

</details>

---

**Q9.** A piece of malware encrypts all files on an infected system and displays a message demanding cryptocurrency payment within 72 hours in exchange for the decryption key. What type of malware is this?

A) Spyware
B) Rootkit
C) Ransomware
D) Logic bomb

<details><summary>Answer</summary>

**C) Ransomware**

Ransomware encrypts the victim's data or locks them out of their system, then demands payment (typically cryptocurrency) for the decryption key. The time-limited demand and cryptocurrency payment are classic ransomware characteristics. Notable examples include WannaCry, NotPetya, and REvil.

</details>

---

**Q10.** A systems administrator discovers that a program installed on a server six months ago has been silently collecting keystrokes and sending them to an external IP address. The program appeared legitimate at installation. What type of malware is this?

A) Worm
B) Trojan with keylogger functionality
C) Ransomware
D) Logic bomb

<details><summary>Answer</summary>

**B) Trojan with keylogger functionality**

A Trojan disguises itself as legitimate software to trick users into installing it. Once installed, it performs malicious actions (here, keylogging) without the user's knowledge. A worm self-replicates across networks without user interaction; a logic bomb triggers on a specific condition; ransomware encrypts data.

</details>

---

**Q11.** Malware on a compromised system opens a covert channel to an external server, allowing the attacker to remotely control the infected machine, exfiltrate data, and install additional tools. Which type of malware best describes this?

A) Rootkit
B) Logic bomb
C) RAT
D) Worm

<details><summary>Answer</summary>

**C) RAT**

A RAT (Remote Access Trojan) establishes a covert remote access channel (typically calling back to an attacker-controlled C2 (Command and Control) server), giving the attacker full control over the infected system. RATs are commonly used in APT (Advanced Persistent Threat) campaigns for initial access and persistence.

</details>

---

**Q12.** A malicious program is discovered on a server that has no persistent files on disk. All of its code resides in memory and uses legitimate built-in Windows tools like PowerShell and WMI for execution. What type of malware is this?

A) Rootkit
B) Fileless malware
C) Logic bomb
D) Spyware

<details><summary>Answer</summary>

**B) Fileless malware**

Fileless malware operates entirely in memory and leverages legitimate system tools (LOLBins — Living-off-the-Land Binaries) like PowerShell, WMI, and cmd.exe to execute, leaving no files on disk. This makes it harder to detect with traditional signature-based antivirus. It is frequently used in APT (Advanced Persistent Threat) operations.

</details>

---

**Q13.** A developer embeds code in a financial application that will delete all transaction records if their user account is ever disabled. The code has existed undetected for two years. What type of malware is this?

A) Trojan
B) Worm
C) Logic bomb
D) Ransomware

<details><summary>Answer</summary>

**C) Logic bomb**

A logic bomb is malicious code that remains dormant until a specific trigger condition is met (here: the developer's account being disabled). This is a classic insider threat scenario. The delayed, conditional execution and the insider as the author are the defining characteristics.

</details>

---

**Q14.** After a Windows workstation is compromised, the attacker modifies the operating system kernel to hide malicious processes, registry keys, and network connections from standard system tools and antivirus software. What type of malware has been installed?

A) RAT
B) Rootkit
C) Spyware
D) Adware

<details><summary>Answer</summary>

**B) Rootkit**

A rootkit modifies the operating system kernel or other low-level components to hide its presence (processes, files, network connections) from the OS itself and security tools. This makes rootkits extremely difficult to detect and remove without booting from external media.

</details>

---

**Q15.** An attacker captures a valid Kerberos authentication response between a user and a domain controller, saves it, and replays it hours later to authenticate as that user. What type of attack is this?

A) Pass-the-hash
B) Kerberoasting
C) Replay attack
D) Golden ticket attack

<details><summary>Answer</summary>

**C) Replay attack**

A replay attack captures valid authentication data (credentials, tokens, or in this case a Kerberos ticket) and retransmits it later to authenticate without knowing the original credentials. Mitigation includes timestamps and nonces in authentication protocols. Pass-the-hash uses an NTLM (New Technology LAN Manager) hash; Kerberoasting extracts service ticket hashes for offline cracking; a golden ticket uses the KRBTGT hash.

</details>

---

**Q16.** An attacker compromises a Windows domain workstation and extracts NTLM password hashes from memory using a credential dumping tool. Without cracking the hashes, the attacker authenticates to other systems on the network using only the captured hash. What is this attack called?

A) Replay attack
B) Pass-the-hash
C) Credential stuffing
D) Kerberoasting

<details><summary>Answer</summary>

**B) Pass-the-hash**

Pass-the-hash is an attack technique specific to NTLM (New Technology LAN Manager) authentication where the attacker uses a captured password hash to authenticate without knowing the underlying plaintext password. The hash itself serves as the credential. This is a critical Windows lateral movement technique.

</details>

---

**Q17.** A security analyst reviews web server logs and finds requests containing `' OR '1'='1` in the username field of a login form. What type of attack is occurring?

A) XSS
B) CSRF
C) SQL injection
D) Command injection

<details><summary>Answer</summary>

**C) SQL injection**

`' OR '1'='1` is a classic SQL injection payload that manipulates the query logic to return true for all rows, potentially bypassing authentication. SQL injection inserts malicious SQL code into input fields to manipulate the database.

</details>

---

**Q18.** An attacker injects a malicious script into a product review field on an e-commerce site. Every user who views that product page subsequently has their session cookie stolen by the script. What type of attack is this?

A) Reflected XSS
B) Stored (Persistent) XSS
C) CSRF
D) SQL injection

<details><summary>Answer</summary>

**B) Stored (Persistent) XSS**

Stored XSS (Cross-Site Scripting) permanently saves the malicious script on the server (e.g., in a database field). Every user who later views the affected page executes the script. Reflected XSS is a one-time attack where the malicious script is in the URL and immediately reflected in the response — it is not stored.

</details>

---

**Q19.** An attacker tricks a user who is authenticated to their bank's website into clicking a malicious link. The link causes the user's browser to make an unauthorized fund transfer request to the bank, using the user's existing session. What type of attack is this?

A) Stored XSS
B) SSRF
C) CSRF
D) Clickjacking

<details><summary>Answer</summary>

**C) CSRF**

CSRF (Cross-Site Request Forgery) exploits the trust a web application has in a user's browser. The attacker crafts a request that performs an action on the target site using the victim's authenticated session. The victim's browser automatically sends session cookies, making the request appear legitimate. CSRF tokens in forms are the primary mitigation.

</details>

---

**Q20.** A web application allows users to provide a URL that the server fetches and displays. An attacker submits `http://169.254.169.254/latest/meta-data/` — the AWS instance metadata endpoint — and retrieves cloud credentials. What type of attack is this?

A) CSRF
B) IDOR
C) SSRF
D) Path traversal

<details><summary>Answer</summary>

**C) SSRF**

SSRF (Server-Side Request Forgery) tricks the server into making HTTP requests to internal resources on behalf of the attacker. The AWS EC2 metadata endpoint (`169.254.169.254`) is a classic SSRF target — it is only reachable from within the instance and returns sensitive cloud credentials. SSRF was a major factor in the 2019 Capital One breach.

</details>

---

**Q21.** A user navigates to `https://bank.example.com/account?id=12345` and notices that changing `12345` to `12346` displays another customer's account details. What vulnerability does this demonstrate?

A) SQL injection
B) Path traversal
C) IDOR
D) CSRF

<details><summary>Answer</summary>

**C) IDOR**

IDOR (Insecure Direct Object Reference) occurs when an application exposes internal object references (database record IDs, filenames) in URLs or parameters without proper authorization checks. The attacker simply increments the ID to access another user's data. This is a common finding in web application security assessments.

</details>

---

**Q22.** An attacker floods a DNS resolver with spoofed responses, causing it to cache a false mapping that redirects users of a popular bank to a fraudulent IP address even when they type the correct URL. What type of attack is this?

A) Evil twin
B) DNS poisoning (cache poisoning)
C) Pharming
D) Typosquatting

<details><summary>Answer</summary>

**B) DNS poisoning (cache poisoning)**

DNS (Domain Name System) cache poisoning injects false DNS records into a resolver's cache, redirecting users to attacker-controlled IPs. Pharming is a broader term that includes DNS poisoning and hosts file modification; DNS poisoning is the more specific and technically correct answer. DNSSEC (Domain Name System Security Extensions) mitigates this by cryptographically signing DNS records.

</details>

---

**Q23.** A threat intelligence report identifies a nation-state APT group that has maintained persistent access to critical infrastructure networks for over two years, exfiltrating data while avoiding detection. Which threat actor category BEST describes this group?

A) Hacktivist
B) Organized crime
C) Script kiddie
D) Nation-state / APT

<details><summary>Answer</summary>

**D) Nation-state / APT**

Nation-state actors (Advanced Persistent Threats) have the highest sophistication, virtually unlimited resources, and strategic long-term objectives. The multi-year dwell time, critical infrastructure targeting, and data exfiltration are hallmarks of nation-state APT (Advanced Persistent Threat) operations. Hacktivists are ideologically motivated; organized crime seeks financial gain; script kiddies lack sophistication.

</details>

---

**Q24.** A company discovers that a software update for their network management platform was compromised at the vendor's build server before distribution. Thousands of customers installed the trojanized update before discovery. What type of attack is this?

A) Watering hole attack
B) Supply chain attack
C) Zero-day exploit
D) Insider threat

<details><summary>Answer</summary>

**B) Supply chain attack**

A supply chain attack compromises a vendor, software update mechanism, or third-party component to reach downstream targets. The SolarWinds SUNBURST attack (2020) is the defining real-world example. Attackers target the supply chain because compromising one vendor can provide access to thousands of customers simultaneously.

</details>

---

**Q25.** An attacker targets the KRBTGT account in an Active Directory environment, extracts its password hash, and uses it to forge Kerberos tickets granting domain admin access to any resource for an extended period. What is this attack called?

A) Pass-the-hash
B) Kerberoasting
C) Silver ticket attack
D) Golden ticket attack

<details><summary>Answer</summary>

**D) Golden ticket attack**

A golden ticket attack uses the KRBTGT account's hash to forge TGTs (Ticket Granting Tickets) for any user, granting unlimited domain access. The KRBTGT account is the Kerberos Key Distribution Center account; controlling its hash gives an attacker the ability to create arbitrary Kerberos tickets. A silver ticket uses a service account hash (more limited scope).

</details>

---

**Q26.** A security team runs a script that tests 200 commonly used passwords against every account in Active Directory, making only one attempt per account to avoid lockout thresholds. What type of attack is this?

A) Brute force
B) Dictionary attack
C) Password spraying
D) Credential stuffing

<details><summary>Answer</summary>

**C) Password spraying**

Password spraying tests a small set of commonly used passwords against many accounts — the inverse of brute force. By trying only one or two passwords per account, the attack stays below lockout thresholds while still covering a wide target surface. Credential stuffing uses breached username/password pairs; dictionary attacks try many passwords against a single account.

</details>

---

**Q27.** A security analyst receives an alert that an internal server began communicating with an external IP address at 2 AM after a software update was applied earlier that day. Investigation reveals the update package was altered in transit. Which type of attack does this represent?

A) Zero-day exploit
B) Insider threat
C) On-path (MITM) attack resulting in a supply chain compromise
D) Logic bomb

<details><summary>Answer</summary>

**C) On-path (MITM) attack resulting in a supply chain compromise**

An on-path (formerly MITM) attacker intercepted the legitimate software update in transit and replaced it with a malicious version. The C2 (Command and Control) communication at 2 AM confirms the malicious payload was executed. This combines an on-path interception with a supply-chain-style compromise.

</details>

---

**Q28.** A vulnerability assessment report shows a finding rated 9.8 on the CVSS v3.1 scale for an internet-facing web server. How should this be prioritized?

A) Low — schedule remediation in the next quarterly patch cycle
B) Medium — investigate within 30 days
C) High — remediate within the normal patching window
D) Critical — remediate immediately, prioritized above other work

<details><summary>Answer</summary>

**D) Critical — remediate immediately, prioritized above other work**

CVSS (Common Vulnerability Scoring System) scores of 9.0–10.0 are rated Critical. An internet-facing server with a 9.8 CVSS score is an extremely high-risk exposure that could be exploited remotely with low complexity. CVSS ranges: None (0.0), Low (0.1–3.9), Medium (4.0–6.9), High (7.0–8.9), Critical (9.0–10.0).

</details>

---

**Q29.** A user reports that their workstation is running slowly, their browser is displaying advertisements they did not request, and their browser homepage has changed without their intervention. Which type of malware is MOST likely responsible?

A) Ransomware
B) Worm
C) Adware / PUP
D) Rootkit

<details><summary>Answer</summary>

**C) Adware / PUP**

Adware displays unwanted advertisements and may modify browser settings (homepage, search engine). It often arrives bundled with legitimate software as a PUP (Potentially Unwanted Program). It does not typically encrypt files, replicate across networks, or hide itself in the kernel.

</details>

---

**Q30.** An employee discovers a USB drive in the company parking lot labeled "Executive Compensation 2024" and plugs it into their work computer. The USB drive silently installs malware. This scenario describes which combination of attack types?

A) Vishing and a Trojan
B) Baiting and a Trojan
C) Spear phishing and ransomware
D) Pretexting and a worm

<details><summary>Answer</summary>

**B) Baiting and a Trojan**

The physical USB drop with an enticing label is baiting — luring the victim's curiosity. The malware that appears to be a legitimate file but installs malicious software is a Trojan. This is a well-documented real-world attack vector (Stuxnet was introduced to Iran's air-gapped nuclear facility via a USB baiting attack).

</details>

---

**Q31.** A security team discovers that an attacker compromised a vendor's software update mechanism and used it to push a backdoored update to all customers. After gaining initial access, the attacker spent four months moving laterally and establishing persistence before being discovered. Which two threat concepts best describe this campaign?

A) Script kiddie attack and zero-day exploit
B) Supply chain attack and APT behavior
C) Insider threat and logic bomb
D) Watering hole attack and ransomware

<details><summary>Answer</summary>

**B) Supply chain attack and APT behavior**

Compromising a vendor's update mechanism is a supply chain attack. The long dwell time (4 months), deliberate lateral movement, and persistent access are hallmarks of APT (Advanced Persistent Threat) behavior. This mirrors the SolarWinds SUNBURST attack characteristics.

</details>

---

**Q32.** Which of the following BEST distinguishes a vulnerability scan from a penetration test?

A) A vulnerability scan exploits vulnerabilities; a penetration test only identifies them.
B) A vulnerability scan identifies potential weaknesses without exploiting them; a penetration test actively attempts to exploit vulnerabilities.
C) A vulnerability scan requires physical access; a penetration test is always remote.
D) A vulnerability scan is conducted by external parties; a penetration test is conducted internally.

<details><summary>Answer</summary>

**B) A vulnerability scan identifies potential weaknesses without exploiting them; a penetration test actively attempts to exploit vulnerabilities.**

Vulnerability scanning is automated and non-exploitative — it identifies and reports potential vulnerabilities. Penetration testing goes further by actively attempting to exploit findings to demonstrate real-world impact and validate controls. Both can be conducted internally or externally, authenticated or unauthenticated.

</details>

---

**Q33.** A security researcher discovers a critical vulnerability in a widely used VPN product. There is no available patch, and the vendor is unaware of the issue. What type of vulnerability is this?

A) Unpatched vulnerability
B) Zero-day vulnerability
C) CVE vulnerability
D) Misconfiguration

<details><summary>Answer</summary>

**B) Zero-day vulnerability**

A zero-day vulnerability is one that is unknown to the vendor (or for which no patch exists) and may be actively exploited. Once the vendor publishes a patch, it is no longer a "zero-day." CVE (Common Vulnerabilities and Exposures) status requires the vulnerability to be known and assigned a CVE identifier; unpatched refers to known vulnerabilities with available but unapplied patches.

</details>

---

**Q34.** An organization's email security gateway blocks messages with spoofed sender domains by checking whether the sending mail server's IP is listed in the domain's authorized sender records. Which email security standard does this describe?

A) DKIM
B) DMARC
C) SPF
D) S/MIME

<details><summary>Answer</summary>

**C) SPF**

SPF (Sender Policy Framework) is a DNS (Domain Name System) record that lists IP addresses and mail servers authorized to send email on behalf of a domain. Receiving mail servers check the SPF record to detect spoofed sender domains. DKIM (DomainKeys Identified Mail) adds a cryptographic signature to email headers; DMARC (Domain-based Message Authentication, Reporting, and Conformance) is the policy layer that specifies what to do when SPF or DKIM fails; S/MIME provides end-to-end email encryption.

</details>

---

**Q35.** A phishing email passes the SPF check because the attacker used a legitimate mail server that is listed in the domain's SPF record. However, the email is rejected because the message body's cryptographic signature does not match the domain's public key. Which email security standard caught this attack?

A) SPF
B) DMARC
C) DKIM
D) TLS

<details><summary>Answer</summary>

**C) DKIM**

DKIM (DomainKeys Identified Mail) adds a cryptographic signature to outgoing email messages. The receiving server verifies the signature against the sender's public key published in DNS (Domain Name System). Even if SPF passes, DKIM can catch message tampering or unauthorized sending because the signature would not match.

</details>

---

**Q36.** A business development team reports that files are missing from the database system and the server log-in screens are showing a lock symbol that requires users to contact an email address to access the system and data. Which of the following attacks is the company facing?

A) Rootkit
B) Spyware
C) Ransomware
D) Bloatware

<details><summary>Answer</summary>

**C) Ransomware**

Ransomware encrypts victim files and demands payment for the decryption key. The lock symbol on the login screen and requirement to contact an address to regain access are hallmark indicators of a ransomware attack. Rootkits provide persistent hidden access; spyware silently collects data; bloatware is unwanted pre-installed software.

</details>

---

**Q37.** Which of the following would be the most helpful in restoring data in the event of a ransomware infection?

A) Load balancing
B) Geographic dispersion
C) Encryption
D) Backups

<details><summary>Answer</summary>

**D) Backups**

Regular, tested, offline or immutable backups are the primary defense against ransomware. If backups exist and are not themselves encrypted by the ransomware (e.g., if kept offline or in air-gapped storage), the organization can restore without paying the ransom. Load balancing improves availability; geographic dispersion reduces disaster risk; encryption is what the ransomware uses.

</details>

---

**Q38.** Which of the following threat actors is the most likely to be hired by a foreign government to attack critical systems located in other countries?

A) Hacktivist
B) Whistleblower
C) Organized crime
D) Unskilled attacker

<details><summary>Answer</summary>

**C) Organized crime**

Nation-state actors and organized crime groups are most often associated with government-sponsored attacks on foreign critical infrastructure. Organized crime has both the resources and motivation (financial or political) for such operations. Hacktivists are motivated by ideology and conduct public campaigns; whistleblowers expose misconduct internally; unskilled attackers (script kiddies) lack the sophistication for targeted government-level attacks.

</details>

---

**Q39.** Which of the following threat actors is the most likely to use common hacking tools found on the internet to attempt to remotely compromise an organization's web server?

A) Organized crime
B) Insider threat
C) Unskilled attacker
D) Nation-state

<details><summary>Answer</summary>

**C) Unskilled attacker**

Unskilled attackers (sometimes called script kiddies) rely on publicly available tools and exploit frameworks rather than developing custom exploits. They lack the sophistication to craft novel attacks. Nation-state actors and organized crime use custom or advanced tools; insider threats leverage privileged access rather than network-based exploitation tools.

</details>

---

**Q40.** An email sent to a CFO appears to be from the CEO, urgently requesting an immediate wire transfer to a new vendor. The email address is subtly misspelled (ceo@cornpany.com instead of ceo@company.com). What type of attack is this?

A) Vishing
B) Whaling
C) Smishing
D) Tailgating

<details><summary>Answer</summary>

**B) Whaling**

Whaling is a form of spear phishing that specifically targets high-level executives ("big fish" or "whales"). This scenario shows classic whaling indicators: targeting the CFO, impersonating the CEO, creating urgency, requesting a large financial transfer, and using a slightly misspelled domain (typosquatting). Vishing uses phone calls; smishing uses SMS text messages; tailgating is a physical access attack.

</details>

---

**Q41.** During a post-incident investigation, forensics reveal an attacker maintained undetected access for nine months, using custom-built malware and sophisticated lateral movement techniques to slowly exfiltrate research data. Which threat actor type is most likely responsible?

A) Script kiddie
B) Hacktivist
C) Insider threat
D) Advanced Persistent Threat (APT)

<details><summary>Answer</summary>

**D) Advanced Persistent Threat (APT)**

APTs are sophisticated, well-resourced threat actors — often state-sponsored — that conduct long-term, stealthy campaigns against specific targets. Key APT indicators: persistent presence over many months, advanced custom tools, targeted objective (research data), and stealth. Script kiddies use off-the-shelf tools; hacktivists seek publicity; insiders use privileged access but would not typically develop custom malware.

</details>

---

**Q42.** An employee clicked a link in a deceptive payment email requesting contact information updates, entered their login credentials on the resulting page, and then received an error message. Which of the following attack types best describes this scenario?

A) Brand impersonation
B) Pretexting
C) Typosquatting
D) Phishing

<details><summary>Answer</summary>

**D) Phishing**

Phishing involves deceptive emails that trick users into revealing credentials or clicking malicious links. The scenario describes a classic credential-harvesting phishing page — a fake site that captures credentials when the user "logs in" and then displays an error to avoid suspicion. Brand impersonation may be a component, but the overarching attack type is phishing.

</details>

---

**Q43.** Which is the strongest indicator that a pass-the-hash attack is being attempted?

A) Kerberos listed as the Authentication Package in event logs
B) Multiple logon attempts with different passwords
C) NTLM listed as Authentication Package and/or NtLmSSP as Logon Process
D) Regular user privilege logon activity

<details><summary>Answer</summary>

**C) NTLM as Authentication Package and/or NtLmSSP as Logon Process**

Pass-the-hash attacks exploit NTLM authentication by capturing the NTLM hash from one system and replaying it to authenticate to another without knowing the plaintext password. Event logs that show NTLM (rather than Kerberos) as the Authentication Package, combined with unusual lateral movement, indicate a pass-the-hash attack. Kerberos is the default for domain environments and is not vulnerable to this specific technique.

</details>

---

**Q44.** What distinguishes a password spraying attack from a traditional brute force attack?

A) No automated program is used in spraying
B) It attempts each password once across many accounts
C) It bypasses lockout policies by exceeding time limits
D) It avoids generating Event ID 4625

<details><summary>Answer</summary>

**B) It attempts each password once across many accounts**

Password spraying avoids account lockout by trying one or a few common passwords (e.g., "Welcome1", "Spring2024!") against a large number of accounts before moving to the next password. Traditional brute force attacks try many passwords against a single account, quickly triggering lockout. Spraying stays below lockout thresholds by spreading attempts across accounts.

</details>

---

**Q45.** A company is expanding its threat surface program and allowing individuals to security test the company's internet-facing application. The company will compensate researchers based on the vulnerabilities discovered. Which of the following best describes the program the company is setting up?

A) Open-source intelligence
B) Penetration testing
C) Red team
D) Bug bounty

<details><summary>Answer</summary>

**D) Bug bounty**

A bug bounty program is a crowdsourced vulnerability disclosure program where external researchers are invited and financially rewarded for finding and responsibly reporting security vulnerabilities. Penetration testing is a contracted, scoped engagement; a red team performs adversarial simulation; open-source intelligence (OSINT) involves gathering publicly available information.

</details>

---

**Q46.** Which characteristic does NOT describe vulnerability scanning (as opposed to penetration testing)?

A) Occasionally gains unauthorized access and exploits vulnerabilities
B) Purpose is reducing the attack surface
C) Objective is identifying risks
D) Typically performed by internal security personnel

<details><summary>Answer</summary>

**A) Occasionally gains unauthorized access and exploits vulnerabilities**

Gaining unauthorized access and actively exploiting vulnerabilities is characteristic of penetration testing, not vulnerability scanning. Vulnerability scans are passive assessments that identify potential weaknesses without exploiting them. They are typically run by internal teams, are intended to reduce attack surface, and identify risk — all of which do apply to vulnerability scanning.

</details>

---

**Q47.** An IT manager is increasing the security capabilities of an organization after a data classification initiative determined that sensitive data could be exfiltrated from the environment. Which of the following solutions would mitigate the risk?

A) XDR
B) SPF
C) DLP
D) DMARC

<details><summary>Answer</summary>

**C) DLP**

Data Loss Prevention (DLP) solutions identify, monitor, and protect sensitive data to prevent unauthorized access, use, or exfiltration. DLP enforces policies on data in use, in motion, and at rest. XDR (Extended Detection and Response) focuses on threat detection; SPF and DMARC are email authentication protocols that prevent domain spoofing and phishing — not data exfiltration.

</details>

---

**Q48.** A security administrator is deploying a DLP solution to prevent the exfiltration of sensitive customer data. Which of the following should the administrator do FIRST?

A) Block access to cloud storage websites
B) Create a rule to block outgoing email attachments
C) Apply classifications to the data
D) Remove all user permissions from shares on the file server

<details><summary>Answer</summary>

**C) Apply classifications to the data**

Data classification must come first. Before DLP policies can be effectively applied, the organization must understand which data is sensitive and requires protection. Without classification, DLP rules are either too broad (blocking legitimate work) or miss sensitive data entirely. Once data is classified, targeted DLP policies can be created that are proportional to the sensitivity level.

</details>

---
