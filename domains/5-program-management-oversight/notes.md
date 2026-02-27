# Domain 5: Security Program Management and Oversight (20%)

## 5.1 Governance

### Security Policies
| Document | Description |
|----------|-------------|
| **Policy** | High-level management directive ("employees must use strong passwords") |
| **Standard** | Specific mandatory requirements ("passwords must be 12+ characters") |
| **Procedure** | Step-by-step instructions for tasks |
| **Guideline** | Recommended but not mandatory advice |
| **Baseline** | Minimum security configuration for a system type |

### Governance Frameworks
- **NIST CSF (Cybersecurity Framework)** — Identify, Protect, Detect, Respond, Recover
- **ISO 27001** — International standard for ISMS (Information Security Management System)
- **COBIT** — IT governance framework
- **ITIL** — IT service management framework

### Organizational Structures
- **CISO (Chief Information Security Officer)** — Heads security program
- **Security committee** — Cross-functional oversight
- **Separation of duties** — No single person controls entire process

---

## 5.2 Risk Management

### Risk Terminology
- **Threat** — Potential cause of an unwanted event
- **Vulnerability** — Weakness that can be exploited
- **Risk** = Threat × Vulnerability × Impact
- **Asset** — Something of value to the organization
- **Exposure** — Being susceptible to a threat

### Risk Calculation
- **SLE (Single Loss Expectancy)** = Asset Value × Exposure Factor
- **ARO (Annualized Rate of Occurrence)** = How often per year
- **ALE (Annualized Loss Expectancy)** = SLE × ARO

> Example: Server worth $100K, 40% exposed, breached once every 5 years
> SLE = $100K × 0.4 = $40K | ARO = 0.2 | ALE = $40K × 0.2 = $8K/year

### Risk Response Options
| Response | Description | Example |
|----------|-------------|---------|
| **Avoid** | Eliminate the risk by not doing the activity | Don't store credit cards |
| **Transfer** | Shift risk to third party | Cyber insurance |
| **Mitigate/Reduce** | Reduce probability or impact | Patch system, add controls |
| **Accept** | Acknowledge and accept the risk | Document residual risk |

### Risk Types
- **Inherent risk** — Risk before any controls
- **Residual risk** — Risk remaining after controls
- **Risk appetite** — Amount of risk org is willing to accept
- **Risk tolerance** — Acceptable variation around risk appetite

### Business Impact Analysis (BIA)
- Identifies critical business functions and their dependencies
- Determines impact of disruptions
- **RTO (Recovery Time Objective)** — Max time before operations must resume
- **RPO (Recovery Point Objective)** — Max acceptable data loss
- **MTTR** — Mean Time to Repair
- **MTBF** — Mean Time Between Failures

---

## 5.3 Compliance

### Key Regulations
| Regulation | Scope | Key Requirement |
|-----------|-------|----------------|
| **GDPR** | EU personal data | Consent, right to erasure, breach notification 72hr |
| **HIPAA** | US healthcare | PHI protection, access controls, audit trails |
| **PCI-DSS** | Credit card data | Cardholder data protection, network segmentation |
| **SOX** | US public companies | Financial data integrity, audit controls |
| **FISMA** | US federal agencies | NIST-based security programs |
| **GLBA** | US financial institutions | Customer financial data protection |
| **FERPA** | US education records | Student record privacy |
| **COPPA** | Children under 13 | Online privacy for children |

### Audit Types
| Type | Description |
|------|-------------|
| **Internal audit** | Performed by org's own staff |
| **External audit** | Independent third-party |
| **Compliance audit** | Verifies adherence to regulation/standard |
| **Penetration test** | Technical security assessment |

---

## 5.4 Data Privacy

### Privacy Concepts
- **PII (Personally Identifiable Information)** — Name, SSN, DOB, address, etc.
- **PHI (Protected Health Information)** — Medical data (HIPAA)
- **Data sovereignty** — Data subject to laws of country where it resides
- **Data residency** — Where data is physically stored
- **Privacy by design** — Build privacy into systems from the start
- **Data minimization** — Collect only what's needed

### Privacy Roles
- **Data controller** — Determines purpose and means of processing (GDPR)
- **Data processor** — Processes data on behalf of controller
- **Data steward** — Internal role managing data quality/governance
- **DPO (Data Protection Officer)** — Required under GDPR for some orgs

---

## 5.5 Third-Party Risk Management

### Vendor Risk
- Suppliers and partners can introduce risk
- **Supply chain attack** — Compromise via trusted vendor (SolarWinds)

### Agreements
| Agreement | Purpose |
|-----------|---------|
| **SLA (Service Level Agreement)** | Defines service performance standards |
| **MOU (Memorandum of Understanding)** | Non-binding intent/relationship document |
| **MOA (Memorandum of Agreement)** | Binding agreement between parties |
| **NDA (Non-Disclosure Agreement)** | Protects confidential information |
| **BPA (Business Partnership Agreement)** | Defines business relationship terms |
| **ISA (Interconnection Security Agreement)** | Technical/security requirements for connected systems |
| **MSA (Master Service Agreement)** | Overarching vendor agreement |

### Vendor Due Diligence
- Security questionnaires
- Right-to-audit clauses
- SOC 2 reports (Type 1: design; Type 2: operating effectiveness)
- Penetration test results

---

## 5.6 Security Awareness and Training

### Training Types
- **Security awareness training** — All employees; phishing, social engineering basics
- **Role-based training** — Technical staff, executives, developers
- **Phishing simulations** — Test employee response to fake phishing emails

### Key Behaviors to Train
- Recognizing phishing
- Password hygiene
- Physical security (tailgating, clean desk)
- Reporting incidents
- Handling sensitive data

### Culture
- Security culture starts at top (tone from leadership)
- Reward reporting, don't punish mistakes
- Regular reminders, not just annual training
