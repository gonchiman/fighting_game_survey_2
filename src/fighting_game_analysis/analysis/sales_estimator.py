def estimate_steam_sales(total_reviews: int, multiplier: int = 35) -> int:
    """Estimate Steam sales from a review count using a review-to-sales multiplier."""
    return total_reviews * multiplier
