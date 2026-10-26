"""Fee and Financial Calculation Tool invoking deterministic decimal engines."""

from decimal import Decimal
from typing import Dict, Any
from .base import BaseTool, ToolResult
from ..calculator import (
    calculate_dubai_det_fees,
    calculate_dubai_chamber_fee,
    calculate_uae_corporate_tax,
    calculate_uae_vat,
    convert_currency,
    DubaiDETFeeRequest,
    DubaiChamberFeeRequest,
    CorporateTaxRequest,
    VATCalculationRequest,
    CurrencyConversionRequest
)


class FeeCalculatorTool(BaseTool):
    name = "fee_calculator"
    description = "Executes deterministic financial calculations for UAE VAT, Corporate Tax, DET fees, Chamber fees, and Currency conversion."
    risk_level = "LOW"
    requires_approval = False

    def run(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        calc_type = params.get("calculation_type", "").lower()
        audit = [f"Deterministic calculation invoked for type '{calc_type}'"]

        try:
            if calc_type in ["det_setup", "business_setup", "det"]:
                req = DubaiDETFeeRequest(
                    license_type=params.get("license_type", "commercial"),
                    annual_office_rent_aed=Decimal(str(params.get("annual_office_rent_aed", 60000))),
                    number_of_activities=int(params.get("number_of_activities", 1)),
                    is_instant_license=bool(params.get("is_instant_license", False))
                )
                res = calculate_dubai_det_fees(req)
                return ToolResult(tool_name=self.name, success=True, data=res.model_dump(), audit_trail=audit)

            elif calc_type in ["chamber", "dubai_chamber", "chamber_membership"]:
                req = DubaiChamberFeeRequest(
                    legal_form=params.get("legal_form", "llc"),
                    share_capital=Decimal(str(params.get("share_capital", 300000))),
                    number_of_partners=int(params.get("number_of_partners", 1)),
                    is_new_registration=bool(params.get("is_new_registration", True))
                )
                res = calculate_dubai_chamber_fee(req)
                return ToolResult(tool_name=self.name, success=True, data=res.model_dump(), audit_trail=audit)

            elif calc_type in ["corporate_tax", "ct"]:
                req = CorporateTaxRequest(
                    taxable_net_profit=Decimal(str(params.get("taxable_net_profit", 0))),
                    annual_revenue=Decimal(str(params["annual_revenue"])) if "annual_revenue" in params else None,
                    is_qualifying_free_zone_person=bool(params.get("is_qualifying_free_zone_person", False)),
                    non_qualifying_revenue=Decimal(str(params.get("non_qualifying_revenue", 0))),
                    elect_small_business_relief=bool(params.get("elect_small_business_relief", False))
                )
                res = calculate_uae_corporate_tax(req)
                return ToolResult(tool_name=self.name, success=True, data=res.model_dump(), audit_trail=audit)

            elif calc_type in ["vat"]:
                req = VATCalculationRequest(
                    amount=Decimal(str(params.get("amount", 0))),
                    is_tax_inclusive=bool(params.get("is_tax_inclusive", False)),
                    vat_category=params.get("vat_category", "standard"),
                    apply_reverse_charge=bool(params.get("apply_reverse_charge", False)),
                    currency=params.get("currency", "AED")
                )
                res = calculate_uae_vat(req)
                return ToolResult(tool_name=self.name, success=True, data=res.model_dump(), audit_trail=audit)

            elif calc_type in ["currency", "fx"]:
                req = CurrencyConversionRequest(
                    amount=Decimal(str(params.get("amount", 0))),
                    from_currency=params.get("from_currency", "USD"),
                    to_currency=params.get("to_currency", "AED")
                )
                res = convert_currency(req)
                return ToolResult(tool_name=self.name, success=True, data=res.model_dump(), audit_trail=audit)

            else:
                return ToolResult(
                    tool_name=self.name,
                    success=False,
                    data={},
                    error_message=f"Unknown calculation_type: '{calc_type}'. Expected: det_setup, chamber, corporate_tax, vat, currency.",
                    verification_passed=False
                )

        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                data={},
                error_message=f"Calculation error: {str(e)}",
                verification_passed=False
            )
