import pandas as pd


def add_estimated_play_hours(df: pd.DataFrame) -> pd.DataFrame:
    """推定プレイ時間の列を追加します。

    Args:
        df: `Date` と `Avg. Players` を含む月次データ。

    Returns:
        月ごとの推定プレイ時間と累積推定プレイ時間を追加したデータ。
    """
    df = df.copy()

    df["Hours in Month"] = df["Date"].dt.days_in_month * 24
    df["Estimated Play Hours"] = df["Avg. Players"] * df["Hours in Month"]
    df["Cumulative Estimated Play Hours"] = df["Estimated Play Hours"].cumsum()

    return df
