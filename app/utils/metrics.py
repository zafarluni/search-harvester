"""
Prometheus metrics instrumentation.
"""

from prometheus_client import Counter, Histogram

SEARCH_COUNT = Counter(
    "searchharvester_search_requests_total",
    "Total SearchHarvester search requests",
)

CACHE_HITS = Counter(
    "searchharvester_cache_hits_total",
    "SearchHarvester cache hits for article extraction",
)

CACHE_MISSES = Counter(
    "searchharvester_cache_misses_total",
    "SearchHarvester cache misses for article extraction",
)

FETCH_TIME = Histogram(
    "searchharvester_fetch_html_seconds",
    "Time spent fetching HTML pages",
    buckets=(0.1, 0.5, 1, 2, 5, 10, 30),
)
