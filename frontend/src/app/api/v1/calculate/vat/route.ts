import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const amount = Number(body.amount) || 0;
    const isInclusive = Boolean(body.is_tax_inclusive);

    let netAmount = amount;
    let vatAmount = 0;
    let totalGross = amount;

    if (isInclusive) {
      netAmount = Math.round((amount / 1.05) * 100) / 100;
      vatAmount = Math.round((amount - netAmount) * 100) / 100;
      totalGross = amount;
    } else {
      netAmount = Math.round(amount * 100) / 100;
      vatAmount = Math.round(netAmount * 0.05 * 100) / 100;
      totalGross = Math.round((netAmount + vatAmount) * 100) / 100;
    }

    return NextResponse.json({
      base_amount: netAmount.toFixed(2),
      vat_rate_percent: "5.00%",
      vat_amount: vatAmount.toFixed(2),
      total_amount: totalGross.toFixed(2),
      is_tax_inclusive: isInclusive,
      vat_category: body.vat_category || "standard",
      apply_reverse_charge: false,
      currency: "AED",
      statutory_authority: "UAE Federal Tax Authority (FTA)",
      statutory_reference: "Federal Decree-Law No. (8) of 2017 on Value Added Tax",
      calculation_steps: [
        {
          step_number: 1,
          description: "Applicable standard VAT rate 5.00%",
          formula: "Federal Decree-Law No. (8) of 2017 Article 3",
          intermediate_value: "0.05",
        },
        {
          step_number: 2,
          description: isInclusive ? "Extract net from inclusive gross" : "Compute 5% on net base",
          formula: isInclusive ? `${totalGross} / 1.05` : `${netAmount} * 0.05`,
          intermediate_value: vatAmount.toFixed(2),
        },
      ],
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
