"""Write the knowledge base articles in kb/ (run from the repo root).

Articles are vendor-neutral: they describe the workflow a lab support desk
follows, not the menus of any specific LIS product.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """# {id}: {title}

| Applies to | Typical priority | First owner | Escalate to |
|---|---|---|---|
| {applies} | {priority} | {owner} | {escalate_to} |

## Symptoms
{symptoms}

## Before you start
{before}

## Steps
{steps}

## Escalate when
{escalate}

## Close the ticket with
{close}
"""

ARTICLES = [
    dict(
        id="KB-001", file="KB-001-label-printer.md",
        title="Specimen label printer not printing or printing blank",
        applies="Collection sites, lab receiving", priority="P3 (P2 if a whole site cannot label)",
        owner="Tier 1", escalate_to="Tier 2 (printer mapping), facilities/IT (hardware)",
        symptoms="- Labels do not print after the order is released.\n"
                 "- Labels print blank, faded, or with missing barcode lines.\n"
                 "- Labels print at a different workstation's printer.",
        before="- Ask which workstation and printer name the user is on.\n"
               "- Ask whether other users at the same site are affected (site-wide = raise priority).\n"
               "- Remind the user to use downtime labels if patients are waiting (KB-008).",
        steps="1. Check the printer for a paper jam, open lid, or error light. Clear it and power-cycle.\n"
              "2. If labels are blank or faded, replace the ribbon and label stock; confirm the stock type matches the printer.\n"
              "3. Print a test label. Scan the barcode with a handheld scanner to confirm it reads.\n"
              "4. If labels print elsewhere, check the workstation's default label printer mapping and correct it.\n"
              "5. Reprint the affected labels and confirm with the user before closing.",
        escalate="- The printer is mapped correctly but still receives nothing (Tier 2: print queue or device mapping).\n"
                 "- Barcodes print but will not scan (Tier 2: label format).\n"
                 "- Hardware fault after ribbon and stock replacement (facilities/IT).",
        close="Printer name, root cause (jam / ribbon / stock / mapping / hardware), labels reprinted Y/N.",
    ),
    dict(
        id="KB-002", file="KB-002-account-lockout.md",
        title="Account locked out or password expired",
        applies="All LIS users", priority="P3 (P2 if the user is the only tech on a bench)",
        owner="Tier 1", escalate_to="Tier 2 (security role problems)",
        symptoms="- \"Account locked\" or \"password expired\" at login.\n"
                 "- User can log in to the workstation but not to the LIS.",
        before="- Verify identity per the identity-verification policy before any reset. Never reset for a caller you cannot verify.\n"
               "- Never ask for, write down, or share the user's password.",
        steps="1. Confirm the username and verify identity.\n"
              "2. Unlock the account or issue a temporary password per the reset procedure.\n"
              "3. Stay on the line while the user logs in and sets a new password.\n"
              "4. If lockouts repeat, ask whether a saved password on another device is retrying the old one.",
        escalate="- The user logs in but is missing menus or functions (security role, see KB-009).\n"
                 "- Several users are locked out at once (possible directory or authentication outage: raise to P1/P2).",
        close="Username, lockout vs expired, verified login Y/N. Do not record passwords.",
    ),
    dict(
        id="KB-003", file="KB-003-analyzer-interface.md",
        title="Analyzer results not crossing to the LIS",
        applies="Core lab, microbiology, blood bank instruments", priority="P2 (P1 if STAT testing is stopped)",
        owner="Tier 2", escalate_to="Tier 3 (interface team or instrument vendor)",
        symptoms="- Results show as complete on the analyzer but not in the LIS.\n"
                 "- The instrument shows as offline or disconnected in the LIS.\n"
                 "- A queue of results is waiting to send.",
        before="- Tell the bench to start manual result entry or downtime procedures if STAT results are delayed (KB-008).\n"
               "- Note the instrument name, time results stopped, and whether one or all instruments are affected.",
        steps="1. Confirm whether the problem is one instrument or several. Several = likely interface engine or network.\n"
              "2. Check the instrument's host connection status and the middleware connection, if used.\n"
              "3. Check the interface queue for a stuck or rejected message. A single bad message can block the queue.\n"
              "4. Restart the instrument connection per the procedure and resend the held results.\n"
              "5. Spot-check three resent results against the analyzer printout before closing.",
        escalate="- The queue will not release or messages keep rejecting (Tier 3).\n"
                 "- Rejected messages show patient ID, accession or unit errors (Tier 3; see the lab-interface-triage runbook).\n"
                 "- No fix within 30 minutes on a P2, 15 minutes on a P1.",
        close="Instrument, start/end time of the outage, root cause, number of results resent and verified.",
    ),
    dict(
        id="KB-004", file="KB-004-order-not-found.md",
        title="Order not found when receiving a specimen",
        applies="Lab receiving, collection sites", priority="P3",
        owner="Tier 1", escalate_to="Tier 2 (order interface), provider (order entry)",
        symptoms="- Scanning the specimen label returns \"order not found\".\n"
                 "- The order exists but was cancelled or is on a different encounter.",
        before="- Do not create a new order without a provider order. Do not relabel a specimen.\n"
               "- Hold the specimen under proper storage conditions while you investigate.",
        steps="1. Search by patient and collection date rather than by accession.\n"
              "2. If the order was cancelled after collection, contact the ordering provider to reinstate or reorder.\n"
              "3. If a duplicate order exists, confirm with the provider which one to cancel.\n"
              "4. Link the specimen to the correct active order and document the change.",
        escalate="- Orders placed in the EHR are not reaching the LIS at all (Tier 2: order interface).\n"
                 "- Patient identity on the specimen does not match the order (follow the misidentification policy).",
        close="Accession, what was wrong (cancelled / duplicate / wrong encounter / not received), who approved the fix.",
    ),
    dict(
        id="KB-005", file="KB-005-result-correction.md",
        title="Correcting a released result",
        applies="All lab sections", priority="P2",
        owner="Tier 2 with the lab supervisor", escalate_to="Lab leadership per the corrected-report policy",
        symptoms="- A released result is wrong (wrong value, wrong test, or wrong patient).",
        before="- A released result may already have been acted on. Speed and documentation both matter.\n"
               "- Wrong-patient results follow the misidentification policy first.",
        steps="1. Confirm the correct value from the instrument record or the repeat test.\n"
              "2. Issue a corrected report through the correction workflow, never by overwriting.\n"
              "3. Notify the ordering provider and document name, date, time and read-back.\n"
              "4. Make sure the corrected result reached the EHR with a corrected status.",
        escalate="- The correction workflow is blocked or the corrected status does not reach the EHR (Tier 2/3).",
        close="Accession, original vs corrected value, provider notified (name/time), corrected status confirmed in EHR.",
    ),
    dict(
        id="KB-006", file="KB-006-worklist-refresh.md",
        title="Worklist or pending list not refreshing",
        applies="Bench techs", priority="P3",
        owner="Tier 1", escalate_to="Tier 2 (worklist filter build)",
        symptoms="- Received specimens do not appear on the bench worklist.\n"
                 "- The pending list shows stale specimens that are already resulted.",
        before="- Ask whether one workstation or all workstations are affected.",
        steps="1. Refresh the worklist and confirm the filter (section, date range, priority) is correct.\n"
              "2. Log out and back in to reset the session.\n"
              "3. Check another workstation. If it works there, clear the local cache per the procedure.\n"
              "4. Receive a test specimen and confirm it appears.",
        escalate="- The same specimens are missing on every workstation (Tier 2: filter or routing build).",
        close="Workstation, filter used, fix applied, test specimen confirmed Y/N.",
    ),
    dict(
        id="KB-007", file="KB-007-qc-lockout.md",
        title="QC failure blocking patient results",
        applies="Core lab and other QC-controlled benches", priority="P2",
        owner="Tier 2 with the bench lead", escalate_to="Lab supervisor, instrument vendor",
        symptoms="- Patient results are held because QC failed or is missing.\n"
                 "- A new QC lot will not accept results.",
        before="- Patient results must not be released around a QC hold. Support restores the workflow; the bench decides on QC acceptability.",
        steps="1. Confirm which rule failed and on which level/lot.\n"
              "2. For a failure: the bench troubleshoots (reagent, calibration, rerun) per the QC procedure.\n"
              "3. For a new lot: confirm the lot and its ranges are built in the LIS; build them if missing and approved.\n"
              "4. Once QC passes, confirm the hold releases and patient results can be verified.",
        escalate="- QC passes on the instrument but the LIS still holds results (Tier 2/3).\n"
                 "- Repeated failures after troubleshooting (vendor).",
        close="Instrument, lot, rule failed or build missing, action taken, time hold released.",
    ),
    dict(
        id="KB-008", file="KB-008-downtime.md",
        title="LIS downtime: what to do",
        applies="Whole laboratory", priority="P1 (unplanned) / P4 (planned-downtime questions)",
        owner="Tier 1 declares, Tier 3 restores", escalate_to="Tier 3 and lab leadership immediately",
        symptoms="- The LIS is unavailable for multiple users or sites.",
        before="- Confirm it is more than one user and more than one workstation.",
        steps="1. Declare downtime per policy and notify lab leadership and the service desk.\n"
              "2. The lab switches to downtime procedures: downtime labels, paper requisitions, manual result reporting by phone for STAT and critical values.\n"
              "3. Post updates on a fixed schedule (for example every 30 minutes) until service is restored.\n"
              "4. After recovery, backload downtime orders and results, and verify a sample against paper records.",
        escalate="- Immediately. Unplanned downtime is always P1.",
        close="Start/end time, cause, number of downtime results backloaded, reconciliation complete Y/N.",
    ),
    dict(
        id="KB-009", file="KB-009-access-request.md",
        title="Requesting new user access or a security role",
        applies="New hires, role changes", priority="P4 (P3 if the user is scheduled on a bench today)",
        owner="Tier 1 intake, Tier 2 builds", escalate_to="Tier 2",
        symptoms="- A new user cannot log in.\n- An existing user is missing a function they need.",
        before="- Access requires manager approval and completed training. Do not grant access without both.",
        steps="1. Collect the user's name, department, role, and start date.\n"
              "2. Attach manager approval and the training record.\n"
              "3. Route to Tier 2 to create the account or assign the role that matches the job, and nothing broader.\n"
              "4. Confirm with the user that they can reach the needed functions.",
        escalate="- Always routes to Tier 2 for the build step.",
        close="User, role granted, approval reference, access confirmed Y/N.",
    ),
]


def main() -> None:
    (ROOT / "kb").mkdir(exist_ok=True)
    for a in ARTICLES:
        (ROOT / "kb" / a["file"]).write_text(TEMPLATE.format(**a), encoding="utf-8")
    print(f"Wrote {len(ARTICLES)} KB articles")


if __name__ == "__main__":
    main()
