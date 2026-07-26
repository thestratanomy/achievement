from dataclasses import dataclass

import requests

_SERPER_URL = "https://google.serper.dev/search"


@dataclass
class SearchResult:
    title: str
    snippet: str
    url: str


def search_web(query: str, api_key: str, max_results: int = 3) -> list[SearchResult]:
    """Search via Serper.dev (Google results) and return up to max_results results."""
    if not api_key:
        return []
    full_query = f"Yogi Adityanath UP {query} 2016 2026"
    try:
        resp = requests.post(
            _SERPER_URL,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": full_query, "num": max_results},
            timeout=10,
        )
        resp.raise_for_status()
        organic = resp.json().get("organic", [])
        return [
            SearchResult(title=r["title"], snippet=r.get("snippet", ""), url=r["link"])
            for r in organic
        ][:max_results]
    except requests.RequestException:
        return []
