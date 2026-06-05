import pandas as pd


def clean_monthly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Clean Steam Charts monthly stats into dated, numeric, chronological rows."""
    df = df.copy()

    df = df[df["Month"] != "Last 30 Days"].copy()

    df["Date"] = pd.to_datetime(df["Month"], format="%B %Y")
    df["Avg. Players"] = pd.to_numeric(df["Avg. Players"], errors="coerce")

    df = df.dropna(subset=["Date", "Avg. Players"])
    df = df.sort_values("Date").reset_index(drop=True)

    return df
