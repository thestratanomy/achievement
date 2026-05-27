# Yogiji UP Achievements Chatbot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Streamlit chatbot that answers questions about UP/Yogi achievements using live DuckDuckGo search + Gemini, hosted free on Streamlit Community Cloud, with a GitHub Pages landing page.

**Architecture:** Streamlit app (`app.py`) calls `web_search.py` for live context, injects results into `gemini_client.py`, and streams replies. `achievements_data.py` provides curated fallback facts filtered by sidebar category. A static `docs/` folder serves as the GitHub Pages landing page with an iframe embed.

**Tech Stack:** Python 3.11+, Streamlit, google-generativeai, duckduckgo-search, pytest

---

## File Map

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI — sidebar, chat loop, sources expander |
| `requirements.txt` | Pinned dependencies |
| `.streamlit/config.toml` | Saffron theme |
| `.gitignore` | Exclude secrets / venv |
| `src/__init__.py` | Package marker |
| `src/achievements_data.py` | Curated facts dict keyed by category |
| `src/web_search.py` | DuckDuckGo search → list of `{title, snippet, url}` |
| `src/gemini_client.py` | Gemini streaming wrapper + system prompt builder |
| `tests/__init__.py` | Package marker |
| `tests/test_achievements_data.py` | Unit tests for fact filtering |
| `tests/test_web_search.py` | Unit tests with mocked DDGS |
| `tests/test_gemini_client.py` | Unit tests with mocked Gemini |
| `docs/index.html` | GitHub Pages landing page |
| `docs/style.css` | CSS with variables for easy editing |

---

## Task 1: Scaffold — dependencies, theme, gitignore

**Files:**
- Create: `requirements.txt`
- Create: `.streamlit/config.toml`
- Create: `.gitignore`
- Create: `src/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```
streamlit==1.35.0
google-generativeai==0.7.2
duckduckgo-search==6.2.1
pytest==8.2.2
pytest-mock==3.14.0
```

- [ ] **Step 2: Create .streamlit/config.toml**

```toml
[theme]
primaryColor = "#FF6B00"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#FFF3E8"
textColor = "#1A1A1A"
font = "sans serif"
```

- [ ] **Step 3: Create .gitignore**

```
.env
__pycache__/
*.pyc
.venv/
*.egg-info/
.streamlit/secrets.toml
```

- [ ] **Step 4: Create empty package markers**

```bash
touch src/__init__.py tests/__init__.py
```

- [ ] **Step 5: Install dependencies**

```bash
pip install -r requirements.txt
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt .streamlit/config.toml .gitignore src/__init__.py tests/__init__.py
git commit -m "chore: scaffold project dependencies and theme"
```

---

## Task 2: achievements_data.py — curated facts

**Files:**
- Create: `src/achievements_data.py`
- Create: `tests/test_achievements_data.py`

- [ ] **Step 1: Write failing tests**

`tests/test_achievements_data.py`:
```python
from src.achievements_data import get_facts, CATEGORIES

def test_categories_contains_all_required():
    required = {"Infrastructure", "Economy", "Industries", "Law & Order", "Health", "Education", "Agriculture"}
    assert required.issubset(set(CATEGORIES))

def test_get_facts_single_category():
    facts = get_facts(["Infrastructure"])
    assert len(facts) > 0
    assert all(isinstance(f, str) for f in facts)

def test_get_facts_multiple_categories():
    facts = get_facts(["Economy", "Industries"])
    assert len(facts) >= 2

def test_get_facts_empty_returns_all():
    all_facts = get_facts([])
    assert len(all_facts) > 10
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_achievements_data.py -v
```
Expected: `ImportError` — module not found.

- [ ] **Step 3: Create src/achievements_data.py**

```python
CATEGORIES = [
    "Infrastructure", "Economy", "Industries",
    "Law & Order", "Health", "Education", "Agriculture",
]

