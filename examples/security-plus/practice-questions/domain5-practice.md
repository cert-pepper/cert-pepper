**Q1.** A risk manager calculates that a flood could destroy a data center worth $5,000,000 and cause a 40% loss of the center's value. Floods are expected to occur once every 10 years in that region. What is the Annualized Loss Expectancy (ALE)?

A) $200,000
B) $2,000,000
C) $500,000
D) $5,000,000

<details><summary>Answer</summary>

**A) $200,000**

ALE (Annualized Loss Expectancy) = SLE × ARO.
- SLE (Single Loss Expectancy) = Asset Value × Exposure Factor = $5,000,000 × 0.40 = $2,000,000
- ARO (Annualized Rate of Occurrence) = 1 occurrence per 10 years = 0.10
- ALE = $2,000,000 × 0.10 = **$200,000**

This means the organization should expect an average annual loss of $200,000 from floods and should spend no more than $200,000 per year on flood controls to be cost-effective.

</details>

---

**Q2.** A company's asset is valued at $1,000,000. A risk assessment determines that a specific threat would destroy 25% of the asset's value if it occurred. What is the Single Loss Expectancy (SLE)?

A) $25,000
B) $250,000
C) $1,000,000
D) $750,000

<details><summary>Answer</summary>

**B) $250,000**

SLE (Single Loss Expectancy) = Asset Value × Exposure Factor (EF) = $1,000,000 × 0.25 = **$250,000**

The EF is the percentage of the asset's value that would be lost in a single incident. SLE is the monetary loss from one occurrence.

</details>

---

**Q3.** An organization experiences ransomware attacks at a rate of approximately 3 times per year. Each attack causes an average loss of $150,000 including recovery costs, downtime, and reputational damage. What is the ALE for ransomware?

A) $50,000
B) $150,000
C) $450,000
D) $3,000,000

<details><summary>Answer</summary>

**C) $450,000**

ALE (Annualized Loss Expectancy) = SLE (Single Loss Expectancy) × ARO (Annualized Rate of Occurrence) = $150,000 × 3 = **$450,000**

With an ALE of $450,000, the organization can justify spending up to $450,000 per year on ransomware prevention and response capabilities.

</details>

---

**Q4.** A healthcare organization is breached and patient records are exposed. The security team is determining which regulatory compliance requirement applies. Which regulation specifically governs the protection of patient health information (PHI) in the United States?

A) PCI-DSS
B) GDPR
C) SOX
D) HIPAA

<details><summary>Answer</summary>

**D) HIPAA**

HIPAA (Health Insurance Portability and Accountability Act) is the U.S. law that governs the protection of Protected Health Information (PHI). It applies to healthcare providers, health plans, and healthcare clearinghouses (covered entities) and their business associates. PCI-DSS (Payment Card Industry Data Security Standard) governs payment card data; GDPR (General Data Protection Regulation) governs EU personal data; SOX (Sarbanes-Oxley Act) governs financial reporting for public companies.

</details>

---

**Q5.** A European customer's personal data is exposed in a breach at a U.S.-based company. Which regulation requires the company to notify the supervisory authority within 72 hours of becoming aware of the breach?

A) HIPAA
B) FISMA
C) GDPR
D) PCI-DSS

<details><summary>Answer</summary>

**C) GDPR**

GDPR (General Data Protection Regulation) requires that controllers notify their supervisory authority within 72 hours of discovering a personal data breach. GDPR applies to any organization that processes personal data of EU/EEA residents, regardless of where the organization is located. HIPAA (Health Insurance Portability and Accountability Act) requires notification within 60 days; PCI-DSS (Payment Card Industry Data Security Standard) has its own incident notification requirements.

</details>

---

**Q6.** A retail company that processes credit card payments must comply with a security standard requiring network segmentation, encryption of cardholder data, and regular vulnerability assessments. Which standard applies?

A) HIPAA
B) SOX
C) PCI-DSS
D) NIST SP 800-53

<details><summary>Answer</summary>

**C) PCI-DSS**

PCI-DSS (Payment Card Industry Data Security Standard) is the security standard for any organization that stores, processes, or transmits payment card data. Its 12 requirements include network segmentation, encryption of cardholder data in transit and at rest, and regular vulnerability assessments and penetration testing.

</details>

---

**Q7.** A CISO wants to implement a cybersecurity program using a framework that organizes security activities into five functions: Identify, Protect, Detect, Respond, and Recover. Which framework is being used?

