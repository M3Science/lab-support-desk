"""Run the SQL report files and render them as Markdown."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


@dataclass
class Report:
    key: str            # file stem, e.g. "01_volume_by_category"
    title: str
    question: str
    sql: str
    columns: list[str]
    rows: list[tuple]

    def column(self, name: str) -> list:
        i = self.columns.index(name)
        return [r[i] for r in self.rows]


def _header(sql: str, tag: str) -> str:
    for line in sql.splitlines():
        if line.startswith(f"-- {tag}:"):
            return line.split(":", 1)[1].strip()
    return ""


def run_all(conn: sqlite3.Connection) -> dict[str, Report]:
    reports = {}
    for path in sorted(SQL_DIR.glob("[0-9][0-9]_*.sql")):
        sql = path.read_text(encoding="utf-8")
        cur = conn.execute(sql)
        reports[path.stem] = Report(
            key=path.stem,
            title=_header(sql, "title"),
            question=_header(sql, "question"),
            sql=sql,
            columns=[d[0] for d in cur.description],
            rows=cur.fetchall(),
        )
    return reports


def kpis(conn: sqlite3.Connection) -> dict[str, float]:
    row = conn.execute("""
        SELECT COUNT(*),
               ROUND(100.0 * AVG(response_met), 1),
               ROUND(100.0 * AVG(resolve_met), 1),
               ROUND(100.0 * AVG(CASE WHEN status = 'Resolved' THEN reopened END), 1),
               SUM(status <> 'Resolved')
        FROM ticket_sla
    """).fetchone()
    return dict(zip(["tickets", "response_met_pct", "resolve_met_pct", "reopen_pct", "open"], row))


def to_markdown_table(r: Report) -> str:
    head = "| " + " | ".join(r.columns) + " |"
    sep = "|" + "---|" * len(r.columns)
    body = ["| " + " | ".join("" if v is None else str(v) for v in row) + " |" for row in r.rows]
    return "\n".join([head, sep, *body])


def build_markdown(reports: dict[str, Report], k: dict[str, float]) -> str:
    out = [
        "# Lab Application Support Desk Report",
        "",
        "Reporting period: 2026-01-05 to 2026-03-29 (12 weeks, synthetic data).",
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| Tickets | {k['tickets']} |",
        f"| First response within SLA | {k['response_met_pct']}% |",
        f"| Resolved within SLA | {k['resolve_met_pct']}% |",
        f"| Reopen rate | {k['reopen_pct']}% |",
        f"| Open at end of period | {k['open']} |",
        "",
    ]
    for r in reports.values():
        out += [f"## {r.title}", "", f"*{r.question}*", "", to_markdown_table(r),
                "", f"Query: `sql/{r.key}.sql`", ""]
    out.append("Findings and recommendations: see docs/FINDINGS.md.")
    return "\n".join(out) + "\n"
