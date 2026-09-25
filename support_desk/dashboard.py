"""Render a self-contained HTML dashboard (no external libraries).

Every chart is a single series in one hue, with direct value labels, a hover
tooltip, and a data table underneath, so nothing depends on color alone.
"""

from __future__ import annotations

from html import escape

from .reports import Report

CSS = """
.viz-root {
  color-scheme: light;
  --surface-0: #f4f4f2; --surface-1: #fcfcfb; --border: #e2e1dc;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #6f6e69;
  --series-1: #2a78d6; --grid: #e7e6e1;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .viz-root {
    color-scheme: dark;
    --surface-0: #111110; --surface-1: #1a1a19; --border: #2e2e2c;
    --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #9a998f;
    --series-1: #3987e5; --grid: #2a2a28;
  }
}
:root[data-theme="dark"] .viz-root {
  color-scheme: dark;
  --surface-0: #111110; --surface-1: #1a1a19; --border: #2e2e2c;
  --text-primary: #ffffff; --text-secondary: #c3c2b7; --text-muted: #9a998f;
  --series-1: #3987e5; --grid: #2a2a28;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--surface-0); }
.viz-root { background: var(--surface-0); color: var(--text-primary);
  font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  max-width: 1120px; margin: 0 auto; padding: 32px 16px 48px; }
h1 { font-size: 24px; margin: 0 0 4px; letter-spacing: -0.01em; }
.sub { color: var(--text-secondary); margin: 0 0 24px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 24px; }
.tile { background: var(--surface-1); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
.tile .label { color: var(--text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }
.tile .value { font-size: 28px; font-weight: 600; margin-top: 4px; font-variant-numeric: tabular-nums; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 500px), 1fr)); gap: 16px; }
.card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 10px; padding: 16px; min-width: 0; }
.card h2 { font-size: 15px; margin: 0 0 2px; }
.card .q { color: var(--text-secondary); font-size: 13px; margin: 0 0 12px; }
svg { display: block; width: 100%; height: auto; overflow: visible; }
.chart { overflow-x: auto; }
svg text { font-family: inherit; }
.axis-label { fill: var(--text-secondary); font-size: 12px; }
.value-label { fill: var(--text-primary); font-size: 12px; font-variant-numeric: tabular-nums; }
.gridline { stroke: var(--grid); stroke-width: 1; }
.bar { fill: var(--series-1); transition: opacity 120ms; }
.hit:hover .bar { opacity: 0.75; }
.hit rect.target { fill: transparent; }
details { margin-top: 10px; }
summary { cursor: pointer; color: var(--text-secondary); font-size: 12px; }
table { border-collapse: collapse; width: 100%; font-size: 12.5px; margin-top: 8px; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); }
th { color: var(--text-secondary); font-weight: 600; }
.wide { grid-column: 1 / -1; }
.table-wrap { overflow-x: auto; }
footer { color: var(--text-muted); font-size: 12px; margin-top: 24px; }
"""


def _table(r: Report) -> str:
    head = "".join(f"<th>{escape(c)}</th>" for c in r.columns)
    rows = "".join(
        "<tr>" + "".join(f"<td>{escape('' if v is None else str(v))}</td>" for v in row) + "</tr>"
        for row in r.rows
    )
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


def _bar_path(x: float, y: float, w: float, h: float, horizontal: bool, r: float = 4) -> str:
    """Bar with a 4px rounded data end; the baseline end stays square."""
    if horizontal:
        r = min(r, w / 2, h / 2)
        return (f"M{x},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} "
                f"V{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} H{x} Z")
    r = min(r, w / 2, h / 2)
    return (f"M{x},{y + h} V{y + r} Q{x},{y} {x + r},{y} "
            f"H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h} Z")


def hbar(r: Report, label_col: str, value_col: str, unit: str = "", max_value: float | None = None) -> str:
    labels, values = r.column(label_col), r.column(value_col)
    row_h, bar_h, left, width = 28, 16, 124, 400
    plot_w = width - left - 56
    top = max_value or max(values) or 1
    height = row_h * len(values) + 8
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(r.title)}">']
    for i, (lab, val) in enumerate(zip(labels, values)):
        y = i * row_h + 4
        w = max(plot_w * val / top, 1)
        tip = f"{lab}: {val}{unit}"
        parts.append(
            f'<g class="hit"><title>{escape(tip)}</title>'
            f'<rect class="target" x="0" y="{y}" width="{width}" height="{row_h}"/>'
            f'<text class="axis-label" x="{left - 10}" y="{y + bar_h / 2 + 4}" text-anchor="end">{escape(str(lab))}</text>'
            f'<path class="bar" d="{_bar_path(left, y, w, bar_h, True)}"/>'
            f'<text class="value-label" x="{left + w + 6}" y="{y + bar_h / 2 + 4}">{val}{unit}</text></g>'
        )
    parts.append("</svg>")
    return "".join(parts)


