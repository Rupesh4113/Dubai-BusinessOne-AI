import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    pending_tasks: [
      {
        task_id: "TASK-RESERVE-001",
        idempotency_key: "IDEM-RES-001",
        tenant_id: "demo_tenant_dubai",
        user_id: "user_op_002",
        action_name: "TRADE_NAME_RESERVATION",
        risk_level: "HIGH",
        status: "PENDING_APPROVAL",
        input_parameters: {
          prompt: "Please reserve trade name 'Falcon Tech Solutions LLC' in Dubai DET",
        },
        approval_token: "AUTH-TOKEN-9F8E7D6C5B4A3921",
        audit_notes: ["Held at High-Risk Supervisory Gate. Awaiting one-time token authorization."],
        created_at_epoch: Date.now() / 1000,
      },
    ],
    total_pending: 1,
  });
}
