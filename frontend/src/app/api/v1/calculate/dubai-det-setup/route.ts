import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const licenseType = (body.license_type || "commercial").toLowerCase();
    const rent = Number(body.annual_office_rent_aed) || 60000;
    const isInstant = Boolean(body.is_instant_license);

    let baseFee = 6000;
    let typeLabel = "Commercial License";
    if (licenseType.includes("prof")) {
      baseFee = 4000;
      typeLabel = "Professional License";
    } else if (licenseType.includes("ind")) {
      baseFee = 8000;
      typeLabel = "Industrial License";
    }

    const initApproval = 120;
    const tradeName = 620;
    const register = 100;
    const innovation = 20;
    const marketFee = isInstant ? 0 : Math.round(rent * 0.05 * 100) / 100;
    const totalCost = initApproval + tradeName + baseFee + register + marketFee + innovation;

    return NextResponse.json({
      license_type: typeLabel,
      initial_approval_fee_aed: initApproval.toFixed(2),
      trade_name_reservation_fee_aed: tradeName.toFixed(2),
      base_license_fee_aed: baseFee.toFixed(2),
      commercial_register_fee_aed: register.toFixed(2),
      market_fee_aed: marketFee.toFixed(2),
      knowledge_and_innovation_dirham_aed: innovation.toFixed(2),
      total_det_setup_cost_aed: totalCost.toFixed(2),
      calculation_steps: [
        {
          step_number: 1,
          description: `Base ${typeLabel} Startup Fee`,
          formula: `DET Law No. 13 of 2011`,
          intermediate_value: `AED ${baseFee.toFixed(2)}`,
        },
        {
          step_number: 2,
          description: isInstant ? "Market Fee Waived (Year 1 Instant License)" : "Dubai Municipality 5% Tenancy Market Fee",
          formula: isInstant ? "Instant Scheme" : `${rent} * 0.05`,
          intermediate_value: `AED ${marketFee.toFixed(2)}`,
        },
      ],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
