import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict
from uuid import uuid4

from fastapi import Body, FastAPI

ALERTS_DIR = Path(os.getenv("ALERTS_DIR", "/alerts"))
ALERTS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Mock Jira/Confluence Logger", version="0.1.0")

async def write_payload(payload: Dict):
    identifier = payload.get("run_id") or str(uuid4())
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = ALERTS_DIR / f"{timestamp}_{identifier}.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return {"path": str(target)}

@app.post("/log")
async def log_event(payload: Dict = Body(...)):
    payload.setdefault("source", "mock-jira")
    return await write_payload(payload)

@app.post("/alert")
async def alert_event(payload: Dict = Body(...)):
    payload["alert"] = True
    return await write_payload(payload)
