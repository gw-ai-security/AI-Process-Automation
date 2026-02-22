#!/usr/bin/env bash
set -euo pipefail

echo "Running valid lead flow"
./scripts/curl_valid.sh

echo "Checking idempotency (repeat)"
./scripts/curl_valid.sh

echo "Simulating bad signature"
./scripts/curl_bad_sig.sh

echo "Simulating replay (old timestamp)"
./scripts/curl_replay.sh

echo "Sending malformed payload"
./scripts/curl_invalid_payload.sh
