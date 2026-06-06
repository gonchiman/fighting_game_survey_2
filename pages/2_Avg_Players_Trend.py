import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from fighting_game_analysis.config.games import GAMES


MONTH_COLUMN = "Month"
AVG_PLAYERS_COLUMN = "Avg. Players"

MODE_EACH = "それぞれの推移"
MODE_SINGLE = "選択したタイトルのみ"

PLOT_MODES = [
    MODE_EACH,
    MODE_SINGLE,
]


st.set_page_config(
    page_title="Avg Players Trend",
    layout="wide",
)

st.title("Monthly Average Players Trend")

st.write(
    "Steam Charts の Avg. Players を使って、"
    "各タイトルの月間平均プレイヤー数の推移を表示します。"
)


def load_game_df(game) -> pd.DataFrame:
    csv_path = Path(game.csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"{game.title} のCSVが見つかりません: {csv_path}")

    df = pd.read_csv(csv_path)

    df = df[df[MONTH_COLUMN] != "Last 30 Days"].copy()

    df["Date"] = pd.to_datetime(
        df[MONTH_COLUMN],
        format="%B %Y",
        errors="coerce",
    )

    df = df.dropna(subset=["Date"])

    df[AVG_PLAYERS_COLUMN] = pd.to_numeric(
        df[AVG_PLAYERS_COLUMN],
        errors="coerce",
    )

    df = df.dropna(subset=[AVG_PLAYERS_COLUMN])

    df = df.sort_values("Date").reset_index(drop=True)

    df["Title"] = game.title

    return df


def create_avg_players_plot(games):
    fig, ax = plt.subplots(figsize=(12, 6))

    for game in games:
        df = load_game_df(game)

        ax.plot(
            df["Date"],
            df[AVG_PLAYERS_COLUMN],
            label=game.title,
        )

    ax.set_title("Monthly Average Players")
    ax.set_xlabel("Year")
    ax.set_ylabel("Avg. Players")

    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", rotation=90)

    ax.grid(True)
    ax.legend()

    fig.tight_layout()

    return fig


plot_mode = st.radio(
    "表示モード",
    options=PLOT_MODES,
)

if plot_mode == MODE_SINGLE:
    selected_game = st.selectbox(
        "表示するタイトル",
        options=GAMES,
        format_func=lambda game: game.title,
    )

    selected_games = [selected_game]

else:
    selected_games = st.multiselect(
        "表示するタイトル",
        options=GAMES,
        default=GAMES,
        format_func=lambda game: game.title,
    )


if not selected_games:
    st.warning("少なくとも1つのタイトルを選択してください。")
    st.stop()


try:
    fig = create_avg_players_plot(selected_games)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()


st.subheader("Avg. Players Graph")

st.pyplot(fig)