import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from fighting_game_analysis.config.games import GAMES


GAME_BY_TITLE = {
    game.title: game
    for game in GAMES
}


def get_display_title(game) -> str:
    latest_game = GAME_BY_TITLE.get(game.title, game)
    return getattr(latest_game, "display_title", latest_game.title)


def load_initial_month_peak(game) -> dict:
    df = pd.read_csv(game.csv_path)

    df = df[df["Month"] != "Last 30 Days"].copy()

    df["Date"] = pd.to_datetime(df["Month"], format="%B %Y", errors="coerce")
    df["Peak Players"] = pd.to_numeric(
        df["Peak Players"].astype(str).str.replace(",", ""),
        errors="coerce",
    )
    df["Avg. Players"] = pd.to_numeric(
        df["Avg. Players"].astype(str).str.replace(",", ""),
        errors="coerce",
    )

    df = df.dropna(subset=["Date", "Peak Players"])
    df = df.sort_values("Date").reset_index(drop=True)

    initial_month = df.iloc[0]

    return {
        "Game": game.title,
        "Display Game": get_display_title(game),
        "Initial Month": initial_month["Month"],
        "Initial Peak Players": initial_month["Peak Players"],
        "Initial Avg. Players": initial_month["Avg. Players"],
    }


st.title("Initial Month Peak Comparison")

selected_games = st.multiselect(
    "Select games",
    options=GAMES,
    default=GAMES,
    format_func=get_display_title,
)

rows = [
    load_initial_month_peak(game)
    for game in selected_games
]

df_result = pd.DataFrame(rows)

if df_result.empty:
    st.warning("No games selected.")
else:
    df_result = df_result.sort_values(
        "Initial Peak Players",
        ascending=False,
    ).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.barh(
        df_result["Display Game"],
        df_result["Initial Peak Players"],
    )

    ax.set_title("Initial Month Peak Players")
    ax.set_xlabel("Peak Players")
    ax.set_ylabel("Game")
    ax.tick_params(axis="y", labelsize=8)

    for i, value in enumerate(df_result["Initial Peak Players"]):
        ax.text(value, i, f" {int(value):,}", va="center")

    ax.invert_yaxis()

    fig.tight_layout()

    st.pyplot(fig)

    st.dataframe(df_result)