def vbar(r: Report, label_col: str, value_col: str) -> str:
    labels, values = r.column(label_col), r.column(value_col)
    width, height, bottom, top_pad = 400, 190, 24, 20
    plot_h = height - bottom - top_pad
    slot = width / len(values)
    bar_w = min(44, slot * 0.6)
    top = max(values) or 1
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{escape(r.title)}">',
             f'<line class="gridline" x1="0" x2="{width}" y1="{height - bottom}" y2="{height - bottom}"/>']
    for i, (lab, val) in enumerate(zip(labels, values)):
        h = plot_h * val / top
        x = i * slot + (slot - bar_w) / 2
        y = height - bottom - h
        bar = f'<path class="bar" d="{_bar_path(x, y, bar_w, h, False)}"/>' if val else ""
        parts.append(
            f'<g class="hit"><title>{escape(f"{lab}: {val}")}</title>'
            f'<rect class="target" x="{i * slot}" y="0" width="{slot}" height="{height}"/>{bar}'
            f'<text class="value-label" x="{x + bar_w / 2}" y="{y - 6}" text-anchor="middle">{val}</text>'
            f'<text class="axis-label" x="{x + bar_w / 2}" y="{height - 6}" text-anchor="middle">{escape(str(lab))}</text></g>'
        )
    parts.append("</svg>")
    return "".join(parts)


def card(r: Report, chart: str = "", wide: bool = False, table_open: bool = False) -> str:
    table = _table(r)
    chart = f'<div class="chart">{chart}</div>' if chart else ""
    body = (f"{chart}<details><summary>Show data table</summary>{table}</details>"
            if chart else table)
    if table_open and chart:
        body = chart + table
    cls = "card wide" if wide else "card"
    return (f'<section class="{cls}"><h2>{escape(r.title)}</h2>'
            f'<p class="q">{escape(r.question)}</p>{body}</section>')


def build_html(reports: dict[str, Report], k: dict[str, float]) -> str:
    R = reports
    tiles = [
        ("Tickets", k["tickets"]),
        ("Response in SLA", f"{k['response_met_pct']}%"),
        ("Resolved in SLA", f"{k['resolve_met_pct']}%"),
        ("Reopen rate", f"{k['reopen_pct']}%"),
        ("Open at period end", k["open"]),
    ]
    tile_html = "".join(
        f'<div class="tile"><div class="label">{escape(t)}</div><div class="value">{v}</div></div>'
        for t, v in tiles)
    cards = [
        card(R["01_volume_by_category"], hbar(R["01_volume_by_category"], "category", "tickets")),
        card(R["03_breach_rate_by_category"],
             hbar(R["03_breach_rate_by_category"], "category", "breach_pct", "%", 100)),
        card(R["02_sla_by_priority"], wide=True),
        card(R["04_escalation_impact"], hbar(R["04_escalation_impact"], "path", "avg_hours", " h")),
        card(R["07_kb_reopen_rate"], hbar(R["07_kb_reopen_rate"], "kb_usage", "reopen_pct", "%")),
        card(R["06_lockouts_by_weekday"], vbar(R["06_lockouts_by_weekday"], "weekday", "lockouts")),
        card(R["08_label_printer_hotspots"], hbar(R["08_label_printer_hotspots"], "location", "tickets")),
        card(R["05_top_recurring_issues"], wide=True),
        card(R["09_open_backlog"], wide=True),
    ]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lab Support Desk Dashboard</title>
<style>{CSS}</style>
</head>
<body>
<main class="viz-root">
<h1>Lab Application Support Desk</h1>
<p class="sub">12 weeks of synthetic lab support tickets, 2026-01-05 to 2026-03-29. Hover a bar for its value; open a table for the numbers.</p>
<div class="tiles">{tile_html}</div>
<div class="grid">{''.join(cards)}</div>
<footer>All data is synthetic. Built with Python and SQLite; every figure comes from a query in the sql/ folder.</footer>
</main>
</body>
</html>
"""
