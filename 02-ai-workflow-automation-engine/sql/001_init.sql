CREATE TABLE IF NOT EXISTS workflow_inputs (
    id SERIAL PRIMARY KEY,
    correlation_id UUID NOT NULL UNIQUE,
    source_type VARCHAR(64) NOT NULL,
    source_system VARCHAR(100) NOT NULL,
    submitted_by VARCHAR(255) NOT NULL,
    priority VARCHAR(16) NOT NULL DEFAULT 'medium',
    content TEXT NOT NULL,
    tags JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(32) NOT NULL DEFAULT 'accepted',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_outputs (
    id SERIAL PRIMARY KEY,
    input_id INTEGER NOT NULL REFERENCES workflow_inputs(id) ON DELETE CASCADE,
    summary TEXT NOT NULL,
    action_items JSONB NOT NULL DEFAULT '[]'::jsonb,
    priority VARCHAR(16) NOT NULL,
    route_to VARCHAR(32) NOT NULL,
    confidence NUMERIC(4, 3),
    reasoning_short TEXT,
    saved_minutes INTEGER NOT NULL DEFAULT 0,
    processing_time_ms INTEGER NOT NULL DEFAULT 0,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_events (
    id SERIAL PRIMARY KEY,
    correlation_id UUID NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    event_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_errors (
    id SERIAL PRIMARY KEY,
    correlation_id UUID,
    error_code VARCHAR(64) NOT NULL,
    error_message TEXT NOT NULL,
    error_context JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_metrics (
    id SERIAL PRIMARY KEY,
    correlation_id UUID,
    metric_name VARCHAR(128) NOT NULL,
    metric_value NUMERIC(12, 2) NOT NULL DEFAULT 0,
    metric_unit VARCHAR(32),
    captured_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
