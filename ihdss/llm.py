import json
import re

import ollama

from .config import EMBED_MODEL, LLM_MODEL


def chat_json(system: str, user: str, model: str = LLM_MODEL, retries: int = 2) -> dict:
    """Ask the local model for a JSON object; retry on malformed output."""
    last = ""
    for _ in range(retries + 1):
        resp = ollama.chat(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            format="json",
            think=False,
            options={"temperature": 0.1},
        )
        last = resp["message"]["content"]
        try:
            return json.loads(last)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", last, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except json.JSONDecodeError:
                    pass
    raise ValueError(f"Model returned invalid JSON: {last[:200]}")


def embed(texts: list[str]) -> list[list[float]]:
    return ollama.embed(model=EMBED_MODEL, input=texts)["embeddings"]
