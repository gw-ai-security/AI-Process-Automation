#!/usr/bin/env bash
set -euo pipefail

BODY='{"email":"max@example.com","name":"Replay Lead","note":"replay test","idempotency_key":"lead-replay"}'
OLD_TIMESTAMP=$(python - <<'PY'
import time
print(int(time.time()) - 3600)
PY
)
export SIGN_TIMESTAMP="$OLD_TIMESTAMP"
export SIGN_BODY="$BODY"
mapfile -t HEADER_VALUES < <(python scripts/sign_webhook.py)
TIMESTAMP="${HEADER_VALUES[0]}"
SIGNATURE="${HEADER_VALUES[1]}"
URL="${PROCESSOR_URL:-http://localhost:8000}/webhook/lead"

curl -i -X POST "$URL" \
  -H "X-Idempotency-Key: lead-replay" \
  -H "X-Source: scripts" \
  -H "X-Timestamp: $TIMESTAMP" \
  -H "X-Signature: $SIGNATURE" \
  -H "Content-Type: application/json" \
  --data-binary "$BODY"
