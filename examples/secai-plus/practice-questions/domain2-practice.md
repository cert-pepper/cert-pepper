# Domain 2 Practice Questions — Securing AI Systems

---

**Q1.** A security architect is building a threat model for a new LLM-powered customer service chatbot. Which resource specifically catalogs adversarial attack techniques against AI and ML systems, analogous to MITRE ATT&CK for traditional cyber threats?

A) OWASP LLM Top 10
B) MITRE ATLAS
C) MIT AI Risk Repository
D) CVE AI Working Group

<details><summary>Answer</summary>

**B) MITRE ATLAS**

MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) is the AI-specific adversarial knowledge base analogous to ATT&CK — it catalogs real-world adversarial ML attack techniques, tactics, and case studies. OWASP LLM Top 10 lists the top 10 security risks specific to LLM applications. MIT AI Risk Repository is a research database of AI risks. CVE AI Working Group focuses on vulnerability enumeration.

</details>

---

**Q2.** An organization implements controls that intercept and inspect all prompts sent to an AI system before they reach the model, filtering out known injection patterns. What type of control is this?

A) Model guardrail
B) Prompt firewall
C) Token limit
D) Modality limit

<details><summary>Answer</summary>

**B) Prompt firewall**

A prompt firewall sits at the gateway layer and filters or blocks malicious prompts before they reach the model — similar to a WAF but for LLM inputs. Model guardrails are built into the model layer to constrain outputs. Token limits cap the length of inputs or outputs. Modality limits restrict input types (e.g., no image uploads).

</details>

---

**Q3.** A disgruntled employee gains access to the company chatbot's reference policy documents and modifies them to provide incorrect guidance to employees. Which attack type does this represent?

A) Model poisoning
B) Data poisoning
C) Prompt injection
D) Jailbreaking

<details><summary>Answer</summary>

**B) Data poisoning**

Data poisoning corrupts the data that an AI system references or learns from — in this case, the policy documents the chatbot uses. Model poisoning targets the model's weights directly. Prompt injection inserts malicious instructions into user inputs at inference time. Jailbreaking uses crafted prompts to bypass safety filters.

</details>

---

**Q4.** A company's AI training pipeline uses a chatbot that exposes employees' names from the training dataset in its responses. Which control would best prevent personal information from appearing in model outputs?

A) Salting
B) Hashing
C) Data minimization
D) Anonymization

<details><summary>Answer</summary>

**D) Anonymization**

Anonymization irreversibly removes or replaces personal identifiers from training data so they cannot be reconstructed — preventing the model from learning and reproducing them. Hashing is a one-way function used for integrity, not privacy in training data. Salting adds random data to hashes to prevent rainbow table attacks. Data minimization reduces the amount of data collected but doesn't remove identifiers already in a dataset.

</details>

---

**Q5.** An AI system deployed as a financial advisor begins making autonomous decisions — purchasing assets and executing contracts — far beyond its intended advisory scope. Which OWASP LLM risk category does this represent?

A) Insecure output handling
B) Sensitive information disclosure
C) Excessive agency
D) Overreliance

<details><summary>Answer</summary>

**C) Excessive agency**

Excessive agency occurs when an AI agent is granted more permissions, capabilities, or autonomy than required for its intended task — allowing it to take actions beyond its scope. Overreliance is when users or systems blindly trust AI outputs without human verification. Insecure output handling fails to sanitize AI outputs before passing them to downstream systems.

</details>

---

**Q6.** A threat actor repeatedly queries a company's ML API with crafted inputs to reconstruct the model's decision boundaries and build a local copy of it. What attack is being performed?

A) Membership inference
B) Model inversion
C) Model theft
D) Transfer learning attack

<details><summary>Answer</summary>

**C) Model theft**

Model theft (also called model extraction) uses the API's input-output pairs to train a surrogate model that mimics the original. Membership inference asks whether a specific record was in training data. Model inversion reconstructs training data samples from model outputs or gradients. Transfer learning attacks exploit weaknesses in pre-trained model knowledge being transferred to new models.

</details>

---

**Q7.** A security team reviewing an AI system's logs notices that the model is returning unusually high-confidence scores for low-quality inputs. Which monitoring control should be implemented to catch this?

