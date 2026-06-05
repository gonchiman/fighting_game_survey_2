import pandas as pd

from fighting_game_analysis.config.games import Game


def load_monthly_stats_csv(game: Game) -> pd.DataFrame:
    """ゲームの月次統計 CSV を読み込みます。

    Args:
        game: 読み込み対象のゲーム。

    Returns:
        CSV から読み込んだ月次統計データ。

    Raises:
        FileNotFoundError: CSV ファイルが存在しない場合。
    """
    if not game.csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {game.csv_path}")

    return pd.read_csv(game.csv_path)
