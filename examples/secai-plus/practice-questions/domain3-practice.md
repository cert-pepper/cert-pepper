# Domain 3 Practice Questions — AI-assisted Security

---

**Q1.** A SOC deploys a system that establishes normal network traffic patterns for each user and device, then alerts when behavior deviates significantly from that baseline. Which AI-enabled security use case does this represent?

A) Signature matching
B) Anomaly detection
C) Automated penetration testing
D) Pattern recognition in threat intelligence

<details><summary>Answer</summary>

**B) Anomaly detection**

Anomaly detection builds a statistical model of normal behavior and alerts on deviations — it does not rely on known attack signatures. This is a core AI-assisted security use case. Signature matching identifies known attack patterns by comparing to a database. Pattern recognition in threat intelligence extracts indicators from large datasets rather than monitoring live traffic baselines.

</details>

---

**Q2.** A developer uses an AI assistant integrated directly into their code editor to identify potential SQL injection vulnerabilities as they write code. What type of AI-enabled tool is being used?

A) Browser plug-in
B) CLI plug-in
C) IDE plug-in
D) MCP server

<details><summary>Answer</summary>

**C) IDE plug-in**

An IDE plug-in integrates AI capabilities directly into the developer's coding environment, enabling real-time vulnerability analysis, code quality checks, and linting without leaving the editor. Browser plug-ins augment web browser functionality. CLI plug-ins add AI capabilities to terminal workflows. MCP servers expose tools and resources to AI agents via the Model Context Protocol.

</details>

---

**Q3.** A threat actor uses an AI model to automatically generate hundreds of targeted spear-phishing emails, each personalized based on scraped social media profiles. Which AI-enhanced attack capability does this represent?

A) Adversarial network
B) Social engineering automation
C) Obfuscation
D) Automated data correlation

<details><summary>Answer</summary>

**B) Social engineering automation**

AI enables threat actors to automate and scale social engineering attacks — personalizing phishing content at scale using scraped data. Adversarial networks (GANs) generate synthetic data like deepfakes. Obfuscation uses AI to hide malicious code. Automated data correlation aggregates data from multiple sources to identify targets or relationships.

</details>

---

**Q4.** An organization implements an AI-driven system that automatically creates and routes incident tickets, enriches them with threat intelligence, and assigns them to the correct analyst team. Which AI security automation capability does this describe?

A) Document synthesis and summarization
B) Change management with AI-assisted approvals
C) Incident response ticket management
D) AI agent orchestration via CI/CD

<details><summary>Answer</summary>

**C) Incident response ticket management**

AI-driven incident response ticket management automates the creation, enrichment, routing, and prioritization of security incidents — reducing mean time to respond. Document synthesis and summarization condenses long reports. Change management with AI-assisted approvals applies to deployment pipelines. CI/CD AI agents focus on code and model deployment, not incident management.

</details>

---

**Q5.** A deepfake video of a company CEO appears to authorize a fraudulent wire transfer. Which AI-generated content threat does this represent?

A) Obfuscation
B) Disinformation
C) Impersonation
D) Misinformation

<details><summary>Answer</summary>

**C) Impersonation**

Impersonation uses AI-generated content (deepfake audio/video) to convincingly portray a specific real person to deceive targets into taking actions — such as authorizing a wire transfer. Misinformation is false content spread without malicious intent. Disinformation is false content spread intentionally to deceive a broader audience rather than impersonate a specific individual.

</details>

---

**Q6.** A security team deploys a Model Context Protocol server to give their AI assistant access to internal vulnerability scanners, threat feeds, and ticketing systems. A security architect warns that improper configuration could grant the AI assistant more access than intended. What risk does this represent?

A) Model inversion
B) Prompt injection via training data
C) Excessive permissions granted to an MCP server
D) Hallucination amplification

<details><summary>Answer</summary>

**C) Excessive permissions granted to an MCP server**

