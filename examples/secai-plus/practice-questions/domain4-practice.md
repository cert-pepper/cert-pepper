# Domain 4 Practice Questions — AI Governance, Risk, and Compliance

---

**Q1.** An organization implements an AI loan approval system that consistently rejects applications from a specific demographic group at higher rates than others, despite similar financial profiles. Which AI risk does this represent?

A) Accidental data leakage
B) Introduction of bias
C) Autonomous system risk
D) IP-related risk

<details><summary>Answer</summary>

**B) Introduction of bias**

Introduction of bias occurs when an AI model learns discriminatory patterns from skewed or unrepresentative training data, leading to unfair outcomes for certain groups. This is both a responsible AI failure (fairness principle) and a regulatory compliance risk under laws like the EU AI Act. Accidental data leakage involves unintended exposure of sensitive data, not discriminatory decisions.

</details>

---

**Q2.** A company adopts AI in its IDS. The security team raises concerns that analysts cannot explain why the AI flagged a specific connection as malicious. Which responsible AI principle is not being met?

A) Inclusiveness
B) Transparency
C) Consistency
D) Explainability

<details><summary>Answer</summary>

**D) Explainability**

Explainability (XAI) is the ability to describe, in human-understandable terms, why an AI system made a specific decision. Without it, analysts cannot validate, challenge, or learn from AI decisions. Transparency refers to openness about how the system works at a higher level; explainability is about specific, per-decision reasoning. Consistency refers to reliable behavior across similar inputs.

</details>

---

**Q3.** An employee uses a free consumer-grade LLM to summarize confidential merger documents, bypassing the organization's approved AI tool. What governance risk does this represent?

A) Reputational loss
B) Shadow AI
C) Autonomous systems risk
D) Third-party compliance evaluation gap

<details><summary>Answer</summary>

**B) Shadow AI**

Shadow AI (a subset of Shadow IT) occurs when employees use unauthorized AI tools outside of organizational governance, visibility, and control. This exposes confidential data to third-party models with unknown data handling practices. The approved AI tool should have organizational data governance controls; the unsanctioned tool does not.

</details>

---

**Q4.** Which compliance framework specifically provides a structured approach for organizations to manage and mitigate AI risks across Govern, Map, Measure, and Manage functions?

A) EU AI Act
B) OECD AI Principles
C) NIST AIRMF
D) ISO AI standards

<details><summary>Answer</summary>

**C) NIST AIRMF**

The NIST AI Risk Management Framework (AIRMF) organizes AI risk management into four core functions: Govern (establish policies and accountability), Map (identify AI context and risks), Measure (assess risks quantitatively), and Manage (implement and monitor controls). The EU AI Act is a regulation, not a management framework. The OECD AI Principles and ISO AI standards are broader guidelines.

</details>

---

**Q5.** Under the EU AI Act, which risk tier describes AI systems used in critical infrastructure (e.g., power grids, water systems) where a failure could cause significant harm?

A) Minimal risk
B) Limited risk
C) High risk
D) Unacceptable risk

<details><summary>Answer</summary>

**C) High risk**

The EU AI Act classifies AI systems used in critical infrastructure as high risk — they are allowed but subject to strict conformity assessments, transparency requirements, and human oversight obligations. Unacceptable risk covers outright prohibited uses (e.g., real-time biometric surveillance in public spaces by law enforcement). Minimal and limited risk apply to systems like recommendation engines or chatbots.

</details>

---

**Q6.** A large enterprise creates a dedicated team responsible for establishing AI standards, sharing best practices, reviewing AI project proposals, and ensuring consistent governance across all business units. What structure does this represent?

A) AI risk committee
B) AI Center of Excellence
C) MLOps pipeline
D) AI audit board

<details><summary>Answer</summary>

**B) AI Center of Excellence**

An AI Center of Excellence (CoE) is a centralized team or function that sets organizational AI standards, promotes best practices, evaluates proposed AI initiatives, and provides governance oversight across business units. It differs from an audit board (which independently reviews after the fact) and a risk committee (which focuses on risk approval decisions rather than capability development and standards).