_FACTS: dict[str, list[str]] = {
    "Infrastructure": [
        "Purvanchal Expressway (340 km) inaugurated 2021, connecting eastern UP to Lucknow.",
        "Bundelkhand Expressway (296 km) inaugurated 2022, boosting backward region connectivity.",
        "Jewar International Airport (Noida) — Asia's largest greenfield airport under construction.",
        "Metro rail extended in Lucknow, Kanpur, Agra, and Meerut under Yogi government.",
        "Ganga Expressway (594 km) — longest expressway in UP, under construction.",
    ],
    "Economy": [
        "UP GDP grew from ₹12.9 lakh crore (2017) to over ₹24 lakh crore (2024).",
        "Global Investors Summit 2023 attracted ₹33.5 lakh crore in investment proposals.",
        "One District One Product (ODOP) scheme promoted 75 unique local products globally.",
        "UP became India's 2nd largest economy by GSDP, overtaking several larger states.",
        "Ease of Doing Business rank improved from 14th (2017) to 2nd (2022) nationally.",
    ],
    "Industries": [
        "UP Defence Industrial Corridor spans Lucknow-Agra-Aligarh-Kanpur-Jhansi-Chitrakoot.",
        "Defence corridor attracted ₹50,000+ crore in investments and 200+ defence companies.",
        "Data centre capacity expanded: UP became a leading data centre hub in North India.",
        "Semiconductor and electronics manufacturing MoUs signed at GIS 2023.",
        "Gorakhpur AIIMS and fertiliser plant revived after decades, creating local employment.",
    ],
    "Law & Order": [
        "Crime rate dropped significantly: murder cases down 24%, robbery down 65% (2017-2022).",
        "Anti-mafia operations: 100+ criminal syndicates dismantled, assets worth ₹3,000+ crore seized.",
        "Anti-encroachment drive recovered thousands of acres of government land.",
        "UP became one of the safest states for women: Dial 1090 and Mission Shakti expanded.",
    ],
    "Health": [
        "Ayushman Bharat UP: 5.5 crore+ beneficiary cards issued, largest state coverage.",
        "COVID-19 management: UP's tracing, testing, treating model praised nationally.",
        "9 new medical colleges operationalised (2017-2024), adding 1,350+ MBBS seats.",
        "UP eliminated Japanese Encephalitis deaths in Gorakhpur, a decades-long problem.",
    ],
    "Education": [
        "Operation Kayakalp renovated 1.5 lakh+ government school buildings.",
        "UP Board results improved year-on-year; mass cheating completely eliminated.",
        "Atal Residential Schools provide free residential education to orphans and labourers' children.",
        "Digital classrooms and smart boards installed in thousands of government schools.",
    ],
    "Agriculture": [
        "UP became India's largest sugarcane producer; sugar mills cleared dues promptly.",
        "PM-KISAN: 2.7 crore+ farmers in UP received direct benefit transfers.",
        "Irrigation coverage expanded: Saryu Canal project completed benefiting 14 lakh hectares.",
        "MSP procurement of wheat and paddy reached record highs under Yogi government.",
    ],
}


def get_facts(categories: list[str]) -> list[str]:
    """Return curated facts for the given categories. Empty list returns all facts."""
    if not categories:
        return [fact for facts in _FACTS.values() for fact in facts]
    result = []
    for cat in categories:
        result.extend(_FACTS.get(cat, []))
    return result
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
pytest tests/test_achievements_data.py -v
```
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/achievements_data.py tests/test_achievements_data.py
git commit -m "feat: add curated UP achievements data with category filtering"
```

---

## Task 3: web_search.py — live DuckDuckGo search

**Files:**
- Create: `src/web_search.py`
- Create: `tests/test_web_search.py`

- [ ] **Step 1: Write failing tests**

`tests/test_web_search.py`:
```python
from src.web_search import search_web, SearchResult

def _mock_results():
    return [
        {"title": "UP GDP Growth", "body": "UP economy grew 8%", "href": "https://example.com/1"},
        {"title": "Yogi Infrastructure", "body": "Expressway inaugurated", "href": "https://example.com/2"},
        {"title": "UP Industries", "body": "Defence corridor progress", "href": "https://example.com/3"},
        {"title": "Extra result", "body": "More info", "href": "https://example.com/4"},
    ]

def test_search_web_returns_three_results(mocker):
    mocker.patch("src.web_search.DDGS").return_value.__enter__.return_value.text.return_value = _mock_results()
    results = search_web("UP economy")
    assert len(results) == 3

def test_search_web_result_structure(mocker):
    mocker.patch("src.web_search.DDGS").return_value.__enter__.return_value.text.return_value = _mock_results()
    results = search_web("UP economy")
    assert isinstance(results[0], SearchResult)
    assert results[0].title == "UP GDP Growth"
    assert results[0].snippet == "UP economy grew 8%"
    assert results[0].url == "https://example.com/1"

def test_search_web_handles_empty_results(mocker):
    mocker.patch("src.web_search.DDGS").return_value.__enter__.return_value.text.return_value = []
    results = search_web("nonexistent query")
    assert results == []
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_web_search.py -v
```
Expected: `ImportError` — module not found.

