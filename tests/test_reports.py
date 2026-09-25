"""Every report query runs, returns data, and the outputs build."""

from support_desk.dashboard import build_html
from support_desk.reports import build_markdown


def test_all_reports_run_and_return_rows(reports):
    assert len(reports) == 9
    for r in reports.values():
        assert r.title and r.question, f"{r.key} is missing its title/question header"
        assert r.rows, f"{r.key} returned no rows"


def test_volume_adds_up(reports, k):
    assert sum(reports["01_volume_by_category"].column("tickets")) == k["tickets"]


def test_weekday_report_has_all_seven_days(reports):
    assert reports["06_lockouts_by_weekday"].column("weekday") == ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def test_outputs_render(reports, k):
    md = build_markdown(reports, k)
    html = build_html(reports, k)
    for r in reports.values():
        assert r.title in md
        assert r.title in html
    assert html.count("<svg") == 6
