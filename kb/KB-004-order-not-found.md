# KB-004: Order not found when receiving a specimen

| Applies to | Typical priority | First owner | Escalate to |
|---|---|---|---|
| Lab receiving, collection sites | P3 | Tier 1 | Tier 2 (order interface), provider (order entry) |

## Symptoms
- Scanning the specimen label returns "order not found".
- The order exists but was cancelled or is on a different encounter.

## Before you start
- Do not create a new order without a provider order. Do not relabel a specimen.
- Hold the specimen under proper storage conditions while you investigate.

## Steps
1. Search by patient and collection date rather than by accession.
2. If the order was cancelled after collection, contact the ordering provider to reinstate or reorder.
3. If a duplicate order exists, confirm with the provider which one to cancel.
4. Link the specimen to the correct active order and document the change.

## Escalate when
- Orders placed in the EHR are not reaching the LIS at all (Tier 2: order interface).
- Patient identity on the specimen does not match the order (follow the misidentification policy).

## Close the ticket with
Accession, what was wrong (cancelled / duplicate / wrong encounter / not received), who approved the fix.
