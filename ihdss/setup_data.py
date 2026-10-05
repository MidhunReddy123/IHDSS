"""One-time setup: create DB, load synthetic patients, build the Chroma knowledge base."""
from . import db
from .data.synthetic import PATIENTS
from .kb.store import ingest


def main(force_kb: bool = False) -> None:
    db.init_db()
    for p in PATIENTS:
        db.save_patient(p)
    n = ingest(force=force_kb)
    print(f"Loaded {len(PATIENTS)} synthetic patients and {n} knowledge-base documents.")


if __name__ == "__main__":
    main()
