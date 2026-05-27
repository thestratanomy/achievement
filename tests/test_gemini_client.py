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