MCP servers expose tools and resources to AI agents, acting as a bridge between the AI and backend systems. If an MCP server is configured with overly broad permissions — such as write access to production systems or access to unrelated data stores — the AI agent can take unintended or dangerous actions. This is the primary security risk of MCP deployments. Model inversion and hallucination are separate AI risk categories.

</details>

---

**Q7.** A red team uses an AI-powered platform that automatically maps an application's attack surface, generates exploit payloads for discovered vulnerabilities, and attempts to chain them into multi-step attack paths. Which AI-enabled use case is this?

A) Threat modeling
B) Fraud detection
C) Automated penetration testing
D) Anomaly detection

<details><summary>Answer</summary>

**C) Automated penetration testing**

Automated penetration testing uses AI to scan targets, generate exploit payloads, and simulate attack chains — augmenting or replacing manual red team steps. Threat modeling identifies potential threats at the design stage rather than actively exploiting them. Fraud detection analyzes transactions for anomalies. Anomaly detection monitors baselines rather than actively probing systems.

</details>

---

**Q8.** A security architect uploads an application's data flow diagram and component inventory to an AI tool. The tool automatically identifies trust boundaries, enumerates potential threats using STRIDE, and generates a prioritized list of mitigations. What AI-enabled use case is this?

A) Vulnerability analysis
B) Signature matching
C) Threat modeling
D) Incident management

<details><summary>Answer</summary>

**C) Threat modeling**

AI-assisted threat modeling analyzes architecture artifacts to automatically enumerate threats, map attack paths, and suggest mitigations — tasks that traditionally required hours of manual effort by experienced security architects. Vulnerability analysis identifies flaws in existing code or configurations. Signature matching compares traffic or files against known-bad patterns. Incident management responds to active events.

</details>

---

**Q9.** A financial institution's AI system assigns a risk score to each card transaction in under 50 milliseconds by comparing it against historical spending patterns, geolocation data, and device fingerprints. Transactions above the threshold are declined automatically. What AI-enabled security use case is this?

A) Anomaly detection
B) Fraud detection
C) Signature matching
D) Threat modeling

<details><summary>Answer</summary>

**B) Fraud detection**

Fraud detection uses AI to score individual transactions in real time against behavioral patterns and contextual signals, enabling automated blocking before a transaction completes. While related to anomaly detection, fraud detection specifically applies to financial transaction integrity with business-impact decisions. Signature matching relies on known-bad patterns rather than statistical scoring. Threat modeling applies to system design, not live transactions.

</details>

---

**Q10.** A DevSecOps team configures their CI/CD pipeline so that every pull request is automatically scanned by an AI assistant that identifies hardcoded credentials, insecure deserialization patterns, and known-vulnerable function calls before the code can be merged. Which AI-enabled capability is this?

A) SCA
B) SAST via AI code scanning
C) Model testing
D) Automated deployment

<details><summary>Answer</summary>

**B) SAST via AI code scanning**

AI-augmented static analysis examines source code in pull requests for security issues before merge — this is code scanning applied at the CI/CD gate. SCA specifically examines third-party dependencies for known CVEs, not first-party code patterns. Model testing validates ML model performance after updates. Automated deployment handles release mechanics.

</details>

---

**Q11.** After integrating a new open-source library, a CI/CD pipeline stage automatically queries a vulnerability database to check whether any of the library's dependencies have known CVEs, then blocks the build if critical findings are present. What AI-augmented DevSecOps capability does this represent?

A) SAST
B) DAST
C) SCA
D) Regression testing

<details><summary>Answer</summary>

**C) SCA**

SCA inventories third-party and open-source dependencies and checks them against vulnerability databases like the NVD. Blocking builds on critical CVE findings is a standard SCA enforcement pattern in CI/CD pipelines. SAST analyzes first-party source code. DAST tests running applications. Regression testing ensures existing functionality still works after changes.

</details>

---

**Q12.** After a developer updates the feature engineering code for a fraud detection model, an automated pipeline stage re-runs the model against a held-out validation dataset and compares accuracy, precision, and recall to pre-update baselines. If any metric drops beyond a threshold, the pipeline fails. What CI/CD practice is this?

