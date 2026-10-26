"""Deterministic Invoice Reconciliation & Discrepancy Detection Engine."""

import re
from decimal import Decimal
from typing import List
from .decimal_calc import to_decimal, quantize_currency
from .models import (
    InvoiceReconciliationRequest,
    InvoiceReconciliationResult,
    ReconciliationVariance
)


def validate_uae_trn(trn: str) -> bool:
    """Validates UAE FTA Tax Registration Number (15 digits, starting with 100)."""
    if not trn:
        return False
    cleaned = trn.strip().replace(" ", "").replace("-", "")
    return bool(re.match(r"^100\d{12}$", cleaned))


def reconcile_invoice(request: InvoiceReconciliationRequest) -> InvoiceReconciliationResult:
    """Performs rigorous line-by-line reconciliation and statutory compliance checks."""
    variances: List[ReconciliationVariance] = []
    audit_notes: List[str] = []

    # 1. TRN validation
    trn_valid = False
    if request.vendor_trn:
        if validate_uae_trn(request.vendor_trn):
            trn_status = "VALID_UAE_FTA_TRN"
            trn_valid = True
            audit_notes.append(f"Vendor TRN {request.vendor_trn} successfully validated against UAE FTA 15-digit schema.")
        else:
            trn_status = "INVALID_UAE_FTA_TRN_FORMAT"
            variances.append(ReconciliationVariance(
                field_name="vendor_trn",
                reported_value=request.vendor_trn,
                calculated_value="15 digits starting with 100",
                variance_amount="N/A",
                severity="CRITICAL",
                explanation="Vendor TRN does not comply with UAE Federal Tax Authority standard (15-digit starting with 100). Invoice may not be eligible for input VAT recovery."
            ))
    else:
        trn_status = "MISSING_VENDOR_TRN"
        variances.append(ReconciliationVariance(
            field_name="vendor_trn",
            reported_value="None",
            calculated_value="Required for VAT Invoices exceeding AED 10,000",
            variance_amount="N/A",
            severity="WARNING",
            explanation="Missing Vendor TRN on invoice."
        ))

    # 2. Line Items Mathematics Verification
    calculated_subtotal = Decimal("0.00")
    calculated_vat_total = Decimal("0.00")
    seen_items = set()

    for item in request.line_items:
        qty = to_decimal(item.quantity)
        price = to_decimal(item.unit_price)
        disc = to_decimal(item.discount_amount)
        vat_rate = to_decimal(item.vat_rate)
        rep_total = to_decimal(item.reported_line_total)

        item_key = (item.description.lower().strip(), str(qty), str(price))
        if item_key in seen_items:
            variances.append(ReconciliationVariance(
                field_name=f"line_{item.line_number}_duplicate",
                reported_value=item.description,
                calculated_value="Unique line item",
                variance_amount="0.00",
                severity="WARNING",
                explanation=f"Potential duplicate line item detected on Line {item.line_number}: '{item.description}' with identical quantity and price."
            ))
        seen_items.add(item_key)

        expected_net = quantize_currency((qty * price) - disc)
        expected_line_vat = quantize_currency(expected_net * vat_rate)
        expected_line_gross = expected_net + expected_line_vat

        # Check line total reported vs expected (some systems report line net, some report line gross)
        diff_from_net = abs(rep_total - expected_net)
        diff_from_gross = abs(rep_total - expected_line_gross)

        if diff_from_net > Decimal("0.02") and diff_from_gross > Decimal("0.02"):
            variances.append(ReconciliationVariance(
                field_name=f"line_{item.line_number}_total",
                reported_value=str(rep_total),
                calculated_value=f"Net: {expected_net} / Gross: {expected_line_gross}",
                variance_amount=str(diff_from_net),
                severity="CRITICAL",
                explanation=f"Line {item.line_number} total arithmetic error: ({qty} * {price} - {disc}) does not match reported {rep_total}."
            ))

        calculated_subtotal += expected_net
        calculated_vat_total += expected_line_vat

    calculated_subtotal = quantize_currency(calculated_subtotal)
    calculated_vat_total = quantize_currency(calculated_vat_total)
    calculated_grand_total = quantize_currency(calculated_subtotal + calculated_vat_total)

    # 3. Header Totals Reconciliation
    rep_subtotal = quantize_currency(to_decimal(request.reported_subtotal))
    rep_vat = quantize_currency(to_decimal(request.reported_vat_total))
    rep_grand = quantize_currency(to_decimal(request.reported_grand_total))

    subtotal_diff = abs(rep_subtotal - calculated_subtotal)
    if subtotal_diff > Decimal("0.02"):
        variances.append(ReconciliationVariance(
            field_name="subtotal",
            reported_value=str(rep_subtotal),
            calculated_value=str(calculated_subtotal),
            variance_amount=str(subtotal_diff),
            severity="CRITICAL",
            explanation=f"Subtotal discrepancy: Reported {rep_subtotal} does not match recalculated sum of lines {calculated_subtotal}."
        ))

    vat_diff = abs(rep_vat - calculated_vat_total)
    if vat_diff > Decimal("0.02"):
        variances.append(ReconciliationVariance(
            field_name="vat_total",
            reported_value=str(rep_vat),
            calculated_value=str(calculated_vat_total),
            variance_amount=str(vat_diff),
            severity="CRITICAL",
            explanation=f"VAT discrepancy: Reported {rep_vat} does not match recalculated 5% tax {calculated_vat_total}."
        ))

    grand_diff = abs(rep_grand - calculated_grand_total)
    if grand_diff > Decimal("0.02"):
        variances.append(ReconciliationVariance(
            field_name="grand_total",
            reported_value=str(rep_grand),
            calculated_value=str(calculated_grand_total),
            variance_amount=str(grand_diff),
            severity="CRITICAL",
            explanation=f"Grand total discrepancy: Reported {rep_grand} does not equal subtotal + VAT ({calculated_grand_total})."
        ))

    has_critical_discrepancy = any(v.severity == "CRITICAL" for v in variances)
    is_valid = not has_critical_discrepancy
    compliance_passed = is_valid and (trn_valid or not request.vendor_trn)

    if not variances:
        audit_notes.append("100% mathematical reconciliation achieved. All line totals, VAT allocations, and grand totals are verified.")

    return InvoiceReconciliationResult(
        invoice_number=request.invoice_number,
        is_valid=is_valid,
        has_discrepancy=len(variances) > 0,
        trn_validation_status=trn_status,
        calculated_subtotal=str(calculated_subtotal),
        calculated_vat_total=str(calculated_vat_total),
        calculated_grand_total=str(calculated_grand_total),
        variances=variances,
        audit_notes=audit_notes,
        compliance_passed=compliance_passed
    )
