-- Lab Application Support Desk schema (SQLite)

DROP VIEW IF EXISTS ticket_sla;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS sla_policy;
DROP TABLE IF EXISTS kb_articles;

CREATE TABLE sla_policy (
    priority          TEXT PRIMARY KEY,          -- P1..P4
    description       TEXT NOT NULL,
    response_minutes  INTEGER NOT NULL,          -- first-response target
    resolve_hours     INTEGER NOT NULL           -- resolution target
);

CREATE TABLE kb_articles (
    kb_id  TEXT PRIMARY KEY,
    title  TEXT NOT NULL,
    path   TEXT NOT NULL
);

CREATE TABLE tickets (
    ticket_id          TEXT PRIMARY KEY,
    opened_at          TEXT NOT NULL,            -- 'YYYY-MM-DD HH:MM'
    priority           TEXT NOT NULL REFERENCES sla_policy(priority),
    category           TEXT NOT NULL,
    subcategory        TEXT NOT NULL,
    location           TEXT NOT NULL,
    requester_role     TEXT NOT NULL,
    assigned_tier      INTEGER NOT NULL CHECK (assigned_tier IN (1, 2, 3)),
    escalated          INTEGER NOT NULL CHECK (escalated IN (0, 1)),
    first_response_at  TEXT,
    resolved_at        TEXT,                     -- NULL while open
    status             TEXT NOT NULL CHECK (status IN ('Open', 'In Progress', 'Resolved')),
    kb_article         TEXT REFERENCES kb_articles(kb_id),
    reopened           INTEGER NOT NULL CHECK (reopened IN (0, 1)),
    resolution         TEXT
);

CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_opened ON tickets(opened_at);

-- One row per ticket with elapsed times and SLA outcomes.
-- Times are calendar hours (no business-hours calendar; see README limitations).
CREATE VIEW ticket_sla AS
WITH secs AS (
    SELECT t.*,
           -- whole seconds, so boundary cases compare exactly (no floating-point drift)
           CAST(strftime('%s', t.first_response_at) AS INTEGER) - CAST(strftime('%s', t.opened_at) AS INTEGER) AS response_secs,
           CAST(strftime('%s', t.resolved_at) AS INTEGER)       - CAST(strftime('%s', t.opened_at) AS INTEGER) AS resolve_secs
    FROM tickets t
)
SELECT
    s.ticket_id, s.opened_at, s.priority, s.category, s.subcategory, s.location,
    s.requester_role, s.assigned_tier, s.escalated, s.first_response_at, s.resolved_at,
    s.status, s.kb_article, s.reopened, s.resolution,
    ROUND(s.response_secs / 60.0, 1)   AS response_minutes,
    ROUND(s.resolve_secs / 3600.0, 2)  AS resolve_hours,
    p.response_minutes AS response_target_min,
    p.resolve_hours    AS resolve_target_hours,
    CASE WHEN s.response_secs <= p.response_minutes * 60 THEN 1 ELSE 0 END AS response_met,
    CASE WHEN s.resolved_at IS NULL THEN NULL
         WHEN s.resolve_secs <= p.resolve_hours * 3600 THEN 1 ELSE 0 END AS resolve_met
FROM secs s
JOIN sla_policy p USING (priority);
