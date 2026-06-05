from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
AVG_PLAYERS_FIGURES_DIR = FIGURES_DIR / "avg_players"
CUMULATIVE_PLAY_HOURS_FIGURES_DIR = FIGURES_DIR / "cumulative_play_hours"
REPORTS_DIR = OUTPUTS_DIR / "reports"
