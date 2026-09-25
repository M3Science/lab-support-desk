"""FINDINGS.md quotes numbers from the data. Fail if they drift apart."""

from pathlib import Path

FINDINGS = (Path(__file__).resolve().parent.parent / "docs" / "FINDINGS.md").read_text()


def row(report, key_col, key):
    i = report.columns.index(key_col)
    return dict(zip(report.columns, next(r for r in report.rows if r[i] == key)))


def test_headline_numbers(k):
    for value in (k["response_met_pct"], k["resolve_met_pct"], k["reopen_pct"]):
        assert f"{value}%" in FINDINGS


def test_interface_breach_and_escalation(reports):
    r = row(reports["03_breach_rate_by_category"], "category", "Analyzer Interface")
    assert f"{r['breach_pct']}%" in FINDINGS
    assert f"{r['escalated_pct']}%" in FINDINGS


def test_escalation_impact(reports):
    for path in ("Escalated to Tier 3", "Resolved at Tier 1-2"):
        r = row(reports["04_escalation_impact"], "path", path)
        assert f"{r['avg_hours']} h" in FINDINGS
        assert f"{r['resolve_met_pct']}%" in FINDINGS


def test_kb_reopen_rates(reports):
    for usage in ("KB article used", "No KB article"):
        r = row(reports["07_kb_reopen_rate"], "kb_usage", usage)
        assert f"{r['reopen_pct']}%" in FINDINGS
        assert f"{r['reopened']} of {r['resolved']}" in FINDINGS


def test_lockout_and_printer_counts(reports):
    lockouts = reports["06_lockouts_by_weekday"]
    mon = lockouts.column("lockouts")[0]
    assert f"{mon} of {sum(lockouts.column('lockouts'))}" in FINDINGS
    vol = row(reports["01_volume_by_category"], "category", "Label Printer")
    assert f"{vol['tickets']} tickets ({vol['pct_of_total']}%)" in FINDINGS
