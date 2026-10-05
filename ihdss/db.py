import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from .config import DB_PATH


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


def init_db() -> None:
    with closing(_conn()) as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY, data TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, patient_id TEXT,
                event TEXT, payload TEXT);
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, patient_id TEXT,
                diagnosis TEXT, decision TEXT, note TEXT);
            """
        )
        c.commit()


def save_patient(p: dict) -> None:
    with closing(_conn()) as c:
        c.execute("INSERT OR REPLACE INTO patients VALUES (?, ?)", (p["id"], json.dumps(p)))
        c.commit()


def get_patient(pid: str) -> dict | None:
    with closing(_conn()) as c:
        r = c.execute("SELECT data FROM patients WHERE id=?", (pid,)).fetchone()
    return json.loads(r["data"]) if r else None


def list_patients() -> list[dict]:
    with closing(_conn()) as c:
        rows = c.execute("SELECT data FROM patients ORDER BY id").fetchall()
    return [json.loads(r["data"]) for r in rows]


def audit(patient_id: str, event: str, payload: dict) -> None:
    with closing(_conn()) as c:
        c.execute(
            "INSERT INTO audit (ts, patient_id, event, payload) VALUES (?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), patient_id, event, json.dumps(payload)),
        )
        c.commit()


def save_feedback(patient_id: str, diagnosis: str, decision: str, note: str = "") -> None:
    with closing(_conn()) as c:
        c.execute(
            "INSERT INTO feedback (ts, patient_id, diagnosis, decision, note) VALUES (?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), patient_id, diagnosis, decision, note),
        )
        c.commit()