A) Log sanitization
B) Rate monitoring
C) Response confidence level monitoring
D) AI cost monitoring

<details><summary>Answer</summary>

**C) Response confidence level monitoring**

Response confidence level monitoring tracks the confidence scores attached to model outputs and alerts when confidence is anomalously high or low — which may indicate model degradation, adversarial inputs, or drift. Rate monitoring tracks query volume. Log sanitization removes sensitive data from logs. AI cost monitoring tracks token and compute usage.

</details>

---

**Q8.** An organization needs to ensure that AI training data cannot be read if intercepted during transfer from a data lake to the training cluster. Which encryption requirement applies?

A) Encryption at rest
B) Encryption in use
C) Encryption in transit
D) Homomorphic encryption

<details><summary>Answer</summary>

**C) Encryption in transit**

Encryption in transit (e.g., TLS) protects data moving across networks — including from a data lake to a training cluster. Encryption at rest protects stored data. Encryption in use (e.g., via trusted execution environments) protects data while being actively processed. Homomorphic encryption allows computation on encrypted data without decrypting it.

</details>

---

**Q9.** A developer receives an email containing a document with hidden instructions embedded in the text. When the document is fed to an LLM assistant, the model executes the hidden instructions instead of summarizing the document. Which OWASP LLM risk does this scenario illustrate?

A) LLM02 — Insecure output handling
B) LLM01 — Prompt injection
C) LLM06 — Sensitive information disclosure
D) LLM08 — Excessive agency

<details><summary>Answer</summary>

**B) LLM01 — Prompt injection**

LLM01 (Prompt injection) occurs when attacker-controlled data in the input — including indirect injection via documents or web pages — overrides the model's intended instructions. LLM02 (Insecure output handling) is when the model's output is passed unsanitized to a downstream system such as a shell or database. LLM06 involves the model leaking confidential data. LLM08 involves the model taking unauthorized actions due to excessive permissions.

</details>

---

**Q10.** A researcher needs a broad database that categorizes AI risks across dimensions including performance failures, misuse, and societal harms — not just adversarial attack techniques. Which resource best fits this need?

A) MITRE ATLAS
B) OWASP LLM Top 10
C) MIT AI Risk Repository
D) CVE AI Working Group

<details><summary>Answer</summary>

**C) MIT AI Risk Repository**

The MIT AI Risk Repository is a comprehensive research database that categorizes AI risks across multiple dimensions — including technical failures, misuse, and systemic societal harms. MITRE ATLAS focuses specifically on adversarial ML attack techniques. OWASP LLM Top 10 covers the top application-level security risks for LLMs. CVE AI Working Group focuses on enumerating AI-specific software vulnerabilities.

</details>

---

**Q11.** An organization wants a standardized identifier system to track and reference disclosed vulnerabilities specific to AI components — similar to how CVE IDs track traditional software vulnerabilities. Which initiative directly addresses this need?

A) MITRE ATLAS
B) MIT AI Risk Repository
C) OWASP LLM Top 10
D) CVE AI Working Group

<details><summary>Answer</summary>

**D) CVE AI Working Group**

The CVE AI Working Group extends the Common Vulnerabilities and Exposures (CVE) program to enumerate and track vulnerabilities specific to AI and ML systems — providing standardized identifiers for AI-related security issues. MITRE ATLAS catalogs adversarial attack techniques. MIT AI Risk Repository categorizes broad AI risk types. OWASP LLM Top 10 identifies top security risks in LLM applications.

</details>

---

**Q12.** A security team is applying a threat-modeling framework to an LLM-based application by analyzing each component for Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege threats. Which framework is being applied?

A) PASTA
B) STRIDE
C) MITRE ATLAS
D) LINDDUN

<details><summary>Answer</summary>

**B) STRIDE**

STRIDE is a threat-modeling framework developed by Microsoft that categorizes threats across six dimensions: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege. It can be applied to AI components just as it is applied to traditional software. PASTA is a risk-centric threat model framework. MITRE ATLAS is an adversarial AI knowledge base, not a threat-modeling framework. LINDDUN focuses on privacy threat modeling.

</details>

---

