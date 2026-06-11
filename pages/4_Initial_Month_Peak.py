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

SUCCESSOR_RELEASE_MONTHS = {
    "Street Fighter V": pd.Timestamp("2023-06-01"),
    "TEKKEN 7": pd.Timestamp("2024-01-01"),
    "Mortal Kombat 11": pd.Timestamp("2023-09-01"),
    "Granblue Fantasy: Versus": pd.Timestamp("2023-12-01"),
    "Granblue Fantasy Versus": pd.Timestamp("2023-12-01"),
}


def get_display_title(game) -> str:
    latest_game = GAME_BY_TITLE.get(game.title, game)
    return getattr(latest_game, "display_title", latest_game.title)


def load_initial_peak_and_stable_avg(
    game,
    stable_start_month: int,
    exclude_after_successor: bool,
) -> dict:
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

    df = df.dropna(subset=["Date", "Peak Players", "Avg. Players"])
    df = df.sort_values("Date").reset_index(drop=True)

    initial_month = df.iloc[0]
    stable_df = df.iloc[stable_start_month - 1:].copy()

    successor_release_month = SUCCESSOR_RELEASE_MONTHS.get(game.title)

    if exclude_after_successor and successor_release_month is not None:
        stable_df = stable_df[stable_df["Date"] < successor_release_month]

    if stable_df.empty:
        stable_avg_players = None
        stable_ratio = None
        stable_period_months = 0
        stable_end_month = None
    else:
        stable_avg_players = stable_df["Avg. Players"].mean()
        stable_ratio = stable_avg_players / initial_month["Peak Players"]
        stable_period_months = len(stable_df)
        stable_end_month = stable_df.iloc[-1]["Month"]

    return {
        "Game": game.title,
        "Display Game": get_display_title(game),
        "Initial Month": initial_month["Month"],
        "Initial Peak Players": initial_month["Peak Players"],
        "Stable Start Month": stable_start_month,
        "Stable End Month": stable_end_month,
        "Stable Period Months": stable_period_months,
        "Successor Release Month": (
            successor_release_month.strftime("%B %Y")
            if successor_release_month is not None
            else None
        ),
        "Successor Period Excluded": (
            exclude_after_successor and successor_release_month is not None
        ),
        "Stable Avg. Players": stable_avg_players,
        "Stable / Initial Peak Ratio": stable_ratio,
    }


st.title("Initial Peak vs Stable Average Players")

stable_start_month = st.slider(
    "Stable period start month",
    min_value=2,
    max_value=24,
    value=7,
)

exclude_after_successor = st.checkbox(
    "Exclude months after successor release",
    value=True,
)

selected_games = st.multiselect(
    "Select games",
    options=GAMES,
    default=GAMES,
    format_func=get_display_title,
)

rows = [
    load_initial_peak_and_stable_avg(
        game,
        stable_start_month,
        exclude_after_successor,
    )
    for game in selected_games
]

df_result = pd.DataFrame(rows)

if df_result.empty:
    st.warning("No games selected.")
    st.stop()

df_result = df_result.dropna(subset=["Stable Avg. Players"])

if df_result.empty:
    st.warning("No games have enough data for the selected stable period.")
    st.stop()

df_result = df_result.sort_values(
    "Initial Peak Players",
    ascending=False,
).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 6))

y_positions = list(range(len(df_result)))
bar_height = 0.35

initial_y_positions = [y - bar_height / 2 for y in y_positions]
stable_y_positions = [y + bar_height / 2 for y in y_positions]

ax.barh(
    initial_y_positions,
    df_result["Initial Peak Players"],
    height=bar_height,
    label="Initial Peak Players",
)

stable_label = f"Stable Avg. Players ({stable_start_month}th month onward)"
if exclude_after_successor:
    stable_label += ", before successor release"

ax.barh(
    stable_y_positions,
    df_result["Stable Avg. Players"],
    height=bar_height,
    label=stable_label,
)

ax.set_yticks(y_positions)
ax.set_yticklabels(df_result["Display Game"], fontsize=8)

ax.set_title("Initial Peak Players vs Stable Average Players", fontsize=12)
ax.set_xlabel("Players", fontsize=10)
ax.set_ylabel("Game", fontsize=10)
ax.tick_params(axis="x", labelsize=9)

for y, value in zip(initial_y_positions, df_result["Initial Peak Players"]):
    ax.text(value, y, f" {int(value):,}", va="center", fontsize=8)

for y, value in zip(stable_y_positions, df_result["Stable Avg. Players"]):
    ax.text(value, y, f" {int(value):,}", va="center", fontsize=8)

ax.legend(fontsize=8)
ax.invert_yaxis()

fig.tight_layout()

st.subheader("Initial Peak Players vs Stable Average Players")

st.pyplot(fig)

st.subheader("Stable / Initial Peak Ratio")

stable_divided_by_initial_peak_df = df_result.set_index("Display Game")[
    ["Stable / Initial Peak Ratio"]
]
sorted_stable_divided_by_initial_peak_df = stable_divided_by_initial_peak_df.sort_values(
    by="Stable / Initial Peak Ratio",
    ascending=False
)

st.bar_chart(sorted_stable_divided_by_initial_peak_df, sort=False)

st.dataframe(
    df_result,
    hide_index=True,
)
