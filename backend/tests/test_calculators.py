"""Automated tests for Dubai BusinessOne AI Deterministic Calculation Engines."""

import pytest
from decimal import Decimal
from backend.app.calculator import (
    calculate_uae_vat,
    calculate_uae_corporate_tax,
    calculate_dubai_chamber_fee,
    calculate_dubai_det_fees,
    convert_currency,
    reconcile_invoice,
    validate_uae_trn,
    VATCalculationRequest,
    CorporateTaxRequest,
    DubaiChamberFeeRequest,
    DubaiDETFeeRequest,
    CurrencyConversionRequest,
    InvoiceReconciliationRequest,
    InvoiceLineItem
)


# ==========================================
# 1. UAE VAT Tests
# ==========================================
def test_standard_vat_exclusive():
    req = VATCalculationRequest(amount=Decimal("1000.00"), is_tax_inclusive=False, vat_category="standard")
    res = calculate_uae_vat(req)
    assert res.base_amount == "1000.00"
    assert res.vat_amount == "50.00"
    assert res.total_amount == "1050.00"
    assert len(res.calculation_steps) >= 3


def test_standard_vat_inclusive():
    # 1050.00 inclusive of 5% should yield 1000.00 base and 50.00 VAT
    req = VATCalculationRequest(amount=Decimal("1050.00"), is_tax_inclusive=True, vat_category="standard")
    res = calculate_uae_vat(req)
    assert res.base_amount == "1000.00"
    assert res.vat_amount == "50.00"
    assert res.total_amount == "1050.00"


def test_zero_rated_and_exempt_vat():
    zero_req = VATCalculationRequest(amount=Decimal("5000.00"), is_tax_inclusive=False, vat_category="zero_rated")
    zero_res = calculate_uae_vat(zero_req)
    assert zero_res.vat_amount == "0.00"
    assert zero_res.total_amount == "5000.00"

    exempt_req = VATCalculationRequest(amount=Decimal("12000.00"), is_tax_inclusive=False, vat_category="exempt")
    exempt_res = calculate_uae_vat(exempt_req)
    assert exempt_res.vat_amount == "0.00"
    assert exempt_res.total_amount == "12000.00"


def test_reverse_charge_mechanism():
    rcm_req = VATCalculationRequest(amount=Decimal("20000.00"), apply_reverse_charge=True)
    rcm_res = calculate_uae_vat(rcm_req)
    assert rcm_res.apply_reverse_charge is True
    assert any("RCM" in step.description or "Reverse Charge" in step.description for step in rcm_res.calculation_steps)


# ==========================================
# 2. UAE Corporate Tax Tests
# ==========================================
def test_corporate_tax_below_threshold():
    # Profit below AED 375,000 should pay 0%
    req = CorporateTaxRequest(taxable_net_profit=Decimal("300000.00"))
    res = calculate_uae_corporate_tax(req)
    assert res.total_tax_payable_aed == "0.00"
    assert res.tier1_exempt_amount == "300000.00"
    assert res.tier2_taxable_amount == "0.00"


def test_corporate_tax_above_threshold():
    # Profit AED 1,000,000 => 375k @ 0% = 0, 625k @ 9% = 56,250 AED
    req = CorporateTaxRequest(taxable_net_profit=Decimal("1000000.00"))
    res = calculate_uae_corporate_tax(req)
    assert res.tier1_exempt_amount == "375000.00"
    assert res.tier2_taxable_amount == "625000.00"
    assert res.total_tax_payable_aed == "56250.00"
    assert res.effective_tax_rate_percent == "5.6250%"


def test_corporate_tax_small_business_relief():
    # Revenue <= AED 3,000,000 with SBR elected
    req = CorporateTaxRequest(
        taxable_net_profit=Decimal("500000.00"),
        annual_revenue=Decimal("2500000.00"),
        elect_small_business_relief=True
    )
    res = calculate_uae_corporate_tax(req)
    assert res.small_business_relief_eligible is True
    assert res.small_business_relief_applied is True
    assert res.total_tax_payable_aed == "0.00"


def test_corporate_tax_qualifying_free_zone():
    # Free Zone person with non-qualifying revenue within de minimis
    req = CorporateTaxRequest(
        taxable_net_profit=Decimal("2000000.00"),
        annual_revenue=Decimal("10000000.00"),
        is_qualifying_free_zone_person=True,
        non_qualifying_revenue=Decimal("100000.00")  # 1% <= 5% de minimis limit
    )
    res = calculate_uae_corporate_tax(req)
    assert res.is_qualifying_free_zone_person is True
    # Non-qualifying revenue 100,000 @ 9% = 9,000 AED
    assert res.total_tax_payable_aed == "9000.00"


