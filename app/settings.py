"""
Define application settings via Pydantic BaseSettings.
Reads from environment for production override and validation.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Search engine selection
    search_engine: str = "duckduckgo"
    # Extra query params for DuckDuckGo (e.g. safesearch, region)
    ddg_params: str = ""

    # Concurrency and HTTP client
    concurrency_limit: int = 10
    max_connections: int = 100
    max_keepalive_connections: int = 20
    http_timeout: float = 10.0

    # Caching
    cache_maxsize: int = 10_000
    cache_ttl_seconds: int = 3_600

    # HTTP headers
    user_agent: str = "Mozilla/5.0"

    # Scraper defaults
    min_paragraph_words: int = 20
    max_total_words: int = 500

    # Logging & metrics
    log_level: str = "INFO"

    # Server defaults
    listen_host: str = "0.0.0.0"
    listen_port: int = 8000


settings = Settings()
