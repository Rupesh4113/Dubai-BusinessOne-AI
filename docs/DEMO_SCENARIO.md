# Competition Demonstration Scenario
## Dubai BusinessOne AI — Intelligent Digital Operations Agent

**Competition Event**: Dubai Chamber Digital AI Agent Competition  
**Scenario Title**: Autonomous Corporate Setup, Deterministic Tax Modeling, and Supervisory Reservation Gate for an International Tech Enterprise.

---

## 1. Scenario Narrative
An international technology investor lands in Dubai and submits the following instruction through the web interface:

> *"I want to establish a technology consulting firm as a Mainland LLC in Dubai with expected year 1 revenue of 1,200,000 AED and 60,000 AED office rent."*

---

## 2. Walkthrough & Execution Stages

### Stage 1: Input Ingestion & Safety Verification
- **User Action**: Enters prompt in web app (supports English, Arabic, Hindi, Urdu, Filipino, Malayalam).
- **Agent Action**: Step 1 (`Sanitization`) inspects prompt against adversarial injection attacks. Security check passes.

### Stage 2: Layer 1 Zero-Inference Cache
- Agent computes SHA-256 fingerprint: `hash(tenant_id, language, normalized_query)`.
- Cache Miss detected on initial submission; execution continues to planning.

### Stage 3: Intent Classification & Entity Extraction
- **Identified Intent**: `BUSINESS_SETUP_INQUIRY`.
- **Extracted Entities**:
  - Legal Form: `Mainland LLC` (Federal Decree-Law No. 32 of 2021: 100% foreign ownership).
  - Annual Revenue: `AED 1,200,000`.
  - Office Lease Rent: `AED 60,000`.

### Stage 4: Authoritative Knowledge Retrieval & Citations
- Retrieves verified regulatory records:
  - `REG-DED-LLC-001`: Dubai DET 100% foreign ownership mainland rules.
  - `REG-CHAMBER-MEM-002`: Dubai Chamber Law No. 1 of 2022 membership schedule.
  - `REG-FTA-CT-003`: Federal Decree-Law No. 47 of 2022 Corporate Tax brackets.
  - `REG-FTA-VAT-004`: Federal Decree-Law No. (8) of 2017 VAT rules.
- Generates structured citations with official URLs and freshness status badges.

### Stage 5: Deterministic Numerical Calculations (Zero LLM Arithmetic)
- **Dubai DET License Setup**:
  - Initial Approval: AED 120
  - Trade Name Reservation: AED 620
  - Base Professional License: AED 4,000
  - Commercial Register: AED 100
  - Knowledge & Innovation Dirhams: AED 20
  - Dubai Municipality Market Fee (5% of AED 60,000 lease): **AED 3,000**
  - **Total DET Setup**: **AED 7,860.00**
- **Dubai Chamber Membership**:
  - LLC Tier B (Capital <= AED 500k): AED 1,200
  - Certificate & Electronic Verification: AED 50
  - **Total Chamber Annual Fee**: **AED 1,250.00**
- **Corporate Tax Liability**:
  - 25% Profit Baseline: AED 300,000
  - Tier 1 (0% up to AED 375,000): **AED 0.00 Tax Payable** (100% exempt!)
- **VAT Liability (5%)**:
  - Tax on AED 1,200,000 revenue: **AED 60,000.00**

### Stage 6: Tool Execution & Verification
- Invokes `official_registry_search` tool: Queries Dubai DET register for name conflicts.
- Invokes `document_generator` tool: Formats full commercial setup dossier.

### Stage 7: Layer 1 Zero-Inference Cache Recording
- Persists verified safe response into Layer 1 Cache.

### Stage 8: Turn 2 Repeat Inquiry (Zero-Inference Proof)
- User or client submits an identical request:
- **Result**: Immediate cache HIT. Agent returns verified response in **1.8ms** with **0 LLM tokens consumed**.
- Telemetry records `+800 Tokens Saved`.

---

## 3. High-Risk Human Approval Showcase
1. User requests: *"Please reserve trade name 'Falcon Tech Solutions LLC' in Dubai DET."*
2. Agent identifies `TRADE_NAME_RESERVATION` as **HIGH RISK**.
3. Operation pauses at the Human Approval Gate; generates one-time token `AUTH-TOKEN-...`.
4. Authorized supervisor opens the **Human Approval Center** in the navigation bar.
5. Supervisor clicks **"Authorize Execution"**.
6. Agent resumes and completes the official reservation in Dubai DET registry, generating Voucher `VOUCHER-DET-...` valid for 60 days.
