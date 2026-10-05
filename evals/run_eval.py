"""Evaluate on synthetic cases: top-1 / top-3 accuracy, citation validity, latency."""
import time

from ihdss import db
from ihdss.agents.graph import diagnose


def matches(pred: str, truth: str) -> bool:
    p, t = pred.lower(), truth.lower()
    return t in p or p in t


def main() -> None:
    patients = db.list_patients()
    top1 = top3 = supported = total_dx = 0
    t0 = time.time()
    for p in patients:
        r = diagnose(p)
        names = [d["diagnosis"] for d in r["differential"]]
        hit1 = bool(names) and matches(names[0], p["truth"])
        hit3 = any(matches(n, p["truth"]) for n in names[:3])
        top1 += hit1
        top3 += hit3
        supported += sum(d["supported"] for d in r["differential"])
        total_dx += len(r["differential"])
        print(f"{p['id']} truth={p['truth']!r} -> {names[:3]} top1={hit1} top3={hit3}")
    n = len(patients)
    print(f"\nTop-1: {top1}/{n}  Top-3: {top3}/{n}  Cited: {supported}/{total_dx}  "
          f"Avg latency: {(time.time() - t0) / n:.1f}s")


if __name__ == "__main__":
    main()
