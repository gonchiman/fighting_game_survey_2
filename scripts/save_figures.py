import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from fighting_game_analysis.analysis.playtime import add_estimated_play_hours
from fighting_game_analysis.config.games import GAMES
from fighting_game_analysis.config.paths import FIGURES_DIR
from fighting_game_analysis.data.steam_charts_cleaner import clean_monthly_stats
from fighting_game_analysis.data.steam_charts_loader import load_monthly_stats_csv
from fighting_game_analysis.visualization.plots import (
    save_avg_players_plot,
    save_cumulative_play_hours_plot,
)


def main() -> None:
    for game in GAMES:
        df = load_monthly_stats_csv(game)
        df = clean_monthly_stats(df)
        df = add_estimated_play_hours(df)

        avg_players_path = FIGURES_DIR / f"{game.csv_path.stem}_avg_players.png"
        cumulative_path = FIGURES_DIR / f"{game.csv_path.stem}_cumulative_play_hours.png"

        save_avg_players_plot(game, df, avg_players_path)
        save_cumulative_play_hours_plot(game, df, cumulative_path)

        print(f"Saved figures: {game.title}")


if __name__ == "__main__":
    main()