**Q13.** An LLM deployed for customer support is configured so that it will never disclose pricing tiers, employee names, or internal process details regardless of how the user phrases the request. This constraint is enforced by the model itself, not by an external filter. What type of control is this?

A) Prompt firewall
B) Model guardrail
C) Rate limit
D) Endpoint access control

<details><summary>Answer</summary>

**B) Model guardrail**

Model guardrails are constraints built into the model layer — via fine-tuning, RLHF, or system-level instruction adherence — that restrict what outputs the model will produce. They operate within the model, unlike prompt firewalls which intercept inputs externally. Rate limits control query frequency. Endpoint access controls govern which callers can reach the API.

</details>

---

**Q14.** A security team standardizes all user inputs to an AI system by wrapping them in a fixed structure that includes role definitions, scope restrictions, and disallowed topic lists before sending them to the model. Which control is being applied?

A) Prompt firewall
B) Model guardrail
C) Prompt template
D) Input quota

<details><summary>Answer</summary>

**C) Prompt template**

Prompt templates enforce a consistent, pre-approved structure for all inputs — reducing the attack surface for prompt injection by limiting where user-controlled text appears and bounding the context the model receives. Prompt firewalls filter malicious content from raw inputs. Model guardrails constrain outputs at the model layer. Input quotas restrict the volume or size of data submitted.

</details>

---

**Q15.** A company's public-facing AI chatbot is subjected to a flood of automated requests that exhaust GPU compute and prevent legitimate users from receiving responses. Which control would most directly mitigate this attack?

A) Token limit
B) Modality limit
C) Rate limiting
D) Prompt firewall

<details><summary>Answer</summary>

**C) Rate limiting**

Rate limiting caps the number of requests a caller or IP can make within a time window, directly mitigating denial-of-service and resource-exhaustion attacks against AI APIs. Token limits cap the size of individual requests but do not prevent a high volume of smaller requests. Modality limits restrict input types. Prompt firewalls filter malicious content, not request volume.

</details>

---

**Q16.** An attacker submits extremely long prompts containing thousands of words of adversarial context to overwhelm an AI model's attention window and manipulate its behavior. Which control best addresses this specific vector?

A) Rate limiting
B) Token limit
C) Input quota
D) Modality limit

<details><summary>Answer</summary>

**B) Token limit**

Token limits cap the maximum number of tokens allowed in a single input or output, preventing oversized prompts from consuming the model's full context window or enabling context-manipulation attacks. Rate limiting controls request frequency, not request size. Input quotas limit data volume over time. Modality limits restrict input types such as images or audio.

</details>

---

**Q17.** An organization's AI pipeline accepts file uploads as context for document summarization. A policy is implemented restricting each user to uploading no more than 10 MB of data per hour across all sessions. Which type of security control is this?

A) Token limit
B) Modality limit
C) Rate limit
D) Input quota

<details><summary>Answer</summary>

**D) Input quota**

Input quotas limit the total volume of data — by size, count, or quantity — that a user or session can submit within a period, distinct from per-request token limits. Token limits apply per individual request. Rate limits cap request frequency. Modality limits restrict input types (e.g., disabling file uploads entirely).

</details>

---

**Q18.** A security policy prohibits users from uploading images, audio files, or video to an AI assistant used for internal HR queries, restricting it to text-only inputs. What type of control enforces this restriction?

A) Input quota
B) Token limit
C) Modality limit
D) Prompt template

<details><summary>Answer</summary>

**C) Modality limit**

Modality limits restrict which input types (modalities) — such as text, images, audio, or video — an AI system will accept, reducing the attack surface for multi-modal injection and data exfiltration. Input quotas limit total data volume. Token limits cap text length. Prompt templates standardize the structure of text inputs.

</details>

---

**Q19.** A company deploys an AI inference API behind a gateway configured to allow requests only from a specific set of internal application servers identified by IP address and service account credentials. Which type of control is this?

A) Model guardrail
B) Prompt firewall
C) Endpoint access control
D) Modality limit

<details><summary>Answer</summary>

**C) Endpoint access control**

Endpoint access controls restrict which callers — identified by IP, credentials, or tokens — can reach the AI API endpoint, enforcing network and identity-based perimeter security. Model guardrails constrain model outputs. Prompt firewalls filter input content. Modality limits restrict input types, not which callers can connect.

