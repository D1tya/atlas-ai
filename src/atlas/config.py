from pathlib import Path


# --------------------------------------------------
# LLM
# --------------------------------------------------

MODEL_NAME = "qwen3:4b"
TEMPERATURE = 0


# --------------------------------------------------
# Research
# --------------------------------------------------

MAX_RESEARCH_QUERIES = 3
MAX_SEARCH_RESULTS = 5

MAX_PAGES_TO_READ = 6
MAX_PAGE_CHARACTERS = 12_000

HTTP_TIMEOUT = 10


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(
    __file__
).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_PATH = DATA_DIR / "atlas.db"   