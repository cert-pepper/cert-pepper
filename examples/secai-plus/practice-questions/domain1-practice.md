# Domain 1 Practice Questions — Basic AI Concepts Related to Cybersecurity

---

**Q1.** A machine learning model performs well on training data but poorly on new, unseen data. What term describes this condition?

A) Underfitting
B) Overfitting
C) Regularization
D) Quantization

<details><summary>Answer</summary>

**B) Overfitting**

Overfitting occurs when a model memorizes training data — including noise — instead of learning generalizable patterns. It shows high training accuracy but poor performance on unseen data. Underfitting is the opposite: the model is too simple to capture patterns even in training data. Quantization reduces model precision to improve efficiency and is unrelated.

</details>

---

**Q2.** An AI model generates a confident, factually incorrect response about a recent security incident that never occurred. What AI behavior does this represent?

A) Overfitting
B) Adversarial example
C) Hallucination
D) Model inversion

<details><summary>Answer</summary>

**C) Hallucination**

Hallucination is when an LLM generates plausible-sounding but factually incorrect or fabricated content. Unlike adversarial examples (crafted inputs designed to fool a model), hallucinations arise from statistical patterns in training data and gaps in grounding. Model inversion reconstructs training data from model outputs.

</details>

---

**Q3.** Which machine learning paradigm trains a model using labeled input-output pairs to predict outcomes for new inputs?

A) Unsupervised learning
B) Reinforcement learning
C) Supervised learning
D) Federated learning

<details><summary>Answer</summary>

**C) Supervised learning**

Supervised learning uses labeled training data — pairs of inputs and known correct outputs — to train a model to map inputs to outputs. Unsupervised learning finds patterns in unlabeled data. Reinforcement learning trains through reward signals, not labeled pairs. Federated learning is a distributed training approach, not a learning paradigm itself.

</details>

---

**Q4.** Which of the following best describes reinforcement learning in a cybersecurity context?

A) Using AI to cluster network events based on unlabeled behavioral patterns
B) Using AI to classify malware samples based on labeled features
C) Using AI to optimize intrusion detection thresholds based on reward feedback
D) Using AI to summarize phishing alerts based on NLP models

<details><summary>Answer</summary>

**C) Using AI to optimize intrusion detection thresholds based on reward feedback**

Reinforcement learning trains an agent through reward and penalty signals — the agent takes actions, receives feedback, and updates its policy to maximize cumulative reward. Adjusting IDS thresholds based on detection outcomes (reward = correct detection, penalty = false positive) is the RL pattern. Option A describes unsupervised learning; Option B describes supervised learning.

</details>

---

**Q5.** A security team wants to reduce a large language model's size for deployment on an edge device while preserving most of its accuracy. Which fine-tuning technique reduces numerical precision of model weights to achieve this?

A) Pruning
B) Quantization
C) Distillation
D) Regularization

<details><summary>Answer</summary>

**B) Quantization**

Quantization reduces the numerical precision of model weights (e.g., from 32-bit float to 8-bit integer), shrinking model size and speeding up inference with minimal accuracy loss. Pruning removes weights that contribute little to model outputs. Distillation trains a smaller student model on the outputs of a larger teacher model — a different technique altogether.

</details>

---

**Q6.** A prompt submitted to an LLM without any examples of the expected output format relies on what prompting technique?

A) One-shot prompting
B) Multi-shot prompting
C) Zero-shot prompting
D) System role prompting

<details><summary>Answer</summary>

**C) Zero-shot prompting**

Zero-shot prompting asks the model to perform a task with no examples. One-shot provides a single example; multi-shot provides several. System role prompting sets the model's persona via the system prompt — a separate concept from the number of examples.

</details>

---

**Q7.** A data engineer discovers that the training dataset for a fraud detection model lacks documentation about where the data originated and how it was transformed before use. Which data security concept is missing?

A) Data balancing
B) Data augmentation
C) Data provenance
D) Data integrity

<details><summary>Answer</summary>

**C) Data provenance**

Data provenance documents the origin of data, who collected it, and all transformations applied before use. Without provenance, the organization cannot verify the data's trustworthiness or detect supply chain tampering. Data integrity confirms data has not been altered; data augmentation synthetically expands a dataset.

</details>

---

**Q8.** An organization uses a system where an LLM retrieves relevant documents from a vector database at query time to improve response accuracy. What technique does this describe?

A) Fine-tuning
B) Federated learning
C) RAG
D) Transfer learning

<details><summary>Answer</summary>

