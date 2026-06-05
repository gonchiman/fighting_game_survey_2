import pandas as pd

from fighting_game_analysis.analysis.playtime import add_estimated_play_hours
from fighting_game_analysis.analysis.sales_estimator import estimate_steam_sales


def test_add_estimated_play_hours_uses_month_length_and_cumulative_sum():
    """月ごとと累積の推定プレイ時間が正しく計算されることを確認します。"""
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
    """入力データが変更されないことを確認します。"""
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
    """デフォルト倍率で推定販売本数が計算されることを確認します。"""
    assert estimate_steam_sales(100) == 3500


def test_estimate_steam_sales_accepts_custom_multiplier():
    """任意の倍率で推定販売本数が計算されることを確認します。"""
    assert estimate_steam_sales(100, multiplier=42) == 4200