</details>

---

**Q20.** Before deploying updates to an AI system's content filters and safety layers, a security team conducts structured adversarial testing by attempting to produce harmful outputs, bypass restrictions, and elicit policy violations using known attack techniques. What is this activity called?

A) Penetration testing
B) Guardrail testing
C) Bias auditing
D) Hallucination auditing

<details><summary>Answer</summary>

**B) Guardrail testing**

Guardrail testing (red-teaming model safety controls) specifically evaluates whether model guardrails, output filters, and safety layers hold up under adversarial attack attempts — confirming they cannot be bypassed. Penetration testing targets infrastructure. Bias auditing checks for discriminatory outputs. Hallucination auditing evaluates factual accuracy of model responses.

</details>

---

**Q21.** Prior to production deployment, an organization evaluates a new AI model by measuring its accuracy on held-out test sets, checking for demographic disparities in predictions, and verifying it does not reproduce training data verbatim. What is the primary security purpose of this evaluation?

A) Guardrail testing
B) Model evaluation as a security control
C) Hallucination auditing
D) Log monitoring

<details><summary>Answer</summary>

**B) Model evaluation as a security control**

Model evaluation before deployment serves as a security control by detecting bias, accuracy failures, memorization of sensitive training data, and behavioral anomalies before they reach production. Guardrail testing focuses on adversarial bypass attempts. Hallucination auditing tracks factual errors in ongoing production outputs. Log monitoring is a runtime detective control, not a pre-deployment evaluation.

</details>

---

**Q22.** A company wants to ensure that only its internal applications — and not external developers or third-party tools — can query its proprietary AI model API. Which control directly governs this?

A) Data access control
B) Model access control
C) Agent access control
D) Modality limit

<details><summary>Answer</summary>

**B) Model access control**

Model access controls govern which users, services, or applications are authorized to call or interact with the AI model — restricting access to the model itself. Data access controls restrict access to training or inference data. Agent access controls limit what actions AI agents can take. Modality limits restrict input types, not who can call the model.

</details>

---

**Q23.** A healthcare organization stores patient records used to train its AI diagnostic model. It implements controls ensuring that only the data science team can access records labeled "PHI" while other teams can only access anonymized training sets. Which principle is being applied?

A) Least privilege
B) Data access control
C) Model access control
D) Agent access control

<details><summary>Answer</summary>

**B) Data access control**

Data access controls segment access to training and inference data by sensitivity classification — ensuring only authorized roles can access sensitive datasets. Least privilege is the broader principle that underpins access control policy. Model access controls restrict access to the model endpoint. Agent access controls limit the actions AI agents can take on external systems.

</details>

---

**Q24.** An AI agent deployed to automate IT operations is granted only the minimum set of API permissions required to restart specific services — not to delete VMs, modify network rules, or access production databases. Which security principle governs this design?

A) Defense in depth
B) Separation of duties
C) Least privilege
D) Zero trust

<details><summary>Answer</summary>

**C) Least privilege**

Applying least privilege to AI agents means granting only the permissions strictly required for the agent's defined task — limiting the blast radius if the agent is compromised or manipulated via prompt injection. Defense in depth layers multiple controls. Separation of duties divides tasks among multiple actors. Zero trust requires continuous verification but is broader than permission scoping.

</details>

---

**Q25.** A development team issues long-lived API keys with full permissions to several LLM endpoints, shares them across multiple services, and never rotates them. A security review flags this as a violation of which control category?

A) Prompt firewall
B) API access control
C) Modality limit
D) Rate limiting

<details><summary>Answer</summary>

**B) API access control**

API access controls include key lifecycle management — issuing scoped, rotated credentials and avoiding shared secrets. Long-lived, over-privileged, shared API keys violate API access control best practices and increase the impact of credential compromise. Prompt firewalls filter input content. Modality limits restrict input types. Rate limiting controls request volume.

</details>

---

**Q26.** A security architect reviewing an AI agent design recommends removing the agent's ability to send emails, create calendar events, and post to Slack — capabilities the agent has never used in production. This recommendation directly reduces which OWASP LLM risk?

A) Overreliance
B) Sensitive information disclosure
C) Excessive agency
D) Insecure plugin design