</details>

---

**Q7.** A financial services firm hires two specialists: one to manage the end-to-end model training, deployment, and monitoring pipelines, and another to design security controls that protect AI systems from adversarial attacks and data poisoning. Which roles are being filled, respectively?

A) AI auditor and data engineer
B) AI risk analyst and AI governance engineer
C) MLOps engineer and AI security architect
D) Data engineer and AI risk analyst

<details><summary>Answer</summary>

**C) MLOps engineer and AI security architect**

An MLOps engineer owns the operational lifecycle of AI models — training pipelines, deployment automation, versioning, and monitoring. An AI security architect designs the security architecture that protects AI systems, including defenses against adversarial inputs, data poisoning, and model theft. These are distinct roles: one focuses on model operationalization, the other on securing AI infrastructure.

</details>

---

**Q8.** An organization's governance team requires that all production AI models enforce data retention limits, logging of model decisions, and access controls on training data. The person responsible for translating these governance requirements into working technical controls is best described as which role?

A) AI auditor
B) AI risk analyst
C) AI governance engineer
D) Data engineer

<details><summary>Answer</summary>

**C) AI governance engineer**

An AI governance engineer bridges policy and implementation — taking governance requirements (retention limits, audit logging, access controls) and implementing them as technical controls within AI systems and infrastructure. This differs from the AI auditor (who independently assesses compliance after implementation) and the AI risk analyst (who identifies and quantifies risks before or during deployment).

</details>

---

**Q9.** After an AI-powered hiring tool is deployed at a large corporation, regulators require an independent review to assess whether the system produces equitable outcomes and complies with anti-discrimination laws. Which AI governance role conducts this review?

A) MLOps engineer
B) AI security architect
C) AI risk analyst
D) AI auditor

<details><summary>Answer</summary>

**D) AI auditor**

An AI auditor independently assesses AI systems for compliance, fairness, and adherence to governance policies — without being part of the team that built or operates the system. Independence is key: auditors provide an objective third-party view. An AI risk analyst identifies risks earlier in the lifecycle, while an MLOps engineer manages operational concerns.

</details>

---

**Q10.** Before an organization launches an AI fraud detection model in production, a specialist reviews its training data sources, identifies potential failure modes, estimates the probability of false positives causing customer harm, and documents residual risks. Which role performs this work?

A) AI auditor
B) AI risk analyst
C) AI governance engineer
D) MLOps engineer

<details><summary>Answer</summary>

**B) AI risk analyst**

An AI risk analyst identifies, assesses, and quantifies risks in AI deployments — including data quality risks, failure mode analysis, and estimating the likelihood and impact of adverse outcomes — before and during deployment. This is distinct from an AI auditor (who performs independent reviews after deployment) and an AI governance engineer (who implements technical controls).

</details>

---

**Q11.** A healthcare AI project requires high-quality, well-labeled patient records for model training. A specialist is tasked with designing and maintaining the pipelines that extract, transform, and load data from hospital systems into the model training environment. Which role does this describe?

A) AI risk analyst
B) AI auditor
C) AI governance engineer
D) Data engineer

<details><summary>Answer</summary>

**D) Data engineer**

A data engineer designs and maintains the data pipelines that collect, process, and deliver data to AI systems. In AI governance, data engineers play a critical role because model quality depends on data quality and lineage. They ensure data provenance, integrity, and consistency — foundational requirements for meeting AI governance and compliance obligations.

</details>

---

**Q12.** A CISO wants to ensure employees use AI tools responsibly and within approved boundaries. The security team drafts a document that defines which AI tools are permitted, prohibited use cases, data handling requirements, and user responsibilities. What type of governance artifact is this?

A) AI risk register
B) AI acceptable-use policy
C) Model card
D) AI audit report

<details><summary>Answer</summary>

**B) AI acceptable-use policy**