A) NIST SP 800-53
B) NIST CSF
C) ISO 27001
D) CIS Controls

<details><summary>Answer</summary>

**B) NIST CSF**

The NIST CSF (Cybersecurity Framework) organizes security activities into five core functions: Identify, Protect, Detect, Respond, and Recover. It is widely adopted as a voluntary framework for improving cybersecurity risk management. NIST SP 800-53 provides a detailed control catalog for federal systems; ISO 27001 is an international ISMS standard; CIS Controls is a prioritized list of security best practices.

</details>

---

**Q8.** A federal government agency is required to implement a formal risk management process that categorizes information systems, selects security controls, implements and assesses those controls, authorizes systems, and monitors them continuously. Which framework mandates this?

A) NIST CSF
B) ISO 27001
C) NIST RMF
D) CIS Controls

<details><summary>Answer</summary>

**C) NIST RMF**

The NIST RMF (Risk Management Framework) (SP 800-37) defines a 6-step process for federal information systems: Categorize, Select, Implement, Assess, Authorize, and Monitor. FISMA (Federal Information Security Management Act) requires federal agencies to follow the RMF. It is more prescriptive than the CSF (Cybersecurity Framework), which is voluntary and framework-based.

</details>

---

**Q9.** An organization decides to purchase a cyber insurance policy to cover financial losses from potential data breaches. Which risk management strategy is this?

A) Risk avoidance
B) Risk acceptance
C) Risk transference
D) Risk mitigation

<details><summary>Answer</summary>

**C) Risk transference**

Risk transference shifts the financial burden of a risk to a third party — in this case, an insurance provider. Cyber insurance does not eliminate the risk, but the financial impact of a breach is transferred to the insurer. Other transference methods include contracts requiring vendors to indemnify the organization. Risk avoidance eliminates the activity; risk acceptance acknowledges and lives with the risk; risk mitigation reduces likelihood or impact.

</details>

---

**Q10.** An organization evaluates a legacy application vulnerability and determines the cost to fix it is $500,000, but the maximum possible loss from exploitation is only $10,000. Management decides not to remediate. Which risk strategy is this?

A) Risk avoidance
B) Risk transference
C) Risk mitigation
D) Risk acceptance

<details><summary>Answer</summary>

**D) Risk acceptance**

Risk acceptance (also called risk tolerance) is acknowledging that a risk exists and consciously choosing not to take action, usually because the cost of mitigation exceeds the potential loss. This must be a documented, informed decision. The organization accepts the $10,000 potential loss rather than spend $500,000 to fix it — a rational business decision.

</details>

---

**Q11.** An organization stops using an unencrypted FTP server for file transfers entirely and switches to SFTP, eliminating the risk of credential interception. Which risk management strategy is this?

A) Risk acceptance
B) Risk transference
C) Risk avoidance
D) Risk mitigation

<details><summary>Answer</summary>

**C) Risk avoidance**

Risk avoidance eliminates the risk by eliminating the activity that creates it. By stopping the use of the insecure FTP protocol entirely, the organization removes the risk rather than trying to reduce or transfer it. This is the most complete risk response but is often impractical for core business functions.

</details>

---

**Q12.** A security manager writes a formal document identifying a $50,000 unmitigated risk in the organization's remote access infrastructure, noting that the risk has been reviewed by the CISO and accepted due to budget constraints. This document is called what?

A) Risk transfer agreement
B) Risk register entry with an exception/acceptance
C) Business impact analysis
D) Vulnerability assessment report

<details><summary>Answer</summary>

**B) Risk register entry with an exception/acceptance**

A risk register is the central repository documenting identified risks, their likelihood, impact, and management response. When a risk is accepted (not mitigated), the decision must be formally documented with CISO or executive sign-off. This creates an audit trail and ensures the acceptance is a deliberate, informed decision rather than neglect.

</details>

---

**Q13.** A business impact analysis (BIA) for an e-commerce company determines that if the payment processing system goes down, the company loses $50,000 per hour. The company sets a maximum acceptable downtime of 4 hours before business viability is threatened. What metric does the 4-hour maximum represent?

A) RPO
B) RTO
C) MTBF
D) MTTR

<details><summary>Answer</summary>

**B) RTO**

RTO (Recovery Time Objective) is the maximum acceptable time to restore a system or service after a disruption. The 4-hour RTO drives the disaster recovery design — backups, failover systems, and recovery procedures must enable restoration within 4 hours. RPO (Recovery Point Objective) is about data loss (how old can the recovered data be); MTTR (Mean Time to Recover) is the average actual recovery time; MTBF (Mean Time Between Failures) measures reliability.

