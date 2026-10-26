"""Deterministic UAE VAT Calculation Engine adhering to Federal Decree-Law No. (8) of 2017."""

from decimal import Decimal
from typing import List
from .decimal_calc import to_decimal, quantize_currency, quantize_rate
from .models import VATCalculationRequest, VATCalculationResult, CalculationStep

STANDARD_VAT_RATE = Decimal("0.05")
ZERO_VAT_RATE = Decimal("0.00")


def calculate_uae_vat(request: VATCalculationRequest) -> VATCalculationResult:
    """Calculates UAE VAT with full statutory provenance and decimal precision."""
    steps: List[CalculationStep] = []
    base_input = to_decimal(request.amount)
    category = request.vat_category.lower().strip()

    # Determine rate
    if category in ["standard", "std", "5%"]:
        applied_rate = STANDARD_VAT_RATE
        rate_label = "5.00%"
        statutory_ref = "Article 3, 25 of Federal Decree-Law No. (8) of 2017 (Standard Rate 5%)"
    elif category in ["zero_rated", "0%", "zero"]:
        applied_rate = ZERO_VAT_RATE
        rate_label = "0.00%"
        statutory_ref = "Article 45 of Federal Decree-Law No. (8) of 2017 (Zero-rated Supplies: exports, healthcare, education)"
    elif category in ["exempt", "exemption"]:
        applied_rate = ZERO_VAT_RATE
        rate_label = "Exempt (0.00%)"
        statutory_ref = "Article 46 of Federal Decree-Law No. (8) of 2017 (Exempt Supplies: financial services, residential lease)"
    elif category in ["out_of_scope", "oos"]:
        applied_rate = ZERO_VAT_RATE
        rate_label = "Out of Scope (0.00%)"
        statutory_ref = "Article 2 of Federal Decree-Law No. (8) of 2017 (Outside UAE Territorial Scope)"
    else:
        raise ValueError(f"Unsupported UAE VAT category '{category}'. Must be one of: standard, zero_rated, exempt, out_of_scope.")

    steps.append(CalculationStep(
        step_number=1,
        description=f"Validate VAT Category: {category.upper()}",
        formula=f"Applicable VAT Rate = {rate_label}",
        intermediate_value=str(applied_rate),
        statutory_reference=statutory_ref
    ))

    if request.is_tax_inclusive:
        # Amount = Net * (1 + rate) => Net = Amount / (1 + rate), VAT = Amount - Net
        total_gross = quantize_currency(base_input)
        divisor = Decimal("1.00") + applied_rate
        net_amount = quantize_currency(total_gross / divisor)
        vat_amount = quantize_currency(total_gross - net_amount)

        steps.append(CalculationStep(
            step_number=2,
            description="Extract Tax-Exclusive Net Amount from Inclusive Gross",
            formula=f"{total_gross} / (1 + {applied_rate})",
            intermediate_value=str(net_amount),
            statutory_reference="Cabinet Decision No. (52) of 2017 Article 26 (Tax-inclusive calculations)"
        ))
        steps.append(CalculationStep(
            step_number=3,
            description="Derive Tax Amount from Difference",
            formula=f"{total_gross} - {net_amount}",
            intermediate_value=str(vat_amount),
            statutory_reference="Executive Regulation Article 27"
        ))
    else:
        # Tax-exclusive input
        net_amount = quantize_currency(base_input)
        vat_amount = quantize_currency(net_amount * applied_rate)
        total_gross = quantize_currency(net_amount + vat_amount)

        steps.append(CalculationStep(
            step_number=2,
            description="Compute VAT from Tax-Exclusive Base",
            formula=f"{net_amount} * {applied_rate}",
            intermediate_value=str(vat_amount),
            statutory_reference="Federal Decree-Law No. (8) of 2017 Article 25"
        ))
        steps.append(CalculationStep(
            step_number=3,
            description="Sum Net Base and VAT for Total Payable",
            formula=f"{net_amount} + {vat_amount}",
            intermediate_value=str(total_gross),
            statutory_reference="Federal Decree-Law No. (8) of 2017 Article 27"
        ))

    if request.apply_reverse_charge:
        steps.append(CalculationStep(
            step_number=4,
            description="Reverse Charge Mechanism (RCM) Applied",
            formula="Recipient accounts for output and input tax simultaneously in Box 3 of VAT Return",
            intermediate_value=f"RCM VAT = {vat_amount}",
            statutory_reference="Article 48 of Federal Decree-Law No. (8) of 2017 (Reverse Charge on Imported Services)"
        ))

    return VATCalculationResult(
        base_amount=str(net_amount),
        vat_rate_percent=rate_label,
        vat_amount=str(vat_amount),
        total_amount=str(total_gross),
        is_tax_inclusive=request.is_tax_inclusive,
        vat_category=category,
        apply_reverse_charge=request.apply_reverse_charge,
        currency=request.currency.upper(),
        calculation_steps=steps
    )
