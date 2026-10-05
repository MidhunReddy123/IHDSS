from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "ihdss.db"
CHROMA_DIR = ROOT / ".chroma"
KB_DIR = ROOT / "ihdss" / "kb" / "docs"

LLM_MODEL = "qwen3:4b"
EMBED_MODEL = "nomic-embed-text"
TOP_K_DOCS = 4

DISCLAIMER = (
    "Decision support for research/education only. Uses synthetic data. "
    "Not a medical device; a licensed clinician must verify every suggestion."
)