</details>

---

**Q14.** The same e-commerce company's BIA also determines that recovering the payment database from backups older than 1 hour would require manual reconciliation of all transactions, which is operationally unacceptable. What does the 1-hour maximum data loss represent?

A) RTO
B) MTBF
C) RPO
D) SLE

<details><summary>Answer</summary>

**C) RPO**

RPO (Recovery Point Objective) is the maximum acceptable amount of data loss measured in time — how old the restored data can be. An RPO of 1 hour means backups must be taken at least every hour so that recovery restores data no more than 1 hour old. This drives backup frequency, replication strategies, and storage design.

</details>

---

**Q15.** An organization's disaster recovery plan requires all critical systems to be restored within 2 hours (RTO = 2 hours) and data to be no more than 15 minutes old upon recovery (RPO = 15 minutes). Which backup/replication strategy BEST meets these requirements?

A) Weekly full backups with daily incrementals
B) Daily full backups to tape stored offsite
C) Continuous synchronous replication to a hot standby site
D) Monthly full backups with transaction log shipping

<details><summary>Answer</summary>

**C) Continuous synchronous replication to a hot standby site**

A 15-minute RPO (Recovery Point Objective) requires near-real-time replication (synchronous replication or very frequent incremental backups). A 2-hour RTO (Recovery Time Objective) requires a hot standby that can be activated rapidly. Weekly tape backups cannot achieve a 15-minute RPO. Synchronous replication keeps the standby in a near-identical state continuously, and hot standby activation typically takes minutes.

</details>

---

**Q16.** A risk assessment identifies the role responsible for determining how data should be classified and who should have access to it. Which role is this?

A) Data custodian
B) Data processor
C) Data owner
D) Data steward

<details><summary>Answer</summary>

**C) Data owner**

The data owner is typically a business executive or manager responsible for a data set. They decide the data's classification level and who is authorized to access it. The data custodian (often IT) implements the technical controls the owner specifies; the data processor (GDPR (General Data Protection Regulation) context) processes data on behalf of the controller; the data steward manages data quality and governance day-to-day.

</details>

---

**Q17.** Under GDPR, which role collects and processes personal data and determines the purposes and means of processing?

A) Data processor
B) Data custodian
C) Data subject
D) Data controller

<details><summary>Answer</summary>

**D) Data controller**

Under GDPR (General Data Protection Regulation), the data controller is the entity that determines why (purpose) and how (means) personal data is processed. A data processor processes data on behalf of the controller (e.g., a cloud vendor). The data subject is the individual whose data is being processed. This distinction is important because controllers have direct accountability to data subjects under GDPR.

</details>

---

**Q18.** A vendor provides cloud-based payroll services to an organization. The vendor processes employee personal data only according to the organization's instructions. Under GDPR, how is the vendor classified?

A) Data controller
B) Data custodian
C) Data processor
D) Data owner

<details><summary>Answer</summary>

**C) Data processor**

Under GDPR (General Data Protection Regulation), an entity that processes personal data on behalf of and under the instructions of another entity is a data processor. The organization (which determines the purpose of processing) is the data controller. Cloud service providers, payroll processors, and marketing platforms typically act as processors.

</details>

---

**Q19.** An organization conducts a thorough security review of a new SaaS vendor before signing a contract, examining the vendor's SOC 2 Type II report, their incident response history, and their data handling practices. Which risk management activity is this?

A) Business impact analysis
B) Third-party risk management / vendor risk assessment
C) Vulnerability assessment
D) Change management review

<details><summary>Answer</summary>

**B) Third-party risk management / vendor risk assessment**

Third-party risk management assesses the security posture of vendors and partners before granting them access to your systems or data. SOC 2 Type II reports demonstrate that a vendor's security controls have been independently audited over a period of time. Right-to-audit clauses in contracts allow organizations to conduct their own vendor audits.

</details>

---

**Q20.** A contract between two organizations includes a clause requiring the vendor to permit the organization to audit the vendor's security controls and access its facilities for inspection at any time with reasonable notice. What type of contract provision is this?

A) NDA
B) SLA
C) Right-to-audit clause
D) MOU

<details><summary>Answer</summary>

**C) Right-to-audit clause**

A right-to-audit clause contractually grants the organization the ability to assess the vendor's security posture through audits, inspections, and document reviews. This is a key third-party risk management tool, especially for vendors handling sensitive data. Without it, the organization must rely entirely on vendor-provided reports.

