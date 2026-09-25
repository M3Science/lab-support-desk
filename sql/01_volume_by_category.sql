-- title: Ticket volume by category
-- question: Where does the support workload come from?
SELECT category,
       COUNT(*)                                   AS tickets,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM tickets), 1) AS pct_of_total
FROM tickets
GROUP BY category
ORDER BY tickets DESC;
