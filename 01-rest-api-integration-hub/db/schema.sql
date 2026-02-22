-- Integration Hub schema (minimal)

create table if not exists runs (
  run_id uuid primary key,
  idempotency_key text not null,
  source text not null,
  received_at timestamptz not null default now(),
  status text not null check (status in ('accepted','processed','failed')),
  error_code text,
  error_message text
);

create unique index if not exists runs_idempotency_key_uq
  on runs (idempotency_key);

create table if not exists audit_events (
  event_id bigserial primary key,
  run_id uuid,
  event_time timestamptz not null default now(),
  event_type text not null,
  actor text,
  payload jsonb not null,
  constraint audit_events_run_fk foreign key (run_id) references runs(run_id) on delete set null
);

create index if not exists audit_events_time_idx
  on audit_events (event_time);

create table if not exists dlq (
  dlq_id bigserial primary key,
  run_id uuid,
  created_at timestamptz not null default now(),
  reason text not null,
  payload jsonb not null,
  retry_count int not null default 0,
  next_retry_at timestamptz,
  status text not null default 'open' check (status in ('open','retrying','resolved','dead')),
  constraint dlq_run_fk foreign key (run_id) references runs(run_id) on delete set null
);

create index if not exists dlq_status_idx
  on dlq (status);

create table if not exists kpi_daily (
  day date primary key,
  received_count int not null default 0,
  processed_count int not null default 0,
  failed_count int not null default 0,
  dlq_open_count int not null default 0,
  avg_processing_ms int
);