</details>

---

**Q21.** An organization publishes a document that formally establishes the data categories the organization handles (Public, Internal, Confidential, Restricted) and the required handling procedures for each category. What type of document is this?

A) Security awareness training policy
B) AUP
C) Data classification policy
D) Business continuity plan

<details><summary>Answer</summary>

**C) Data classification policy**

A data classification policy defines the categories or tiers of data sensitivity and the required handling, storage, transmission, and disposal procedures for each category. It is foundational to implementing appropriate security controls — you cannot protect data appropriately without knowing its sensitivity level.

</details>

---

**Q22.** A financial services firm's security team conducts mandatory annual training that simulates phishing emails to test whether employees click on malicious links and report the results to management. Which security program element does this represent?

A) Tabletop exercise
B) Security awareness training with phishing simulation
C) Red team assessment
D) Vulnerability management

<details><summary>Answer</summary>

**B) Security awareness training with phishing simulation**

Security awareness training combined with phishing simulations tests and reinforces employee vigilance against social engineering. Simulation results provide measurable metrics (click rate, report rate) that demonstrate program effectiveness and identify employees who need additional training. This is a key element of a Security Program Management and Oversight program.

</details>

---

**Q23.** A penetration test reveals that an organization's web application contains a SQL injection vulnerability. However, the organization decides not to patch it because fixing it would require a complete application rewrite that isn't planned for 18 months. Management formally documents this decision. Which term describes the unmitigated vulnerability during this 18-month period?

A) Residual risk
B) Inherent risk
C) Risk avoidance
D) Accepted risk with residual exposure

<details><summary>Answer</summary>

**A) Residual risk**

Residual risk is the risk that remains after controls have been applied (or in this case, after a conscious decision not to apply all available controls). It is the risk the organization is left carrying. Inherent risk is the risk before any controls are applied. Formally documenting the acceptance of residual risk is required for compliance and good governance.

</details>

---

**Q24.** An organization stores sensitive employee data. A privacy officer conducts a formal evaluation to understand how the data is collected, processed, and stored, and identifies the privacy risks associated with a new HR system before deployment. What is this process called?

A) BIA
B) PIA
C) Risk register review
D) DLP audit

<details><summary>Answer</summary>

**B) PIA**

A PIA (Privacy Impact Assessment) systematically evaluates how a project, system, or process handles personal data, identifying privacy risks and ensuring compliance with privacy laws (GDPR (General Data Protection Regulation), HIPAA (Health Insurance Portability and Accountability Act), CCPA (California Consumer Privacy Act)). PIAs should be conducted before deploying new systems that collect or process personal data. They are required by several regulations including GDPR (as a DPIA (Data Protection Impact Assessment)) for high-risk processing.

</details>

---

**Q25.** A security program metric shows that 94% of employees completed mandatory security awareness training this quarter, up from 78% last quarter. The CISO presents this to the board. Which type of security metric is this?

A) Threat intelligence indicator
B) Vulnerability management KPI
C) KPI for the security awareness program
D) Risk register update

<details><summary>Answer</summary>

**C) KPI for the security awareness program**

Completion rates for security awareness training are KPIs (Key Performance Indicators) that measure the effectiveness and reach of the security program. KPIs quantify progress toward security objectives and are used to demonstrate program value to leadership and the board. Other awareness training KPIs include phishing simulation click rates and time-to-report metrics.

</details>

---

**Q26.** An organization's agreement with a cloud service provider guarantees 99.9% uptime, defines response times for support tickets, and specifies penalties if the provider fails to meet these guarantees. What type of agreement is this?

A) MOU
B) NDA
C) SLA
D) ISA

<details><summary>Answer</summary>

**C) SLA**

An SLA (Service Level Agreement) formally defines the level of service expected from a provider, including uptime guarantees, performance metrics, support response times, and remedies/penalties for non-compliance. It is a legally binding contract. An MOU (Memorandum of Understanding) is typically less formal and used for partnerships; an NDA (Non-Disclosure Agreement) governs confidentiality; an ISA (Interconnection Security Agreement) defines security requirements for interconnected systems.

</details>

---

**Q27.** Two government agencies want to connect their networks to share data but need to formally document the security requirements, authorized data flows, and technical controls governing the connection before it is established. Which agreement type is MOST appropriate?

A) SLA
B) NDA
C) MOU
D) ISA

