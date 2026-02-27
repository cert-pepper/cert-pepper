# Domain 1 Practice Questions: General Security Concepts

---

**Q1.** A security analyst wants to ensure that no single employee can both initiate and approve financial transactions. Which security principle does this implement?

A) Least privilege
B) Separation of duties
C) Job rotation
D) Mandatory vacation

<details><summary>Answer</summary>

**B) Separation of duties**

Separation of duties ensures no single person can complete a sensitive process alone, preventing fraud and errors. Least privilege limits permissions, job rotation moves people between roles, and mandatory vacation forces others to cover a role temporarily.

</details>

---

**Q2.** Which cryptographic algorithm is considered MOST appropriate for encrypting large amounts of data at rest?

A) RSA
B) ECC
C) AES
D) SHA-256

<details><summary>Answer</summary>

**C) AES**

AES is a symmetric encryption algorithm — fast and efficient for large data volumes. RSA and ECC are asymmetric (slower, used for key exchange and digital signatures). SHA-256 is a hash function, not encryption.

</details>

---

**Q3.** A user receives an email appearing to be from their bank. The email contains a link to a fake website designed to steal credentials. What type of attack is this?

A) Vishing
B) Spear phishing
C) Phishing
D) Pretexting

<details><summary>Answer</summary>

**C) Phishing**

Phishing is a mass email campaign impersonating a trusted entity. Spear phishing is targeted at a specific individual. Vishing uses phone/voice calls. Pretexting involves fabricating a scenario to manipulate.

</details>

---

**Q4.** Which of the following provides non-repudiation?

A) Symmetric encryption
B) Digital signature
C) Hashing
D) Access control list

<details><summary>Answer</summary>

**B) Digital signature**

Digital signatures use the sender's private key and verify with the public key, proving the sender's identity and that they cannot deny sending the message. Hashing provides integrity but not identity. Symmetric encryption requires a shared key that both parties know, so either could have created the message.

</details>

---

**Q5.** A PKI certificate has been compromised and must be invalidated before its expiration date. Which mechanism provides REAL-TIME certificate status?

A) CRL
B) OCSP
C) CSR
D) CA

<details><summary>Answer</summary>

**B) OCSP**

OCSP (Online Certificate Status Protocol) provides real-time certificate revocation status. CRL (Certificate Revocation List) is a periodically updated list — not real-time. CSR is used to request a certificate. CA issues certificates.

</details>

---

**Q6.** Which authentication factor is a fingerprint scan?

A) Something you know
B) Something you have
C) Something you are
D) Somewhere you are

<details><summary>Answer</summary>

**C) Something you are**

Biometrics (fingerprint, retina, voice) are "something you are" factors. Passwords are "something you know." Smart cards/tokens are "something you have." Location-based is "somewhere you are."

</details>

---

**Q7.** A security team wants to prevent attackers who obtain the password database from using pre-computed hash tables. Which technique should they use?

A) Key stretching
B) Salting
C) Tokenization
D) Encryption

<details><summary>Answer</summary>

**B) Salting**

Salting adds random data to each password before hashing, making pre-computed rainbow table attacks ineffective because each hash is unique even for identical passwords. Key stretching (bcrypt, PBKDF2) makes hashing slower to slow brute force — both are often used together.

</details>

---

**Q8.** An organization implements multiple layers of security controls so that if one fails, others remain. This is an example of:

A) Least privilege
B) Zero trust
C) Defense in depth
D) Separation of duties

<details><summary>Answer</summary>

**C) Defense in depth**

Defense in depth (layered security) uses multiple controls so no single failure exposes the organization. Zero trust assumes breach and verifies every request. Least privilege minimizes permissions.

</details>

---

**Q9.** Which type of security control is a warning banner displayed before login?

A) Preventive, Technical
B) Detective, Operational
C) Deterrent, Technical
D) Corrective, Managerial

<details><summary>Answer</summary>

**C) Deterrent, Technical**

A login warning banner is intended to discourage unauthorized access (deterrent) and is implemented via technology (technical). It doesn't prevent or detect — it warns.

</details>

---

**Q10.** Diffie-Hellman is used for which cryptographic purpose?

A) Encrypting data at rest
B) Hashing passwords
C) Securely exchanging encryption keys
D) Creating digital signatures

<details><summary>Answer</summary>

**C) Securely exchanging encryption keys**

Diffie-Hellman is a key exchange protocol that allows two parties to establish a shared secret over an insecure channel without transmitting the key itself. It does not encrypt data or sign messages directly.

</details>
