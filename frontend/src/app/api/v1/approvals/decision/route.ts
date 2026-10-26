import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const taskId = body.task_id;
    const decision = body.decision || "APPROVE";

    return NextResponse.json({
      task_id: taskId,
      status: decision === "APPROVE" ? "APPROVED_AND_EXECUTED" : "REJECTED",
      message: `Task ${taskId} has been ${decision === "APPROVE" ? "authorized and executed" : "rejected"} by human supervisor.`,
      executed_result: {
        voucher_number: `VOUCHER-DET-${Math.random().toString(36).substring(2, 8).toUpperCase()}`,
        status: "OFFICIALLY_RESERVED",
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
