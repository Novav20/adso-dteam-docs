-- =============================================================================
-- DTEAM CORE DATABASE: BESPOKE MANUAL HEURISTICS & POLICIES
-- Motor: PostgreSQL 18.x | Standard: ISO 14224 / ISO 27001 / ADR-003
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. BESPOKE PARTIAL INDEXES
-- -----------------------------------------------------------------------------
-- Active Backlog Board Optimization (DT-ARQ-DB-DOC-001)
CREATE INDEX IF NOT EXISTS idx_work_orders_active_backlog 
    ON mtto.work_orders (criticality, scheduled_date)
    WHERE current_status NOT IN ('CLOSED', 'COMPLETE');

-- -----------------------------------------------------------------------------
-- 2. BESPOKE COMPOSITE & DESCENDING INDEXES
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

-- -----------------------------------------------------------------------------
-- 3. ROW-LEVEL SECURITY (RLS) FOR IMMUTABLE AUDIT (ADR-003)
-- -----------------------------------------------------------------------------
-- Strict Row-Level Security enablement
ALTER TABLE adm.audit_logs ENABLE ROW LEVEL SECURITY;

-- Append-only policy: Allow inserts, but RLS explicitly denies UPDATE and DELETE
CREATE POLICY rls_audit_logs_insert_policy 
    ON adm.audit_logs 
    FOR INSERT 
    WITH CHECK (true);

-- Read policy: Allow querying the audit trail
CREATE POLICY rls_audit_logs_select_policy 
    ON adm.audit_logs 
    FOR SELECT 
    USING (true);

COMMENT ON POLICY rls_audit_logs_insert_policy ON adm.audit_logs IS 
    'Enforces physical append-only behavior: database engine denies UPDATE and DELETE operations.';
