"""Tool Registry and Execution Policy Controller."""

from typing import Dict, List, Optional, Any
from .base import BaseTool, ToolResult
from .official_registry_tool import OfficialRegistrySearchTool
from .fee_calculator_tool import FeeCalculatorTool
from .invoice_reconciliation_tool import InvoiceReconciliationTool
from .trade_license_tool import TradeLicenseReservationTool
from .document_generator_tool import DocumentGeneratorTool


class ToolRegistry:
    """Central registry and security sandbox for authorized agent tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        # Register standard suite
        self.register(OfficialRegistrySearchTool())
        self.register(FeeCalculatorTool())
        self.register(InvoiceReconciliationTool())
        self.register(TradeLicenseReservationTool())
        self.register(DocumentGeneratorTool())

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "risk_level": t.risk_level,
                "requires_approval": t.requires_approval,
                "required_role": t.required_role
            }
            for t in self._tools.values()
        ]

    def execute_tool(self, tool_name: str, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        """Executes tool safely through risk and permission policies."""
        tool = self._tools.get(tool_name)
        if not tool:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                data={},
                error_message=f"Unauthorized or unknown tool: '{tool_name}'",
                verification_passed=False
            )

        # Enforce human approval if tool is marked HIGH RISK or requires approval
        if tool.requires_approval and not context.get("human_approved", False):
            return ToolResult(
                tool_name=tool.name,
                success=False,
                data={"risk_level": tool.risk_level, "requires_approval": True},
                error_message="Action held: Requires explicit Human Supervisor Approval before execution.",
                verification_passed=False,
                audit_trail=["Execution intercepted by Risk Assessment Gate (Awaiting Human Approval)."]
            )

        return tool.run(params, context)


tool_registry = ToolRegistry()