- [ ] **Step 3: Create src/web_search.py**

```python
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
```

- [ ] **Step 4: Run tests to confirm pass**

```bash
pytest tests/test_web_search.py -v
```
Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add src/web_search.py tests/test_web_search.py
git commit -m "feat: add DuckDuckGo web search module"
```

---

## Task 4: gemini_client.py — Gemini streaming wrapper

**Files:**
- Create: `src/gemini_client.py`
- Create: `tests/test_gemini_client.py`

- [ ] **Step 1: Write failing tests**

`tests/test_gemini_client.py`:
```python
from src.web_search import SearchResult
from src.gemini_client import build_prompt, stream_answer

def test_build_prompt_contains_query():
    prompt = build_prompt("What expressways were built?", [], [])
    assert "expressways" in prompt.lower()

def test_build_prompt_includes_web_snippets():
    results = [SearchResult("Title", "Purvanchal Expressway opened", "https://x.com")]
    prompt = build_prompt("expressways", results, [])
    assert "Purvanchal Expressway opened" in prompt

def test_build_prompt_includes_curated_facts():
    prompt = build_prompt("economy", [], ["UP GDP doubled since 2017"])
    assert "UP GDP doubled since 2017" in prompt

def test_stream_answer_yields_chunks(mocker):
    mock_chunk = mocker.MagicMock()
    mock_chunk.text = "Great progress"
    mock_model = mocker.MagicMock()
    mock_model.generate_content.return_value = [mock_chunk]
    mocker.patch("src.gemini_client.genai.GenerativeModel", return_value=mock_model)
    mocker.patch("src.gemini_client.genai.configure")
    chunks = list(stream_answer("test prompt", api_key="fake-key"))
    assert chunks == ["Great progress"]
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_gemini_client.py -v
```
Expected: `ImportError` — module not found.

- [ ] **Step 3: Create src/gemini_client.py**

```python
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
```

- [ ] **Step 4: Run all tests**

```bash
pytest -v
```
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add src/gemini_client.py tests/test_gemini_client.py
git commit -m "feat: add Gemini streaming client with prompt builder"
```

---

## Task 5: app.py — Streamlit UI

**Files:**
- Create: `app.py`

- [ ] **Step 1: Create app.py**

```python
import streamlit as st
from src.achievements_data import get_facts, CATEGORIES
from src.web_search import search_web
from src.gemini_client import build_prompt, stream_answer

st.set_page_config(
    page_title="यूपी की उपलब्धियां | UP Achievements",
    page_icon="🏛️",
    layout="wide",
)

with st.sidebar:
    st.title("फ़िल्टर | Filter")
    selected = st.multiselect(
        "Category",
        options=CATEGORIES,
        default=CATEGORIES,
        help="Select categories to include in AI context",
    )
    st.markdown("---")
    st.caption("Live data from the web · Powered by Google Gemini")

st.markdown(
    "<h1 style='text-align:center;color:#FF6B00;'>🏛️ योगी सरकार की उपलब्धियां</h1>"
    "<h3 style='text-align:center;color:#555;'>UP Achievements — Last 10 Years (2016–2026)</h3>",
    unsafe_allow_html=True,
)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- [{s['title']}]({s['url']})")

if prompt := st.chat_input("Ask about UP achievements… / यूपी की उपलब्धियां पूछें…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.error("GEMINI_API_KEY not set in Streamlit secrets.")
        st.stop()

    with st.spinner("Searching the web…"):
        web_results = search_web(prompt)
        curated = get_facts(selected)

    full_prompt = build_prompt(prompt, web_results, curated)

    with st.chat_message("assistant"):
        response_text = st.write_stream(stream_answer(full_prompt, api_key))

    sources = [{"title": r.title, "url": r.url} for r in web_results]
    if sources:
        with st.expander("Sources"):
            for s in sources:
                st.markdown(f"- [{s['title']}]({s['url']})")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "sources": sources,
    })
```

