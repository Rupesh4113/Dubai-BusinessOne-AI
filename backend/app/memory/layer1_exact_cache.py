"""Layer 1: Exact-Answer Cache with SHA-256 Fingerprinting and Zero-Inference Reuse."""

import hashlib
import json
import time
from typing import Dict, Any, Optional
from pydantic import BaseModel


class CachedAnswer(BaseModel):
    """Cached verified answer record."""
    cache_key: str
    tenant_id: str
    normalized_query: str
    response_data: Dict[str, Any]
    created_at_epoch: float
    ttl_seconds: int
    hit_count: int = 0
    estimated_tokens_saved: int = 0
    regulatory_version: str = "2026.1"
    is_time_sensitive: bool = False  # If True (e.g. live balances, live FX), never reuse stale cache


class ExactAnswerCache:
    """In-memory and Redis-compatible high-performance Layer 1 cache."""

    def __init__(self, default_ttl_seconds: int = 86400):
        self.default_ttl = default_ttl_seconds
        self._store: Dict[str, CachedAnswer] = {}
        self.total_hits = 0
        self.total_misses = 0

    @staticmethod
    def generate_fingerprint(tenant_id: str, query: str, context_params: Optional[Dict[str, Any]] = None, language: str = "en") -> str:
        """Generates deterministic SHA-256 cache key from normalized parameters."""
        normalized_q = " ".join(query.lower().strip().split())
        params_str = ""
        if context_params:
            # Sort keys for deterministic JSON serialization
            params_str = json.dumps(context_params, sort_keys=True)
        raw_key = f"{tenant_id}:{language}:{normalized_q}:{params_str}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def get(self, cache_key: str) -> Optional[CachedAnswer]:
        """Retrieves verified cached answer if unexpired and not stale."""
        entry = self._store.get(cache_key)
        if not entry:
            self.total_misses += 1
            return None

        # Check time-sensitive veto
        if entry.is_time_sensitive:
            # Time-sensitive requests (e.g. live account balances) expire within 60 seconds
            if time.time() - entry.created_at_epoch > 60:
                del self._store[cache_key]
                self.total_misses += 1
                return None

        # Check TTL
        if time.time() - entry.created_at_epoch > entry.ttl_seconds:
            del self._store[cache_key]
            self.total_misses += 1
            return None

        entry.hit_count += 1
        entry.estimated_tokens_saved += 800  # Average task inference tokens
        self.total_hits += 1
        return entry

    def set(
        self,
        cache_key: str,
        tenant_id: str,
        normalized_query: str,
        response_data: Dict[str, Any],
        ttl_seconds: Optional[int] = None,
        is_time_sensitive: bool = False
    ) -> CachedAnswer:
        """Stores verified response in exact cache."""
        ttl = ttl_seconds or self.default_ttl
        entry = CachedAnswer(
            cache_key=cache_key,
            tenant_id=tenant_id,
            normalized_query=normalized_query,
            response_data=response_data,
            created_at_epoch=time.time(),
            ttl_seconds=ttl,
            hit_count=0,
            estimated_tokens_saved=0,
            is_time_sensitive=is_time_sensitive
        )
        self._store[cache_key] = entry
        return entry

    def invalidate_tenant(self, tenant_id: str) -> int:
        """Purges cache entries for a specific tenant."""
        keys_to_remove = [k for k, v in self._store.items() if v.tenant_id == tenant_id]
        for k in keys_to_remove:
            del self._store[k]
        return len(keys_to_remove)

    def get_stats(self) -> Dict[str, Any]:
        """Returns cache telemetry and zero-inference reuse metrics."""
        total_requests = self.total_hits + self.total_misses
        hit_ratio = (self.total_hits / total_requests) if total_requests > 0 else 0.0
        total_tokens_saved = sum(e.estimated_tokens_saved for e in self._store.values())

        return {
            "total_cached_entries": len(self._store),
            "total_hits": self.total_hits,
            "total_misses": self.total_misses,
            "hit_ratio_percent": round(hit_ratio * 100, 2),
            "estimated_zero_inference_tokens_saved": total_tokens_saved
        }


# Global instance
layer1_cache = ExactAnswerCache()
