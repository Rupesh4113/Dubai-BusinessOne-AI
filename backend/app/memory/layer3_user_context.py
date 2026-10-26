"""Layer 3: User and Organization Memory with Strict Tenant Isolation."""

import time
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class TenantProfile(BaseModel):
    """Consented business entity and organizational memory profile."""
    tenant_id: str
    company_name: str
    trade_license_number: Optional[str] = None
    legal_form: str = "llc"
    preferred_language: str = "en"
    preferred_currency: str = "AED"
    trn: Optional[str] = None
    registered_activities: list[str] = []
    user_consent_granted: bool = True
    last_updated_epoch: float = Field(default_factory=time.time)
    workflow_state_context: Dict[str, Any] = Field(default_factory=dict)


class UserOrganizationMemory:
    """Manages Layer 3 tenant profiles and contextual preferences."""

    def __init__(self):
        self._profiles: Dict[str, TenantProfile] = {}
        # Prepopulate demo enterprise tenant
        self._profiles["demo_tenant_dubai"] = TenantProfile(
            tenant_id="demo_tenant_dubai",
            company_name="Apex Global Technologies LLC",
            trade_license_number="CN-1092834",
            legal_form="llc",
            preferred_language="en",
            preferred_currency="AED",
            trn="100349821000003",
            registered_activities=["Information Technology Consultancy", "Software Design"]
        )

    def get_profile(self, tenant_id: str) -> Optional[TenantProfile]:
        """Retrieves tenant profile strictly partitioned by tenant_id."""
        return self._profiles.get(tenant_id)

    def update_profile(self, tenant_id: str, updates: Dict[str, Any]) -> TenantProfile:
        """Updates or creates consented organizational profile."""
        if tenant_id not in self._profiles:
            profile = TenantProfile(tenant_id=tenant_id, company_name=updates.get("company_name", "New Enterprise"))
            self._profiles[tenant_id] = profile
        else:
            profile = self._profiles[tenant_id]

        for k, v in updates.items():
            if hasattr(profile, k):
                setattr(profile, k, v)
        profile.last_updated_epoch = time.time()
        return profile

    def update_workflow_context(self, tenant_id: str, key: str, value: Any) -> None:
        """Stores ongoing workflow context (e.g. pending license application draft)."""
        if tenant_id in self._profiles:
            self._profiles[tenant_id].workflow_state_context[key] = value

    def clear_workflow_context(self, tenant_id: str) -> None:
        """Clears temporary workflow context upon task completion."""
        if tenant_id in self._profiles:
            self._profiles[tenant_id].workflow_state_context.clear()


layer3_memory = UserOrganizationMemory()
