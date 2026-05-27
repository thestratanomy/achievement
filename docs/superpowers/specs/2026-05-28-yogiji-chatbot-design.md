# Yogiji UP Achievements Chatbot — Design Spec

**Date**: 2026-05-28
**Target build time**: 2 hours
**Stack**: Streamlit + Gemini (free tier) + DuckDuckGo search
**Hosting**: Streamlit Community Cloud (app) + GitHub Pages (landing page)

---

## 1. Architecture

```
yogiji/
├── app.py                    # Streamlit entry point
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Saffron theme
├── src/
│   ├── gemini_client.py      # Gemini API wrapper + system prompt
│   ├── web_search.py         # DuckDuckGo live search (duckduckgo-search lib)
│   └── achievements_data.py  # Curated static UP/Yogi facts (fallback/seed)
└── docs/                     # GitHub Pages (enable in repo Settings → Pages → /docs)
    ├── index.html
    └── style.css
```

## 2. Data Flow

1. User submits a question in the chat UI.
2. `web_search.py` runs a DuckDuckGo text search: `"Yogi Adityanath UP {query} 2016-2026"`, returns top 3 snippets + URLs.
3. Snippets + matching curated facts from `achievements_data.py` are injected into the Gemini system prompt as context.
4. Gemini streams a reply; language auto-matches the user's message (Hindi or English).
5. Reply renders in `st.chat_message`; a collapsible "Sources" expander shows the live URLs used.

## 3. UI — Streamlit App

- **Theme**: saffron (`primaryColor = "#FF6B00"`) via `.streamlit/config.toml`
- **Header**: "योगी सरकार की उपलब्धियां | UP Achievements — Last 10 Years"
- **Sidebar**: category filter (multiselect chips) — filters which curated facts are included in the prompt context
- **Chat area**: `st.chat_message` bubbles (user right, AI left), streaming output
- **Sources expander**: collapsible, shown below each AI reply
- **Footer**: "Live data from the web · Powered by Google Gemini"

### Sidebar Categories

| Category | Seeds in achievements_data.py |
|---|---|
| Infrastructure | Purvanchal/Bundelkhand expressways, Jewar airport, metro cities |
| Economy | ODOP scheme, Global Investors Summit, UP GDP rank improvement |
| Industries | Defence corridor (Lucknow–Agra), data centres, semiconductor MoUs |
| Law & Order | Crime rate reduction stats, anti-mafia/anti-encroachment ops |
| Health | Ayushman Bharat UP coverage, COVID management, new medical colleges |
| Education | Operation Kayakalp, school renovations, mid-day meal improvements |
| Agriculture | MSP procurement records, PM-KISAN beneficiaries, irrigation coverage |

## 4. UI — GitHub Pages Landing Page

- **File**: `docs/index.html` + `docs/style.css`
- **Hero**: full-width saffron gradient, bold Hindi + English headline, brief 3-line description
- **Iframe**: embeds the Streamlit Community Cloud URL at full height, responsive
- **Edit guide**: comment block at top of `index.html` labelling every editable section; CSS variables at top of `style.css` for colour/font changes
- **No build step** — plain HTML/CSS, editable in any text editor

## 5. Gemini System Prompt

```
You are an expert on Uttar Pradesh governance under Chief Minister Yogi Adityanath (2017–2026).
Answer questions using ONLY the provided context (web search results + curated facts).
Be factual, cite figures where available. If context is insufficient, say so.
Reply in the same language the user used (Hindi or English).
```

## 6. Hosting Setup (post-build steps)

| Step | Action |
|---|---|
| 1 | Push repo to GitHub (public) |
| 2 | Go to share.streamlit.io → New app → pick repo + `app.py` |
| 3 | Add `GEMINI_API_KEY` in Streamlit secrets |
| 4 | Copy the `.streamlit.app` URL into `docs/index.html` iframe src |
| 5 | GitHub repo Settings → Pages → Source: `/docs` folder |
| 6 | Site live at `https://<username>.github.io/yogiji` |

## 7. Dependencies

```
streamlit
google-generativeai
duckduckgo-search
```

## 8. Acceptance Criteria

- [ ] Chat answers questions about UP/Yogi achievements with live web context
- [ ] Sidebar category filter narrows the curated fact context
- [ ] Sources expander shows URLs for each reply
- [ ] GitHub Pages landing page loads and iframe shows the Streamlit app
- [ ] `GEMINI_API_KEY` is never committed — stored only in Streamlit secrets
- [ ] All editable sections in `index.html` and `style.css` are clearly commented
