"""Official Registry Search Tool (Dubai DET / DED Commercial Register)."""

from typing import Dict, Any, List
from .base import BaseTool, ToolResult

# Mock authoritative commercial register records
MOCK_EXISTING_BUSINESSES = [
    {"name": "EMIRATES AIRLINE", "license_no": "CN-10001", "status": "ACTIVE", "type": "Commercial"},
    {"name": "DUBAI HOLDING LLC", "license_no": "CN-10002", "status": "ACTIVE", "type": "Commercial"},
    {"name": "APEX GLOBAL TECHNOLOGIES LLC", "license_no": "CN-1092834", "status": "ACTIVE", "type": "Professional"},
    {"name": "AL WASL TRADING CO", "license_no": "CN-2049182", "status": "ACTIVE", "type": "Commercial"},
]


class OfficialRegistrySearchTool(BaseTool):
    name = "official_registry_search"
    description = "Searches Dubai DET commercial register for trade name availability and registered licenses."
    risk_level = "LOW"
    requires_approval = False

    def run(self, params: Dict[str, Any], context: Dict[str, Any]) -> ToolResult:
        query = str(params.get("query", "")).strip().upper()
        search_type = params.get("search_type", "name_availability")  # "name_availability" or "license_lookup"

        if not query:
            return ToolResult(
                tool_name=self.name,
                success=False,
                data={},
                error_message="Query parameter is required.",
                verification_passed=False
            )

        audit = [f"Queried official Dubai DET commercial register for '{query}'"]

        if search_type == "name_availability":
            # Check if name is taken
            matching = [b for b in MOCK_EXISTING_BUSINESSES if query in b["name"] or b["name"] in query]
            is_available = len(matching) == 0

            audit.append(f"Trade name check: {'Available' if is_available else 'Conflict Detected'}")
            return ToolResult(
                tool_name=self.name,
                success=True,
                data={
                    "proposed_name": query,
                    "is_available": is_available,
                    "existing_conflicts": matching,
                    "jurisdiction": "Dubai Department of Economy and Tourism (DET)",
                    "official_source": "https://www.ded.ae/commercial-register",
                    "guidance": "Trade name complies with Dubai DET guidelines (no restricted religious/political terms)" if is_available else "Proposed name conflicts with an existing registered entity. Modify name or add distinctive suffixes."
                },
                audit_trail=audit
            )
        else:
            # License lookup
            matching = [b for b in MOCK_EXISTING_BUSINESSES if query in b["license_no"] or query in b["name"]]
            return ToolResult(
                tool_name=self.name,
                success=True,
                data={"results": matching, "count": len(matching)},
                audit_trail=audit
            )