A) SCA
B) Automated deployment
C) Code scanning
D) Model regression testing

<details><summary>Answer</summary>

**D) Model regression testing**

Model regression testing validates that ML model performance metrics remain within acceptable bounds after code or data changes — preventing silent degradation of security models in production. SCA examines dependencies for CVEs. Code scanning checks source code for vulnerabilities. Automated deployment manages release mechanics, not model quality.

</details>

---

**Q13.** While browsing a website, a user's browser extension analyzes the page in real time and highlights several indicators: a mismatched domain in the URL, a login form requesting unusual fields, and a certificate issued just 24 hours ago. What type of AI-enabled tool is this?

A) CLI plug-in
B) IDE plug-in
C) MCP server
D) Browser plug-in

<details><summary>Answer</summary>

**D) Browser plug-in**

A browser plug-in integrates AI capabilities directly into the web browsing experience, enabling real-time analysis of visited pages for phishing indicators such as domain anomalies, suspicious form fields, and certificate age. IDE plug-ins operate within development environments. CLI plug-ins add capabilities to terminal workflows. MCP servers provide tool and resource access to AI agents.

</details>

---

**Q14.** A security engineer runs a terminal command that pipes a target IP range to an AI-assisted tool. The tool queries threat intelligence APIs, identifies exposed services, and returns a prioritized list of findings — all from the command line without opening a graphical interface. What type of AI-enabled tool is this?

A) Browser plug-in
B) Chatbot
C) CLI plug-in
D) IDE plug-in

<details><summary>Answer</summary>

**C) CLI plug-in**

A CLI plug-in extends terminal workflows with AI capabilities, enabling security engineers to perform vulnerability scans, threat lookups, and analysis without leaving the command line. Browser plug-ins operate within web browsers. Chatbots require interactive natural-language exchanges. IDE plug-ins integrate into development environments.

</details>

---

**Q15.** A SIEM generates 50,000 alerts per day. A SOC team deploys an AI system that reads each alert batch, groups correlated events, and produces a one-paragraph plain-language summary of the top five incident candidates for the on-call analyst each morning. What AI-enabled use case is this?

A) Anomaly detection
B) Signature matching
C) Log summarization
D) Incident response ticket management

<details><summary>Answer</summary>

**C) Log summarization**

AI-assisted log summarization condenses high-volume SIEM alert output into human-readable summaries, reducing analyst cognitive load and accelerating triage. Anomaly detection identifies deviations from baselines but does not produce narrative summaries. Signature matching compares events against known-bad patterns. Incident response ticket management handles routing and enrichment of already-identified incidents.

</details>

---

**Q16.** A state-sponsored group releases AI-generated news articles claiming a major bank has been hacked, causing a brief stock drop. Security researchers confirm the articles are fabricated and distributed by coordinated accounts. Which AI-generated content threat does this represent?

A) Impersonation
B) Misinformation
C) Disinformation
D) Adversarial example

<details><summary>Answer</summary>

**C) Disinformation**

Disinformation is deliberately fabricated or manipulated content spread with the intent to deceive — the coordinated campaign to manipulate markets distinguishes this as disinformation. Misinformation is false content spread without malicious intent (e.g., a user shares an inaccurate article not knowing it is false). Impersonation targets a specific individual. Adversarial examples are specially crafted inputs that fool ML models, not content campaigns.

</details>

---

**Q17.** A malware author uses an LLM-based tool to automatically rewrite the same malicious payload in dozens of functional variants, each with different variable names, control flow structures, and encoding schemes, to defeat signature-based detection. Which AI-enhanced attack capability does this represent?

A) Adversarial network
B) Automated data correlation
C) AI-generated malware obfuscation
D) Reconnaissance

<details><summary>Answer</summary>

**C) AI-generated malware obfuscation**

