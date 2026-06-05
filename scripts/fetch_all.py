import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(SRC_DIR))

from fighting_game_analysis.config.games import GAMES
from fighting_game_analysis.data.steam_charts_fetcher import save_monthly_stats_csv


def main() -> None:
    """Fetch and save monthly Steam Charts CSV files for configured games."""
    for game in GAMES:
        save_monthly_stats_csv(game)
        print(f"Saved: {game.title}")


if __name__ == "__main__":
    main()
