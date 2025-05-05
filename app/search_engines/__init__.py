"""
Plugin registry for all SearchEngine implementations.
"""

from typing import Dict

from app.search_engines.base import SearchEngine
from app.search_engines.duckduckgo import DuckDuckGoEngine

ENGINES: Dict[str, SearchEngine] = {"duckduckgo": DuckDuckGoEngine()}
