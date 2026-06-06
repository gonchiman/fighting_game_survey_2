import pandas as pd


def create_player_analysis_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[df["Month"] != "Last 30 Days"]

    # Steam Charts は新しい月が上にあるので、古い月 → 新しい月に並べ替える
    df = df.iloc[::-1].reset_index(drop=True)

    df["Avg. Players"] = pd.to_numeric(df["Avg. Players"], errors="coerce")

    df["Months Since Release"] = range(len(df))

    mean = df["Avg. Players"].mean()
    std = df["Avg. Players"].std(ddof=0)

    if std == 0:
        df["Deviation Score"] = 50
    else:
        df["Deviation Score"] = 50 + 10 * (df["Avg. Players"] - mean) / std

    initial_players = df.loc[0, "Avg. Players"]
    df["Initial Month Ratio"] = df["Avg. Players"] / initial_players * 100

    df["MoM Ratio"] = df["Avg. Players"].pct_change() * 100 + 100

    df["Cumulative Avg. Players"] = df["Avg. Players"].cumsum()

    total_players = df["Avg. Players"].sum()
    df["Cumulative Ratio"] = df["Cumulative Avg. Players"] / total_players * 100

    df["Percentile Rank"] = df["Avg. Players"].rank(pct=True) * 100

    return df