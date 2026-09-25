-- title: Escalation impact on P2 tickets
-- question: How much time does an escalation add to a high-priority ticket?
SELECT CASE escalated WHEN 1 THEN 'Escalated to Tier 3' ELSE 'Resolved at Tier 1-2' END AS path,
       COUNT(*)                                        AS resolved,
       ROUND(AVG(resolve_hours), 1)                    AS avg_hours,
       ROUND(100.0 * AVG(resolve_met), 1)              AS resolve_met_pct
FROM ticket_sla
WHERE resolved_at IS NOT NULL AND priority = 'P2'
GROUP BY escalated
ORDER BY escalated;