- [ ] **Step 2: Run locally to verify UI**

```bash
GEMINI_API_KEY=your_real_key streamlit run app.py
```
Expected: browser opens at `http://localhost:8501`, saffron header visible, sidebar category filter, chat input at bottom.

- [ ] **Step 3: Commit**

```bash
git add app.py
git commit -m "feat: add Streamlit chat UI with sidebar and sources expander"
```

---

## Task 6: GitHub Pages landing page

**Files:**
- Create: `docs/style.css`
- Modify: `docs/index.html` (already exists as placeholder from spec — replace fully)

- [ ] **Step 1: Create docs/style.css**

```css
/* ═══════════════════════════════════════
   EDIT HERE — change colours & fonts
   ═══════════════════════════════════════ */
:root {
  --primary:  #FF6B00;
  --dark:     #1A1A1A;
  --light-bg: #FFF8F2;
  --font:     'Segoe UI', sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font); color: var(--dark); background: var(--light-bg); }

.hero {
  background: linear-gradient(135deg, var(--primary) 0%, #FF9A3C 100%);
  color: #fff;
  text-align: center;
  padding: 60px 20px 40px;
}
.hero h1 { font-size: clamp(1.8rem, 5vw, 3rem); margin-bottom: 10px; }
.hero p  { font-size: 1.1rem; opacity: 0.9; max-width: 600px; margin: 0 auto 20px; }

.embed-wrap { width: 100%; height: 85vh; min-height: 600px; border: none; }

footer { text-align: center; padding: 16px; font-size: 0.85rem; color: #888; background: #fff; }
```

- [ ] **Step 2: Create docs/index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- EDIT: page title -->
  <title>योगी सरकार की उपलब्धियां | UP Achievements</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>

  <!-- EDIT: hero headline and description -->
  <div class="hero">
    <h1>🏛️ योगी सरकार की उपलब्धियां</h1>
    <p>
      Explore 10 years of Uttar Pradesh's transformation under CM Yogi Adityanath.
      Ask anything — powered by live web search and Google Gemini AI.
    </p>
  </div>

  <!-- EDIT: replace src with your Streamlit Community Cloud URL -->
  <iframe
    class="embed-wrap"
    src="https://YOUR-APP-NAME.streamlit.app/?embed=true"
    allow="clipboard-write"
    loading="lazy"
  ></iframe>

  <!-- EDIT: footer text -->
  <footer>Built with Streamlit · Hosted free on GitHub Pages &amp; Streamlit Community Cloud</footer>

</body>
</html>
```

- [ ] **Step 3: Commit**

```bash
git add docs/style.css docs/index.html
git commit -m "feat: add GitHub Pages landing page with iframe embed"
```

---

## Task 7: Deploy

- [ ] **Step 1: Push to GitHub**

```bash
git remote add origin https://github.com/YOUR_USERNAME/yogiji.git
git push -u origin master
```

- [ ] **Step 2: Deploy on Streamlit Community Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Select repo `yogiji`, branch `master`, main file `app.py`
3. **Advanced settings → Secrets** — paste:
   ```toml
   GEMINI_API_KEY = "paste-your-key-here"
   ```
4. Click **Deploy**. Copy the resulting `.streamlit.app` URL.

- [ ] **Step 3: Paste Streamlit URL into docs/index.html**

Open `docs/index.html`, replace `https://YOUR-APP-NAME.streamlit.app/?embed=true` with your real URL.

- [ ] **Step 4: Enable GitHub Pages**

GitHub repo → **Settings → Pages → Source**: branch `master`, folder `/docs` → Save.
Site goes live at `https://YOUR_USERNAME.github.io/yogiji`.

- [ ] **Step 5: Final push**

```bash
git add docs/index.html
git commit -m "chore: set live Streamlit URL in landing page"
git push origin master
```

- [ ] **Step 6: Verify acceptance criteria**

- [ ] Chat answers UP/Yogi questions with live web context
- [ ] Sidebar category filter works
- [ ] Sources expander shows URLs per reply
- [ ] GitHub Pages site loads with iframe embed
- [ ] `GEMINI_API_KEY` absent from all committed files

---

> **Get a free Gemini API key:** [aistudio.google.com](https://aistudio.google.com) → Sign in → Get API key
