# SecAI+ Key Concepts Flashcards

## AI Fundamentals (Objective 1.1)

**Generative AI** → AI that creates new content (text, images, audio, code) by learning patterns from training data. | Creates, not just classifies

**Discriminative model** → An AI model that learns to distinguish between classes (e.g., malware vs. benign) rather than generate new content. | Judges what something is; doesn't create

**Transformer** → Neural network architecture using attention mechanisms to process sequences in parallel; foundation of modern LLMs. | The architecture behind GPT, BERT, and friends

**GAN** → Two-network system (generator + discriminator) that trains by competing; used to generate realistic synthetic data and deepfakes. | Artist vs. art critic training each other

**LLM** → A large-scale transformer model trained on vast text data to generate, complete, or transform language. | GPT, Claude, Gemini — "large" refers to parameter count

**SLM** → A smaller language model optimized for efficiency and edge deployment with fewer parameters than an LLM. | LLM on a diet — less capable but faster and cheaper

**NLP** → The AI field enabling computers to understand, interpret, and generate human language. | The umbrella that covers LLMs, sentiment analysis, and translation

**Supervised learning** → ML trained on labeled input-output pairs to predict outputs for new inputs. | Teacher provides answer key; model learns from it

**Unsupervised learning** → ML that finds patterns or clusters in unlabeled data without predefined output labels. | No answer key — model discovers structure itself

**Reinforcement learning** → ML trained via reward/penalty signals where an agent learns by taking actions in an environment. | Reward good behavior, penalize bad — like training a dog

**Federated learning** → Distributed ML where models train locally on devices and share only gradients, not raw data. | Train together, share only the math, not the data

**Fine-tuning** → Continuing to train a pre-trained model on a smaller task-specific dataset to specialize its behavior. | Foundation coat + specialized top coat

**Epoch** → One complete pass through the entire training dataset during model training. | One lap around the training track

**Pruning** → Removing low-importance weights from a neural network to reduce size and improve inference speed. | Trimming dead branches from the model tree

**Quantization** → Reducing numerical precision of model weights (e.g., 32-bit → 8-bit) to shrink model size and speed up inference. | Lower resolution = smaller file, similar quality

**Model validation** → Evaluating a model on a held-out dataset during training to tune hyperparameters and detect overfitting. | The dress rehearsal before the final exam

**Overfitting** → A model that memorizes training data (including noise) and generalizes poorly to new inputs. | Studying the answer key instead of the material

**Zero-shot prompting** → Prompting an LLM to perform a task with no examples provided. | Figure it out yourself

**One-shot prompting** → Providing a single example in the prompt to guide the model's response format or behavior. | One example before the real question

**Multi-shot prompting** → Providing multiple examples in the prompt to establish a clear pattern for the model. | Several examples = clearer expectation

**System prompt** → Instructions placed before the conversation that configure the model's persona, constraints, and behavior. | The model's job description, set by the app developer

**User prompt** → The input provided by the end user at inference time that the model responds to. | The question the user actually asks

**Prompt template** → A reusable, structured prompt with defined format and placeholders, used to standardize AI interactions. | Mad-libs for AI inputs

## Data Security in AI (Objective 1.2)

**Data provenance** → A record of where data originated and all transformations applied before use. | The data's birth certificate and travel history

**Data lineage** → End-to-end tracking of data as it moves through systems and transformations in a pipeline. | The data's complete family tree

**Data integrity** → Assurance that data has not been altered in an unauthorized or unintended way. | It is what it says it is

**Data augmentation** → Generating additional synthetic training samples to expand a dataset (e.g., image flipping, synonym replacement). | Growing the training set without collecting more real data

**Data balancing** → Adjusting class distribution in a training dataset to reduce model bias toward majority classes. | Evening the playing field for minority classes

**Watermarking** → Embedding a detectable (possibly invisible) signal in AI-generated content to identify its source or ownership. | Invisible signature on AI-generated output

**RAG** → Architecture that enhances LLM responses by retrieving relevant documents from a vector store at query time. | Look it up before answering — grounds the LLM in current data

**Embedding** → A dense numerical vector representing a token, phrase, or document in a high-dimensional space. | Words as coordinates — similar meanings cluster together

**Vector storage** → A database optimized for storing and querying high-dimensional embeddings used in RAG and semantic search. | The library where embeddings live

**Structured data** → Data organized in a predefined schema with fixed fields (e.g., relational database tables, CSV files). | Rows and columns — the data fits neatly in a spreadsheet

**Semi-structured data** → Data with some organization but no fixed schema (e.g., JSON, XML, YAML). | Organized but flexible — has keys and values, no rigid table

**Unstructured data** → Data with no predefined format (e.g., images, audio, raw text, binary files). | No schema, no table — free-form content

## AI Lifecycle Security (Objective 1.3)

**AI lifecycle** → The end-to-end process of building and operating an AI system: business use case → data collection → data preparation → model development → evaluation → deployment → monitoring → iteration. | The AI development assembly line