<details><summary>Answer</summary>

**D) ISA**

An ISA (Interconnection Security Agreement) is used specifically to document the technical and security requirements for connecting two separate organizational networks (especially government systems). It details authorized data flows, encryption requirements, access controls, and responsibilities. NIST SP 800-47 provides guidance on ISAs.

</details>

---

**Q28.** A company implements the NIST Cybersecurity Framework. During the "Identify" function, they discover they have no documented inventory of all their data assets, systems, or external dependencies. What process is the organization LACKING?

A) Incident response planning
B) Asset management
C) Vulnerability management
D) Configuration management

<details><summary>Answer</summary>

**B) Asset management**

Asset management involves maintaining a comprehensive, accurate inventory of all hardware, software, data, and external dependencies. The NIST CSF (Cybersecurity Framework) "Identify" function includes asset management as foundational — you cannot protect what you don't know exists. A lack of asset inventory is a critical security program gap.

</details>

---

**Q29.** An organization's business continuity plan requires that if the primary data center becomes unavailable, the backup site should be operational within 4 hours and have all data current to within 30 minutes of the outage. This plan drives which technical requirement?

A) Quarterly vulnerability assessments
B) Near-real-time data replication and a warm/hot standby site
C) Annual penetration testing
D) Daily offline tape backups

<details><summary>Answer</summary>

**B) Near-real-time data replication and a warm/hot standby site**

A 30-minute RPO (Recovery Point Objective) requires replication more frequent than daily backups — the organization needs near-continuous or at minimum very frequent incremental replication. A 4-hour RTO (Recovery Time Objective) requires a pre-provisioned warm or hot standby that can be activated without starting from scratch. Daily tape backups could result in up to 24 hours of data loss, failing the 30-minute RPO requirement.

</details>

---

**Q30.** A company is required by their cyber insurance policy to conduct annual penetration tests and patch critical vulnerabilities within 30 days. This is an example of which type of compliance driver?

A) Legal regulation
B) Contractual obligation
C) Voluntary framework adoption
D) Internal policy

<details><summary>Answer</summary>

**B) Contractual obligation**

Requirements mandated by a contractual agreement — such as a cyber insurance policy — are contractual compliance obligations. Other examples include PCI-DSS (Payment Card Industry Data Security Standard) requirements for payment processors and SOC 2 requirements for SaaS (Software as a Service) providers serving enterprise customers. This is distinct from legal regulations (HIPAA (Health Insurance Portability and Accountability Act), GDPR (General Data Protection Regulation)) which are mandated by law.

</details>

---

**Q31.** An organization's BIA indicates that a key website can tolerate a maximum of three hours of downtime. Which of the following terms refers to this three-hour maximum?

A) RPO
B) MTTR
C) MTBF
D) RTO

<details><summary>Answer</summary>

**D) RTO**

The Recovery Time Objective (RTO) defines the maximum acceptable duration of downtime for a system or process — in this case, three hours. The Recovery Point Objective (RPO) defines the maximum acceptable data loss measured in time. MTTR (Mean Time to Repair) is the average time to restore a system; MTBF (Mean Time Between Failures) measures reliability/availability over time.

</details>

---

**Q32.** A company wants to verify that a cloud service provider's security controls are functioning correctly. Which of the following would provide the MOST comprehensive assessment?

A) Reviewing the provider's self-assessment questionnaire
B) Requesting a copy of the provider's SOC 2 Type II report
C) Conducting an internal vulnerability scan of the provider's systems
D) Reviewing the provider's marketing materials

<details><summary>Answer</summary>

**B) Requesting a copy of the provider's SOC 2 Type II report**

A SOC 2 Type II report is an independent third-party audit that evaluates the design AND operating effectiveness of a service organization's security controls over a period of time (typically 6–12 months). Type II provides much stronger assurance than Type I (which only checks design). Self-assessments are not independent; vulnerability scanning a provider's systems requires permission and may not cover logical controls; marketing materials have no audit value.

</details>

---

**Q33.** An organization's security team is implementing a new security awareness training program. Which of the following metrics would BEST demonstrate the program's effectiveness at reducing risk?

A) Number of employees who completed training
B) Score averages on training assessments
C) Reduction in the number of successful phishing simulations over time
D) Number of security policies acknowledged by employees

<details><summary>Answer</summary>

**C) Reduction in the number of successful phishing simulations over time**

