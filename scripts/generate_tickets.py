"""Generate the synthetic ticket dataset in data/.

Everything is invented. There are no real people, systems, or organizations.
The generator is seeded, so it produces the same dataset every run.

The data contains a few deliberate patterns so the analysis has something
real to find (see README "About the data"):
  - label printer tickets are the largest category and cluster at ED and
    outpatient draw sites
  - account lockouts spike on Monday mornings
  - analyzer interface tickets escalate to Tier 3 often and breach SLA most
  - tickets closed without a knowledge base article are reopened more often

Run from the repo root:  python scripts/generate_tickets.py
"""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 42
N_TICKETS = 240
START = datetime(2026, 1, 5)   # a Monday
WEEKS = 12

SLA_POLICY = [  # priority, description, response_minutes, resolve_hours
    ("P1", "Critical: lab or patient care stopped", 15, 4),
    ("P2", "High: a workflow or instrument is blocked", 30, 8),
    ("P3", "Medium: single user or workaround available", 240, 24),
    ("P4", "Low: request or question", 480, 72),
]

KB_ARTICLES = [
    ("KB-001", "Specimen label printer not printing or printing blank", "kb/KB-001-label-printer.md"),
    ("KB-002", "Account locked out or password expired", "kb/KB-002-account-lockout.md"),
    ("KB-003", "Analyzer results not crossing to the LIS", "kb/KB-003-analyzer-interface.md"),
    ("KB-004", "Order not found when receiving a specimen", "kb/KB-004-order-not-found.md"),
    ("KB-005", "Correcting a released result", "kb/KB-005-result-correction.md"),
    ("KB-006", "Worklist or pending list not refreshing", "kb/KB-006-worklist-refresh.md"),
    ("KB-007", "QC failure blocking patient results", "kb/KB-007-qc-lockout.md"),
    ("KB-008", "LIS downtime: what to do", "kb/KB-008-downtime.md"),
    ("KB-009", "Requesting new user access or a security role", "kb/KB-009-access-request.md"),
]

# category: (weight, kb, [(subcategory, priority, base_tier, resolution), ...])
CATEGORIES = {
    "Label Printer": (26, "KB-001", [
        ("Printer not printing", "P3", 1, "Cleared jam and restarted printer"),
        ("Labels blank or faded", "P3", 1, "Replaced ribbon and label stock"),
        ("Wrong default printer", "P3", 1, "Reassigned workstation default printer"),
    ]),
    "LIS Access": (20, "KB-002", [
        ("Account locked out", "P3", 1, "Unlocked account and verified login"),
        ("Password expired", "P3", 1, "Reset password and verified login"),
        ("Missing security role", "P4", 2, "Added security role after manager approval"),
    ]),
    "Analyzer Interface": (15, "KB-003", [
        ("Results not crossing to LIS", "P2", 2, "Restarted interface connection and resent results"),
        ("Interface queue backed up", "P2", 2, "Cleared stuck message and released queue"),
        ("Instrument offline in LIS", "P2", 2, "Re-established instrument connection"),
    ]),
    "Order / Accession": (12, "KB-004", [
        ("Order not found for specimen", "P3", 1, "Located order and relinked specimen"),
        ("Duplicate order", "P3", 1, "Cancelled duplicate with provider approval"),
        ("Order cancelled after collection", "P3", 2, "Reinstated order and notified provider"),
    ]),
    "QC Lockout": (9, "KB-007", [
        ("QC failure blocking results", "P2", 2, "Reviewed QC, recalibrated, released hold"),
        ("New QC lot not built", "P2", 2, "Built QC lot and ranges in LIS"),
    ]),
    "Result Correction": (8, "KB-005", [
        ("Result filed to wrong test", "P2", 2, "Issued corrected report and notified provider"),
        ("Corrected report needed", "P2", 2, "Issued corrected report and notified provider"),
    ]),
    "Worklist": (7, "KB-006", [
        ("Worklist not refreshing", "P3", 1, "Refreshed session and cleared cache"),
        ("Pending list missing specimens", "P3", 2, "Corrected worklist filter build"),
    ]),
    "Downtime": (3, "KB-008", [
        ("Unplanned LIS downtime", "P1", 3, "Vendor restored service; downtime results backloaded"),
        ("Planned downtime question", "P4", 1, "Sent downtime schedule and procedure"),
    ]),
}

LOCATIONS = ["Core Lab", "Microbiology", "Blood Bank", "Emergency Dept", "ICU", "Outpatient Draw"]
ROLES = ["Bench tech", "Phlebotomist", "Nurse", "Provider", "Lab supervisor"]


def pick_opened(rng: random.Random, category: str, subcategory: str) -> datetime:
    day = rng.randrange(WEEKS * 7)
    # Pattern: lockouts spike on Monday mornings after the weekend
    if subcategory == "Account locked out" and rng.random() < 0.55:
        day = rng.randrange(WEEKS) * 7          # a Monday
        hour = rng.choice([6, 7, 7, 8, 8, 9])
    else:
        hour = rng.choices(range(24), weights=[1] * 6 + [4] * 12 + [2] * 6)[0]
    return START + timedelta(days=day, hours=hour, minutes=rng.randrange(60))