**Human-in-the-loop** → A design requiring human review and approval before an AI system takes consequential actions. | AI proposes; human approves

**Human oversight** → Ongoing monitoring of AI system behavior by humans to detect failures, drift, or misuse. | The supervisor who watches the AI work — after the fact

**Model drift** → Degradation in model performance over time as real-world data distribution shifts away from training data. | The model falls behind changing reality

**MLOps** → Practices for operationalizing ML models — automating training, deployment, monitoring, and retraining pipelines. | DevOps applied to ML — the answer when drift hits

## Threat Modeling (Objective 2.1)

**MITRE ATLAS** → MITRE's knowledge base of adversarial ML attack techniques, analogous to ATT&CK for AI systems. | ATT&CK's AI-specific cousin

**OWASP LLM Top 10** → OWASP's list of the 10 most critical security risks in LLM-based applications. | OWASP Top 10 but for chatbots and AI APIs

**MIT AI Risk Repository** → MIT research database cataloging AI risks across ethical, technical, and societal dimensions. | Academic risk catalog for AI

**CVE AI Working Group** → An initiative extending the CVE program to enumerate and track AI-specific vulnerabilities. | CVE program adapted for AI flaws

## AI Attacks (Objective 2.6)

**Prompt injection** → Embedding malicious instructions in user input to override the LLM's system prompt or intended behavior. | SQL injection but for LLMs

**Jailbreaking** → Using crafted prompts (role-play, encoding, multi-turn) to bypass an LLM's safety filters. | Lock-picking the AI's guardrails

**Data poisoning** → Corrupting training data to cause the model to learn incorrect behavior. | Poisoning the well before anyone drinks

**Model poisoning** → Directly manipulating model weights or training process to insert backdoors or degrade performance. | Tampering with the model itself, not its data

**Backdoor attack** → Poisoning a model to behave normally except when a specific trigger input is present, revealing attacker-controlled behavior. | Hidden switch only the attacker knows

**Model inversion** → Reconstructing training data samples from model outputs or gradients — a privacy attack. | Running the model in reverse to recover its memories

**Training data extraction** → A variant of model inversion where exact training samples are recovered from model outputs. | Tricking the model into quoting its training data verbatim

**Model theft** → Extracting a model's behavior by querying its API and training a local surrogate. | Building a copy by asking enough questions

**Membership inference** → Determining whether a specific record was included in a model's training set. | Was my medical record used to train this model?

**Excessive agency** → An AI agent granted more permissions or capabilities than necessary for its intended task. | AI with too many keys to too many doors

**Overreliance** → Users or systems trusting AI outputs without appropriate human verification or skepticism. | The AI said so, so it must be right

**Insecure output handling** → Failing to sanitize AI-generated outputs before passing them to downstream systems (e.g., SQL, HTML, shell). | AI output → shell command with no sanitization = RCE

**AI supply chain attack** → Compromising model weights, datasets, or dependencies before they reach the organization. | Poisoning the package before delivery

**Model skewing** → Manipulating an AI model to shift its outputs in a direction that benefits the attacker. | Nudging the model's compass

**Transfer learning attack** → Exploiting knowledge embedded in a pre-trained model when it is fine-tuned for a new task. | Trojan horse hidden in the foundation model

**Model DoS** → Overwhelming an AI system with computationally expensive or repeated requests to degrade or deny service. | DDoS but for inference endpoints

**Hallucination** → An LLM generating plausible-sounding but factually incorrect or fabricated content. | Confident lies — the model fills gaps with invention

## Security Controls for AI (Objective 2.2–2.5)

**Model guardrail** → A control built into or around a model to constrain its outputs and prevent harmful, off-topic, or policy-violating responses. | Bumpers on the AI's bowling lane

**Prompt firewall** → A gateway-layer filter that intercepts and blocks malicious or policy-violating prompts before they reach the model. | WAF for LLM inputs

**Rate limiting** → Restricting the number of requests a client can make to an AI API in a given time window. | Speed bumps on the AI highway

**Token limit** → A cap on the number of tokens in a single request or response, preventing abuse and controlling costs. | Turns off the tap after N words

**Input quota** → A control limiting the volume or size of data submitted to an AI system per session or time period. | Portion control for AI inputs

**Modality limit** → A control restricting the types of input (e.g., text only, no image or audio uploads) an AI system accepts. | Only accepts text — no image attachments allowed

**Endpoint access control** → Restricting which systems, users, or roles can invoke an AI model's API endpoint. | The bouncer at the AI API door

**Guardrail testing** → Proactively testing model guardrails with adversarial inputs to verify they hold under attack. | Red-teaming the AI's guardrails

**Response confidence level** → A monitoring metric tracking how certain a model is about its outputs; anomalies may indicate adversarial inputs or drift. | The model's self-reported certainty — watch for suspiciously high or low values

**Log sanitization** → Removing or masking sensitive data (PII, credentials, tokens) from AI system logs before storage or transmission. | Scrubbing the AI's diary before filing it

