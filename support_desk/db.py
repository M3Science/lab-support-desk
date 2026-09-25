"""Build support_desk.db from sql/schema.sql and the CSV files in data/."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "support_desk.db"


def load_csv(conn: sqlite3.Connection, table: str, path: Path) -> int:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    cols = list(rows[0])
    sql = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})"
    conn.executemany(sql, [[r[c] if r[c] != "" else None for c in cols] for r in rows])
    return len(rows)


def build(db_path: Path = DB_PATH) -> sqlite3.Connection:
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
    load_csv(conn, "sla_policy", ROOT / "data" / "sla_policy.csv")
    load_csv(conn, "kb_articles", ROOT / "data" / "kb_articles.csv")
    n = load_csv(conn, "tickets", ROOT / "data" / "tickets.csv")
    conn.commit()
    print(f"Built {db_path.name} with {n} tickets")
    return conn
