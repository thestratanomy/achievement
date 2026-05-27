from dataclasses import dataclass
from duckduckgo_search import DDGS


@dataclass
class SearchResult:
    title: str
    snippet: str
    url: str


def search_web(query: str, max_results: int = 3) -> list[SearchResult]:
    """Search DuckDuckGo and return up to max_results results."""
    full_query = f"Yogi Adityanath UP {query} 2016 2026"
    try:
        with DDGS() as ddgs:
            raw = ddgs.text(full_query, max_results=max_results + 1)
        return [
            SearchResult(title=r["title"], snippet=r["body"], url=r["href"])
            for r in (raw or [])
        ][:max_results]
    except Exception:
        return []
