import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    tasks: [
      {
        task_id: "TASK-1740000001-A1B2",
        action_name: "BUSINESS_SETUP_INQUIRY",
        risk_level: "LOW",
        status: "COMPLETED",
        idempotency_key: "IDEM-001-SETUP",
        audit_notes: ["Completed deterministic setup calculations with 100% precision."],
      },
      {
        task_id: "TASK-1740000002-C3D4",
        action_name: "TRADE_NAME_RESERVATION",
        risk_level: "HIGH",
        status: "PENDING_APPROVAL",
        idempotency_key: "IDEM-002-RES",
        audit_notes: ["Held at High-Risk Supervisory Gate awaiting supervisor token."],
      },
      {
        task_id: "TASK-1740000003-E5F6",
        action_name: "INVOICE_RECONCILIATION",
        risk_level: "MEDIUM",
        status: "VERIFIED",
        idempotency_key: "IDEM-003-INV",
        audit_notes: ["Reconciled line items. Verified 15-digit FTA TRN."],
      },
    ],
    count: 3,
  });
}
