"""Caching utilities for performance optimization."""

from __future__ import annotations

import functools
import hashlib
import json
import time
from typing import Any, Callable, Optional, TypeVar
from collections import OrderedDict
from dataclasses import dataclass, field


T = TypeVar("T")


@dataclass
class CacheEntry:
    """Cache entry with metadata."""

    value: Any
    expires_at: float
    hits: int = 0
    created_at: float = field(default_factory=time.time)


class LRUCache:
    """Thread-safe LRU cache with TTL support."""

    def __init__(self, maxsize: int = 128, ttl: Optional[float] = None):
        """Initialize LRU cache.

        Args:
            maxsize: Maximum number of items to store
            ttl: Time-to-live in seconds (None for no expiration)
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Any:
        """Get item from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        entry = self._cache.get(key)

        if entry is None:
            self._misses += 1
            return None

        # Check expiration
        if self.ttl and time.time() > entry.expires_at:
            del self._cache[key]
            self._misses += 1
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)
        entry.hits += 1
        self._hits += 1

        return entry.value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set item in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional override for TTL
        """
        # Remove oldest if at capacity
        if len(self._cache) >= self.maxsize and key not in self._cache:
            self._cache.popitem(last=False)

        # Calculate expiration
        effective_ttl = ttl if ttl is not None else self.ttl
        expires_at = time.time() + effective_ttl if effective_ttl else float("inf")

        self._cache[key] = CacheEntry(
            value=value,
            expires_at=expires_at,
        )
        self._cache.move_to_end(key)

    def delete(self, key: str) -> bool:
        """Delete item from cache.

        Args:
            key: Cache key

        Returns:
            True if item was deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def keys(self) -> list[str]:
        """Get all cache keys."""
        return list(self._cache.keys())

    def info(self) -> dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0

        return {
            "size": len(self._cache),
            "maxsize": self.maxsize,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
            "ttl": self.ttl,
        }

    def cleanup_expired(self) -> int:
        """Remove expired entries.

        Returns:
            Number of entries removed
        """
        if not self.ttl:
            return 0

        now = time.time()
        expired = [
            key for key, entry in self._cache.items()
            if now > entry.expires_at
        ]

        for key in expired:
            del self._cache[key]

        return len(expired)


def cached(
    cache: Optional[LRUCache] = None,
    key_func: Optional[Callable] = None,
    ttl: Optional[float] = None,
):
    """Decorator for caching function results.

    Args:
        cache: LRUCache instance (creates new if None)
        key_func: Function to generate cache key from arguments
        ttl: Time-to-live in seconds

    Example:
        @cached(cache=LRUCache(maxsize=100), ttl=300)
        def get_model_summary(rid: str) -> dict:
            return fetch_from_api(rid)
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        nonlocal cache
        if cache is None:
            cache = LRUCache(maxsize=128, ttl=ttl)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key from function name and arguments
                key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
                cache_key = f"{func.__name__}:{hashlib.md5(key_data.encode()).hexdigest()}"

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result)

            return result

        # Attach cache to function for external access
        wrapper.cache = cache

        return wrapper
    return decorator


# Global caches for common use cases
_model_cache = LRUCache(maxsize=64, ttl=600)  # 10 minutes TTL
_case_cache = LRUCache(maxsize=128, ttl=300)  # 5 minutes TTL
_summary_cache = LRUCache(maxsize=256, ttl=60)  # 1 minute TTL


def get_model_cache() -> LRUCache:
    """Get global model cache."""
    return _model_cache


def get_case_cache() -> LRUCache:
    """Get global case cache."""
    return _case_cache


def get_summary_cache() -> LRUCache:
    """Get global summary cache."""
    return _summary_cache


def clear_all_caches() -> None:
    """Clear all global caches."""
    _model_cache.clear()
    _case_cache.clear()
    _summary_cache.clear()


def get_cache_stats() -> dict[str, dict[str, Any]]:
    """Get statistics for all caches."""
    return {
        "model_cache": _model_cache.info(),
        "case_cache": _case_cache.info(),
        "summary_cache": _summary_cache.info(),
    }
