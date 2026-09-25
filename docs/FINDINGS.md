# Findings and Recommendations

**Period:** 12 weeks, 240 tickets (synthetic data).
Every number below comes from a query in `sql/`. The test suite checks
that these figures still match the data (`tests/test_findings.py`).

> The dataset was generated with a few deliberate patterns (see README,
> "About the data"). This write-up shows how I would find, size and act on
> patterns like these in a real support queue.

## Summary

| Measure | Result |
|---|---|
| First response within SLA | 87.5% |
| Resolved within SLA | 81.8% |
| Reopen rate | 7.6% |
| Open at end of period | 4 |

The desk mostly meets its targets. The misses cluster in one place:
**P2 tickets resolve within SLA only 63.2% of the time**, compared with 90.2% for P3.

## 1. Analyzer interface tickets drive most SLA misses

- Analyzer Interface has the highest resolution breach rate: **59.5%**, against 15.4% or less for every other category.
- **57.1%** of these tickets escalate to Tier 3.
- Among P2 tickets, the escalated ones average **16.5 h** to resolve and meet SLA **11.1%** of the time. Those handled at Tier 1-2 average **5.5 h** and meet SLA **91.8%** of the time.

**Recommendations**
- Give Tier 2 a documented first-hour checklist for interface issues (KB-003), so fewer tickets need Tier 3.
- Agree on an interface-team response target that fits inside the 8-hour P2 window, and track it separately.
- Add queue-depth alerting so a stuck interface is caught before the bench calls.

## 2. Label printers are the largest source of volume

- Label Printer is the top category: **68 tickets (28.3%)**.
- **"Wrong default printer"** is the single most common issue (30 tickets). That is a configuration problem, not a hardware one.
- **54%** of printer tickets (37 of 68) come from **Outpatient Draw and the Emergency Dept**.

**Recommendations**
- Audit workstation-to-printer mappings at those two sites first.
- Schedule preventive maintenance (ribbon and stock checks) at high-volume collection sites.
- Publish KB-001 as a one-page guide posted at each printer.

## 3. Account lockouts cluster on Mondays

- **14 of 17** lockouts (82%) were opened on a Monday, mostly between 06:00 and 10:00.

**Recommendations**
- Offer self-service password reset, which would remove most of these tickets.
- Send a Friday reminder before password-expiry dates.
- Staff Tier 1 for the Monday-morning peak.

## 4. Knowledge base articles make fixes stick

- Tickets resolved **with a KB article** were reopened **3.6%** of the time (6 of 169).
- Tickets resolved **without one** were reopened **17.9%** of the time (12 of 67), about five times as often.

**Recommendations**
- Require a KB link, or a "no article exists" flag, at closure.
- Review "no article" tickets monthly to decide which new articles to write.

## What I would measure next

- SLA in business hours instead of calendar hours.
- First-contact resolution rate at Tier 1.
- Time spent waiting on the user versus time spent on the ticket.
- Whether the recommended changes lower printer and lockout volume over the next quarter.
