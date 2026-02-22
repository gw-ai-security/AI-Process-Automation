import os
import json
import uuid
from datetime import datetime, timezone
from typing import Optional

import psycopg
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="Integration Hub Processor", version="0.2.0")


def get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set")
    return db_url


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.get("/health")
def health():
    payload = {"check": "health", "at": now_utc()}

    with psycopg.connect(get_db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                insert into audit_events (run_id, event_type, actor, payload)
                values (%s, %s, %s, %s::jsonb)
                """,
                (None, "health_check", "system", json.dumps(payload)),
            )

    return {"status": "ok"}


@app.post("/webhook/lead")
async def webhook_lead(
    request: Request,
    x_idempotency_key: Optional[str] = Header(default=None),
    x_source: Optional[str] = Header(default="unknown"),
):
    """
    Minimal intake endpoint:
    - requires X-Idempotency-Key
    - creates run_id
    - inserts into runs (accepted)
    - writes audit event lead_received
    """
    if not x_idempotency_key:
        raise HTTPException(status_code=400, detail="Missing X-Idempotency-Key header")

    body = await request.json()
    run_id = uuid.uuid4()

    with psycopg.connect(get_db_url()) as conn:
        with conn.cursor() as cur:
            # idempotency: if key already exists -> return previous run
            cur.execute(
                "select run_id, status from runs where idempotency_key = %s",
                (x_idempotency_key,),
            )
            existing = cur.fetchone()
            if existing:
                existing_run_id, status = existing
                return {
                    "status": "duplicate",
                    "run_id": str(existing_run_id),
                    "existing_status": status,
                }

            cur.execute(
                """
                insert into runs (run_id, idempotency_key, source, status)
                values (%s, %s, %s, %s)
                """,
                (run_id, x_idempotency_key, x_source, "accepted"),
            )

            cur.execute(
                """
                insert into audit_events (run_id, event_type, actor, payload)
                values (%s, %s, %s, %s::jsonb)
                """,
                (
                    run_id,
                    "lead_received",
                    "webhook",
                    json.dumps({"at": now_utc(), "source": x_source, "body": body}),
                ),
            )

    return {"status": "accepted", "run_id": str(run_id)}