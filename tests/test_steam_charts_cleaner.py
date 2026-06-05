import pandas as pd

from fighting_game_analysis.data.steam_charts_cleaner import clean_monthly_stats


def test_clean_monthly_stats_removes_summary_rows_and_sorts_by_date():
    """集計行が除外され、月次データが日付順に並ぶことを確認します。"""
    df = pd.DataFrame(
        {
            "Month": ["March 2024", "Last 30 Days", "January 2024", "February 2024"],
            "Avg. Players": ["30.5", "999", "10", "20"],
        }
    )

    result = clean_monthly_stats(df)

    assert result["Month"].tolist() == ["January 2024", "February 2024", "March 2024"]
    assert result["Avg. Players"].tolist() == [10.0, 20.0, 30.5]
    assert result["Date"].tolist() == pd.to_datetime(
        ["2024-01-01", "2024-02-01", "2024-03-01"]
    ).tolist()


def test_clean_monthly_stats_drops_rows_with_invalid_player_counts():
    """平均プレイヤー数が数値でない行が除外されることを確認します。"""
    df = pd.DataFrame(
        {
            "Month": ["January 2024", "February 2024"],
            "Avg. Players": ["not a number", "25"],
        }
    )

    result = clean_monthly_stats(df)

    assert result["Month"].tolist() == ["February 2024"]
    assert result["Avg. Players"].tolist() == [25]


def test_clean_monthly_stats_does_not_mutate_input():
    """クリーニング時に入力データが変更されないことを確認します。"""
    df = pd.DataFrame(
        {
            "Month": ["January 2024"],
            "Avg. Players": ["10"],
        }
    )

    clean_monthly_stats(df)

    assert "Date" not in df.columns
    assert df["Avg. Players"].tolist() == ["10"]
