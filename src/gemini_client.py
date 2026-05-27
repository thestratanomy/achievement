import google.generativeai as genai
from src.web_search import SearchResult

_SYSTEM = (
    "You are an expert on Uttar Pradesh governance under Chief Minister Yogi Adityanath (2017-2026). "
    "Answer questions using ONLY the provided context (web search results + curated facts). "
    "Be factual and cite figures where available. If context is insufficient, say so honestly. "
    "Reply in the same language the user used (Hindi or English)."
)


def build_prompt(query: str, web_results: list[SearchResult], curated_facts: list[str]) -> str:
    parts = [_SYSTEM, "", f"User question: {query}", ""]
    if web_results:
        parts.append("=== Live web context ===")
        for r in web_results:
            parts.append(f"- [{r.title}]({r.url}): {r.snippet}")
        parts.append("")
    if curated_facts:
        parts.append("=== Curated facts ===")
        for fact in curated_facts:
            parts.append(f"- {fact}")
        parts.append("")
    parts.append("Answer:")
    return "\n".join(parts)


def stream_answer(prompt: str, api_key: str):
    """Yield text chunks from Gemini (streaming)."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text
