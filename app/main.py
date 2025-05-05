"""
FastAPI application entrypoint for SearchHarvester.
Includes structured logging, metrics endpoint, and JSON/Markdown output.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import httpx
from fastapi import FastAPI, Query, Depends, HTTPException, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.dependencies import get_http_client, get_search_engine
from app.utils.logging_config import configure_logging
from app.utils.metrics import SEARCH_COUNT
from app.models import ArticleResult
from app.scraper.client import extract_readable_text

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Handle app startup and shutdown lifecycle."""
    yield
    client = await get_http_client()
    await client.aclose()


app = FastAPI(
    title="SearchHarvester API",
    description="SearchHarvester: Asynchronous, pluggable web content harvester.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get(
    "/search",
    response_model=list[ArticleResult],
    responses={200: {"content": {"text/markdown": {}}}},
)
async def search_content(
    query: str = Query(..., min_length=1),
    sources: int = Query(1, ge=1, le=10),
    format: str = Query("markdown", pattern="^(json|markdown)$"),
    client: httpx.AsyncClient = Depends(get_http_client),
    engine=Depends(get_search_engine),
):
    """
    Search for pages and extract readable excerpts until `sources` working results are found.

    - **query**: search query
    - **sources**: number of successful articles to retrieve (1–10)
    - **format**: `json` or `markdown`
    """
    SEARCH_COUNT.inc()

    # 1) Perform search
    try:
        urls = await engine.search(query, sources * 2, client)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    if not urls:
        raise HTTPException(status_code=404, detail="No results found.")

    # 2) Extract & filter content
    articles: list[ArticleResult] = []
    for url in urls:
        art = await extract_readable_text(url, client)
        if art.word_count == 0 or not art.content.strip():
            continue
        articles.append(art)
        if len(articles) >= sources:
            break

    if not articles:
        raise HTTPException(status_code=404, detail="No readable content found.")

    # 3) Return in requested format
    if format == "markdown":
        md_parts = []
        for art in articles:
            if art.title:
                md_parts.append(f"## {art.title}")
            md_parts.append(f"_Source: <{art.source}>_")
            md_parts.append(art.content)
        md = "\n\n".join(md_parts)
        return Response(content=md, media_type="text/markdown")

    return articles


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    data = generate_latest()
    return Response(data, media_type=CONTENT_TYPE_LATEST)
