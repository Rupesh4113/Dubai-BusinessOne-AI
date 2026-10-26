"""Deterministic Dubai Department of Economy and Tourism (DET / DED) Licensing Fee Engine."""

from decimal import Decimal
from typing import List
from .decimal_calc import to_decimal, quantize_currency
from .models import DubaiDETFeeRequest, DubaiDETFeeResult, CalculationStep

INITIAL_APPROVAL_FEE = Decimal("120.00")
TRADE_NAME_FEE = Decimal("620.00")
COMMERCIAL_REGISTER_FEE = Decimal("100.00")
KNOWLEDGE_INNOVATION_FEE = Decimal("20.00")  # AED 10 Knowledge + AED 10 Innovation
MARKET_FEE_PERCENT = Decimal("0.05")  # 5% of annual lease


def calculate_dubai_det_fees(request: DubaiDETFeeRequest) -> DubaiDETFeeResult:
    """Calculates official DET / DED business startup and license fees with step-by-step breakdown."""
    steps: List[CalculationStep] = []
    license_type = request.license_type.lower().strip()
    rent = to_decimal(request.annual_office_rent_aed)
    activities = max(1, request.number_of_activities)

    # 1. Base license fee based on activity type
    if license_type in ["commercial", "general_trading", "trading"]:
        base_fee = Decimal("6000.00")
        type_label = "Commercial License"
    elif license_type in ["professional", "services", "consulting"]:
        base_fee = Decimal("4000.00")
        type_label = "Professional License"
    elif license_type in ["industrial", "manufacturing"]:
        base_fee = Decimal("8000.00")
        type_label = "Industrial License"
    elif license_type in ["tourism", "travel"]:
        base_fee = Decimal("7500.00")
        type_label = "Tourism License"
    else:
        base_fee = Decimal("5000.00")
        type_label = "General Business License"

    # Additional activity fee: AED 500 per activity over 1
    extra_activity_fee = Decimal("0.00")
    if activities > 1:
        extra_activity_fee = Decimal(str((activities - 1) * 500))
        base_fee += extra_activity_fee

    steps.append(CalculationStep(
        step_number=1,
        description=f"Base License Classification: {type_label}",
        formula=f"Base Fee AED {base_fee - extra_activity_fee} + Additional Activities ({activities - 1} * AED 500) = AED {base_fee}",
        intermediate_value=f"AED {quantize_currency(base_fee)}",
        statutory_reference="DET Commercial Licensing Guide & Law No. 13 of 2011"
    ))

    # 2. Fixed statutory fees
    steps.append(CalculationStep(
        step_number=2,
        description="Statutory Government Processing Vouchers",
        formula=f"Initial Approval (AED {INITIAL_APPROVAL_FEE}) + Trade Name Reservation (AED {TRADE_NAME_FEE}) + Commercial Register (AED {COMMERCIAL_REGISTER_FEE})",
        intermediate_value=f"AED {INITIAL_APPROVAL_FEE + TRADE_NAME_FEE + COMMERCIAL_REGISTER_FEE}",
        statutory_reference="Executive Council Resolution No. (30) of 2017"
    ))

    # 3. Market Fee (Dubai Municipality Tenancy Fee 5%)
    if request.is_instant_license:
        market_fee = Decimal("0.00")
        steps.append(CalculationStep(
            step_number=3,
            description="Dubai Municipality Market Fee Waiver (Instant License Year 1)",
            formula="No lease agreement requirement for year 1 under Instant License initiative",
            intermediate_value="AED 0.00",
            statutory_reference="Dubai DET Instant License Scheme Guidelines"
        ))
    else:
        market_fee = quantize_currency(rent * MARKET_FEE_PERCENT)
        steps.append(CalculationStep(
            step_number=3,
            description="Dubai Municipality Market Fee (5% of Annual Tenancy)",
            formula=f"{quantize_currency(rent)} * 5%",
            intermediate_value=f"AED {market_fee}",
            statutory_reference="Local Order No. (2) of 1962 & Tenancy Market Fee Regulations"
        ))

    # 4. Total calculation
    total_cost = (
        INITIAL_APPROVAL_FEE
        + TRADE_NAME_FEE
        + base_fee
        + COMMERCIAL_REGISTER_FEE
        + market_fee
        + KNOWLEDGE_INNOVATION_FEE
    )

    steps.append(CalculationStep(
        step_number=4,
        description="Consolidate Total DET Official Setup Cost",
        formula=f"{INITIAL_APPROVAL_FEE} + {TRADE_NAME_FEE} + {base_fee} + {COMMERCIAL_REGISTER_FEE} + {market_fee} + {KNOWLEDGE_INNOVATION_FEE}",
        intermediate_value=f"AED {quantize_currency(total_cost)}",
        statutory_reference="Consolidated DET Commercial Voucher"
    ))

    return DubaiDETFeeResult(
        license_type=type_label,
        initial_approval_fee_aed=str(quantize_currency(INITIAL_APPROVAL_FEE)),
        trade_name_reservation_fee_aed=str(quantize_currency(TRADE_NAME_FEE)),
        base_license_fee_aed=str(quantize_currency(base_fee)),
        commercial_register_fee_aed=str(quantize_currency(COMMERCIAL_REGISTER_FEE)),
        market_fee_aed=str(market_fee),
        knowledge_and_innovation_dirham_aed=str(quantize_currency(KNOWLEDGE_INNOVATION_FEE)),
        total_det_setup_cost_aed=str(quantize_currency(total_cost)),
        calculation_steps=steps
    )