# ==========================================
# 3. Dubai Chamber Fee Schedule Tests
# ==========================================
def test_dubai_chamber_llc_fees():
    # LLC with capital <= 500k
    req = DubaiChamberFeeRequest(legal_form="llc", share_capital=Decimal("300000.00"), is_new_registration=True)
    res = calculate_dubai_chamber_fee(req)
    assert res.base_membership_fee_aed == "1200.00"
    assert res.certificate_and_verification_fee_aed == "50.00"
    assert res.total_chamber_fee_aed == "1250.00"

    # LLC with capital > 500k
    req_high = DubaiChamberFeeRequest(legal_form="llc", share_capital=Decimal("1000000.00"), is_new_registration=False)
    res_high = calculate_dubai_chamber_fee(req_high)
    assert res_high.base_membership_fee_aed == "2200.00"
    assert res_high.certificate_and_verification_fee_aed == "0.00"
    assert res_high.total_chamber_fee_aed == "2200.00"


def test_dubai_chamber_foreign_branch():
    req = DubaiChamberFeeRequest(legal_form="branch_foreign", is_new_registration=True)
    res = calculate_dubai_chamber_fee(req)
    assert res.base_membership_fee_aed == "2200.00"
    assert res.total_chamber_fee_aed == "2250.00"


# ==========================================
# 4. Dubai DET Fee Setup Tests
# ==========================================
def test_dubai_det_commercial_setup():
    # Commercial license with AED 60,000 annual rent
    req = DubaiDETFeeRequest(license_type="commercial", annual_office_rent_aed=Decimal("60000.00"))
    res = calculate_dubai_det_fees(req)
    # Market fee = 5% of 60,000 = 3,000
    # Total = 120 (initial approval) + 620 (trade name) + 6000 (base) + 100 (register) + 3000 (market) + 20 (innovation/knowledge) = 9860
    assert res.market_fee_aed == "3000.00"
    assert res.total_det_setup_cost_aed == "9860.00"


def test_dubai_det_instant_license():
    req = DubaiDETFeeRequest(license_type="professional", is_instant_license=True)
    res = calculate_dubai_det_fees(req)
    # Instant license has no rent/market fee in year 1
    assert res.market_fee_aed == "0.00"
    # Base 4000 + 120 + 620 + 100 + 20 = 4860
    assert res.total_det_setup_cost_aed == "4860.00"


# ==========================================
# 5. Currency Conversion Tests
# ==========================================
def test_currency_conversion_usd_to_aed():
    req = CurrencyConversionRequest(amount=Decimal("1000.00"), from_currency="USD", to_currency="AED")
    res = convert_currency(req)
    assert res.exchange_rate == "3.6725"
    assert res.converted_amount == "3672.50"
    assert res.is_pegged_rate is True


def test_currency_conversion_aed_to_usd():
    req = CurrencyConversionRequest(amount=Decimal("3672.50"), from_currency="AED", to_currency="USD")
    res = convert_currency(req)
    assert res.converted_amount == "1000.00"
    assert res.is_pegged_rate is True


# ==========================================
# 6. Invoice Reconciliation Tests
# ==========================================
def test_trn_validation():
    assert validate_uae_trn("100234567890003") is True
    assert validate_uae_trn("100-234567890-003") is True
    assert validate_uae_trn("200234567890003") is False  # Must start with 100
    assert validate_uae_trn("100123") is False  # Too short


def test_invoice_reconciliation_clean():
    lines = [
        InvoiceLineItem(
            line_number=1,
            description="IT Consulting Services",
            quantity=Decimal("10.00"),
            unit_price=Decimal("500.00"),
            discount_amount=Decimal("0.00"),
            vat_rate=Decimal("0.05"),
            reported_line_total=Decimal("5000.00")
        )
    ]
    req = InvoiceReconciliationRequest(
        invoice_number="INV-2026-001",
        vendor_trn="100998877665544",
        invoice_date="2026-03-01",
        line_items=lines,
        reported_subtotal=Decimal("5000.00"),
        reported_vat_total=Decimal("250.00"),
        reported_grand_total=Decimal("5250.00")
    )
    res = reconcile_invoice(req)
    assert res.is_valid is True
    assert res.has_discrepancy is False
    assert res.calculated_grand_total == "5250.00"
    assert res.compliance_passed is True


def test_invoice_reconciliation_with_discrepancy():
    lines = [
        InvoiceLineItem(
            line_number=1,
            description="Software License",
            quantity=Decimal("2.00"),
            unit_price=Decimal("1000.00"),
            reported_line_total=Decimal("2000.00")
        )
    ]
    req = InvoiceReconciliationRequest(
        invoice_number="INV-2026-002",
        vendor_trn="100998877665544",
        invoice_date="2026-03-01",
        line_items=lines,
        reported_subtotal=Decimal("2000.00"),
        reported_vat_total=Decimal("50.00"),  # Incorrect VAT (should be 100.00)
        reported_grand_total=Decimal("2050.00")
    )
    res = reconcile_invoice(req)
    assert res.is_valid is False
    assert res.has_discrepancy is True
    assert any(v.field_name == "vat_total" for v in res.variances)
