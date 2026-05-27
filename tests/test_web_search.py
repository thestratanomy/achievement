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
