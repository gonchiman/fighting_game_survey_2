from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from fighting_game_analysis.config.games import Game


def save_avg_players_plot(
    game: Game,
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save a line plot of monthly average players for a game."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Avg. Players"], marker="o")

    plt.title(f"{game.title} - Monthly Average Players")
    plt.xlabel("Month")
    plt.ylabel("Avg. Players")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def save_cumulative_play_hours_plot(
    game: Game,
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Save a line plot of cumulative estimated play hours for a game."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Cumulative Estimated Play Hours"], marker="o")

    plt.title(f"{game.title} - Cumulative Estimated Play Hours")
    plt.xlabel("Month")
    plt.ylabel("Cumulative Estimated Play Hours")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()
