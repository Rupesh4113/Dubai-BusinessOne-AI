"""Pydantic data models for deterministic calculation engine."""

from typing import List, Optional, Dict, Any
from decimal import Decimal
from pydantic import BaseModel, Field


class CalculationStep(BaseModel):
    """Provenance tracking for intermediate calculation steps."""
    step_number: int
    description: str
    formula: str
    intermediate_value: str
    statutory_reference: Optional[str] = None


class VATCalculationRequest(BaseModel):
    """Input for UAE VAT calculation."""
    amount: Decimal = Field(..., description="Base amount in AED or specified currency")
    is_tax_inclusive: bool = Field(default=False, description="Whether base amount already includes 5% VAT")
    vat_category: str = Field(
        default="standard",
        description="Category: 'standard' (5%), 'zero_rated' (0%), 'exempt' (0%), 'out_of_scope' (0%)"
    )
    apply_reverse_charge: bool = Field(default=False, description="Apply Reverse Charge Mechanism (RCM)")
    currency: str = Field(default="AED", description="Currency code (e.g. AED, USD, EUR)")


class VATCalculationResult(BaseModel):
    """Deterministic result for UAE VAT calculation."""
    base_amount: str
    vat_rate_percent: str
    vat_amount: str
    total_amount: str
    is_tax_inclusive: bool
    vat_category: str
    apply_reverse_charge: bool
    currency: str
    statutory_authority: str = "UAE Federal Tax Authority (FTA)"
    statutory_reference: str = "Federal Decree-Law No. (8) of 2017 on Value Added Tax (Articles 25-27)"
    calculation_steps: List[CalculationStep]


class CorporateTaxRequest(BaseModel):
    """Input for UAE Corporate Tax calculation."""
    taxable_net_profit: Decimal = Field(..., description="Annual taxable net profit in AED")
    annual_revenue: Optional[Decimal] = Field(None, description="Total annual revenue in AED (for Small Business Relief check)")
    is_qualifying_free_zone_person: bool = Field(
        default=False,
        description="Whether entity qualifies for 0% Free Zone Qualifying Income rate"
    )
    non_qualifying_revenue: Optional[Decimal] = Field(
        default=Decimal("0.00"),
        description="Revenue from non-qualifying activities (for QFZP de minimis check)"
    )
    elect_small_business_relief: bool = Field(
        default=False,
        description="Elect for Small Business Relief under Ministerial Decision No. 73 of 2023 (revenue <= AED 3M)"
    )


class CorporateTaxResult(BaseModel):
    """Deterministic result for UAE Corporate Tax calculation."""
    taxable_net_profit: str
    annual_revenue: Optional[str]
    small_business_relief_eligible: bool
    small_business_relief_applied: bool
    tier1_exempt_amount: str  # AED 0 to 375,000 at 0%
    tier2_taxable_amount: str  # Amount above AED 375,000 at 9%
    effective_tax_rate_percent: str
    total_tax_payable_aed: str
    is_qualifying_free_zone_person: bool
    statutory_authority: str = "UAE Federal Tax Authority (FTA)"
    statutory_reference: str = "Federal Decree-Law No. 47 of 2022 on the Taxation of Corporations and Businesses"
    calculation_steps: List[CalculationStep]


class DubaiChamberFeeRequest(BaseModel):
    """Input for Dubai Chamber of Commerce membership fee calculation."""
    legal_form: str = Field(..., description="Legal form: 'llc', 'sole_proprietorship', 'civil_company', 'branch_foreign', 'branch_local', 'freezone_branch'")
    share_capital: Optional[Decimal] = Field(default=Decimal("300000.00"), description="Declared share capital in AED")
    number_of_partners: Optional[int] = Field(default=1, description="Number of individual/corporate shareholders")
    is_new_registration: bool = Field(default=True, description="New registration vs annual renewal")


class DubaiChamberFeeResult(BaseModel):
    """Deterministic Dubai Chamber fee schedule result."""
    legal_form: str
    share_capital_aed: str
    base_membership_fee_aed: str
    certificate_and_verification_fee_aed: str
    total_chamber_fee_aed: str
    schedule_tier: str
    renewal_cycle: str = "Annual"
    statutory_authority: str = "Dubai Chamber of Commerce"
    statutory_reference: str = "Dubai Chamber Executive Regulations & Approved Fee Schedule"
    calculation_steps: List[CalculationStep]


class DubaiDETFeeRequest(BaseModel):
    """Input for Dubai Department of Economy and Tourism (DET / DED) initial setup calculation."""
    license_type: str = Field(..., description="Type: 'commercial', 'professional', 'industrial', 'tourism'")
    annual_office_rent_aed: Decimal = Field(default=Decimal("60000.00"), description="Annual office lease amount for 5% market fee")
    number_of_activities: int = Field(default=1, description="Number of licensed commercial activities")
    is_instant_license: bool = Field(default=False, description="Instant License without initial lease requirement for year 1")


class DubaiDETFeeResult(BaseModel):
    """Deterministic DET business setup breakdown."""
    license_type: str
    initial_approval_fee_aed: str
    trade_name_reservation_fee_aed: str
    base_license_fee_aed: str
    commercial_register_fee_aed: str
    market_fee_aed: str  # 5% of lease value or AED 0 if instant license
    knowledge_and_innovation_dirham_aed: str
    total_det_setup_cost_aed: str
    statutory_authority: str = "Dubai Department of Economy and Tourism (DET)"
    statutory_reference: str = "DET Commercial Licensing & Dubai Municipality Market Fee Regulations"
    calculation_steps: List[CalculationStep]


class CurrencyConversionRequest(BaseModel):
    """Currency conversion input."""
    amount: Decimal = Field(..., description="Amount to convert")
    from_currency: str = Field(..., description="Source currency code (e.g., USD, EUR, GBP, INR, SAR)")
    to_currency: str = Field(default="AED", description="Target currency code (e.g., AED)")


class CurrencyConversionResult(BaseModel):
    """Deterministic currency conversion with timestamp and provenance."""
    amount: str
    from_currency: str
    to_currency: str
    exchange_rate: str
    converted_amount: str
    rate_timestamp: str
    rate_source: str
    is_pegged_rate: bool
    calculation_steps: List[CalculationStep]


class InvoiceLineItem(BaseModel):
    """Single line item in invoice reconciliation."""
    line_number: int
    description: str
    quantity: Decimal
    unit_price: Decimal
    discount_amount: Decimal = Decimal("0.00")
    vat_rate: Decimal = Decimal("0.05")
    reported_line_total: Decimal


class InvoiceReconciliationRequest(BaseModel):
    """Input for invoice reconciliation and validation."""
    invoice_number: str
    vendor_trn: Optional[str] = None
    buyer_trn: Optional[str] = None
    invoice_date: str
    currency: str = "AED"
    line_items: List[InvoiceLineItem]
    reported_subtotal: Decimal
    reported_vat_total: Decimal
    reported_grand_total: Decimal


class ReconciliationVariance(BaseModel):
    """Identified variance or discrepancy in invoice."""
    field_name: str
    reported_value: str
    calculated_value: str
    variance_amount: str
    severity: str  # 'CRITICAL', 'WARNING', 'INFO'
    explanation: str


class InvoiceReconciliationResult(BaseModel):
    """Comprehensive invoice validation and reconciliation result."""
    invoice_number: str
    is_valid: bool
    has_discrepancy: bool
    trn_validation_status: str
    calculated_subtotal: str
    calculated_vat_total: str
    calculated_grand_total: str
    variances: List[ReconciliationVariance]
    audit_notes: List[str]
    compliance_passed: bool
