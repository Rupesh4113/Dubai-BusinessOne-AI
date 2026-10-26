import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const legalForm = (body.legal_form || "llc").toLowerCase();
    const capital = Number(body.share_capital) || 300000;
    const isNew = Boolean(body.is_new_registration ?? true);

    let baseFee = 1200;
    let tierName = "LLC / Commercial (Tier B)";

    if (legalForm.includes("branch_foreign") || legalForm.includes("foreign")) {
      baseFee = 2200;
      tierName = "Branch of Foreign Company";
    } else if (legalForm.includes("branch_local") || legalForm.includes("local")) {
      baseFee = 1000;
      tierName = "Branch of Local Mainland Company";
    } else if (legalForm.includes("sole") || legalForm.includes("prof")) {
      baseFee = 700;
      tierName = "Sole Professional Establishment";
    } else if (capital > 500000) {
      baseFee = 2200;
      tierName = "LLC / Commercial (Capital > AED 500,000) - Tier A";
    }

    const certFee = isNew ? 50 : 0;
    const totalFee = baseFee + certFee;

    return NextResponse.json({
      legal_form: legalForm,
      share_capital_aed: capital.toFixed(2),
      base_membership_fee_aed: baseFee.toFixed(2),
      certificate_and_verification_fee_aed: certFee.toFixed(2),
      total_chamber_fee_aed: totalFee.toFixed(2),
      schedule_tier: tierName,
      renewal_cycle: "Annual",
      calculation_steps: [
        {
          step_number: 1,
          description: "Dubai Chamber Tariff Classification",
          formula: tierName,
          intermediate_value: `AED ${baseFee.toFixed(2)}`,
        },
      ],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