Effective security awareness training should produce measurable behavioral change. Tracking click rates on simulated phishing campaigns over time directly measures whether employees are applying what they learned. Completion rates, assessment scores, and policy acknowledgments measure training participation and knowledge, but not real-world behavior change. The reduction in successful simulation attacks is the most direct measure of risk reduction.

</details>

---

**Q34.** Which of the following best describes the difference between a risk assessment and a vulnerability assessment?

A) A risk assessment identifies technical weaknesses; a vulnerability assessment evaluates business impact
B) A vulnerability assessment identifies weaknesses; a risk assessment evaluates likelihood and impact of threats
C) They are the same process with different names
D) A risk assessment is performed by external parties; a vulnerability assessment is performed internally

<details><summary>Answer</summary>

**B) A vulnerability assessment identifies technical weaknesses; a risk assessment evaluates likelihood and impact**

Vulnerability assessments systematically identify and catalog technical weaknesses in systems (missing patches, misconfigurations, etc.). Risk assessments go further by analyzing the likelihood that a vulnerability will be exploited and the business impact if it is, resulting in a risk rating used to prioritize remediation and resource allocation. Risk assessment incorporates vulnerability data as an input but also considers threat intelligence, asset value, and business context.

</details>

---

**Q35.** An organization is working on its business continuity plan. Which of the following is the PRIMARY purpose of a Business Impact Analysis (BIA)?

A) Identify the technical vulnerabilities in all critical systems
B) Determine the financial cost of all security incidents over the past year
C) Identify and prioritize critical business functions and the impact of their disruption
D) Create the disaster recovery procedures for IT systems

<details><summary>Answer</summary>

**C) Identify and prioritize critical business functions and the impact of their disruption**

A Business Impact Analysis (BIA) is the foundation of business continuity planning. It identifies which business processes are critical to the organization's survival, determines the impact of disrupting each process (financial, operational, reputational), and establishes recovery priorities, RTOs, and RPOs. It is a business process, not a technical IT exercise. Technical recovery procedures come after the BIA informs which systems are most critical.

</details>

---

**Q36.** An organization wants to evaluate the security posture of a vendor before entering into a contract for cloud services. Which of the following represents a third-party risk management activity?

A) Conducting a penetration test on internal systems
B) Performing a vendor risk assessment using a standardized questionnaire
C) Reviewing internal security policies
D) Scanning the vendor's public-facing website with automated tools

<details><summary>Answer</summary>

**B) Performing a vendor risk assessment using a standardized questionnaire**

Third-party risk management involves assessing and managing risks introduced by external vendors, suppliers, and partners. A standardized vendor risk assessment questionnaire (often based on frameworks like the Shared Assessments Standardized Information Gathering (SIG) questionnaire or the CAIQ for cloud vendors) evaluates the vendor's security controls, compliance posture, and risk to the organization. Internal penetration tests and policy reviews address internal risk; scanning a vendor's website without permission is not authorized and provides limited information.

</details>

---

**Q37.** Which of the following risk response strategies involves shifting the financial consequences of a risk to a third party?

A) Avoid
B) Mitigate
C) Transfer
D) Accept

<details><summary>Answer</summary>

**C) Transfer**

Risk transfer shifts the financial burden of a risk to another party — most commonly through cyber liability insurance or contractual indemnification clauses. The risk itself is not eliminated; only the financial impact is transferred. Risk avoidance eliminates the risk by not engaging in the risky activity; risk mitigation reduces the likelihood or impact; risk acceptance acknowledges the risk and consciously decides to bear it.

</details>

---

**Q38.** Which of the following frameworks is specifically designed to help organizations manage and reduce cybersecurity risk and is widely used by critical infrastructure sectors in the United States?

A) ISO 27001
B) COBIT
C) NIST Cybersecurity Framework (CSF)
D) PCI DSS

<details><summary>Answer</summary>

**C) NIST Cybersecurity Framework (CSF)**

The NIST CSF was originally developed for critical infrastructure sectors and has since become widely adopted across industries. It organizes cybersecurity activities into five core functions: Identify, Protect, Detect, Respond, and Recover. ISO 27001 is an international standard for information security management; COBIT is an IT governance framework; PCI DSS is a compliance standard specifically for payment card data security.

</details>

---

**Q39.** An organization has decided to accept a risk rather than implement a control to mitigate it. Which of the following documents should be used to formally record this decision?

A) Risk register
B) System security plan
C) Memorandum of understanding
D) Statement of applicability

<details><summary>Answer</summary>

**A) Risk register**

