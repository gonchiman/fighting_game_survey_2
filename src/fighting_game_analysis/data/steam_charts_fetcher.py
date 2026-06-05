from io import StringIO
from urllib.parse import urljoin

import pandas as pd
from playwright.sync_api import sync_playwright

from fighting_game_analysis.config.games import Game
from fighting_game_analysis.config.urls import STEAM_CHARTS_APP_BASE_URL


def fetch_monthly_stats(game: Game) -> pd.DataFrame:
    url = urljoin(STEAM_CHARTS_APP_BASE_URL, str(game.app_id))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30000,
            )

            html = page.content()
            tables = pd.read_html(StringIO(html))

            if not tables:
                raise ValueError(f"No tables found for {game.title}")

            return tables[0]

        finally:
            browser.close()


def save_monthly_stats_csv(game: Game) -> None:
    game.csv_path.parent.mkdir(parents=True, exist_ok=True)

    df = fetch_monthly_stats(game)
    df.to_csv(game.csv_path, index=False, encoding="utf-8-sig")