An AI acceptable-use policy (AUP) is a governance document that defines the boundaries of permitted AI tool use within an organization — specifying approved tools, prohibited use cases (e.g., processing PII in unapproved systems), data handling requirements, and user accountability. It is a foundational AI governance procedure that reduces Shadow AI risk and aligns employee behavior with organizational policy.

</details>

---

**Q13.** A research team training a health outcomes model wants to allow external parties to query aggregate statistics derived from a sensitive patient dataset, while ensuring no individual patient's data can be inferred from the query results. Which responsible AI technique addresses this requirement?

A) Federated learning
B) Model watermarking
C) Differential privacy
D) Explainability logging

<details><summary>Answer</summary>

**C) Differential privacy**

Differential privacy adds calibrated mathematical noise to query outputs or training processes so that no individual record can be identified or inferred from the results. It provides a formal privacy guarantee, making it distinct from general anonymization. Federated learning keeps data local during training but does not prevent inference attacks on aggregate statistics.

</details>

---

**Q14.** A startup trains a large language model on text scraped from public websites, including books, articles, and code repositories, without reviewing the licensing terms of the source material. Which AI risk category does this create?

A) Reputational loss
B) Autonomous system risk
C) IP-related risk
D) Model drift

<details><summary>Answer</summary>

**C) IP-related risk**

IP-related risk arises when AI training uses copyrighted content without proper licensing or authorization, potentially exposing the organization to intellectual property infringement claims. This is a distinct risk category from reputational loss (which may follow but is a consequence) and model drift (which relates to degraded performance over time due to data distribution changes).

</details>

---

**Q15.** A bank deploys an AI chatbot that gives a customer incorrect financial advice, leading to a significant loss. The incident becomes public news, causing customers to lose confidence in the institution and prompting regulatory scrutiny. Which AI risk does the public fallout represent?

A) Accidental data leakage
B) Reputational loss
C) IP-related risk
D) Autonomous system risk

<details><summary>Answer</summary>

**B) Reputational loss**

Reputational loss occurs when a public AI failure erodes stakeholder and customer trust in the organization. Even if the underlying technical incident is contained, the perception damage — media coverage, customer churn, regulatory attention — constitutes a distinct and significant business risk. This is separate from the direct harm caused by the incorrect advice, which may create additional liability.

</details>

---

**Q16.** A security operations team deploys an AI-based phishing classifier that achieved 96% accuracy in testing. Six months after deployment, the model's production accuracy drops to 72% as threat actors evolve their phishing techniques. Which AI risk does this illustrate?

A) Shadow AI
B) IP-related risk
C) Reputational loss
D) Model drift

<details><summary>Answer</summary>

**D) Model drift**

Model drift occurs when a model's performance degrades over time because the real-world data distribution it encounters in production diverges from the training data distribution. In adversarial domains like phishing detection, threat actors actively evolve their techniques, accelerating drift. Model drift is an ongoing governance and risk concern requiring continuous monitoring and retraining schedules, not just an MLOps operational issue.

</details>

---

**Q17.** After an AI-driven inventory management system is integrated with a supply chain platform, it begins generating purchase orders that create runaway inventory cycles — the AI system's outputs become inputs that feed back and amplify each other in unexpected ways. Which AI risk category does this represent?

A) Model drift
B) Unintended system interactions
C) Autonomous system risk
D) Shadow AI

<details><summary>Answer</summary>

**B) Unintended system interactions**

Unintended system interactions occur when an AI system's outputs feed into other systems in ways not anticipated during design, causing emergent downstream effects. This is distinct from autonomous system risk (which concerns AI acting without human authorization) and model drift (which is about performance degradation). Complex integrations between AI and operational systems create feedback loops that can amplify errors unpredictably.

</details>

---

**Q18.** A company's AI governance policy requires that before any AI model is used in a business process, it must be reviewed and formally approved by the AI governance board. An employee discovers a third-party vendor is using an unapproved AI model to process invoices on the company's behalf. How should this model be classified?

