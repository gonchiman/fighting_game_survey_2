import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from fighting_game_analysis.analysis.playtime import add_estimated_play_hours
from fighting_game_analysis.config.games import GAMES
from fighting_game_analysis.data.steam_charts_cleaner import clean_monthly_stats
from fighting_game_analysis.data.steam_charts_fetcher import save_monthly_stats_csv
from fighting_game_analysis.data.steam_charts_loader import load_monthly_stats_csv


st.set_page_config(
    page_title="Fighting Game Steam Analysis",
    layout="wide",
)

st.title("Fighting Game Steam Analysis")

st.write(
    "Steam Charts の月間平均プレイヤー数をもとに、"
    "推定月間プレイ時間と累積推定プレイ時間を可視化します。"
)

games = st.multiselect(
    "分析対象タイトル",
    options=GAMES,
    default=GAMES,
    format_func=lambda game: game.title,
)

if st.button("Steam Charts データを更新"):
    if not games:
        st.warning("少なくとも1つのタイトルを選択してください。")
    else:
        with st.spinner("データを取得中..."):
            for game in games:
                save_monthly_stats_csv(game)
        st.success("CSVを更新しました。")

if games:
    dfs = []

    for game in games:
        try:
            game_df = load_monthly_stats_csv(game)
        except FileNotFoundError:
            st.warning(f"{game.title} のCSVが見つかりません。先にデータを更新してください。")
            continue

        game_df = clean_monthly_stats(game_df)
        game_df = add_estimated_play_hours(game_df)
        game_df.insert(0, "Game", game.title)
        dfs.append(game_df)

    if not dfs:
        st.stop()

    df = pd.concat(dfs, ignore_index=True)

    st.subheader("分析データ")
    st.dataframe(df)

    fig, ax = plt.subplots(figsize=(12, 6))

    for game_title, game_df in df.groupby("Game"):
        ax.plot(
            game_df["Date"],
            game_df["Cumulative Estimated Play Hours"],
            label=game_title,
        )

    ax.set_title("Cumulative Estimated Play Hours")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Estimated Play Hours")
    ax.xaxis.set_major_locator(mdates.YearLocator(1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", rotation=90)
    ax.legend()

    fig.tight_layout()

    st.subheader("累積推定プレイ時間グラフ")
    st.pyplot(fig)

    csv = df.to_csv(index=False, encoding="utf-8-sig")

    st.download_button(
        label="分析CSVをダウンロード",
        data=csv,
        file_name="total_analysis.csv",
        mime="text/csv",
    )
