-- title: Account lockouts by weekday
-- question: When do lockouts happen, and could self-service reset help?
WITH days(num, weekday) AS (
    VALUES ('1', 'Mon'), ('2', 'Tue'), ('3', 'Wed'), ('4', 'Thu'),
           ('5', 'Fri'), ('6', 'Sat'), ('0', 'Sun')
)
SELECT d.weekday,
       COUNT(t.ticket_id)                              AS lockouts
FROM days d
LEFT JOIN tickets t
       ON strftime('%w', t.opened_at) = d.num
      AND t.subcategory = 'Account locked out'
GROUP BY d.num, d.weekday
ORDER BY CASE d.num WHEN '0' THEN 7 ELSE CAST(d.num AS INTEGER) END;
