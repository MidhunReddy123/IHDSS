"""Chroma-backed knowledge base. One chunk per guideline file (files are short summaries)."""
import chromadb

from ..config import CHROMA_DIR, KB_DIR, TOP_K_DOCS
from ..llm import embed

_COLLECTION = "guidelines"


def _collection():
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(_COLLECTION, metadata={"hnsw:space": "cosine"})


def ingest(force: bool = False) -> int:
    col = _collection()
    if col.count() and not force:
        return col.count()
    files = sorted(KB_DIR.glob("*.md"))
    texts = [f.read_text(encoding="utf-8") for f in files]
    ids = [f.stem for f in files]
    col.upsert(ids=ids, documents=texts, embeddings=embed(texts))
    return len(ids)


def search(query: str, k: int = TOP_K_DOCS) -> list[dict]:
    col = _collection()
    res = col.query(query_embeddings=embed([query]), n_results=min(k, col.count()))
    return [
        {"id": i, "text": d, "distance": dist}
        for i, d, dist in zip(res["ids"][0], res["documents"][0], res["distances"][0])
    ]
