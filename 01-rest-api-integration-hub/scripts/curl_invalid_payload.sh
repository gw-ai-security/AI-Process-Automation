#!/usr/bin/env bash
set -euo pipefail

BODY='{"email":"invalid@example.com","name":"Invalid Payload","note":"missing brace"'
export SIGN_BODY="$BODY"
mapfile -t HEADER_VALUES < <(python scripts/sign_webhook.py)
TIMESTAMP="${HEADER_VALUES[0]}"
SIGNATURE="${HEADER_VALUES[1]}"
URL="${PROCESSOR_URL:-http://localhost:8000}/webhook/lead"

curl -i -X POST "$URL" \
  -H "X-Idempotency-Key: lead-invalid-payload" \
  -H "X-Source: scripts" \
  -H "X-Timestamp: $TIMESTAMP" \
  -H "X-Signature: $SIGNATURE" \
  -H "Content-Type: application/json" \
  --data-binary "$BODY"
