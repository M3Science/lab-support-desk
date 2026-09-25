-- title: SLA compliance by priority
-- question: Are we meeting response and resolution targets?
SELECT priority,
       COUNT(*)                                     AS tickets,
       response_target_min                          AS response_target_min,
       ROUND(100.0 * AVG(response_met), 1)          AS response_met_pct,
       resolve_target_hours                         AS resolve_target_hrs,
       ROUND(100.0 * AVG(resolve_met), 1)           AS resolve_met_pct
FROM ticket_sla
GROUP BY priority
ORDER BY priority;
