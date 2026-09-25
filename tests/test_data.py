"""Data integrity checks on the synthetic ticket set."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_ticket_count(conn):
    assert conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0] == 240


def test_timestamps_are_in_order(conn):
    bad = conn.execute("""
        SELECT COUNT(*) FROM tickets
        WHERE first_response_at < opened_at
           OR (resolved_at IS NOT NULL AND resolved_at < opened_at)
    """).fetchone()[0]
    assert bad == 0


def test_resolved_tickets_have_resolution_and_open_ones_do_not(conn):
    assert conn.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Resolved' AND "
                        "(resolved_at IS NULL OR resolution IS NULL)").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM tickets WHERE status <> 'Resolved' AND "
                        "resolved_at IS NOT NULL").fetchone()[0] == 0


def test_every_kb_reference_exists_as_a_file(conn):
    for kb_id, path in conn.execute("SELECT kb_id, path FROM kb_articles"):
        assert (ROOT / path).exists(), f"{kb_id} missing: {path}"
    orphans = conn.execute("SELECT COUNT(*) FROM tickets WHERE kb_article IS NOT NULL "
                           "AND kb_article NOT IN (SELECT kb_id FROM kb_articles)").fetchone()[0]
    assert orphans == 0


def test_p1_tickets_are_always_escalated(conn):
    assert conn.execute("SELECT COUNT(*) FROM tickets WHERE priority = 'P1' AND escalated = 0").fetchone()[0] == 0
