-- title: Reopen rate with and without a KB article
-- question: Do knowledge base articles make fixes stick?
SELECT CASE WHEN kb_article IS NULL THEN 'No KB article' ELSE 'KB article used' END AS kb_usage,
       COUNT(*)                                        AS resolved,
       SUM(reopened)                                   AS reopened,
       ROUND(100.0 * AVG(reopened), 1)                 AS reopen_pct
FROM tickets
WHERE status = 'Resolved'
GROUP BY kb_usage
ORDER BY kb_usage;