def pick_location(rng: random.Random, category: str) -> str:
    if category == "Label Printer":  # Pattern: printers at high-volume collection sites
        return rng.choices(LOCATIONS, weights=[2, 1, 1, 5, 2, 5])[0]
    if category in ("Analyzer Interface", "QC Lockout"):
        return rng.choices(LOCATIONS, weights=[6, 2, 2, 0, 0, 0])[0]
    return rng.choice(LOCATIONS)


def main() -> None:
    rng = random.Random(SEED)
    policy = {p: (resp, res) for p, _, resp, res in SLA_POLICY}
    cats = list(CATEGORIES)
    weights = [CATEGORIES[c][0] for c in cats]

    rows = []
    for _ in range(N_TICKETS):
        category = rng.choices(cats, weights=weights)[0]
        _, kb, subs = CATEGORIES[category]
        if category == "LIS Access":
            subcategory, priority, tier, resolution = rng.choices(subs, weights=[5, 3, 2])[0]
        else:
            subcategory, priority, tier, resolution = rng.choice(subs)
        if category == "LIS Access" and subcategory == "Missing security role":
            kb = "KB-009"
        opened = pick_opened(rng, category, subcategory)
        location = pick_location(rng, category)
        role = rng.choice(ROLES)

        resp_target, res_target = policy[priority]
        # Most first responses land inside target; about 10% run late
        resp_min = rng.uniform(0.2, 0.9) * resp_target if rng.random() > 0.10 else rng.uniform(1.1, 2.5) * resp_target

        # Resolution time as a share of the target; escalations add time
        res_hours = rng.uniform(0.15, 0.85) * res_target
        escalated = 0
        if category == "Analyzer Interface" and rng.random() < 0.45:
            escalated, tier = 1, 3        # Pattern: vendor/interface team escalations
            res_hours += rng.uniform(4, 20)
        elif tier == 2 and rng.random() < 0.10:
            escalated, tier = 1, 3
            res_hours += rng.uniform(2, 12)
        elif rng.random() < 0.06:
            res_hours = rng.uniform(1.05, 2.0) * res_target   # ordinary late ticket
        if priority == "P1":
            escalated = 1
        # Tickets opened in the final days are more likely to still be in progress
        if opened > START + timedelta(weeks=WEEKS, days=-4) and rng.random() < 0.5:
            res_hours += rng.uniform(72, 120)

        # Pattern: tickets without a KB article get reopened more often
        kb_used = kb if rng.random() < 0.70 else ""
        reopened = int(rng.random() < (0.05 if kb_used else 0.22))
        if reopened:
            res_hours += rng.uniform(2, 24)

        rows.append({
            "opened_at": opened,
            "priority": priority,
            "category": category,
            "subcategory": subcategory,
            "location": location,
            "requester_role": role,
            "assigned_tier": tier,
            "escalated": escalated,
            "kb_article": kb_used,
            "reopened": reopened,
            "first_response_at": opened + timedelta(minutes=resp_min),
            "resolved_at": opened + timedelta(hours=res_hours),
            "resolution": resolution,
        })

    rows.sort(key=lambda r: r["opened_at"])
    period_end = START + timedelta(weeks=WEEKS)
    fmt = "%Y-%m-%d %H:%M"

    with open(DATA / "tickets.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ticket_id", "opened_at", "priority", "category", "subcategory", "location",
                    "requester_role", "assigned_tier", "escalated", "first_response_at",
                    "resolved_at", "status", "kb_article", "reopened", "resolution"])
        for i, r in enumerate(rows, start=1):
            # Tickets whose resolution falls after the reporting period are still open
            still_open = r["resolved_at"] > period_end
            status = rng.choice(["Open", "In Progress"]) if still_open else "Resolved"
            w.writerow([
                f"INC{100000 + i}", r["opened_at"].strftime(fmt), r["priority"], r["category"],
                r["subcategory"], r["location"], r["requester_role"], r["assigned_tier"],
                r["escalated"], r["first_response_at"].strftime(fmt),
                "" if still_open else r["resolved_at"].strftime(fmt), status,
                "" if still_open else r["kb_article"], 0 if still_open else r["reopened"],
                "" if still_open else r["resolution"],
            ])

    with open(DATA / "sla_policy.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["priority", "description", "response_minutes", "resolve_hours"])
        w.writerows(SLA_POLICY)

    with open(DATA / "kb_articles.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["kb_id", "title", "path"])
        w.writerows(KB_ARTICLES)

    print(f"Wrote {len(rows)} tickets to {DATA / 'tickets.csv'}")


if __name__ == "__main__":
    main()
