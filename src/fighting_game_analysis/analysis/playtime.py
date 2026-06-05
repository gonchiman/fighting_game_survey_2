import pandas as pd


def add_estimated_play_hours(df: pd.DataFrame) -> pd.DataFrame:
    """Add monthly and cumulative estimated play-hour columns to a data frame."""
    df = df.copy()

    df["Hours in Month"] = df["Date"].dt.days_in_month * 24
    df["Estimated Play Hours"] = df["Avg. Players"] * df["Hours in Month"]
    df["Cumulative Estimated Play Hours"] = df["Estimated Play Hours"].cumsum()

    return df
