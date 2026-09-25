-- title: Top recurring issues
-- question: Which specific problems keep coming back?
SELECT subcategory                                     AS issue,
       category,
       COUNT(*)                                        AS tickets,
       ROUND(AVG(resolve_hours), 1)                    AS avg_resolve_hours
FROM ticket_sla
GROUP BY subcategory, category
ORDER BY tickets DESC
LIMIT 8;
