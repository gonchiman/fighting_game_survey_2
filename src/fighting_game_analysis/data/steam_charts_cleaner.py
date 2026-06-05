import pandas as pd


def clean_monthly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Steam Charts の月次統計を分析しやすい形式に整えます。

    Args:
        df: Steam Charts から取得した月次統計データ。

    Returns:
        日付と平均プレイヤー数を整形し、日付順に並べたデータ。
    """
    df = df.copy()

    df = df[df["Month"] != "Last 30 Days"].copy()

    df["Date"] = pd.to_datetime(df["Month"], format="%B %Y")
    df["Avg. Players"] = pd.to_numeric(df["Avg. Players"], errors="coerce")

    df = df.dropna(subset=["Date", "Avg. Players"])
    df = df.sort_values("Date").reset_index(drop=True)

    return df
