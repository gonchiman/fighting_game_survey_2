def estimate_steam_sales(total_reviews: int, multiplier: int = 35) -> int:
    """レビュー数から Steam の推定販売本数を計算します。

    Args:
        total_reviews: Steam の総レビュー数。
        multiplier: レビュー数に掛ける推定倍率。

    Returns:
        推定販売本数。
    """
    return total_reviews * multiplier
