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
        st.error("API key not configured. Contact the site admin.")
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
