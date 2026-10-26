"""Invoice Reconciliation Tool."""

from decimal import Decimal
from typing import Dict, Any
from .base import BaseTool, ToolResult
from ..calculator import reconcile_invoice, InvoiceReconciliationRequest, InvoiceLineItem


class InvoiceReconciliationTool(BaseTool):
    name = "invoice_reconciler"
    description = "Performs mathematical line-item reconciliation, VAT validation, and TRN format verification on commercial invoices."
    risk_level = "LOW"
    requires_approval = False

    def run(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        audit = ["Initiated invoice reconciliation"]
        try:
            line_items_raw = params.get("line_items", [])
            parsed_lines = []
            for item in line_items_raw:
                parsed_lines.append(InvoiceLineItem(
                    line_number=item.get("line_number", 1),
                    description=item.get("description", "Line Item"),
                    quantity=Decimal(str(item.get("quantity", 1))),
                    unit_price=Decimal(str(item.get("unit_price", 0))),
                    discount_amount=Decimal(str(item.get("discount_amount", 0))),
                    vat_rate=Decimal(str(item.get("vat_rate", 0.05))),
                    reported_line_total=Decimal(str(item.get("reported_line_total", 0)))
                ))

            req = InvoiceReconciliationRequest(
                invoice_number=params.get("invoice_number", "INV-UNKNOWN"),
                vendor_trn=params.get("vendor_trn"),
                buyer_trn=params.get("buyer_trn"),
                invoice_date=params.get("invoice_date", "2026-03-01"),
                currency=params.get("currency", "AED"),
                line_items=parsed_lines,
                reported_subtotal=Decimal(str(params.get("reported_subtotal", 0))),
                reported_vat_total=Decimal(str(params.get("reported_vat_total", 0))),
                reported_grand_total=Decimal(str(params.get("reported_grand_total", 0)))
            )

            result = reconcile_invoice(req)
            audit.extend(result.audit_notes)
            return ToolResult(
                tool_name=self.name,
                success=True,
                data=result.model_dump(),
                verification_passed=result.compliance_passed,
                audit_trail=audit
            )

        except Exception as e:
            return ToolResult(
                tool_name=self.name,
                success=False,
                data={},
                error_message=f"Reconciliation processing failure: {str(e)}",
                verification_passed=False
            )
