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
SELECT
    t.*,
    ROUND((julianday(t.first_response_at) - julianday(t.opened_at)) * 24 * 60, 1) AS response_minutes,
    ROUND((julianday(t.resolved_at)       - julianday(t.opened_at)) * 24, 2)      AS resolve_hours,
    p.response_minutes AS response_target_min,
    p.resolve_hours    AS resolve_target_hours,
    CASE WHEN (julianday(t.first_response_at) - julianday(t.opened_at)) * 24 * 60 <= p.response_minutes
         THEN 1 ELSE 0 END AS response_met,
    CASE WHEN t.resolved_at IS NULL THEN NULL
         WHEN (julianday(t.resolved_at) - julianday(t.opened_at)) * 24 <= p.resolve_hours
         THEN 1 ELSE 0 END AS resolve_met
FROM tickets t
JOIN sla_policy p USING (priority);
