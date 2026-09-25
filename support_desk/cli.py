"""Build the database, run every report, and write the outputs.

Usage (from the repo root):
    python -m support_desk
Writes:
    support_desk.db   SQLite database (rebuilt each run)
    docs/report.md    all report tables in Markdown
    docs/index.html   the dashboard (also served by GitHub Pages)
"""

from __future__ import annotations

from .dashboard import build_html
from .db import DB_PATH, ROOT, build
from .reports import build_markdown, kpis, run_all


def main() -> int:
    conn = build(DB_PATH)
    reports = run_all(conn)
    k = kpis(conn)
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "report.md").write_text(build_markdown(reports, k), encoding="utf-8")
    (docs / "index.html").write_text(build_html(reports, k), encoding="utf-8")
    conn.close()
    print(f"Ran {len(reports)} reports: {k['tickets']} tickets, "
          f"{k['resolve_met_pct']}% resolved within SLA, {k['open']} open.")
    print("Wrote docs/report.md and docs/index.html")
    return 0
