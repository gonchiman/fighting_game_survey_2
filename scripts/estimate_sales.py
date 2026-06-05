import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from fighting_game_analysis.analysis.sales_estimator import estimate_steam_sales
from fighting_game_analysis.config.games import GAMES
from fighting_game_analysis.data.steam_review_fetcher import fetch_review_summary


def main() -> None:
    """設定済みゲームの Steam 推定販売本数を出力します。"""
    for game in GAMES:
        summary = fetch_review_summary(game.app_id)
        total_reviews = summary["total_reviews"]

        estimated_sales = estimate_steam_sales(total_reviews)

        print(f"{game.title}:")
        print(f"  Reviews: {total_reviews}")
        print(f"  Estimated Steam sales: {estimated_sales}")
        print()


if __name__ == "__main__":
    main()
