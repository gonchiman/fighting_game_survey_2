from dataclasses import dataclass
from pathlib import Path

from fighting_game_analysis.config.paths import RAW_DATA_DIR


@dataclass(frozen=True)
class Game:
    title: str
    app_id: int
    short_title: str | None = None

    @property
    def display_title(self) -> str:
        return self.short_title or self.title

    @property
    def csv_path(self) -> Path:
        filename = (
            self.title.lower()
            .replace(" ", "_")
            .replace(":", "")
            .replace("-", "_")
            .replace("'", "")
        )
        return RAW_DATA_DIR / f"{filename}.csv"


MAIN_GAMES = [
    Game("Street Fighter V", 310950, "SFV"),
    Game("TEKKEN 7", 389730),
    Game("DRAGON BALL FighterZ", 678950, "DBFZ"),
    Game("SOULCALIBUR VI", 544750, "SCVI"),
    Game("Mortal Kombat 11", 976310, "MK11"),
    Game("GUILTY GEAR -STRIVE-", 1384160, "GGST"),
    Game("Street Fighter 6", 1364780, "SF6"),
    Game("TEKKEN 8", 1778820),
    Game("Granblue Fantasy Versus: Rising", 2157560, "GBVSR"),
    Game("JoJo's Bizarre Adventure: All-Star Battle R", 1372110, "JoJo ASBR"),
    Game("FATAL FURY: City of the Wolves", 2492040, "Fatal Fury CotW"),
]

EXCLUDED_GAMES = [
    Game("Granblue Fantasy: Versus", 1090630, "GBVS"),
]

GAMES = MAIN_GAMES
