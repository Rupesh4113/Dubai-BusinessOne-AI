import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const netProfit = Number(body.taxable_net_profit) || 0;
    const annualRevenue = body.annual_revenue ? Number(body.annual_revenue) : null;
    const electSBR = Boolean(body.elect_small_business_relief);

    // Small Business Relief: revenue <= 3,000,000 AED
    const sbrEligible = annualRevenue !== null && annualRevenue <= 3000000;
    if (sbrEligible && electSBR) {
      return NextResponse.json({
        taxable_net_profit: netProfit.toFixed(2),
        annual_revenue: annualRevenue?.toFixed(2),
        small_business_relief_eligible: true,
        small_business_relief_applied: true,
        tier1_exempt_amount: netProfit.toFixed(2),
        tier2_taxable_amount: "0.00",
        effective_tax_rate_percent: "0.00%",
        total_tax_payable_aed: "0.00",
        is_qualifying_free_zone_person: false,
        calculation_steps: [
          {
            step_number: 1,
            description: "Small Business Relief (SBR) Election Applied",
            formula: "Revenue <= AED 3,000,000",
            intermediate_value: "0.00 AED Tax",
          },
        ],
      });
    }

    let tier1Exempt = 0;
    let tier2Taxable = 0;
    let taxPayable = 0;

    if (netProfit <= 375000) {
      tier1Exempt = netProfit;
      tier2Taxable = 0;
      taxPayable = 0;
    } else {
      tier1Exempt = 375000;
      tier2Taxable = netProfit - 375000;
      taxPayable = Math.round(tier2Taxable * 0.09 * 100) / 100;
    }

    const effRate = netProfit > 0 ? ((taxPayable / netProfit) * 100).toFixed(4) : "0.0000";

    return NextResponse.json({
      taxable_net_profit: netProfit.toFixed(2),
      annual_revenue: annualRevenue?.toFixed(2) || null,
      small_business_relief_eligible: sbrEligible,
      small_business_relief_applied: false,
      tier1_exempt_amount: tier1Exempt.toFixed(2),
      tier2_taxable_amount: tier2Taxable.toFixed(2),
      effective_tax_rate_percent: `${effRate}%`,
      total_tax_payable_aed: taxPayable.toFixed(2),
      is_qualifying_free_zone_person: false,
      calculation_steps: [
        {
          step_number: 1,
          description: "Tier 1: 0% up to AED 375,000",
          formula: `${tier1Exempt.toFixed(2)} * 0%`,
          intermediate_value: "0.00 AED",
        },
        {
          step_number: 2,
          description: "Tier 2: 9% above AED 375,000",
          formula: `${tier2Taxable.toFixed(2)} * 9%`,
          intermediate_value: `${taxPayable.toFixed(2)} AED`,
        },
      ],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
