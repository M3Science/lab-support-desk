# Triage and Escalation Matrix

Use this at intake to set priority, choose the first owner, and know the clock you are working against.

## Priority definitions and SLA targets

| Priority | Definition | Example | First response | Resolve |
|---|---|---|---|---|
| **P1** Critical | Lab or patient care stopped for many users | Unplanned LIS downtime; STAT results not crossing | 15 min | 4 h |
| **P2** High | A workflow or instrument is blocked | Analyzer interface down; QC hold on patient results; corrected report | 30 min | 8 h |
| **P3** Medium | One user affected, or a workaround exists | Label printer down at one station; account locked out | 4 h | 24 h |
| **P4** Low | Request or question | New security role; planned-downtime question | 8 h | 72 h |

SLA targets are measured in calendar hours in this project (see README limitations).

## Raise the priority when

- **Patient safety** is involved: a wrong-patient result, a critical value that cannot be delivered, or a mislabeled specimen. Treat it as P1 and bring in the supervisor.
- **Scope grows:** the same problem at more than one site or instrument. Raise it one level and look for a shared cause.
- **Timing matters:** STAT or ED testing is delayed. Raise it one level.

## Escalation tiers

| Tier | Who | Owns | Hand off with |
|---|---|---|---|
| 1 | Support desk / super users | Intake, password resets, printers, worklists, order lookups | What was tried, exact error text, time started, users affected |
| 2 | LIS analysts | Test build, security roles, printer mapping, QC lots, worklist filters, corrections | The Tier 1 notes plus configuration checked |
| 3 | Interface team / vendor | Interface engine, instrument connections, outages | Tier 2 findings, message IDs, instrument logs |

## Escalation timing

| Priority | Escalate to the next tier if not resolved within |
|---|---|
| P1 | 15 minutes, and notify lab leadership immediately |
| P2 | 30 minutes of hands-on work |
| P3 | 4 hours |
| P4 | 1 business day |

## Every ticket, before closing

1. Confirm the fix with the user. Don't close on "should be fixed."
2. Link the KB article that was used, or flag that one is missing.
3. Record the root cause, not just the symptom.
