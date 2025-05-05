"""
Define FastAPI dependencies: settings, HTTP client, search engine factory.
"""

from fastapi import Depends, HTTPException
import httpx
from httpx import Limits

from app.search_engines.base import SearchEngine
from app.search_engines import ENGINES
from app.settings import Settings, settings

_http_client: httpx.AsyncClient | None = None


def get_settings() -> Settings:
    """Return the application settings singleton."""
    return settings


async def get_http_client(
    settings: Settings = Depends(get_settings),
) -> httpx.AsyncClient:
    """
    Return a shared AsyncClient configured from settings.
    Closes on app shutdown.
    """
    global _http_client
    if _http_client is None:
        limits = Limits(
            max_connections=settings.max_connections,
            max_keepalive_connections=settings.max_keepalive_connections,
        )
        _http_client = httpx.AsyncClient(
            headers={"User-Agent": settings.user_agent},
            timeout=settings.http_timeout,
            limits=limits,
        )
    return _http_client


async def get_search_engine(
    settings: Settings = Depends(get_settings),
) -> SearchEngine:
    """Instantiate the proper SearchEngine based on settings.search_engine."""
    engine = ENGINES.get(settings.search_engine)
    if engine is None:
        raise HTTPException(
            status_code=500,
            detail=f"Unsupported search engine: {settings.search_engine}",
        )
    return engine
