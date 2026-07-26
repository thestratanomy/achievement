from src.web_search import search_web, SearchResult


def _mock_response(mocker, organic):
    resp = mocker.MagicMock()
    resp.raise_for_status.return_value = None
    resp.json.return_value = {"organic": organic}
    return resp


def _mock_organic():
    return [
        {"title": "UP GDP Growth", "snippet": "UP economy grew 8%", "link": "https://example.com/1"},
        {"title": "Yogi Infrastructure", "snippet": "Expressway inaugurated", "link": "https://example.com/2"},
        {"title": "UP Industries", "snippet": "Defence corridor progress", "link": "https://example.com/3"},
        {"title": "Extra result", "snippet": "More info", "link": "https://example.com/4"},
    ]


def test_search_web_returns_three_results(mocker):
    mocker.patch("src.web_search.requests.post", return_value=_mock_response(mocker, _mock_organic()))
    results = search_web("UP economy", api_key="fake-key")
    assert len(results) == 3


def test_search_web_result_structure(mocker):
    mocker.patch("src.web_search.requests.post", return_value=_mock_response(mocker, _mock_organic()))
    results = search_web("UP economy", api_key="fake-key")
    assert isinstance(results[0], SearchResult)
    assert results[0].title == "UP GDP Growth"
    assert results[0].snippet == "UP economy grew 8%"
    assert results[0].url == "https://example.com/1"


def test_search_web_handles_empty_results(mocker):
    mocker.patch("src.web_search.requests.post", return_value=_mock_response(mocker, []))
    results = search_web("nonexistent query", api_key="fake-key")
    assert results == []


def test_search_web_no_api_key_returns_empty():
    assert search_web("UP economy", api_key="") == []


def test_search_web_handles_request_exception(mocker):
    import requests

    mocker.patch("src.web_search.requests.post", side_effect=requests.RequestException("boom"))
    results = search_web("UP economy", api_key="fake-key")
    assert results == []
