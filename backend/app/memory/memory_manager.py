"""Unified 4-Layer Memory and Zero-Inference Manager."""

from typing import Dict, Any, Optional, List
from .layer1_exact_cache import layer1_cache, CachedAnswer
from .layer2_knowledge_base import layer2_kb
from .layer3_user_context import layer3_memory, TenantProfile
from .layer4_execution_history import layer4_history, ExecutionRecord


class MemoryManager:
    """Coordinates Layer 1 (Exact Answer Cache), Layer 2 (Verified Knowledge),

    Layer 3 (User/Org Context), and Layer 4 (Execution History & Idempotency).
    """

    def __init__(self):
        self.l1 = layer1_cache
        self.l2 = layer2_kb
        self.l3 = layer3_memory
        self.l4 = layer4_history

    def check_layer1_exact_match(
        self,
        tenant_id: str,
        query: str,
        context_params: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> Optional[CachedAnswer]:
        """Layer 1 Check: Returns verified cached response with ZERO LLM inference cost."""
        fingerprint = self.l1.generate_fingerprint(tenant_id, query, context_params, language)
        return self.l1.get(fingerprint)

    def record_layer1_verified_answer(
        self,
        tenant_id: str,
        query: str,
        response_data: Dict[str, Any],
        context_params: Optional[Dict[str, Any]] = None,
        language: str = "en",
        ttl_seconds: Optional[int] = None,
        is_time_sensitive: bool = False
    ) -> CachedAnswer:
        """Stores verified answer in Layer 1 for future zero-inference reuse."""
        fingerprint = self.l1.generate_fingerprint(tenant_id, query, context_params, language)
        return self.l1.set(
            cache_key=fingerprint,
            tenant_id=tenant_id,
            normalized_query=query,
            response_data=response_data,
            ttl_seconds=ttl_seconds,
            is_time_sensitive=is_time_sensitive
        )

    def query_layer2_knowledge(self, query: str, category: Optional[str] = None, max_results: int = 5) -> List[Dict[str, Any]]:
        """Layer 2 Search: Retrieves verified official regulatory clauses."""
        return self.l2.retrieve(query, category=category, max_results=max_results)

    def get_layer3_context(self, tenant_id: str) -> Optional[TenantProfile]:
        """Layer 3 Retrieval: Consented enterprise profile and preferences."""
        return self.l3.get_profile(tenant_id)

    def get_layer4_execution_history(self, tenant_id: str, limit: int = 20) -> List[ExecutionRecord]:
        """Layer 4 Audit: Immutable execution logs."""
        return self.l4.list_tasks(tenant_id, limit=limit)

    def get_telemetry(self) -> Dict[str, Any]:
        """System-wide memory telemetry."""
        return {
            "layer1_cache_stats": self.l1.get_stats(),
            "layer4_pending_approvals_count": len(self.l4.list_pending_approvals())
        }


memory_manager = MemoryManager()
