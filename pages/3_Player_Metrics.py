import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.fighting_game_analysis.analysis.player_metrics import create_player_analysis_table


RAW_DATA_DIR = BASE_DIR / "data" / "raw"


st.title("Player Metrics Analysis")

csv_paths = sorted(RAW_DATA_DIR.glob("*.csv"))

if not csv_paths:
    st.error("data/raw に CSV ファイルがありません。")
    st.stop()

selected_csv = st.selectbox(
    "Game Title",
    csv_paths,
    format_func=lambda path: path.stem.replace("_", " ").title()
)

df = pd.read_csv(selected_csv)
analysis_df = create_player_analysis_table(df)

st.subheader("Analysis Table")

st.dataframe(
    analysis_df[
        [
            "Months Since Release",
            "Month",
            "Avg. Players",
            "Deviation Score",
            "Initial Month Ratio",
            "MoM Ratio",
            "Cumulative Ratio",
            "Percentile Rank",
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.subheader("Summary")

latest = analysis_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Initial Avg. Players",
    f"{analysis_df.loc[0, 'Avg. Players']:.1f}"
)

col2.metric(
    "Max Avg. Players",
    f"{analysis_df['Avg. Players'].max():.1f}"
)

col3.metric(
    "Latest Initial Ratio",
    f"{latest['Initial Month Ratio']:.1f}%"
)

col4.metric(
    "Latest Deviation Score",
    f"{latest['Deviation Score']:.1f}"
)

st.subheader("Deviation Score")

deviation_chart_df = analysis_df.set_index("Months Since Release")[
    ["Deviation Score"]
]

st.line_chart(deviation_chart_df)

st.subheader("Initial Month Ratio")

initial_ratio_chart_df = analysis_df.set_index("Months Since Release")[
    ["Initial Month Ratio"]
]

st.line_chart(initial_ratio_chart_df)

st.subheader("Month-over-Month Ratio")

mom_ratio_chart_df = analysis_df.set_index("Months Since Release")[
    ["MoM Ratio"]
]

st.line_chart(mom_ratio_chart_df)

st.subheader("Cumulative Ratio")

cumulative_ratio_chart_df = analysis_df.set_index("Months Since Release")[
    ["Cumulative Ratio"]
]

st.line_chart(cumulative_ratio_chart_df)