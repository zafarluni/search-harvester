# SearchHarvester API

SearchHarvester is an asynchronous, pluggable web content harvester built with FastAPI. It searches web pages, extracts readable text snippets, and serves them via a JSON or Markdown API.

## Features

- Plugin-based Search Engines: Easily swap or extend search backends (e.g., DuckDuckGo, Google, custom).
- Asynchronous & Concurrent: Uses httpx.AsyncClient and asyncio to fetch multiple pages in parallel.
- Configurable: All settings are centralized in settings.py and overrideable via environment variables.
- Caching: In-memory TTL cache for scraped pages to reduce duplicate requests.
- Metrics & Monitoring: Prometheus metrics endpoint for tracking requests, cache hits, and latencies.
- Structured Logging: JSON-formatted logs with timestamps, configurable log level, and request IDs.

## Directory Structure

.
├── models.py
├── dependencies.py
├── main.py
├── settings.py
├── search_engines
│   ├── base.py
│   └── duckduckgo.py
├── utils
│   ├── cache.py
│   ├── metrics.py
│   └── logging_config.py
└── scraper
    └── client.py

## Quick Start

1. Clone the Repo

   git clone https://github.com/your-org/searchharvester.git
   cd searchharvester

2. Set Up Your Environment

You can use either uv (recommended) or traditional venv + pip.

Option A: Using uv (Recommended)

1. Install uv:

   curl -Ls https://astral.sh/uv/install.sh | sh

2. Create virtual env & install deps:

   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt

Option B: Using Built-in Tools

   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Configure Environment Variables

Create a .env file in the project root:

   SEARCH_ENGINE=duckduckgo
   CONCURRENCY_LIMIT=10
   CACHE_MAXSIZE=10000
   CACHE_TTL_SECONDS=3600
   HTTP_TIMEOUT=10.0
   USER_AGENT="Mozilla/5.0"
   LOG_LEVEL=INFO

4. Run the Server

   uvicorn main:app --host 0.0.0.0 --port 8000

## API Reference

GET /search

- query (string, required): Search term (min length 1)
- sources (int, default 1): Number of articles to return (1–10)
- format (string, default markdown): json or markdown

Responses:
- 200 OK: Success
- 404 Not Found: No readable results
- 502 Bad Gateway: Upstream search error

GET /metrics

- Prometheus-compatible metrics endpoint.

## Configuration Options

Environment Variable     | Default       | Description
------------------------ | ------------- | ---------------------------------------------
SEARCH_ENGINE            | duckduckgo    | Which search engine to use
CONCURRENCY_LIMIT        | 10            | Max parallel fetches
CACHE_MAXSIZE            | 10000         | Max entries in in-memory cache
CACHE_TTL_SECONDS        | 3600          | Time-to-live for cache entries (seconds)
HTTP_TIMEOUT             | 10.0          | Timeout for HTTP requests (seconds)
USER_AGENT               | Mozilla/5.0   | Default User-Agent header
LOG_LEVEL                | INFO          | Logging level (DEBUG, INFO, WARN, etc.)

## Extending & Customizing

1. Add a new search engine
   - Create a class inheriting from SearchEngine in search_engines/
   - Register it in the ENGINES map
   - Set SEARCH_ENGINE to your new key

2. Swap caching backend
   - Replace utils/cache.py with a Redis or disk-backed implementation

3. Advanced Logging/Metrics
   - Modify utils/logging_config.py or utils/metrics.py to add custom processors or instruments

## Dependency Management with uv

If you're using uv, managing dependencies is simple:

   uv pip install <package-name>
   uv pip freeze > requirements.txt

Note: uv manages its own lock file internally. You can optionally generate requirements.txt for compatibility.

## License

MIT License (LICENSE)
