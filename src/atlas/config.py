from pathlib import Path


MODEL_NAME = "qwen3:4b"

TEMPERATURE = 0

MAX_SEARCH_RESULTS = 5


PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]


DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


DATABASE_PATH = (
    DATA_DIR / "atlas.db"
)