"""
Abstract base for search engine plugins.
"""

from abc import ABC, abstractmethod
import httpx


class SearchEngine(ABC):
    @abstractmethod
    async def search(self, query: str, num_results: int, client: httpx.AsyncClient) -> list[str]:
        """
        Return up to `num_results` result URLs for the given query.
        """
        ...
