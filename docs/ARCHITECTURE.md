# System Architecture & Technical Specifications
## Dubai BusinessOne AI — Intelligent Digital Operations Agent

```mermaid
flowchart TD
    subgraph MultiChannel["Multimodal & Channel Ingestion"]
        Web["Next.js Web / PWA (RTL/LTR)"]
        WA["WhatsApp Cloud API Adapter"]
        Teams["MS Teams Webhook Adapter"]
        REST["Direct REST API / Webhooks"]
    end

    subgraph SecurityGate["Security & Identity Boundary"]
        JWT["JWT Auth & Role-Based Access Control"]
        InjectionShield["Prompt-Injection & Adversarial Defenses"]
        TenantIsolator["Tenant Partitioning & Verification"]
    end

    subgraph StateMachine["Agent Orchestration Core"]
        Sanitize["1. Input Sanitization"]
        L1Check{"2. Layer 1 Zero-Inference Cache"}
        Intent["3. Intent & Entity Classifier"]
        L2Retrieval["4. Layer 2 Official Knowledge Retrieval"]
        CalcEngine["5. Deterministic Decimal Engine"]
        RiskAssess{"6. Risk Assessment Gate"}
        
        subgraph RiskTiers["Risk-Tier Policy"]
            LowTier["Low Risk: Auto-Authorize"]
            MedTier["Medium Risk: Audited Pass"]
            HighTier["High Risk: Human Supervisor Gate"]
        end

        Sandbox["8. Tool Execution Sandbox"]
        PostVerif["9. Postcondition Verification"]
        Synthesizer["10. Model Router & Multi-Language Synthesis"]
        L4Audit["11. Layer 4 Immutable Execution Audit"]
        L1Store["12. Layer 1 Cache Persistence"]
    end

    subgraph OfficialServices["Official External & Regulatory Adapters"]
        DETRegistry["Dubai DET Commercial Register"]
        ChamberService["Dubai Chamber Services"]
        FTAPortal["Federal Tax Authority Portal"]
    end

    MultiChannel --> SecurityGate
    SecurityGate --> Sanitize --> L1Check
    L1Check -- HIT (0 Tokens) --> MultiChannel
    L1Check -- MISS --> Intent --> L2Retrieval --> CalcEngine --> RiskAssess
    RiskAssess --> LowTier --> Sandbox
    RiskAssess --> MedTier --> Sandbox
    RiskAssess --> HighTier
    HighTier -- Awaiting Token --> MultiChannel
    HighTier -- Authorized by Supervisor --> Sandbox
    Sandbox --> OfficialServices
    Sandbox --> PostVerif --> Synthesizer --> L4Audit --> L1Store --> MultiChannel
```

---

## 1. Component Layer Details

### 1.1 Ingestion Layer
- **Next.js 14 Web / PWA**: Reactive React 18 interface with native bidirectional support for Left-to-Right (`ltr`) and Right-to-Left (`rtl`) layout rendering.
- **Channel Adapters**:
  - `EmailNotificationAdapter`: SMTP / transactional email dispatcher.
  - `WhatsAppNotificationAdapter`: Meta Cloud API compliant webhook dispatcher.
  - `TeamsNotificationAdapter`: Microsoft Adaptive Card webhook integration.
  - `WebhookNotificationAdapter`: Cryptographically signed HMAC-SHA256 event emitter.

### 1.2 Security & Governance Boundary
- **Password Hashing**: PBKDF2-HMAC-SHA256 with 100,000 rounds and random cryptographic salts.
- **JWT Session Tokens**: Signed tokens enforcing Role-Based Access Control (RBAC): `ADMIN`, `SUPERVISOR`, `OPERATOR`, `VIEWER`.
- **Prompt Injection Defense**: Regex pattern scanning for adversarial directives, system prompt overrides, and unauthorized commands.

### 1.3 Deterministic Calculation Engine
- All math is executed strictly in Python `decimal.Decimal` with statutory `ROUND_HALF_UP` rounding.
- No LLM arithmetic hallucinations are permitted in financial, fee, or tax calculations.
- Full provenance tracking captures mathematical formulas, line-by-line steps, and legal statutory references for every calculation.

### 1.4 4-Tier Memory & Zero-Inference Reuse
- **Layer 1: Exact Answer Cache**: SHA-256 fingerprinting on normalized prompt, tenant ID, and language. Instant zero-token retrieval. Time-sensitive queries (e.g. live account balances) are automatically invalidated within 60 seconds.
- **Layer 2: Verified Knowledge Base**: Curated database of verified official UAE and Dubai legal statutes with freshness indicators.
- **Layer 3: User & Organization Memory**: Securely isolated tenant profile data.
- **Layer 4: Execution History**: Durable store tracking task states, idempotency keys, and supervisor approval tokens.
