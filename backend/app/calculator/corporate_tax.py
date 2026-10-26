"""Deterministic UAE Corporate Tax Engine according to Federal Decree-Law No. 47 of 2022."""

from decimal import Decimal
from typing import List
from .decimal_calc import to_decimal, quantize_currency, quantize_rate
from .models import CorporateTaxRequest, CorporateTaxResult, CalculationStep

EXEMPT_THRESHOLD_AED = Decimal("375000.00")
SBR_REVENUE_THRESHOLD_AED = Decimal("3000000.00")
STANDARD_CT_RATE = Decimal("0.09")
ZERO_CT_RATE = Decimal("0.00")
DE_MINIMIS_CAP_AED = Decimal("5000000.00")
DE_MINIMIS_PERCENT = Decimal("0.05")


def calculate_uae_corporate_tax(request: CorporateTaxRequest) -> CorporateTaxResult:
    """Calculates UAE Corporate Tax with statutory step provenance and decimal precision."""
    steps: List[CalculationStep] = []
    net_profit = to_decimal(request.taxable_net_profit)
    annual_revenue = to_decimal(request.annual_revenue) if request.annual_revenue is not None else None
    non_qual_rev = to_decimal(request.non_qualifying_revenue)

    if net_profit < Decimal("0.00"):
        # Tax loss carried forward
        steps.append(CalculationStep(
            step_number=1,
            description="Tax Loss Identification",
            formula=f"Net Profit = {net_profit} < 0",
            intermediate_value="0.00",
            statutory_reference="Federal Decree-Law No. 47 of 2022 Article 37 (Tax Loss Relief: Carry forward up to 75% of future taxable income)"
        ))
        return CorporateTaxResult(
            taxable_net_profit=str(quantize_currency(net_profit)),
            annual_revenue=str(quantize_currency(annual_revenue)) if annual_revenue else None,
            small_business_relief_eligible=False,
            small_business_relief_applied=False,
            tier1_exempt_amount="0.00",
            tier2_taxable_amount="0.00",
            effective_tax_rate_percent="0.00%",
            total_tax_payable_aed="0.00",
            is_qualifying_free_zone_person=request.is_qualifying_free_zone_person,
            calculation_steps=steps
        )

    # 1. Check Small Business Relief (SBR)
    sbr_eligible = False
    sbr_applied = False
    if annual_revenue is not None and annual_revenue <= SBR_REVENUE_THRESHOLD_AED:
        sbr_eligible = True
        if request.elect_small_business_relief:
            sbr_applied = True
            steps.append(CalculationStep(
                step_number=1,
                description="Small Business Relief (SBR) Election Applied",
                formula=f"Annual Revenue ({annual_revenue}) <= Threshold ({SBR_REVENUE_THRESHOLD_AED})",
                intermediate_value="0.00 Tax Payable",
                statutory_reference="Ministerial Decision No. 73 of 2023 & Federal Decree-Law No. 47 of 2022 Article 21"
            ))
            return CorporateTaxResult(
                taxable_net_profit=str(quantize_currency(net_profit)),
                annual_revenue=str(quantize_currency(annual_revenue)),
                small_business_relief_eligible=True,
                small_business_relief_applied=True,
                tier1_exempt_amount=str(quantize_currency(net_profit)),
                tier2_taxable_amount="0.00",
                effective_tax_rate_percent="0.00%",
                total_tax_payable_aed="0.00",
                is_qualifying_free_zone_person=request.is_qualifying_free_zone_person,
                calculation_steps=steps
            )

    # 2. Check Qualifying Free Zone Person (QFZP) regime
    if request.is_qualifying_free_zone_person:
        # Check de minimis rule: Non-qualifying revenue must not exceed lower of 5% of total revenue or AED 5,000,000
        de_minimis_limit = DE_MINIMIS_CAP_AED
        if annual_revenue is not None and annual_revenue > Decimal("0.00"):
            percent_limit = quantize_currency(annual_revenue * DE_MINIMIS_PERCENT)
            de_minimis_limit = min(percent_limit, DE_MINIMIS_CAP_AED)

        de_minimis_met = non_qual_rev <= de_minimis_limit

        if de_minimis_met:
            # QFZP qualifies for 0% on Qualifying Income
            steps.append(CalculationStep(
                step_number=1,
                description="Qualifying Free Zone Person (QFZP) Status Verified",
                formula=f"Non-qualifying revenue ({non_qual_rev}) <= De Minimis Limit ({de_minimis_limit})",
                intermediate_value="0% on Qualifying Income",
                statutory_reference="Cabinet Decision No. 55 of 2023 & Ministerial Decision No. 139 of 2023"
            ))
            tax_payable = Decimal("0.00")
            if non_qual_rev > Decimal("0.00"):
                # Non-qualifying income taxed at 9%
                non_qual_tax = quantize_currency(non_qual_rev * STANDARD_CT_RATE)
                tax_payable = non_qual_tax
                steps.append(CalculationStep(
                    step_number=2,
                    description="Tax on Non-Qualifying Free Zone Income",
                    formula=f"{non_qual_rev} * 9%",
                    intermediate_value=str(non_qual_tax),
                    statutory_reference="Cabinet Decision No. 55 of 2023 Article 3"
                ))

            effective_rate = quantize_rate((tax_payable / net_profit * Decimal("100.00")) if net_profit > 0 else Decimal("0.00"))
            return CorporateTaxResult(
                taxable_net_profit=str(quantize_currency(net_profit)),
                annual_revenue=str(quantize_currency(annual_revenue)) if annual_revenue else None,
                small_business_relief_eligible=sbr_eligible,
                small_business_relief_applied=False,
                tier1_exempt_amount=str(quantize_currency(net_profit)),
                tier2_taxable_amount=str(quantize_currency(non_qual_rev)),
                effective_tax_rate_percent=f"{effective_rate}%",
                total_tax_payable_aed=str(tax_payable),
                is_qualifying_free_zone_person=True,
                calculation_steps=steps
            )
        else:
            steps.append(CalculationStep(
                step_number=1,
                description="QFZP De Minimis Breach - Disqualified from 0% Free Zone Benefit",
                formula=f"Non-qualifying revenue ({non_qual_rev}) > De Minimis Limit ({de_minimis_limit})",
                intermediate_value="Entire profit subject to Standard 9% regime",
                statutory_reference="Cabinet Decision No. 55 of 2023 Article 4 (Tainted Status for 5 tax periods)"
            ))

    # 3. Standard Regime Tier Calculation
    steps.append(CalculationStep(
        step_number=1,
        description="Statutory Tax Bracket Separation",
        formula=f"Tier 1 (0%): Up to {EXEMPT_THRESHOLD_AED} AED | Tier 2 (9%): Above {EXEMPT_THRESHOLD_AED} AED",
        intermediate_value=f"Net Profit = {quantize_currency(net_profit)} AED",
        statutory_reference="Federal Decree-Law No. 47 of 2022 Article 3(1)"
    ))

    if net_profit <= EXEMPT_THRESHOLD_AED:
        tier1_amount = net_profit
        tier2_amount = Decimal("0.00")
        tax_payable = Decimal("0.00")
        effective_rate = Decimal("0.00")

        steps.append(CalculationStep(
            step_number=2,
            description="Entire Net Profit Falls Within 0% Exemption Bracket",
            formula=f"{net_profit} * 0%",
            intermediate_value="0.00 AED",
            statutory_reference="Federal Decree-Law No. 47 of 2022 Article 3(1)(a)"
        ))
    else:
        tier1_amount = EXEMPT_THRESHOLD_AED
        tier2_amount = net_profit - EXEMPT_THRESHOLD_AED
        tax_payable = quantize_currency(tier2_amount * STANDARD_CT_RATE)
        effective_rate = quantize_rate((tax_payable / net_profit) * Decimal("100.00"))

        steps.append(CalculationStep(
            step_number=2,
            description="Tier 1 Exempt Allocation (0%)",
            formula=f"{EXEMPT_THRESHOLD_AED} * 0%",
            intermediate_value="0.00 AED",
            statutory_reference="Federal Decree-Law No. 47 of 2022 Article 3(1)(a)"
        ))
        steps.append(CalculationStep(
            step_number=3,
            description="Tier 2 Taxable Amount Allocation (9%)",
            formula=f"({quantize_currency(net_profit)} - {EXEMPT_THRESHOLD_AED}) * 9% = {quantize_currency(tier2_amount)} * 0.09",
            intermediate_value=f"{tax_payable} AED",
            statutory_reference="Federal Decree-Law No. 47 of 2022 Article 3(1)(b)"
        ))

    return CorporateTaxResult(
        taxable_net_profit=str(quantize_currency(net_profit)),
        annual_revenue=str(quantize_currency(annual_revenue)) if annual_revenue else None,
        small_business_relief_eligible=sbr_eligible,
        small_business_relief_applied=False,
        tier1_exempt_amount=str(quantize_currency(tier1_amount)),
        tier2_taxable_amount=str(quantize_currency(tier2_amount)),
        effective_tax_rate_percent=f"{effective_rate}%",
        total_tax_payable_aed=str(tax_payable),
        is_qualifying_free_zone_person=request.is_qualifying_free_zone_person,
        calculation_steps=steps
    )