AI-powered obfuscation automates the generation of polymorphic or metamorphic malware variants that retain malicious functionality while evading signature-based detection. Adversarial networks (GANs) generate synthetic media or poisoned training data. Automated data correlation aggregates OSINT for targeting. Reconnaissance maps the attack surface before exploitation.

</details>

---

**Q18.** Before launching an attack, a threat actor uses an LLM to aggregate information from LinkedIn, job postings, GitHub repositories, and leaked credentials to build a detailed map of a target organization's technology stack, key personnel, and potential entry points. Which AI-enhanced capability is this?

A) Social engineering
B) AI-assisted reconnaissance
C) Automated attack generation
D) Adversarial network

<details><summary>Answer</summary>

**B) AI-assisted reconnaissance**

AI-assisted reconnaissance uses LLMs and automation to aggregate and correlate OSINT from disparate public sources — reducing the time needed to map an organization's attack surface compared to manual methods. Social engineering uses gathered information to deceive people but is a separate phase. Automated attack generation creates exploits after the target is identified. Adversarial networks produce synthetic training data.

</details>

---

**Q19.** A threat actor deploys an AI-coordinated botnet that analyzes a target's network defenses in real time and dynamically shifts the volumetric attack vector from UDP flood to HTTP flood when upstream scrubbing mitigation is detected. Which AI-enhanced attack does this represent?

A) Spear-phishing automation
B) Adversarial example generation
C) AI-coordinated DDoS
D) Automated data correlation

<details><summary>Answer</summary>

**C) AI-coordinated DDoS**

AI-coordinated DDoS attacks use machine learning to adapt the attack pattern — switching protocols, rates, or vectors in response to defensive countermeasures — making them significantly harder to mitigate with static rate-limiting or scrubbing rules. Spear-phishing automation targets individuals. Adversarial examples fool ML classifiers. Automated data correlation aggregates information for targeting rather than executing volumetric attacks.

</details>

---

**Q20.** A threat actor trains a generative adversarial network to produce thousands of synthetic network traffic samples labeled as benign, then injects these samples into a vendor's public threat intelligence sharing platform. The goal is to corrupt the training data used by downstream security ML models. Which AI-enhanced attack does this represent?

A) Obfuscation
B) Training data poisoning via adversarial networks
C) Automated reconnaissance
D) Model inversion

<details><summary>Answer</summary>

**B) Training data poisoning via adversarial networks**

Adversarial networks (GANs) can generate highly realistic synthetic data to poison shared datasets — causing downstream ML models trained on that data to misclassify malicious traffic as benign. Obfuscation modifies malware to evade detection. Automated reconnaissance gathers information before an attack. Model inversion reconstructs training data from model outputs; it does not inject data.

</details>

---

**Q21.** An automated tool systematically sends thousands of crafted HTTP requests to a web application, varying parameters, headers, and payloads to identify injection points, broken access controls, and authentication bypasses without human direction. Which AI-enhanced attack capability does this represent?

A) Social engineering automation
B) AI-generated malware obfuscation
C) Automated attack vector discovery
D) Adversarial network

<details><summary>Answer</summary>

**C) Automated attack vector discovery**

Automated attack vector discovery uses AI to systematically probe applications for exploitable weaknesses — going beyond simple fuzzing by learning from each response to prioritize subsequent probes. Social engineering automation targets people. Malware obfuscation generates evasive payloads for use after access is gained. Adversarial networks produce synthetic training data rather than probing live systems.

</details>

---

**Q22.** A threat actor uses an AI tool to encode shellcode as a series of innocuous-looking arithmetic operations, then wraps it in a legitimate-appearing document macro. Each generated variant passes through multiple antivirus engines cleanly. Which AI-enhanced attack technique does this describe?

A) Reconnaissance
B) AI-assisted DDoS
C) Training data poisoning
D) AI-generated payload obfuscation

<details><summary>Answer</summary>

**D) AI-generated payload obfuscation**