A risk register is a formal document used to record, track, and manage identified risks and the organization's chosen response to each. When a risk acceptance decision is made, it should be documented in the risk register with the justification, the risk owner, and the review date. This provides accountability and ensures the decision is periodically reviewed. A system security plan documents security controls; an MOU is an agreement between parties; a statement of applicability (used in ISO 27001) records which controls apply.

</details>

---

**Q40.** Which of the following BEST describes the purpose of a penetration test authorization document?

A) It defines the security architecture to be tested
B) It provides written permission for the tester to conduct the assessment and defines the scope
C) It lists all vulnerabilities discovered during the test
D) It certifies the tester's professional credentials

<details><summary>Answer</summary>

**B) It provides written permission for the tester to conduct the assessment and defines the scope**

Before any penetration test, a formal authorization document (sometimes called a Statement of Work, Rules of Engagement, or Penetration Testing Agreement) must be signed. This document grants explicit legal permission, defines what systems are in scope, what techniques are allowed, the timeline, emergency contacts, and escalation procedures. Without this document, penetration testing activities could be considered unauthorized computer access under laws such as the CFAA.

</details>

---

**Q41.** A security team is conducting a tabletop exercise to prepare for a potential ransomware incident. Which of the following BEST describes the purpose of this activity?

A) To deploy and test actual ransomware in a controlled lab environment
B) To evaluate employee security awareness training completion rates
C) To discuss and walk through incident response procedures in a simulated scenario without using live systems
D) To perform vulnerability scanning on backup systems

<details><summary>Answer</summary>

**C) To discuss and walk through incident response procedures without using live systems**

A tabletop exercise is a discussion-based simulation where key personnel talk through their roles and actions in a hypothetical scenario (e.g., "What would you do if ransomware was detected at 2 AM?"). It identifies gaps in plans, clarifies roles, and builds team familiarity with response procedures — all without the risk or cost of testing on live systems. It is part of the "Prepare" phase of incident response and business continuity planning.

</details>

---

**Q42.** Which of the following compliance frameworks is most applicable to an organization that processes payment card data?

A) HIPAA
B) GDPR
C) SOX
D) PCI DSS

<details><summary>Answer</summary>

**D) PCI DSS**

The Payment Card Industry Data Security Standard (PCI DSS) is the compliance framework specifically designed to protect cardholder data. It is mandated by payment card brands (Visa, Mastercard, etc.) for any entity that stores, processes, or transmits credit/debit card data. HIPAA applies to healthcare data; GDPR applies to personal data of EU residents; SOX applies to financial reporting for publicly traded companies.

</details>

---

**Q43.** Which of the following BEST describes the benefit of homomorphic encryption?

A) Share data with third parties without any privacy concerns
B) Process encrypted data without decrypting it first
C) Store and manipulate data as simple integers for efficiency
D) All of the above

<details><summary>Answer</summary>

**D) All of the above**

Homomorphic encryption allows computations to be performed on encrypted ciphertext, producing results that, when decrypted, match the result of performing the same operations on the plaintext. This enables cloud providers to process sensitive data without ever seeing the decrypted values, preserving privacy. It enables sharing for processing without privacy risk, allows arithmetic operations (store/manipulate as integers), and performs computation on encrypted data.

</details>

---

**Q44.** What does a lack of entropy in a cryptographic system result in?

A) A stronger, more efficient algorithm
B) An algorithm that is easier to crack
C) A more complex algorithm
D) A more expensive algorithm to implement

<details><summary>Answer</summary>

**B) An algorithm that is easier to crack**

Entropy refers to the randomness or unpredictability in a cryptographic system. Low entropy means the key space or initialization values are predictable, allowing attackers to more easily brute-force or guess the key. Strong cryptographic systems require high-entropy random number generators (RNGs). Predictable pseudo-random number generators are a common cryptographic vulnerability.

</details>

---

**Q45.** What does the OCSP (Online Certificate Status Protocol) specifically support?

A) Hashing protocols for file integrity
B) Steganographic embedding
C) Low latency certificate revocation checking
D) Elliptic Curve key generation

<details><summary>Answer</summary>

**C) Low latency certificate revocation checking**

OCSP provides real-time certificate revocation status checking without requiring clients to download and parse an entire Certificate Revocation List (CRL). Each query/response cycle is fast (low latency), making it preferable to CRLs for time-sensitive connections. OCSP stapling is a further optimization where the server pre-fetches and caches its own OCSP response.

</details>

---

**Q46.** Which of the following correctly describes Bcrypt?

