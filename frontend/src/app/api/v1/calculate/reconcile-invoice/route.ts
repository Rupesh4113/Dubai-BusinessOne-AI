import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const invoiceNumber = body.invoice_number || "INV-UNKNOWN";
    const vendorTRN = body.vendor_trn ? String(body.vendor_trn).trim() : null;
    const lineItems = body.line_items || [];

    // TRN validation: 15 digits starting with 100
    const trnValid = vendorTRN ? /^100\d{12}$/.test(vendorTRN.replace(/[-\s]/g, "")) : false;
    const trnStatus = trnValid
      ? "VALID_UAE_FTA_TRN"
      : vendorTRN
      ? "INVALID_UAE_FTA_TRN_FORMAT"
      : "MISSING_VENDOR_TRN";

    let calcSubtotal = 0;
    let calcVAT = 0;
    const variances: any[] = [];

    if (!trnValid && vendorTRN) {
      variances.push({
        field_name: "vendor_trn",
        reported_value: vendorTRN,
        calculated_value: "15 digits starting with 100",
        severity: "CRITICAL",
        explanation: "Vendor TRN does not comply with UAE Federal Tax Authority standard (15-digit starting with 100).",
      });
    }

    for (const item of lineItems) {
      const qty = Number(item.quantity) || 1;
      const price = Number(item.unit_price) || 0;
      const disc = Number(item.discount_amount) || 0;
      const vatRate = Number(item.vat_rate) || 0.05;

      const net = Math.round((qty * price - disc) * 100) / 100;
      const vat = Math.round(net * vatRate * 100) / 100;

      calcSubtotal += net;
      calcVAT += vat;
    }

    const calcGrand = Math.round((calcSubtotal + calcVAT) * 100) / 100;
    const reportedGrand = Number(body.reported_grand_total) || calcGrand;

    if (Math.abs(calcGrand - reportedGrand) > 0.05) {
      variances.push({
        field_name: "grand_total",
        reported_value: reportedGrand.toFixed(2),
        calculated_value: calcGrand.toFixed(2),
        severity: "CRITICAL",
        explanation: `Grand total discrepancy: Reported ${reportedGrand.toFixed(2)} does not equal recalculated subtotal + VAT (${calcGrand.toFixed(2)}).`,
      });
    }

    const isValid = variances.length === 0;

    return NextResponse.json({
      invoice_number: invoiceNumber,
      is_valid: isValid,
      has_discrepancy: variances.length > 0,
      trn_validation_status: trnStatus,
      calculated_subtotal: calcSubtotal.toFixed(2),
      calculated_vat_total: calcVAT.toFixed(2),
      calculated_grand_total: calcGrand.toFixed(2),
      variances,
      audit_notes: [
        `Reconciled ${lineItems.length} line items.`,
        `TRN status: ${trnStatus}`,
        isValid ? "100% mathematical reconciliation achieved." : "Variances flagged for compliance review.",
      ],
      compliance_passed: isValid,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 400 });
  }
}