<details><summary>Answer</summary>

**C) Excessive agency**

Removing unused capabilities from an AI agent applies least privilege to directly reduce excessive agency risk — limiting what actions the agent can take if its instructions are manipulated. Overreliance involves trusting AI outputs without verification. Sensitive information disclosure involves leaking confidential data. Insecure plugin design involves vulnerabilities in plugin interfaces.

</details>

---

**Q27.** An organization building a training dataset for an AI model tags each data record with one of four sensitivity levels — Public, Internal, Confidential, and Restricted — to guide access decisions and processing rules. What practice does this implement?

A) Data minimization
B) Data masking
C) Data classification labeling
D) Pseudonymization

<details><summary>Answer</summary>

**C) Data classification labeling**

Data classification labels assign sensitivity tiers to data records, enabling access controls, encryption requirements, and handling rules to be enforced based on the data's sensitivity level. Data minimization limits the volume of data collected. Data masking replaces real values with fictitious ones. Pseudonymization replaces identifiers with pseudonyms while preserving data utility.

</details>

---

**Q28.** A data preparation pipeline replaces real customer account numbers with randomly generated fictitious numbers before the dataset is used for AI model training. If the original values need to be retrieved, a separate lookup table is maintained. Which technique is this?

A) Anonymization
B) Data redaction
C) Data masking
D) Hashing

<details><summary>Answer</summary>

**C) Data masking**

Data masking replaces real values with fictitious but structurally consistent substitutes — preserving the data's format for testing or training while protecting real values. The key distinction from anonymization is that masking may be reversible via a lookup table. Anonymization is irreversible. Data redaction removes or blacks out values entirely. Hashing produces a one-way digest, not a substitute value.

</details>

---

**Q29.** A data engineering team replaces all customer names in an AI training dataset with randomly assigned codes (e.g., "CUST-4821"), while retaining a separate encrypted mapping table that can re-link codes to real names if legally required. Which data protection technique is this?

A) Anonymization
B) Pseudonymization
C) Data masking
D) Tokenization

<details><summary>Answer</summary>

**B) Pseudonymization**

Pseudonymization replaces direct identifiers with pseudonyms while maintaining a reversible link via a separate key or mapping — making re-identification possible under controlled conditions. This distinguishes it from anonymization, which is irreversible. Data masking replaces values with fictitious ones. Tokenization substitutes sensitive values with non-sensitive tokens typically managed by a vault, and may or may not preserve reversibility.

</details>

---

**Q30.** A team building a fraud-detection AI model is advised to collect only transaction amount, timestamp, and merchant category for training — not full cardholder names, billing addresses, or phone numbers — since those fields are not needed for the model's predictions. Which data security principle does this advice apply?

A) Data pseudonymization
B) Data redaction
C) Data classification
D) Data minimization

<details><summary>Answer</summary>

**D) Data minimization**

Data minimization limits data collection to only what is strictly necessary for the intended purpose — reducing privacy risk, limiting what a compromised model could expose, and shrinking the sensitive data footprint in training pipelines. Pseudonymization replaces identifiers. Redaction removes values from existing data. Classification labels data by sensitivity but does not reduce what is collected.

</details>

---

**Q31.** A company stores its fine-tuned proprietary AI model weights on a cloud storage volume. A policy requires that the weight files be encrypted using AES-256 when not being accessed by the training or inference service. Which requirement applies?

A) Encryption in transit
B) Encryption in use
C) Encryption at rest
D) Homomorphic encryption

<details><summary>Answer</summary>

**C) Encryption at rest**

Encryption at rest protects data stored on disk or in object storage — including AI model weight files — when they are not being actively read or processed. Encryption in transit protects data moving across networks. Encryption in use protects data during active computation, typically via trusted execution environments. Homomorphic encryption allows computation on ciphertext.

</details>

---

**Q32.** An organization processes highly sensitive legal documents inside an AI inference pipeline and requires that plaintext data never be exposed to the cloud hypervisor or other tenants — even during active computation. Which technology satisfies this requirement?

A) TLS 1.3
B) AES-256 at rest
C) Trusted execution environment
D) Differential privacy

<details><summary>Answer</summary>

**C) Trusted execution environment**

