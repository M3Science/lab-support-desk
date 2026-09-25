-- title: Label printer tickets by location
-- question: Where should preventive printer maintenance start?
SELECT location,
       COUNT(*)                                        AS tickets
FROM tickets
WHERE category = 'Label Printer'
GROUP BY location
ORDER BY tickets DESC;
