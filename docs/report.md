# Lab Application Support Desk Report

Reporting period: 2026-01-05 to 2026-03-29 (12 weeks, synthetic data).

| Measure | Value |
|---|---|
| Tickets | 240 |
| First response within SLA | 87.5% |
| Resolved within SLA | 81.8% |
| Reopen rate | 7.6% |
| Open at end of period | 4 |

## Ticket volume by category

*Where does the support workload come from?*

| category | tickets | pct_of_total |
|---|---|---|
| Label Printer | 68 | 28.3 |
| Analyzer Interface | 42 | 17.5 |
| LIS Access | 37 | 15.4 |
| Order / Accession | 33 | 13.8 |
| QC Lockout | 20 | 8.3 |
| Result Correction | 14 | 5.8 |
| Worklist | 14 | 5.8 |
| Downtime | 12 | 5.0 |

Query: `sql/01_volume_by_category.sql`

## SLA compliance by priority

*Are we meeting response and resolution targets?*

| priority | tickets | response_target_min | response_met_pct | resolve_target_hrs | resolve_met_pct |
|---|---|---|---|---|---|
| P1 | 7 | 15 | 85.7 | 4 | 85.7 |
| P2 | 76 | 30 | 90.8 | 8 | 63.2 |
| P3 | 147 | 240 | 85.0 | 24 | 90.2 |
| P4 | 10 | 480 | 100.0 | 72 | 100.0 |

Query: `sql/02_sla_by_priority.sql`

## Resolution SLA breach rate by category

*Which kinds of problems miss their targets most often?*

| category | resolved | breached | breach_pct | escalated_pct |
|---|---|---|---|---|
| Analyzer Interface | 42 | 25 | 59.5 | 57.1 |
| Worklist | 13 | 2 | 15.4 | 0.0 |
| Result Correction | 14 | 2 | 14.3 | 14.3 |
| Label Printer | 67 | 7 | 10.4 | 0.0 |
| Order / Accession | 31 | 3 | 9.7 | 3.2 |
| Downtime | 12 | 1 | 8.3 | 58.3 |
| LIS Access | 37 | 2 | 5.4 | 0.0 |
| QC Lockout | 20 | 1 | 5.0 | 5.0 |

Query: `sql/03_breach_rate_by_category.sql`

## Escalation impact on P2 tickets

*How much time does an escalation add to a high-priority ticket?*

| path | resolved | avg_hours | resolve_met_pct |
|---|---|---|---|
| Resolved at Tier 1-2 | 49 | 5.5 | 91.8 |
| Escalated to Tier 3 | 27 | 16.5 | 11.1 |

Query: `sql/04_escalation_impact.sql`

## Top recurring issues

*Which specific problems keep coming back?*

| issue | category | tickets | avg_resolve_hours |
|---|---|---|---|
| Wrong default printer | Label Printer | 30 | 14.6 |
| Labels blank or faded | Label Printer | 26 | 15.0 |
| Account locked out | LIS Access | 17 | 11.6 |
| Duplicate order | Order / Accession | 16 | 13.5 |
| Results not crossing to LIS | Analyzer Interface | 16 | 16.1 |
| Interface queue backed up | Analyzer Interface | 15 | 10.1 |
| Password expired | LIS Access | 15 | 14.8 |
| Printer not printing | Label Printer | 12 | 16.1 |

Query: `sql/05_top_recurring_issues.sql`

## Account lockouts by weekday

*When do lockouts happen, and could self-service reset help?*

| weekday | lockouts |
|---|---|
| Mon | 14 |
| Tue | 1 |
| Wed | 0 |
| Thu | 1 |
| Fri | 1 |
| Sat | 0 |
| Sun | 0 |

Query: `sql/06_lockouts_by_weekday.sql`

## Reopen rate with and without a KB article

*Do knowledge base articles make fixes stick?*

| kb_usage | resolved | reopened | reopen_pct |
|---|---|---|---|
| KB article used | 169 | 6 | 3.6 |
| No KB article | 67 | 12 | 17.9 |

Query: `sql/07_kb_reopen_rate.sql`

## Label printer tickets by location

*Where should preventive printer maintenance start?*

| location | tickets |
|---|---|
| Outpatient Draw | 20 |
| Emergency Dept | 17 |
| Core Lab | 15 |
| Blood Bank | 9 |
| ICU | 7 |

Query: `sql/08_label_printer_hotspots.sql`

## Open backlog at end of period

*What is still open, and how old is it?*

| ticket_id | priority | category | subcategory | status | tier | age_hours |
|---|---|---|---|---|---|---|
| INC100234 | P3 | Order / Accession | Order not found for specimen | In Progress | 1 | 55.7 |
| INC100235 | P3 | Label Printer | Wrong default printer | Open | 1 | 45.2 |
| INC100239 | P3 | Order / Accession | Order cancelled after collection | In Progress | 2 | 10.3 |
| INC100240 | P3 | Worklist | Worklist not refreshing | Open | 1 | 4.9 |

Query: `sql/09_open_backlog.sql`

Findings and recommendations: see docs/FINDINGS.md.
