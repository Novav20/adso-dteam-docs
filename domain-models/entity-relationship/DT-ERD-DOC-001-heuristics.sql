-- =============================================================================
-- DTEAM CORE DATABASE: BESPOKE MANUAL HEURISTICS & POLICIES
-- Engine: PostgreSQL 18.x + TimescaleDB | Standard: ISO 14224 / ISO 27001 / ADR-003 / ADR-010
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. BESPOKE PARTIAL & UNIQUE INDEXES
-- -----------------------------------------------------------------------------
-- ISO 14224 1:1 Active Slot Occupancy Invariant (ADR-010 / INV-025)
CREATE UNIQUE INDEX IF NOT EXISTS uq_asset_installations_active_slot
    ON tax.asset_installations (functional_location_id)
    WHERE removed_at IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_asset_installations_active_unit
    ON tax.asset_installations (equipment_unit_id)
    WHERE removed_at IS NULL;

-- Active Backlog Board Optimization (DT-ARQ-DB-DOC-001)
CREATE INDEX IF NOT EXISTS idx_work_orders_active_backlog
    ON mtto.work_orders (criticality, scheduled_date)
    WHERE current_status NOT IN ('CLOSED', 'COMPLETE');

-- -----------------------------------------------------------------------------
-- 2. TIMESCALEDB HYPERTABLE CONFIGURATION
-- -----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS timescaledb;

SELECT create_hypertable(
    'vis.telemetry_signals',
    'timestamp',
    if_not_exists => TRUE
);

-- -----------------------------------------------------------------------------
-- 3. BESPOKE COMPOSITE & DESCENDING INDEXES
-- -----------------------------------------------------------------------------
-- LATERAL Subquery Optimization for Latest Telemetry Reading (VIS-033 / DT-ARQ-DB-DOC-001)
CREATE INDEX IF NOT EXISTS idx_telemetry_signals_latest_lookup
    ON vis.telemetry_signals (equipment_unit_id, timestamp DESC);

-- Inventory Movement Chronology
CREATE INDEX IF NOT EXISTS idx_inventory_transactions_timestamp
    ON inv.inventory_transactions (timestamp DESC);

-- RIME Prioritization Scoring
CREATE INDEX IF NOT EXISTS idx_backlog_items_priority_score
    ON mtto.backlog_items (priority_score DESC);

-- Auth Token Expiration Tracking
CREATE INDEX IF NOT EXISTS idx_auth_tokens_expires_at
    ON adm.auth_tokens (expires_at);

-- Audit Log Chronological Search
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp
    ON adm.audit_logs (timestamp DESC);

-- Audit Log Entity Lookup
CREATE INDEX IF NOT EXISTS idx_audit_logs_entity
    ON adm.audit_logs (entity_type, entity_id);

-- 7-Year Audit Retention Partition Window Lookup (ADM-032 / FR-350 / FR-358)
CREATE INDEX IF NOT EXISTS idx_audit_retention_partitions_period
    ON adm.audit_retention_partitions (period_start DESC, period_end DESC);

-- -----------------------------------------------------------------------------
-- 4. ROW-LEVEL SECURITY (RLS) FOR IMMUTABLE AUDIT (ADR-003)
-- -----------------------------------------------------------------------------
-- Strict Row-Level Security enforcement (applies to table owner too; requires non-SUPERUSER/NOBYPASSRLS app roles)
ALTER TABLE adm.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE adm.audit_logs FORCE ROW LEVEL SECURITY;
REVOKE UPDATE, DELETE, TRUNCATE ON adm.audit_logs FROM PUBLIC;

-- Append-only policy: Allow inserts, while RLS + REVOKE deny UPDATE and DELETE
DROP POLICY IF EXISTS rls_audit_logs_insert_policy ON adm.audit_logs;
CREATE POLICY rls_audit_logs_insert_policy
    ON adm.audit_logs
    FOR INSERT
    WITH CHECK (true);

-- Read policy: Allow querying the audit trail
DROP POLICY IF EXISTS rls_audit_logs_select_policy ON adm.audit_logs;
CREATE POLICY rls_audit_logs_select_policy
    ON adm.audit_logs
    FOR SELECT
    USING (true);

COMMENT ON POLICY rls_audit_logs_insert_policy ON adm.audit_logs IS
    'Enforces physical append-only behavior: database engine denies UPDATE and DELETE operations.';

-- -----------------------------------------------------------------------------
-- 5. DECLARATIVE RANGE PARTITIONING FOR 7-YEAR AUDIT RETENTION (FR-350 / FR-358)
-- -----------------------------------------------------------------------------
-- Idempotent dynamic bootstrap: provisions Q1-Q4 of the current UTC year plus
-- next-year Q1 lookahead (5 quarters total) and revokes mutating privileges on
-- each child partition. Ongoing future quarters are pre-created by the scheduled
-- AuditPartitionProvisioningJob / pg_cron worker before quarter rollover.
DO $$
DECLARE
    base_year_utc timestamp := date_trunc('year', timezone('UTC', now()));
    q_idx         integer;
    q_start_utc   timestamp;
    q_end_utc     timestamp;
    part_name     text;
BEGIN
    FOR q_idx IN 0..4 LOOP
        q_start_utc := base_year_utc + make_interval(months => q_idx * 3);
        q_end_utc   := q_start_utc + interval '3 months';
        part_name   := format(
            'part_audit_%s_q%s',
            to_char(q_start_utc, 'YYYY'),
            EXTRACT(QUARTER FROM q_start_utc)::integer
        );

        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS adm.%I PARTITION OF adm.audit_logs FOR VALUES FROM (%L) TO (%L)',
            part_name,
            q_start_utc AT TIME ZONE 'UTC',
            q_end_utc AT TIME ZONE 'UTC'
        );

        EXECUTE format(
            'REVOKE UPDATE, DELETE, TRUNCATE ON adm.%I FROM PUBLIC',
            part_name
        );
    END LOOP;
END $$;

CREATE TABLE IF NOT EXISTS adm.part_audit_default
    PARTITION OF adm.audit_logs DEFAULT;
REVOKE UPDATE, DELETE, TRUNCATE ON adm.part_audit_default FROM PUBLIC;
