# REST API Documentation
## Dubai BusinessOne AI — Intelligent Digital Operations Agent

Base URL: `http://localhost:8000/api/v1`

---

## 1. Authentication & RBAC

### `POST /api/v1/auth/login`
Authenticates a user and returns a signed JWT.
- **Request Body**:
  ```json
  {
    "email": "admin@businessone.dubai.ae",
    "password": "DubaiBizOne2026!Secure"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "expires_in_seconds": 86400,
    "user": {
      "user_id": "user_admin_001",
      "email": "admin@businessone.dubai.ae",
      "role": "ADMIN",
      "tenant_id": "demo_tenant_dubai"
    }
  }
  ```

---

## 2. Operations Agent Endpoints

### `POST /api/v1/agent/chat`
Submits a natural language business instruction to the agent state machine.
- **Request Body**:
  ```json
  {
    "prompt": "I want to establish a technology consulting firm as a Mainland LLC in Dubai with expected year 1 revenue of 1,200,000 AED and 60,000 AED office rent.",
    "language": "en",
    "idempotency_key": "unique-uuid-optional",
    "approval_token": "AUTH-TOKEN-... (optional to resume high-risk task)"
  }
  ```
- **Response**: Full `AgentTaskState` snapshot including intent, intermediate calculations, risk tier, citations, executed tools, audit trail, and formatted response.

### `GET /api/v1/agent/tasks`
Returns recent tasks and immutable audit trails for the tenant.

### `GET /api/v1/agent/telemetry`
Returns zero-inference reuse stats and token savings.

---

## 3. Human Approval Gate Endpoints

### `GET /api/v1/approvals/pending`
Lists all operations currently paused awaiting supervisor authorization.

### `POST /api/v1/approvals/decision`
Supervisor approves or rejects a high-risk operation using an authorization token.
- **Request Body**:
  ```json
  {
    "task_id": "TASK-1740000000-A1B2C3",
    "approval_token": "AUTH-TOKEN-9F8E7D6C5B4A3921",
    "decision": "APPROVE",
    "comments": "Verified commercial dossier."
  }
  ```

---

## 4. Deterministic Calculation Engines

- `POST /api/v1/calculate/vat`: Computes UAE VAT (5%, inclusive, zero-rated, exempt, RCM).
- `POST /api/v1/calculate/corporate-tax`: Computes UAE Corporate Tax (0% up to 375k, 9% above, SBR, Free Zone QFZP).
- `POST /api/v1/calculate/dubai-det-setup`: Computes Dubai DET license fees and 5% market fee.
- `POST /api/v1/calculate/dubai-chamber-fee`: Computes Dubai Chamber membership fee by capital tier.
- `POST /api/v1/calculate/currency`: Converts currencies via CBUAE fixed peg and reference rates.
- `POST /api/v1/calculate/reconcile-invoice`: Validates invoice mathematics and 15-digit TRN.
