"""
DuckDuckGo implementation of the SearchEngine interface.
"""

from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse, parse_qs, unquote
import httpx

from app.search_engines.base import SearchEngine
from app.settings import settings


class DuckDuckGoEngine(SearchEngine):
    async def search(self, query: str, num_results: int, client: httpx.AsyncClient) -> list[str]:
        # Build URL, including optional extra params
        base = "https://html.duckduckgo.com/html/"
        params = f"?q={quote_plus(query)}"
        if settings.ddg_params:
            params += f"&{settings.ddg_params}"
        resp = await client.get(base + params)
        resp.raise_for_status()

        # Parse results
        soup = BeautifulSoup(resp.text, "html.parser")
        links: list[str] = []
        for a in soup.select("a.result__a", limit=num_results * 2):
            parsed = urlparse(str(a["href"]))
            real = parse_qs(parsed.query).get("uddg", [None])[0]
            if real:
                links.append(unquote(real))
                if len(links) >= num_results:
                    break
        return links
