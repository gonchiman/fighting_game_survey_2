from fighting_game_analysis.config.urls import STEAM_REVIEWS_BASE_URL
from fighting_game_analysis.data import steam_review_fetcher


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload
        self.raise_for_status_called = False

    def raise_for_status(self):
        self.raise_for_status_called = True

    def json(self):
        return self.payload


def test_fetch_review_summary_requests_expected_endpoint(monkeypatch):
    response = FakeResponse({"query_summary": {"total_reviews": 1234}})
    captured = {}

    def fake_get(url, params, timeout):
        captured["url"] = url
        captured["params"] = params
        captured["timeout"] = timeout
        return response

    monkeypatch.setattr(steam_review_fetcher.requests, "get", fake_get)

    result = steam_review_fetcher.fetch_review_summary(1364780)

    assert result == {"total_reviews": 1234}
    assert captured["url"] == f"{STEAM_REVIEWS_BASE_URL}1364780"
    assert captured["params"] == {
        "json": 1,
        "language": "all",
        "purchase_type": "all",
        "num_per_page": 0,
    }
    assert captured["timeout"] == 10
    assert response.raise_for_status_called is True