A trusted execution environment (TEE) — such as Intel SGX or AMD SEV — provides hardware-enforced isolation that keeps data encrypted and inaccessible to the hypervisor or host OS even while it is being actively processed, implementing encryption in use. TLS 1.3 protects data in transit. AES-256 at rest protects stored data. Differential privacy adds noise to outputs to protect individual records statistically.

</details>

---

**Q33.** A medical AI assistant generates discharge summaries that contain patient names and diagnosis codes in its output. Before these summaries are logged and stored, a post-processing step scans them and removes or blacks out any detected PII. Which control is this?

A) Data masking
B) Pseudonymization
C) Data redaction
D) Anonymization

<details><summary>Answer</summary>

**C) Data redaction**

Data redaction removes or blanks out sensitive values from output text — preventing PII from being persisted in logs or downstream systems. Unlike masking, which substitutes fictitious values, redaction eliminates the value entirely. Pseudonymization replaces identifiers with coded pseudonyms. Anonymization irreversibly removes identifiers from source datasets, typically before training rather than in live outputs.

</details>

---

**Q34.** Researchers demonstrate that by querying a deployed language model with targeted prompts, they can recover verbatim sentences from the model's training corpus, including personal emails. Which attack is being demonstrated, and what controls best prevent it?

A) Model inversion; output filtering and rate limiting
B) Membership inference; differential privacy and data minimization
C) Training data extraction; data minimization and anonymization
D) Model theft; API key rotation and endpoint access controls

<details><summary>Answer</summary>

**C) Training data extraction; data minimization and anonymization**

Training data extraction (a form of data leakage) recovers verbatim training samples from model outputs via targeted queries. The primary mitigations are data minimization — reducing how much sensitive data enters training — and anonymization — removing personal identifiers before training so they cannot be extracted. Membership inference determines if a record was in training data but does not recover content. Model inversion reconstructs input features from outputs.

</details>

---

**Q35.** An organization deploying a customer-facing AI chatbot implements a system that logs the full text of every user query sent to the model for security review and incident response. What monitoring control is this?

A) Log sanitization
B) Prompt monitoring
C) Response confidence level monitoring
D) Hallucination auditing

<details><summary>Answer</summary>

**B) Prompt monitoring**

Prompt monitoring logs and inspects all queries (prompts) submitted to the AI system, enabling detection of injection attempts, policy violations, and anomalous patterns in user inputs. Log sanitization removes sensitive data from existing logs. Response confidence level monitoring tracks model certainty scores. Hallucination auditing evaluates factual accuracy of model outputs.

</details>

---

**Q36.** An AI system's query logs are found to contain customer credit card numbers and session tokens submitted in user prompts. A remediation task removes these values from stored logs before they are forwarded to the SIEM. Which control is being applied?

A) Log protection
B) Prompt monitoring
C) Log sanitization
D) Data redaction in outputs

<details><summary>Answer</summary>

**C) Log sanitization**

Log sanitization removes or masks sensitive data — such as PII, credentials, or payment card numbers — from AI system logs before they are stored or forwarded, limiting exposure if logs are accessed. Log protection prevents tampering with logs after they are written. Prompt monitoring captures all queries for review. Data redaction in outputs removes PII from model-generated responses.

</details>

---

**Q37.** After a security incident, an investigation team discovers that audit logs for an AI system were deleted by a threat actor who had gained write access to the logging infrastructure. Which control should have been implemented to prevent this?

A) Log sanitization
B) Rate monitoring
C) Log protection
D) Prompt monitoring

<details><summary>Answer</summary>

**C) Log protection**

Log protection prevents unauthorized modification or deletion of audit logs — typically through write-once storage, append-only log streams, cryptographic integrity checks, or forwarding logs to an immutable SIEM. Log sanitization removes sensitive content from logs. Rate monitoring detects anomalous query volumes. Prompt monitoring captures query content.

</details>

---

**Q38.** A security analyst notices a sudden spike in token consumption and API costs for a company's AI service that coincides with no corresponding increase in legitimate user activity. The analyst flags this as a potential abuse indicator. Which monitoring control surfaced this signal?

A) Hallucination auditing
B) Bias auditing
C) AI cost monitoring
D) Response confidence level monitoring

