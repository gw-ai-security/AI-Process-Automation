from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mock CRM", version="0.1.0")

store: Dict[str, Dict[str, Any]] = {}

class LeadPayload(BaseModel):
    run_id: str
    payload: Dict[str, Any]

@app.post("/leads/upsert")
async def upsert_lead(data: LeadPayload):
    key = data.payload.get("idempotency_key") or data.run_id
    action = "updated" if key in store else "created"
    entry = {
        "run_id": data.run_id,
        "payload": data.payload,
        "last_seen": datetime.now(timezone.utc).isoformat(),
    }
    crm_id = store.get(key, {}).get("crm_id") or str(uuid4())
    entry["crm_id"] = crm_id
    store[key] = entry
    return {
        "crm_id": crm_id,
        "action": action,
        "key": key,
        "status": "ok",
    }
