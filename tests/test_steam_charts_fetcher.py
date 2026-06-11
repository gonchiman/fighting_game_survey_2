from io import StringIO

import pandas as pd

from fighting_game_analysis.config.games import Game
from fighting_game_analysis.config.urls import STEAM_CHARTS_APP_BASE_URL
from fighting_game_analysis.data import steam_charts_fetcher


def test_fetch_monthly_stats_reads_first_table_from_steam_charts_page(monkeypatch):
    game = Game("Test Fighter", 12345)
    captured = {}
    html = """
    <html>
        <body>
            <table>
                <thead>
                    <tr><th>Month</th><th>Avg. Players</th></tr>
                </thead>
                <tbody>
                    <tr><td>January 2024</td><td>10.5</td></tr>
                </tbody>
            </table>
        </body>
    </html>
    """

    def fake_fetch_page_html(url):
        captured["url"] = url
        return html

    monkeypatch.setattr(steam_charts_fetcher, "fetch_page_html", fake_fetch_page_html)

    result = steam_charts_fetcher.fetch_monthly_stats(game)

    expected = pd.read_html(StringIO(html))[0]
    pd.testing.assert_frame_equal(result, expected)
    assert captured["url"] == f"{STEAM_CHARTS_APP_BASE_URL}12345"


def test_fetch_monthly_stats_raises_when_no_tables_found(monkeypatch):
    game = Game("Test Fighter", 12345)

    monkeypatch.setattr(
        steam_charts_fetcher,
        "fetch_page_html",
        lambda url: "<html><body>No stats here</body></html>",
    )

    try:
        steam_charts_fetcher.fetch_monthly_stats(game)
    except ValueError as exc:
        assert str(exc) == "No tables found for Test Fighter"
    else:
        raise AssertionError("Expected ValueError")
