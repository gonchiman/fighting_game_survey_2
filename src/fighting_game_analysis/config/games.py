from dataclasses import dataclass
from pathlib import Path

from fighting_game_analysis.config.paths import RAW_DATA_DIR


@dataclass(frozen=True)
class Game:
    title: str
    app_id: int

    @property
    def csv_path(self) -> Path:
        """ゲームの月次統計 CSV パスを返します。

        Returns:
            生データ CSV の保存先パス。
        """
        filename = self.title.lower().replace(" ", "_").replace(":", "").replace("-", "_")
        return RAW_DATA_DIR / f"{filename}.csv"


MAIN_GAMES = [
    Game("Street Fighter V", 310950),
    Game("TEKKEN 7", 389730),
    Game("DRAGON BALL FighterZ", 678950),
    Game("SOULCALIBUR VI", 544750),
    Game("Mortal Kombat 11", 976310),
    Game("GUILTY GEAR -STRIVE-", 1384160),
    Game("Street Fighter 6", 1364780),
    Game("TEKKEN 8", 1778820),
    Game("Granblue Fantasy Versus: Rising", 2157560),
]

EXCLUDED_GAMES = [
    Game("Granblue Fantasy: Versus", 1090630),
]

GAMES = MAIN_GAMES