**C) RAG**

Retrieval-augmented generation (RAG) combines a generative model with a retrieval step — documents are embedded into a vector store, and at query time the most relevant chunks are retrieved and injected into the prompt. This grounds responses in current data without retraining. Fine-tuning updates model weights on new data; federated learning is distributed training.

</details>

---

**Q9.** When configuring an AI assistant for a security operations center, an engineer wants to ensure the model always responds as a cybersecurity expert and never discusses unrelated topics. Which component of the prompt structure should be used to enforce this behavior?

A) User prompt
B) Few-shot examples
C) System prompt
D) Prompt template variable

<details><summary>Answer</summary>

**C) System prompt**

The system prompt establishes the model's role, persona, and behavioral constraints before any user interaction begins. It enforces tone, restricts topic scope, and defines the model's identity throughout the conversation. User prompts contain the end-user's specific queries. Prompt template variables are placeholders filled at runtime — they do not enforce model behavior.

</details>

---

**Q10.** A security analyst is classifying data assets before training an anomaly detection model. Network packet captures are binary files with no predefined schema. Server configuration files use key-value pairs with some nesting. User authentication logs are rows in a relational database table. Which classification correctly maps these data types?

A) Packet captures = structured; config files = unstructured; auth logs = semi-structured
B) Packet captures = unstructured; config files = semi-structured; auth logs = structured
C) Packet captures = semi-structured; config files = structured; auth logs = unstructured
D) Packet captures = unstructured; config files = structured; auth logs = semi-structured

<details><summary>Answer</summary>

**B) Packet captures = unstructured; config files = semi-structured; auth logs = structured**

Structured data fits a rigid schema (relational tables, fixed columns). Semi-structured data has some organization but no fixed schema (JSON, XML, YAML config files). Unstructured data has no predefined format (binary packet captures, images, raw text). Correctly classifying data types before training determines preprocessing requirements and model compatibility.

</details>

---

**Q11.** A media organization wants to detect AI-generated disinformation before it spreads. Which technique embeds imperceptible signals into AI-generated content to identify its source?

A) Adversarial perturbation
B) Steganography
C) Digital watermarking
D) Content fingerprinting

<details><summary>Answer</summary>

**C) Digital watermarking**

AI watermarking embeds imperceptible signals — statistical patterns in token distributions or pixel-level modifications — into generated content that can later be detected by the issuing organization. It enables attribution and supports takedown of disinformation. Steganography hides arbitrary data in media but is not designed for AI output attribution. Adversarial perturbation manipulates inputs to fool models, not label outputs.

</details>

---

**Q12.** A healthcare consortium wants to train a shared fraud detection model across multiple hospitals without any hospital sharing patient records with the others. Which training approach enables this?

A) Transfer learning
B) Federated learning
C) Unsupervised learning
D) Centralized learning

<details><summary>Answer</summary>

**B) Federated learning**

Federated learning trains a shared model by sending the model to each participant, training locally on that participant's private data, and returning only weight updates (gradients) to a central aggregator — never the raw data itself. This preserves privacy by keeping sensitive records local. Centralized learning requires all data to be pooled in one location, which creates privacy and regulatory risks.

</details>

---

**Q13.** An AI project team has completed business requirements gathering and data collection. According to the AI development lifecycle, which stage comes immediately after data preparation?

A) Model deployment
B) Model monitoring
C) Model development and selection
D) Business use case definition

<details><summary>Answer</summary>

**C) Model development and selection**

The standard AI lifecycle progresses: business use case definition → data collection → data preparation → model development and selection → model training → model evaluation → deployment → monitoring. After data is cleaned, labeled, and split into training and validation sets, the team selects an architecture and trains candidate models. Deployment and monitoring come later in the cycle.

</details>

---

**Q14.** An autonomous AI system flags potential insider threats and immediately revokes user access without human review. A second system flags potential insider threats and queues them for a security analyst to approve before any action is taken. Which of the following correctly describes the second system?

A) Automated response
B) Human oversight
C) Human-in-the-loop
D) Reinforcement learning from human feedback

<details><summary>Answer</summary>

**C) Human-in-the-loop**

Human-in-the-loop (HITL) requires human approval before the AI system takes consequential action — a human is in the decision path. Human oversight monitors AI behavior after the fact without blocking individual decisions. The first system (automatic revocation) exemplifies full automation. RLHF is a training technique that uses human feedback to improve model outputs, not an operational control pattern.

</details>

---

