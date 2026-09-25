# KB-007: QC failure blocking patient results

| Applies to | Typical priority | First owner | Escalate to |
|---|---|---|---|
| Core lab and other QC-controlled benches | P2 | Tier 2 with the bench lead | Lab supervisor, instrument vendor |

## Symptoms
- Patient results are held because QC failed or is missing.
- A new QC lot will not accept results.

## Before you start
- Patient results must not be released around a QC hold. Support restores the workflow; the bench decides on QC acceptability.

## Steps
1. Confirm which rule failed and on which level/lot.
2. For a failure: the bench troubleshoots (reagent, calibration, rerun) per the QC procedure.
3. For a new lot: confirm the lot and its ranges are built in the LIS; build them if missing and approved.
4. Once QC passes, confirm the hold releases and patient results can be verified.

## Escalate when
- QC passes on the instrument but the LIS still holds results (Tier 2/3).
- Repeated failures after troubleshooting (vendor).

## Close the ticket with
Instrument, lot, rule failed or build missing, action taken, time hold released.