**AI cost monitoring** → Tracking token usage, compute costs, and API call volumes as both a financial and security control signal. | High spend = possible abuse or model DoS

## Data Protection Controls (Objective 2.4)

**Anonymization** → Irreversibly removing or replacing personal identifiers from data so individuals cannot be re-identified. | One-way street — identity cannot be recovered

**Pseudonymization** → Replacing personal identifiers with pseudonyms that can be reversed with a separate key. | Reversible anonymization — the key unlocks real identity

**Data masking** → Replacing real data values with realistic but fictitious substitutes while preserving format. | Fake data that looks real — used in non-production environments

**Data redaction** → Blacking out or removing specific sensitive fields from data or documents. | The black bar over classified information

**Data minimization** → Collecting and retaining only the data necessary for a specific, defined purpose. | If you don't need it, don't collect it

**Encryption in transit** → Protecting data from interception while it moves between systems (e.g., TLS). | A sealed envelope for data crossing networks

**Encryption at rest** → Protecting stored data from unauthorized access (e.g., AES encryption of database files). | A locked safe for data sitting still

**Encryption in use** → Protecting data while it is actively being processed (e.g., via trusted execution environments). | A secure room where data can be worked on without being seen

## AI-assisted Security (Objective 3.1–3.3)

**MCP server** → A server that exposes tools and resources to AI agents via the Model Context Protocol, enabling agentic workflows. | The AI's API to the outside world

**SOAR** → Security Orchestration, Automation, and Response — automates security workflows and playbooks using AI. | AI-powered incident response dispatcher

**SCA** → Software Composition Analysis — automated scanning of open-source dependencies for known vulnerabilities. | What's in your code's supply chain?

**AI agent** → An autonomous AI system that perceives inputs, reasons about them, uses tools, and takes actions to accomplish goals. | AI that acts, not just responds

**Deepfake** → AI-generated synthetic media (video, audio, image) that convincingly portrays a real person saying or doing something they did not. | Synthetic impersonation — the AI forgery

**Disinformation** → Deliberately false or manipulated content spread with the intent to deceive. | Intentional lies at scale — a coordinated deception campaign

**Misinformation** → False content spread without malicious intent, often due to the sharer not knowing it is incorrect. | Accidental lies — no intent to deceive

**Impersonation** → Using AI-generated content to convincingly portray a specific real person in order to deceive targets. | The deepfake with a victim in mind

## Governance and Compliance (Objective 4.1–4.3)

**AI Center of Excellence** → A centralized organizational body that sets AI standards, best practices, governance policies, and oversight for AI initiatives. | AI's internal standards body

**Shadow AI** → Unauthorized use of AI tools by employees outside organizational governance and visibility. | Shadow IT but for AI — the unsanctioned chatbot everyone's using

**NIST AIRMF** → NIST's AI Risk Management Framework with four functions: Govern, Map, Measure, Manage. | The AI risk playbook — Govern/Map/Measure/Manage

**EU AI Act** → EU regulation classifying AI systems by risk tier (unacceptable, high, limited, minimal) with obligations per tier. | GDPR's AI sibling — risk tiers drive obligations

**OECD AI Principles** → International principles for responsible AI development: inclusive growth, human-centered values, transparency, robustness, accountability. | The G7+ nations' shared AI rulebook

**Data sovereignty** → The concept that data is subject to the laws and governance of the country where it is collected or processed. | Data follows the flag of where it lives

**Sanctioned AI** → AI tools formally approved and governed by organizational policy. | The official, approved AI tool

**Unsanctioned AI** → AI tools used without organizational review or approval. | The AI tool no one knows you're using

**Explainability (XAI)** → The ability to explain, in human-understandable terms, why an AI model made a specific decision. | Show your work — required for trust and audits

**Differential privacy** → A mathematical privacy technique that adds calibrated noise to data or model outputs to prevent individual re-identification. | Plausible deniability built into the math

**AI auditor** → A role responsible for independently assessing AI systems for compliance, fairness, accuracy, and adherence to governance policies. | The AI's independent reviewer

**AI governance engineer** → A role responsible for implementing and maintaining the technical controls and frameworks that enforce AI governance policies. | Builds the guardrails the AI auditor checks

**MLOps engineer** → A role that manages the operational lifecycle of ML models — training, deployment, monitoring, and retraining pipelines. | DevOps engineer for the model factory

**AI security architect** → A role responsible for designing security controls that protect AI systems from adversarial attacks, misuse, and data breaches. | Security architect specializing in AI attack surfaces

**AI risk analyst** → A role that identifies, assesses, and quantifies risks in AI deployments before and during production. | Risk manager focused on AI failure modes

**Introduction of bias** → AI producing unfair or discriminatory outputs due to skewed or unrepresentative training data. | The model learned the world's prejudices from its training data

**Reputational loss** → Organizational damage to trust and brand resulting from a public AI failure or misuse. | When the AI embarrasses the company in public

**Accidental data leakage** → Unintended exposure of sensitive information through AI model outputs or system misconfigurations. | The model revealing secrets it learned in training
