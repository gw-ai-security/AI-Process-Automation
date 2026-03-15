# Threat Model

## Assets

- operational intake text
- routing and priority decisions
- workflow event and error logs
- KPI and timing data

## Main Risks

- sensitive operational content leakage in logs
- unauthorized API access in exposed environments
- prompt/response manipulation when using live LLM endpoints
- database credential exposure in misconfigured deployments

## Current Mitigations

- scoped MVP endpoints only
- environment-driven configuration
- explicit error logging and event trails
- strict JSON parsing for model output

## Deferred Controls

- authentication and authorization
- secrets vault integration
- encryption at rest and retention policy enforcement
- request rate limiting and abuse controls