AI-generated payload obfuscation uses machine learning to morph or encode shellcode into forms that evade static and heuristic antivirus detection while preserving execution behavior. Reconnaissance maps targets before exploitation. AI-assisted DDoS is a volumetric attack technique. Training data poisoning corrupts ML model datasets rather than modifying malicious code.

</details>

---

**Q23.** A SOC analyst with no programming background uses a drag-and-drop security platform to build a workflow that automatically blocks an IP address in the firewall, disables the associated Active Directory account, and creates a ticket — all triggered by a SIEM alert. Which AI automation capability does this represent?

A) AI agent orchestration
B) Low-code/no-code security automation
C) CI/CD model testing
D) Document synthesis

<details><summary>Answer</summary>

**B) Low-code/no-code security automation**

Low-code/no-code platforms allow security practitioners without programming skills to build automated response workflows using visual interfaces. This democratizes automation by removing the scripting barrier. AI agent orchestration involves autonomous AI agents executing multi-step tasks. CI/CD model testing validates ML models in deployment pipelines. Document synthesis condenses reports into summaries.

</details>

---

**Q24.** Before approving a change request to update a critical authentication service, an AI system analyzes the change's scope, the service's historical incident rate, current threat intelligence, and deployment timing to produce a risk score and recommended approval/defer decision. Which AI automation capability does this represent?

A) Incident response ticket management
B) Automated deployment
C) AI-assisted change management approval
D) Document synthesis

<details><summary>Answer</summary>

**C) AI-assisted change management approval**

AI-assisted change management uses machine learning to evaluate change requests against risk signals — reducing the manual overhead of change advisory board reviews while improving consistency. Incident response ticket management handles active security events. Automated deployment executes approved changes. Document synthesis condenses informational content rather than making risk decisions.

</details>

---

**Q25.** Minutes after a new application version is deployed, AI-driven monitoring detects a spike in error rates and a drop in successful authentication. The system rolls back to the previous version and files an incident ticket before any analyst intervenes. Which AI automation capability does this represent?

A) Low-code/no-code scripting
B) Automated deployment and rollback
C) CI/CD code scanning
D) AI-assisted change management approval

<details><summary>Answer</summary>

**B) Automated deployment and rollback**

AI-driven automated deployment and rollback uses monitoring signals to trigger version rollbacks without human intervention — minimizing the blast radius of a bad release. Low-code/no-code scripting builds workflows visually but does not drive autonomous runtime decisions. CI/CD code scanning runs at build time, not post-deployment. Change management approval occurs before deployment.

</details>

---

**Q26.** A threat intelligence analyst receives 40 vendor advisories, incident reports, and vulnerability disclosures each week. An AI system reads each document, extracts key indicators, timelines, and actor attributions, and produces a two-page briefing per report. Which AI automation capability does this represent?

A) Incident response ticket management
B) Anomaly detection
C) Document synthesis and summarization
D) Automated attack vector discovery

<details><summary>Answer</summary>

**C) Document synthesis and summarization**

Document synthesis and summarization uses AI to distill large volumes of threat intelligence text into concise, structured briefings — reducing the time analysts spend on reading and extraction. Incident response ticket management automates event routing. Anomaly detection monitors behavioral baselines. Automated attack vector discovery probes live systems for weaknesses.

</details>

---

**Q27.** After retraining a network intrusion detection model on six months of new traffic data, a team runs the updated model against a fixed benchmark dataset containing labeled attack and benign samples. They compare the new model's false positive rate and detection rate against the previous version before promoting it to production. Which AI automation practice does this represent?

A) SCA
B) Code scanning
C) Low-code workflow automation
D) AI model regression testing

<details><summary>Answer</summary>

**D) AI model regression testing**

AI model regression testing validates that a retrained or updated model maintains acceptable performance on a standardized benchmark before production promotion — ensuring security posture does not degrade after model updates. SCA checks third-party dependency vulnerabilities. Code scanning analyzes source code for security flaws. Low-code workflow automation builds operational runbooks without programming.

</details>

---