<details><summary>Answer</summary>

**C) AI cost monitoring**

AI cost monitoring tracks token usage, compute consumption, and API billing — and when costs spike without a corresponding business justification, it serves as a security signal indicating scraping, model extraction attempts, DoS, or unauthorized use. Hallucination auditing tracks factual accuracy. Bias auditing detects discriminatory outputs. Response confidence monitoring tracks certainty scores.

</details>

---

**Q39.** An AI-powered legal research assistant is found to be generating case citations that do not exist. The security team implements a process to regularly sample model outputs, verify factual claims against authoritative sources, and track the error rate over time. Which monitoring control is this?

A) Bias auditing
B) Hallucination auditing
C) Response confidence level monitoring
D) Prompt monitoring

<details><summary>Answer</summary>

**B) Hallucination auditing**

Hallucination auditing systematically measures and tracks the rate at which an AI model generates fabricated or factually incorrect outputs — enabling teams to detect model degradation, distribution shift, or adversarial manipulation that increases hallucination rates. Bias auditing examines demographic disparities in outputs. Response confidence monitoring tracks the model's self-reported certainty. Prompt monitoring logs incoming queries.

</details>

---

**Q40.** A financial services company running an AI-based loan approval system discovers that the model denies loans at a significantly higher rate for applicants from specific ZIP codes that correlate with racial demographics. The company implements monthly statistical testing of approval rates across demographic groups. Which monitoring control is this?

A) Hallucination auditing
B) Response confidence level monitoring
C) AI cost monitoring
D) Bias and fairness auditing

<details><summary>Answer</summary>

**D) Bias and fairness auditing**

Bias and fairness auditing systematically measures whether an AI model produces discriminatory or disparate-impact outcomes across demographic groups — a critical security and compliance control for high-stakes AI systems. Hallucination auditing tracks factual errors. Response confidence monitoring tracks certainty scores. AI cost monitoring tracks resource consumption.

</details>

---

**Q41.** A company's AI governance policy requires maintaining a record of every user identity, timestamp, and model endpoint accessed for all queries to its internal AI systems, reviewed monthly for unauthorized access. Which monitoring activity does this describe?

A) Prompt monitoring
B) Hallucination auditing
C) Access auditing
D) Log sanitization

<details><summary>Answer</summary>

**C) Access auditing**

Access auditing records who accessed the AI model, when, and via which endpoint — enabling detection of unauthorized access, privilege escalation, and insider threats. Prompt monitoring logs the content of queries. Hallucination auditing evaluates factual correctness of outputs. Log sanitization removes sensitive data from logs rather than reviewing them.

</details>

---

**Q42.** A monitoring system alerts the security team when any single API client exceeds 500 queries per minute to the AI inference endpoint — a pattern consistent with model scraping or automated extraction. Which monitoring control triggered this alert?

A) AI cost monitoring
B) Rate monitoring
C) Response confidence level monitoring
D) Prompt monitoring

<details><summary>Answer</summary>

**B) Rate monitoring**

Rate monitoring detects anomalously high query volumes from a single source — a pattern that indicates model extraction (scraping), denial-of-service attempts, or automated abuse. AI cost monitoring tracks aggregate compute spend. Response confidence monitoring tracks certainty scores. Prompt monitoring records query content.

</details>

---

**Q43.** A threat actor implants a hidden trigger in an AI image-classification model during the training process. The model performs normally on all inputs except those containing a specific watermark pattern, which causes it to misclassify malware as benign. Which attack type is this, and which controls best detect it?

A) Data poisoning; input validation and rate limiting
B) Backdoor/trojan attack; model auditing and adversarial testing
C) Model inversion; differential privacy and output filtering
D) Jailbreaking; guardrail testing and prompt firewalls

<details><summary>Answer</summary>

**B) Backdoor/trojan attack; model auditing and adversarial testing**

A backdoor (trojan) attack embeds a hidden trigger during training that causes specific malicious behavior only when the trigger pattern is present, while appearing normal otherwise. Detection requires model auditing — inspecting model behavior and weights — and adversarial testing with trigger-pattern candidates. Data poisoning corrupts training data without a specific trigger. Jailbreaking bypasses safety filters at inference time.

</details>

---

