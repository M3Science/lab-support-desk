"""The SLA view must classify boundary cases correctly."""

import sqlite3
from pathlib import Path

import pytest

SCHEMA = (Path(__file__).resolve().parent.parent / "sql" / "schema.sql").read_text()


@pytest.fixture
def db():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    c.execute("INSERT INTO sla_policy VALUES ('P2', 'High', 30, 8)")
    return c


def add(db, tid, opened, responded, resolved, status="Resolved"):
    db.execute("""INSERT INTO tickets (ticket_id, opened_at, priority, category, subcategory, location,
                  requester_role, assigned_tier, escalated, first_response_at, resolved_at, status, reopened)
                  VALUES (?, ?, 'P2', 'c', 's', 'l', 'r', 2, 0, ?, ?, ?, 0)""",
               (tid, opened, responded, resolved, status))


def sla(db, tid):
    return db.execute("SELECT response_met, resolve_met FROM ticket_sla WHERE ticket_id = ?", (tid,)).fetchone()


def test_exactly_on_target_counts_as_met(db):
    add(db, "A", "2026-01-05 08:00", "2026-01-05 08:30", "2026-01-05 16:00")
    assert sla(db, "A") == (1, 1)


def test_one_minute_late_is_a_breach(db):
    add(db, "B", "2026-01-05 08:00", "2026-01-05 08:31", "2026-01-05 16:01")
    assert sla(db, "B") == (0, 0)


def test_open_ticket_has_no_resolve_result(db):
    add(db, "C", "2026-01-05 08:00", "2026-01-05 08:10", None, status="Open")
    assert sla(db, "C") == (1, None)


def test_overnight_ticket(db):
    add(db, "D", "2026-01-05 22:00", "2026-01-05 22:20", "2026-01-06 05:59")
    assert sla(db, "D") == (1, 1)
