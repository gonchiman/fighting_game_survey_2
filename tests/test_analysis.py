import pandas as pd

from fighting_game_analysis.analysis.playtime import add_estimated_play_hours
from fighting_game_analysis.analysis.sales_estimator import estimate_steam_sales


def test_add_estimated_play_hours_uses_month_length_and_cumulative_sum():
    """Check monthly play hours and cumulative play hours are calculated correctly."""
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-02-01", "2024-03-01"]),
            "Avg. Players": [10, 20],
        }
    )

    result = add_estimated_play_hours(df)

    assert result["Hours in Month"].tolist() == [29 * 24, 31 * 24]
    assert result["Estimated Play Hours"].tolist() == [6960, 14880]
    assert result["Cumulative Estimated Play Hours"].tolist() == [6960, 21840]


def test_add_estimated_play_hours_does_not_mutate_input():
    """Check estimated play-hour columns are added to a copy of the input."""
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01"]),
            "Avg. Players": [5],
        }
    )

    add_estimated_play_hours(df)

    assert "Hours in Month" not in df.columns
    assert "Estimated Play Hours" not in df.columns
    assert "Cumulative Estimated Play Hours" not in df.columns


def test_estimate_steam_sales_uses_default_multiplier():
    """Check the default review-to-sales multiplier is used."""
    assert estimate_steam_sales(100) == 3500


def test_estimate_steam_sales_accepts_custom_multiplier():
    """Check a custom review-to-sales multiplier can be provided."""
    assert estimate_steam_sales(100, multiplier=42) == 4200
