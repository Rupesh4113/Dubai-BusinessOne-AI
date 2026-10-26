"""Deterministic Dubai Chamber of Commerce Membership Fee Calculation Engine."""

from decimal import Decimal
from typing import List
from .decimal_calc import to_decimal, quantize_currency
from .models import DubaiChamberFeeRequest, DubaiChamberFeeResult, CalculationStep

CHAMBER_CERTIFICATE_FEE = Decimal("50.00")


def calculate_dubai_chamber_fee(request: DubaiChamberFeeRequest) -> DubaiChamberFeeResult:
    """Calculates official Dubai Chamber of Commerce membership fees based on legal form and capital."""
    steps: List[CalculationStep] = []
    legal_form = request.legal_form.lower().strip()
    capital = to_decimal(request.share_capital)
    partners = request.number_of_partners or 1

    steps.append(CalculationStep(
        step_number=1,
        description=f"Identify Entity Legal Structure: {legal_form.upper()}",
        formula=f"Legal Form = {legal_form}, Declared Capital = AED {quantize_currency(capital)}, Partners = {partners}",
        intermediate_value=legal_form,
        statutory_reference="Dubai Chamber of Commerce Law No. (1) of 2022 & Executive Fee Regulations"
    ))

    if legal_form in ["llc", "limited_liability_company", "commercial"]:
        if capital > Decimal("500000.00"):
            base_fee = Decimal("2200.00")
            tier_name = "LLC / Commercial (Capital > AED 500,000) - Tier A"
        else:
            base_fee = Decimal("1200.00")
            tier_name = "LLC / Commercial (Capital <= AED 500,000) - Tier B"
    elif legal_form in ["branch_foreign", "foreign_branch"]:
        base_fee = Decimal("2200.00")
        tier_name = "Branch of Foreign Company / International Enterprise"
    elif legal_form in ["branch_local", "local_branch"]:
        base_fee = Decimal("1000.00")
        tier_name = "Branch of UAE Local Mainland Company"
    elif legal_form in ["freezone_branch", "free_zone_branch"]:
        base_fee = Decimal("2200.00")
        tier_name = "Branch of Free Zone Enterprise Operating in Dubai"
    elif legal_form in ["sole_proprietorship", "sole_establishment", "professional", "civil_company"]:
        if partners > 1:
            base_fee = Decimal("1000.00")
            tier_name = "Civil Company / Multi-partner Professional Services"
        else:
            base_fee = Decimal("700.00")
            tier_name = "Individual Professional / Sole Establishment"
    else:
        # Default commercial fallback
        base_fee = Decimal("1200.00")
        tier_name = "Standard Commercial Entity"

    steps.append(CalculationStep(
        step_number=2,
        description="Determine Annual Membership Base Fee",
        formula=f"Fee Schedule Tier: {tier_name}",
        intermediate_value=f"AED {quantize_currency(base_fee)}",
        statutory_reference="Dubai Chamber Official Tariff Schedule"
    ))

    cert_fee = CHAMBER_CERTIFICATE_FEE if request.is_new_registration else Decimal("0.00")
    if cert_fee > 0:
        steps.append(CalculationStep(
            step_number=3,
            description="Chamber Membership Certificate & Electronic Verification",
            formula=f"Fixed statutory documentation fee: AED {cert_fee}",
            intermediate_value=f"AED {cert_fee}",
            statutory_reference="Dubai Chamber Electronic Attestation Regulation"
        ))

    total_fee = base_fee + cert_fee

    steps.append(CalculationStep(
        step_number=4 if cert_fee > 0 else 3,
        description="Compute Total Dubai Chamber Fees",
        formula=f"{base_fee} + {cert_fee}",
        intermediate_value=f"AED {quantize_currency(total_fee)}",
        statutory_reference="Total Annual Obligation"
    ))

    return DubaiChamberFeeResult(
        legal_form=legal_form,
        share_capital_aed=str(quantize_currency(capital)),
        base_membership_fee_aed=str(quantize_currency(base_fee)),
        certificate_and_verification_fee_aed=str(quantize_currency(cert_fee)),
        total_chamber_fee_aed=str(quantize_currency(total_fee)),
        schedule_tier=tier_name,
        renewal_cycle="Annual",
        calculation_steps=steps
    )
