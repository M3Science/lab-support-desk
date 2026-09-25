-- title: Open backlog at end of period
-- question: What is still open, and how old is it?
SELECT ticket_id, priority, category, subcategory, status, assigned_tier AS tier,
       ROUND((julianday('2026-03-30 00:00') - julianday(opened_at)) * 24, 1) AS age_hours
FROM tickets
WHERE status <> 'Resolved'
ORDER BY priority, age_hours DESC;
