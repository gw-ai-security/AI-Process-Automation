#!/usr/bin/env bash
set -euo pipefail

BODY='{"email":"max@example.com","name":"Bad Signature","note":"bad sig","idempotency_key":"lead-bad-sig"}'
export SIGN_BODY="$BODY"
mapfile -t HEADER_VALUES < <(python scripts/sign_webhook.py)
TIMESTAMP="${HEADER_VALUES[0]}"
INVALID_SIGNATURE="sha256=deadbeef"
URL="${PROCESSOR_URL:-http://localhost:8000}/webhook/lead"

curl -i -X POST "$URL" \
  -H "X-Idempotency-Key: lead-bad-sig" \
  -H "X-Source: scripts" \
  -H "X-Timestamp: $TIMESTAMP" \
  -H "X-Signature: $INVALID_SIGNATURE" \
  -H "Content-Type: application/json" \
  --data-binary "$BODY"
