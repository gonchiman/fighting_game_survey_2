import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.fighting_game_analysis.analysis.sales_estimator import estimate_steam_sales
from src.fighting_game_analysis.data.steam_review_fetcher import fetch_review_summary


APP_IDS = {
    "Street Fighter V": 310950,
    "TEKKEN 7": 389730,
    "DRAGON BALL FighterZ": 678950,
    "SOULCALIBUR VI": 544750,
    "Mortal Kombat 11": 976310,
    "GUILTY GEAR -STRIVE-": 1384160,
    "Street Fighter 6": 1364780,
}


def main() -> None:
    for title, app_id in APP_IDS.items():
        summary = fetch_review_summary(app_id)
        total_reviews = summary["total_reviews"]

        estimated_sales = estimate_steam_sales(total_reviews)

        print(f"{title}:")
        print(f"  Reviews: {total_reviews}")
        print(f"  Estimated Steam sales: {estimated_sales}")
        print()


if __name__ == "__main__":
    main()