**Q44.** A user crafts an elaborate multi-turn conversation in which they gradually reframe the AI assistant's persona and instructions, eventually causing the model to produce content that its built-in safety filters would normally block. Which attack is being performed, and what controls mitigate it?

A) Prompt injection; input sanitization and token limits
B) Jailbreaking; guardrail testing and prompt firewalls
C) Data poisoning; model auditing and retraining
D) Membership inference; differential privacy

<details><summary>Answer</summary>

**B) Jailbreaking; guardrail testing and prompt firewalls**

Jailbreaking uses crafted prompts — including persona manipulation, role-play framing, and multi-turn escalation — to bypass model safety filters and elicit policy-violating outputs. Mitigations include prompt firewalls (external input filtering) and guardrail testing (verifying safety controls hold under adversarial conditions). Prompt injection involves overriding system instructions. Data poisoning corrupts training data. Membership inference queries training set membership.

</details>

---

**Q45.** An attacker queries a healthcare AI model with a large set of records and determines, with statistically significant confidence, which patient records were included in the model's training dataset — without accessing the dataset directly. Which attack is this, and what is the primary technical control?

A) Training data extraction; data minimization and anonymization
B) Model inversion; encryption at rest
C) Membership inference; differential privacy
D) Model theft; API key rotation

<details><summary>Answer</summary>

**C) Membership inference; differential privacy**

Membership inference attacks exploit the statistical difference in how a model responds to records it was trained on versus records it was not. Differential privacy adds calibrated mathematical noise to the training process or outputs, making it statistically indistinguishable whether any individual record was in the training set. Training data extraction recovers verbatim content. Model inversion reconstructs input features. Model theft builds a surrogate model.

</details>

---

**Q46.** An AI chatbot generates SQL queries that are passed directly to a database engine without validation. An attacker crafts a prompt that causes the model to output a DROP TABLE statement, which is then executed. Which risk category does this represent, and what is the primary control?

A) Excessive agency; least privilege for agent permissions
B) Prompt injection; input sanitization
C) Insecure output handling; output validation and sanitization
D) Overreliance; human-in-the-loop review

<details><summary>Answer</summary>

**C) Insecure output handling; output validation and sanitization**

Insecure output handling (OWASP LLM02) occurs when AI-generated output is passed unsanitized to a downstream interpreter — such as a database, shell, or browser — enabling injection attacks. The control is output validation: treating AI outputs as untrusted input to downstream systems and sanitizing or restricting them before execution. Excessive agency is about unauthorized actions. Prompt injection attacks the input layer.

</details>

---

**Q47.** A threat actor who has compromised an AI system's feedback loop submits large volumes of manipulated responses designed to shift the model's future outputs toward results that benefit the attacker's interests. Which attack is this, and what control helps detect it?

A) Data poisoning; training data provenance checks
B) Model skewing; output integrity monitoring
C) Backdoor attack; adversarial testing
D) Jailbreaking; guardrail testing

<details><summary>Answer</summary>

**B) Model skewing; output integrity monitoring**

Model skewing shifts the statistical distribution of model outputs over time toward attacker-preferred results — often through poisoned feedback, RLHF manipulation, or online learning exploitation. Output integrity monitoring detects drift in output distributions and biases that deviate from a known-good baseline. Data poisoning corrupts training data before model deployment. Backdoor attacks implant trigger-based behavior.

</details>

---

**Q48.** A company downloads a popular open-source LLM from a public model repository and integrates it into their product. Months later, researchers discover the model weights had been replaced with a malicious version containing backdoor behavior. Which attack category does this represent, and what is the primary preventive control?

A) Backdoor attack; model auditing and red-teaming
B) Data poisoning; training data validation
C) AI supply chain attack; model provenance verification
D) Model theft; endpoint access controls

<details><summary>Answer</summary>

**C) AI supply chain attack; model provenance verification**

An AI supply chain attack compromises a model, dataset, or component upstream of the consuming organization — for example, by replacing legitimate model weights in a public repository with a trojaned version. Model provenance verification — checking cryptographic signatures, hashes, and the chain of custody for model artifacts before integration — is the primary preventive control. Backdoor attack describes the payload, but the delivery mechanism here is supply chain compromise.

</details>

---
