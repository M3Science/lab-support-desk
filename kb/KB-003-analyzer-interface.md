# KB-003: Analyzer results not crossing to the LIS

| Applies to | Typical priority | First owner | Escalate to |
|---|---|---|---|
| Core lab, microbiology, blood bank instruments | P2 (P1 if STAT testing is stopped) | Tier 2 | Tier 3 (interface team or instrument vendor) |

## Symptoms
- Results show as complete on the analyzer but not in the LIS.
- The instrument shows as offline or disconnected in the LIS.
- A queue of results is waiting to send.

## Before you start
- Tell the bench to start manual result entry or downtime procedures if STAT results are delayed (KB-008).
- Note the instrument name, time results stopped, and whether one or all instruments are affected.

## Steps
1. Confirm whether the problem is one instrument or several. Several = likely interface engine or network.
2. Check the instrument's host connection status and the middleware connection, if used.
3. Check the interface queue for a stuck or rejected message. A single bad message can block the queue.
4. Restart the instrument connection per the procedure and resend the held results.
5. Spot-check three resent results against the analyzer printout before closing.

## Escalate when
- The queue will not release or messages keep rejecting (Tier 3).
- Rejected messages show patient ID, accession or unit errors (Tier 3; see the lab-interface-triage runbook).
- No fix within 30 minutes on a P2, 15 minutes on a P1.

## Close the ticket with
Instrument, start/end time of the outage, root cause, number of results resent and verified.
