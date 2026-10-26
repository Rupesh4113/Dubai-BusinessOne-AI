# Security & Threat Model
## Dubai BusinessOne AI — Intelligent Digital Operations Agent

---

## 1. Threat Modeling Framework (STRIDE)

| Threat Category | Threat Description | Implemented Mitigation |
|:---|:---|:---|
| **Spoofing Identity** | Adversary attempts to impersonate an authorized business owner or supervisor. | PBKDF2-HMAC-SHA256 password hashing (100k rounds) + Signed JWT with 24h expiration and role verification. |
| **Tampering with Data** | Attacker modifies calculation amounts, tax rates, or statutory citations. | Deterministic Python Decimal calculations with hardcoded statutory rates (VAT 5%, CT 9%, CBUAE peg 3.6725). Client cannot alter calculation logic. |
| **Repudiation** | User denies performing an official trade name reservation or filing. | Layer 4 immutable execution records storing task ID, user ID, tenant ID, timestamp, and human approval token. |
| **Information Disclosure** | Cross-tenant data leakage or prompt injection exfiltrating system secrets. | Strict tenant partitioning in Layer 1 & Layer 3 memory + Automated prompt injection scanner neutralizing exfiltration commands. |
| **Denial of Service (DoS)** | High-frequency inference requests exhausting computational resources. | Layer 1 Exact Answer Cache with SHA-256 fingerprinting serving repeated queries with zero LLM inference. |
| **Elevation of Privilege** | Operator attempts to bypass supervisor approval for high-risk actions. | Server-side risk policy gate: High-risk tools explicitly require verified supervisor approval token in execution context. |

---

## 2. Prompt-Injection Defenses
The agent enforces pre-execution scanning against known prompt injection and jailbreak signatures:
- Direct override directives (`ignore all previous instructions`, `system override`)
- Role manipulation (`you are now in unrestricted mode`, `jailbreak`)
- Credential exfiltration (`reveal api keys`, `dump database`)
- Malicious HTML/script tagging (`<script>`, `javascript:`)

Any request triggering these signatures is immediately aborted at Step 1 (`Sanitization`), logged as a security alert in Layer 4, and returned with a formal security policy violation message.

---

## 3. Human-in-the-Loop Supervisory Controls
High-risk operations (such as official trade name reservation in the Dubai DET registry) cannot be executed autonomously by the agent. The workflow automatically transitions to `PENDING_APPROVAL`, generates an ephemeral, cryptographically random authorization token (`AUTH-TOKEN-...`), and requires explicit review and confirmation from an authorized supervisor before proceeding.

---

## 4. UAE Regulatory & Data Residency Compliance
- Designed in accordance with **UAE Federal Decree-Law No. (45) of 2021 on Personal Data Protection (PDPL)**.
- Data isolation ensures tenant data is never exposed across organizational boundaries.
- No biometric or facial recognition records are collected or stored.