**Q15.** Before training a network intrusion detection model, a data engineer removes duplicate log entries, corrects malformed IP addresses, and standardizes timestamp formats. Which data preparation activity does this describe?

A) Data augmentation
B) Data labeling
C) Data cleansing
D) Data provenance

<details><summary>Answer</summary>

**C) Data cleansing**

Data cleansing (also called data cleaning) removes or corrects inaccurate, duplicate, and malformed records to improve data quality before training. Without cleansing, noisy data degrades model accuracy and can introduce systematic errors. Data augmentation generates additional synthetic training samples. Data labeling assigns ground-truth class labels to records. Data provenance tracks data origin and transformation history.

</details>

---

**Q16.** An attacker is using a generative AI tool to produce realistic synthetic videos of an executive authorizing wire transfers. Which AI architecture generates these convincing fake videos by having two competing neural networks — one that creates content and one that evaluates its realism?

A) Transformer
B) RNN
C) GAN
D) SLM

<details><summary>Answer</summary>

**C) GAN**

A GAN (generative adversarial network) consists of a generator, which creates synthetic content, and a discriminator, which tries to distinguish real from synthetic content. The two networks compete: the generator improves to fool the discriminator, and the discriminator improves to detect fakes. This adversarial loop produces highly realistic outputs. Deepfakes and synthetic media are a primary security concern enabled by GANs.

</details>

---

**Q17.** A security operations center needs to deploy an AI model directly on network sensors with limited compute and memory. Which type of language model is most appropriate for this constraint, and what is the primary trade-off?

A) LLM — more efficient than SLMs but requires cloud connectivity
B) SLM — more efficient and edge-deployable but generally less capable than LLMs
C) LLM — supports on-device inference without cloud dependency
D) SLM — equivalent capability to LLMs but requires specialized hardware

<details><summary>Answer</summary>

**B) SLM — more efficient and edge-deployable but generally less capable than LLMs**

Small language models (SLMs) have fewer parameters than large language models (LLMs), making them faster and deployable on constrained hardware such as edge sensors without cloud connectivity. The trade-off is reduced reasoning capability and narrower knowledge compared to LLMs. LLMs require significant compute and memory, making them unsuitable for direct on-device deployment in most operational environments.

</details>

---

**Q18.** A researcher is comparing modern LLMs to earlier recurrent neural networks for processing security log sequences. Which architectural feature allows transformers to process all tokens in a sequence in parallel and capture long-range dependencies more effectively than RNNs?

A) Backpropagation
B) Dropout regularization
C) Self-attention mechanism
D) Gradient clipping

<details><summary>Answer</summary>

**C) Self-attention mechanism**

The self-attention mechanism allows transformers to compute relationships between every token in a sequence simultaneously, regardless of distance. This enables parallel processing of the entire sequence and effective capture of long-range dependencies. RNNs process tokens sequentially and struggle with long-range dependencies due to vanishing gradients. Backpropagation is a general training algorithm; dropout and gradient clipping are regularization and training stability techniques.

</details>

---

**Q19.** A threat intelligence team observes that a new malware family changes its code structure and obfuscation on every infection. Traditional signature-based antivirus cannot keep up with the variants. Which AI-driven threat capability is most likely responsible for generating these rapidly evolving samples?

A) Adversarial ML
B) AI-generated polymorphic malware
C) Model inversion attacks
D) Automated spear-phishing

<details><summary>Answer</summary>

**B) AI-generated polymorphic malware**

AI-generated polymorphic malware uses generative AI to continuously mutate code structure, obfuscation layers, and signatures while preserving malicious functionality. Each variant looks different to signature-based detection, shortening the window in which traditional defenses are effective. Adversarial ML crafts inputs to fool AI classifiers. Model inversion attacks extract training data from model outputs. Automated spear-phishing targets credential theft, not evasion of AV signatures.

</details>

---

**Q20.** After training a new malware classifier, the security team measures its accuracy, precision, recall, and F1 score against a held-out test dataset that was not used during training. Which stage of the AI lifecycle does this activity represent?

A) Data preparation
B) Model training
C) Model deployment
D) Model evaluation

<details><summary>Answer</summary>

**D) Model evaluation**

Model evaluation measures how well a trained model generalizes to unseen data using metrics such as accuracy, precision, recall, and F1 score. It occurs after training and before deployment, using a held-out test set to get an unbiased performance estimate. If the model does not meet performance thresholds, the team returns to training or data preparation. Deployment makes the model available for production use; monitoring tracks performance post-deployment.

</details>

---
