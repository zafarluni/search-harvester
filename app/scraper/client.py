"""
Core scraping routines: fetch HTML, extract readable text, cache results.
"""

import asyncio
import re

import httpx
from readability import Document
from bs4 import BeautifulSoup

from app.models import ArticleResult
from app.utils.cache import get_cached, set_cached
from app.utils.metrics import FETCH_TIME, CACHE_HITS, CACHE_MISSES
from app.settings import settings


# Concurrency semaphore
SEM = asyncio.BoundedSemaphore(settings.concurrency_limit)


async def fetch_html(url: str, client: httpx.AsyncClient) -> str:
    """Fetch raw HTML with concurrency limit and timing."""
    async with SEM:
        with FETCH_TIME.time():
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text


async def extract_readable_text(
    url: str,
    client: httpx.AsyncClient,
) -> ArticleResult:
    """Return a cleaned, readable excerpt or empty placeholder."""
    # Check cache first
    cached = get_cached(url)
    if cached:
        CACHE_HITS.inc()
        return ArticleResult.model_validate(cached)
    else:
        CACHE_MISSES.inc()

    try:
        html = await fetch_html(url, client)
        doc = Document(html)
        summary_html = doc.summary()

        # Parse and strip non-content
        soup = BeautifulSoup(summary_html, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "form", "aside"]):
            tag.decompose()

        # Extract & filter paragraphs
        paragraphs: list[str] = []
        total_words = 0
        for p in soup.find_all("p"):
            text = re.sub(r"\s+", " ", p.get_text(separator=" ", strip=True)).strip()
            # Remove bracketed citations [1], etc.
            text = re.sub(r"\[.*?\]", "", text).strip()
            word_count = len(text.split())
            if word_count < settings.min_paragraph_words:
                continue
            if total_words + word_count > settings.max_total_words:
                break
            paragraphs.append(text)
            total_words += word_count

        content = "\n\n".join(paragraphs)
        result = ArticleResult(
            source=url,
            title=doc.short_title() or "",
            content=content,
            word_count=total_words,
        )

    except httpx.HTTPError:
        result = ArticleResult(source=url, title="", content="", word_count=0)
    except Exception:
        result = ArticleResult(source=url, title="", content="", word_count=0)

    # Cache for next time
    set_cached(url, result.model_dump())
    return result
