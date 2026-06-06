import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from fighting_game_analysis.config.games import GAMES
from fighting_game_analysis.data.steam_charts_fetcher import save_monthly_stats_csv


st.set_page_config(
    page_title="Fighting Game Steam Analysis",
    layout="wide",
)

st.title("Fighting Game Steam Analysis")

st.write(
    "Steam Charts の月間平均プレイヤー数を使って、"
    "格闘ゲームのプレイヤー数推移と累積推定プレイ時間を可視化するアプリです。"
)


st.subheader("Pages")

st.page_link("pages/1_Cumulative_Play_Hours.py", label="Cumulative Play Hours")
st.page_link("pages/2_Avg_Players_Trend.py", label="Avg Players Trend")


st.subheader("Data Update")

selected_games = st.multiselect(
    "更新するタイトル",
    options=GAMES,
    default=GAMES,
    format_func=lambda game: game.title,
)

if st.button("選択したタイトルのCSVを更新"):
    if not selected_games:
        st.warning("少なくとも1つのタイトルを選択してください。")
        st.stop()

    with st.spinner("Steam Charts からデータを取得中..."):
        for game in selected_games:
            save_monthly_stats_csv(game)

    st.success("CSVを更新しました。")