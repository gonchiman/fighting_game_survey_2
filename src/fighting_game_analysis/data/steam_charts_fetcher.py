from io import StringIO
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import pandas as pd

from fighting_game_analysis.config.games import Game
from fighting_game_analysis.config.urls import STEAM_CHARTS_APP_BASE_URL


REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    ),
}
REQUEST_TIMEOUT_SECONDS = 30


def fetch_page_html(url: str) -> str:
    request = Request(url, headers=REQUEST_HEADERS)

    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def fetch_monthly_stats(game: Game) -> pd.DataFrame:
    url = urljoin(STEAM_CHARTS_APP_BASE_URL, str(game.app_id))

    html = fetch_page_html(url)
    try:
        tables = pd.read_html(StringIO(html))
    except ValueError as exc:
        raise ValueError(f"No tables found for {game.title}") from exc

    if not tables:
        raise ValueError(f"No tables found for {game.title}")

    return tables[0]


def save_monthly_stats_csv(game: Game) -> None:
    game.csv_path.parent.mkdir(parents=True, exist_ok=True)

    df = fetch_monthly_stats(game)
    df.to_csv(game.csv_path, index=False, encoding="utf-8-sig")
