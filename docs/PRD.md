# Product Requirements Document (PRD)
## Dubai BusinessOne AI — Intelligent Digital Operations Agent
**Event**: Dubai Chamber Digital AI Agent Competition  
**Version**: 1.0.0 (Production-Ready)  
**Status**: APPROVED & IMPLEMENTED  

---

## 1. Executive Summary
Dubai BusinessOne AI is an enterprise-grade digital operations agent designed to automate commercial, legal, and regulatory operations for entrepreneurs, foreign investors, and enterprises operating in Dubai and the UAE. Unlike conversational chatbots or static interfaces, Dubai BusinessOne AI operates as an autonomous operational partner: understanding instructions, verifying authoritative rules against official UAE portals (Dubai Chamber, DET, FTA), executing deterministic mathematical and financial calculations with Decimal precision, enforcing supervisory human approval gates for high-risk operations, recording immutable audit trails, and reusing verified answers at zero inference cost.

---

## 2. Target Users & Personas
1. **International Investors & Entrepreneurs**: Seeking to establish mainland or free-zone entities in Dubai, calculate exact statutory government fees, understand 100% foreign ownership laws, and reserve trade names.
2. **Operations & Finance Managers**: Requiring automated invoice line-item reconciliation, UAE FTA 15-digit TRN validation, VAT and Corporate Tax calculations, and dispute identification.
3. **Corporate Supervisors & Compliance Officers**: Overseeing regulatory submissions, approving high-risk transactions with one-time authorization tokens, and auditing compliance logs.

---

## 3. Functional Requirements

### 3.1 Intelligent Reasoning & Decision Support
- Natural language instruction decomposition into structured tasks.
- Distinction between verified facts, assumptions, and missing data.
- Strict citation of statutory references (Federal Decree-Laws, Cabinet Decisions, Dubai Executive Council Resolutions).
- Explicit uncertainty communication without hallucinating official laws.
- Human-in-the-Loop approval gate for high-impact or ambiguous actions.

### 3.2 Deterministic Financial & Tax Calculation Engines
- Zero-error math using statutory `decimal.Decimal` arithmetic and `ROUND_HALF_UP` bank rounding.
- **UAE VAT (5%)**: Standard rate, inclusive gross extraction, zero-rated exports, exempt supplies, and Reverse Charge Mechanism (RCM).
- **UAE Corporate Tax (Federal Decree-Law No. 47 of 2022)**: 0% on profits up to AED 375,000; 9% on profits exceeding AED 375,000; Small Business Relief (SBR) election for revenue <= AED 3M; Qualifying Free Zone Person (QFZP) 0% regime with 5% de minimis check.
- **Dubai Chamber Membership Fees (Law No. 1 of 2022)**: Tier A/B schedules based on legal form, capital thresholds, and foreign branch rules.
- **Dubai DET Business Setup Fees (Law No. 13 of 2011)**: Commercial/Professional/Industrial base licenses, initial approval, trade name reservation, commercial register, knowledge/innovation vouchers, and 5% Dubai Municipality market tenancy fees with Year 1 Instant License waiver.
- **Currency Conversion**: Central Bank of UAE (CBUAE) fixed peg (USD/AED = 3.6725) and daily reference exchange rates.
- **Invoice Reconciliation**: 15-digit TRN validation, line-item arithmetic verification, and discrepancy identification.

### 3.3 4-Tier Memory & Zero-Inference Reuse
- **Layer 1 (Exact Answer Cache)**: SHA-256 fingerprinting based on normalized query, tenant ID, and language. Instant sub-millisecond retrieval with 0 LLM tokens consumed. Time-sensitive veto prevents stale balance/FX reuse.
- **Layer 2 (Verified Knowledge Base)**: Curated official legal clauses and executive regulations with freshness indicators.
- **Layer 3 (User & Organization Memory)**: Consented corporate preferences, preferred currency, language, and legal structure with strict cross-tenant isolation.
- **Layer 4 (Execution History & Idempotency)**: Immutable audit trail, task states, idempotency key deduplication, and cryptographic supervisor approval tokens.

### 3.4 Risk-Tiered Action Framework
- **LOW Risk**: Public knowledge query, fee calculation, document drafting (Auto-executed).
- **MEDIUM Risk**: Invoice discrepancy auditing, profile updates (Audited execution).
- **HIGH Risk**: Official trade name reservation, commercial registry filing, financial commitments (Held at supervisor gate until authorized with one-time token).

### 3.5 Multilingual & Multimodal Support
- Full interface localization in **6 languages**: English, Arabic (العربية - RTL), Hindi (हिन्दी), Urdu (اردو - RTL), Filipino (Tagalog), and Malayalam (മലയാളം).
- Instant reactive language switching with bidirectional LTR/RTL layout support.
