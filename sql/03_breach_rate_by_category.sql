-- title: Resolution SLA breach rate by category
-- question: Which kinds of problems miss their targets most often?
SELECT category,
       COUNT(*)                                        AS resolved,
       SUM(1 - resolve_met)                            AS breached,
       ROUND(100.0 * (1 - AVG(resolve_met)), 1)        AS breach_pct,
       ROUND(100.0 * AVG(escalated), 1)                AS escalated_pct
FROM ticket_sla
WHERE resolve_met IS NOT NULL
GROUP BY category
ORDER BY breach_pct DESC;
