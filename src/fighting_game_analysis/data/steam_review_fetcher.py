import requests

from fighting_game_analysis.config.urls import STEAM_REVIEWS_BASE_URL


def fetch_review_summary(app_id: int) -> dict:
    """Fetch Steam review summary metadata for an app."""
    url = f"{STEAM_REVIEWS_BASE_URL}{app_id}"
    params = {
        "json": 1,
        "language": "all",
        "purchase_type": "all",
        "num_per_page": 0,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()["query_summary"]
