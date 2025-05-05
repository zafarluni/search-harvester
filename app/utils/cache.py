"""
In-memory TTL cache wrapper for URL results.
"""

from cachetools import TTLCache
from app.settings import settings
from typing import Optional

# module-level cache, initialized using settings
URL_CACHE: TTLCache[str, dict] = TTLCache(
    maxsize=settings.cache_maxsize,
    ttl=settings.cache_ttl_seconds,
)


def get_cached(url: str) -> Optional[dict]:
    """Return cached data or None."""
    return URL_CACHE.get(url)


def set_cached(url: str, value: dict) -> None:
    """Cache data for given URL."""
    URL_CACHE[url] = value