A) Private model
B) Sanctioned model
C) Unsanctioned model
D) Open-source model

<details><summary>Answer</summary>

**C) Unsanctioned model**

An unsanctioned model is one used in an organizational context without having gone through the required review and approval process. Even when used by a vendor on the company's behalf, the model falls under the organization's governance obligations. Sanctioned models have been reviewed and formally approved. This distinction is foundational to AI governance frameworks.

</details>

---

**Q19.** An organization is evaluating whether to deploy a proprietary AI model on its own on-premises infrastructure versus using a public cloud AI API. The primary concern is that sending sensitive customer data to an external API may violate contractual data handling obligations. Which deployment consideration does this reflect?

A) Model drift risk
B) IP-related risk
C) Private vs. public model deployment
D) Shadow AI

<details><summary>Answer</summary>

**C) Private vs. public model deployment**

Private model deployment keeps data within organizational boundaries, enabling control over data handling, access, and compliance with contractual or regulatory obligations. Public model deployment (via external APIs) introduces data sovereignty and confidentiality risks because data leaves the organization's control. This trade-off between capability access and data governance is a core AI compliance decision.

</details>

---

**Q20.** An international technology company trains AI models using customer data collected in Germany, stores intermediate model artifacts in Singapore, and runs inference workloads in the United States. Legal counsel warns that each jurisdiction imposes different requirements on how the data and model outputs may be processed. Which compliance concept does this describe?

A) Model drift
B) Data sovereignty
C) Third-party compliance evaluation
D) Differential privacy

<details><summary>Answer</summary>

**B) Data sovereignty**

Data sovereignty is the principle that data is subject to the laws and regulations of the jurisdiction in which it is collected or processed. Cross-border AI deployments must account for differing national requirements — such as GDPR in the EU — at each stage of the data and model lifecycle, including training, storage, and inference.

</details>

---

**Q21.** A multinational organization adopts a set of intergovernmental AI principles emphasizing that AI should be human-centered, transparent, robust, secure, and that developers should be held accountable for their systems' outcomes. Which framework or body established these principles?

A) EU AI Act
B) NIST AIRMF
C) OECD
D) ISO

<details><summary>Answer</summary>

**C) OECD**

The OECD AI Principles, adopted in 2019, were the first intergovernmental standard on AI. They call for AI that is inclusive and sustainable, human-centered, transparent and explainable, robust and secure, and for which developers and deployers remain accountable. The EU AI Act is a binding regulation (not principles); NIST AIRMF is a risk management framework; ISO AI standards address technical and quality aspects.

</details>

---

**Q22.** A hospital system is building an AI diagnostic tool. Legal counsel determines that because the model will process protected health information, it must comply with federal patient privacy regulations governing the use, disclosure, and safeguarding of that data — regardless of the AI vendor's own policies. Which industry-specific compliance obligation applies?

A) GDPR
B) PCI DSS
C) HIPAA
D) SOX

<details><summary>Answer</summary>

**C) HIPAA**

HIPAA (Health Insurance Portability and Accountability Act) governs the use, disclosure, and safeguarding of protected health information (PHI) in the United States. When AI systems process PHI — including using it as training data or for inference — HIPAA's Privacy and Security Rules apply to both the covered entity and any business associates (including AI vendors). This makes HIPAA a foundational compliance requirement for healthcare AI.

</details>

---

**Q23.** An AI governance team conducts a review to determine whether an organization's AI vendors are adhering to contractual data handling, model transparency, and bias testing requirements. Which governance activity does this represent?

A) Shadow AI remediation
B) Internal model audit
C) Third-party compliance evaluation
D) Differential privacy assessment

<details><summary>Answer</summary>

**C) Third-party compliance evaluation**

Third-party compliance evaluation involves assessing whether external vendors and partners who build or operate AI systems on an organization's behalf meet the required governance, security, and regulatory standards. This is distinct from an internal model audit (which covers models owned by the organization) and addresses the governance gap that arises when AI capabilities are sourced externally.

</details>

---
