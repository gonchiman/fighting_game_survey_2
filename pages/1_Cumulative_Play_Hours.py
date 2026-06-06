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
ESTIMATED_PLAY_HOURS_COLUMN = "Estimated Play Hours"
CUMULATIVE_PLAY_HOURS_COLUMN = "Cumulative Estimated Play Hours"


st.set_page_config(
    page_title="Cumulative Play Hours",
    layout="wide",
)

st.title("Cumulative Estimated Play Hours")

st.write(
    "Steam Charts の Avg. Players を使って、"
    "月間推定プレイ時間と累積推定プレイ時間を計算します。"
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

    df["Hours In Month"] = df["Date"].dt.days_in_month * 24

    df[ESTIMATED_PLAY_HOURS_COLUMN] = (
        df[AVG_PLAYERS_COLUMN] * df["Hours In Month"]
    )

    df["Title"] = game.title

    return df[
        [
            "Title",
            "Date",
            MONTH_COLUMN,
            AVG_PLAYERS_COLUMN,
            "Hours In Month",
            ESTIMATED_PLAY_HOURS_COLUMN,
        ]
    ]


def create_total_df(games) -> pd.DataFrame:
    dfs = []

    for game in games:
        dfs.append(load_game_df(game))

    all_df = pd.concat(dfs, ignore_index=True)

    total_df = (
        all_df.groupby("Date", as_index=False)[ESTIMATED_PLAY_HOURS_COLUMN]
        .sum()
        .sort_values("Date")
        .reset_index(drop=True)
    )

    total_df[CUMULATIVE_PLAY_HOURS_COLUMN] = total_df[
        ESTIMATED_PLAY_HOURS_COLUMN
    ].cumsum()

    total_df[MONTH_COLUMN] = total_df["Date"].dt.strftime("%B %Y")

    return total_df[
        [
            "Date",
            MONTH_COLUMN,
            ESTIMATED_PLAY_HOURS_COLUMN,
            CUMULATIVE_PLAY_HOURS_COLUMN,
        ]
    ]


def create_cumulative_plot(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        df["Date"],
        df[CUMULATIVE_PLAY_HOURS_COLUMN],
        marker="o",
    )

    ax.set_title("Cumulative Estimated Play Hours")
    ax.set_xlabel("Month")
    ax.set_ylabel("Cumulative Estimated Play Hours")
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", rotation=90)

    ax.grid(True)
    fig.tight_layout()

    return fig


with st.sidebar:
    selected_games = st.multiselect(
        "分析対象タイトル",
        options=GAMES,
        default=GAMES,
        format_func=lambda game: game.title,
    )

if not selected_games:
    st.warning("少なくとも1つのタイトルを選択してください。")
    st.stop()

try:
    total_df = create_total_df(selected_games)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

st.subheader("Cumulative Graph")

fig = create_cumulative_plot(total_df)
st.pyplot(fig)

st.subheader("Total Analysis Data")

display_df = total_df.copy()
display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m")

st.dataframe(
    display_df,
    hide_index=True,
)

csv = display_df.to_csv(index=False, encoding="utf-8-sig")

st.download_button(
    label="CSVをダウンロード",
    data=csv,
    file_name="cumulative_play_hours.csv",
    mime="text/csv",
)
