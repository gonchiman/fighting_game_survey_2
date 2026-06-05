import pandas as pd

from fighting_game_analysis.config.games import Game


def load_monthly_stats_csv(game: Game) -> pd.DataFrame:
    """Load a game's raw monthly Steam Charts CSV file."""
    if not game.csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {game.csv_path}")

    return pd.read_csv(game.csv_path)