A) Based on the AES block cipher and used to generate 256-bit hashes
B) Produces a 128-bit result and does not use salt
C) Was selected as the winner of the 2015 Password Hashing Competition
D) Based on the Blowfish block cipher and designed to protect shadow password files

<details><summary>Answer</summary>

**D) Based on the Blowfish block cipher and designed to protect shadow password files**

Bcrypt is a password hashing function based on the Blowfish block cipher. It was designed by Niels Provos and David Mazières specifically for hashing passwords, incorporating a cost factor (work factor) that can be increased over time to counteract faster hardware. It uses a random salt and produces a 60-character output. Note: Argon2 won the 2015 Password Hashing Competition, not bcrypt.

</details>

---

**Q47.** What makes PEM certificates a commonly misunderstood format?

A) They are used exclusively for email encryption
B) They can share public keys in certificates, install private keys on servers, and use .key extension for private key files — but are not limited to email
C) They use a binary format incompatible with most web servers
D) They cannot be converted to other certificate formats

<details><summary>Answer</summary>

**B) They can share public keys in certificates, install private keys on servers, and use .key extension for private key files — but are not limited to email**

PEM (Privacy Enhanced Mail) certificates use Base64 encoding with BEGIN/END headers and are the most commonly used certificate format for web servers (Apache, Nginx), but are named for their original use case (email). They can contain certificates (.crt, .pem), private keys (.key), or certificate chains. The common misconception is that they are only for email — in reality, they are the standard format for Linux/Unix web servers.

</details>

---

**Q48.** Which of the following is the correct use of public and private keys in asymmetric encryption for confidentiality?

A) Only the public key can decrypt information encrypted with the public key
B) The private key encrypts data; only the matching public key can decrypt it
C) Either key in a pair can decipher data regardless of which key encrypted it
D) Private keys should be freely shared to enable decryption by any party

<details><summary>Answer</summary>

**B) Private key encrypts; only matching public key decrypts**

This describes the digital signature use case: the sender encrypts (signs) with their private key; anyone with the public key can verify (decrypt) the signature. For confidentiality (sending a secret message), the reverse applies: encrypt with the recipient's PUBLIC key; only the recipient's private key can decrypt. The exam tests both directions — knowing which key serves which purpose is critical.

</details>

---

**Q49.** Which of the following certificate formats is the predecessor to P12 and is commonly used on Windows systems?

A) P7B
B) PEM
C) PFX
D) CER

<details><summary>Answer</summary>

**C) PFX**

PFX (Personal Information Exchange) is the predecessor to the PKCS#12 (.p12) format and is used to store a certificate along with its private key in a single password-protected file. It is commonly used on Windows for importing/exporting certificates with private keys. P7B stores the certificate and certificate chain but not the private key; PEM is a Base64 encoded format; CER is typically a DER-encoded certificate without the private key.

</details>

---

**Q50.** What is the primary purpose of the Serial Number field in a digital certificate?

A) Identifies the certificate owner (subject)
B) Indicates the certificate's validity dates
C) Uniquely identifies the certificate and is used by the CA to validate revocation status
D) Indicates the permitted uses of the certificate

<details><summary>Answer</summary>

**C) Uniquely identifies the certificate; used by the CA to validate revocation**

Every certificate issued by a CA contains a unique serial number assigned by that CA. The serial number is referenced in the Certificate Revocation List (CRL) to identify which specific certificates have been revoked. When checking revocation status, the serial number is sent in the OCSP request. The subject field identifies the owner; validity dates appear in the Not Before/Not After fields; key usage extensions indicate permitted uses.

</details>

---

**Q51.** What is the notable weakness in relying on the MD5 hashing algorithm for security purposes today?

A) It produces a 256-bit hash that is too slow for modern systems
B) It cannot be used for file integrity verification
C) It produces a 128-bit hash, but collisions have been demonstrated, making it cryptographically broken
D) It uses only hexadecimal characters, limiting its output space

<details><summary>Answer</summary>

**C) Produces a 128-bit hash; collisions demonstrated — cryptographically broken**

MD5 generates a 128-bit hash value displayed as 32 hexadecimal characters. While still used for non-security purposes (quick checksums), MD5 is cryptographically broken because practical collision attacks have been demonstrated — meaning two different inputs can produce the same MD5 hash. This makes it unsuitable for digital signatures, certificate fingerprints, or password hashing. SHA-256 or SHA-3 should be used instead.

</details>

---
