from fighting_game_analysis.config.urls import STEAM_REVIEWS_BASE_URL
from fighting_game_analysis.data import steam_review_fetcher


class FakeResponse:
    def __init__(self, payload):
        """フェイクレスポンスの内容と呼び出し状態を保持します。

        Args:
            payload: `json()` で返すデータ。
        """
        self.payload = payload
        self.raise_for_status_called = False

    def raise_for_status(self):
        """ステータス検証が呼ばれたことを記録します。"""
        self.raise_for_status_called = True

    def json(self):
        """フェイクの JSON レスポンスを返します。

        Returns:
            初期化時に渡されたデータ。
        """
        return self.payload


def test_fetch_review_summary_requests_expected_endpoint(monkeypatch):
    """レビュー概要が期待した URL とパラメータで取得されることを確認します。"""
    response = FakeResponse({"query_summary": {"total_reviews": 1234}})
    captured = {}

    def fake_get(url, params, timeout):
        """リクエスト引数を記録してフェイクレスポンスを返します。

        Args:
            url: リクエスト URL。
            params: クエリパラメータ。
            timeout: タイムアウト秒数。

        Returns:
            フェイクレスポンス。
        """
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
