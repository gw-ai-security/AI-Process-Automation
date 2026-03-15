# KPI Model

## Core Metrics

- total processed inputs
- success rate (outputs / inputs)
- average processing time (ms)
- routing distribution by target area
- total estimated saved minutes

## ROI Formula

`saved_minutes = manual_baseline_minutes - automated_minutes`

This is an estimated automation impact model, not a validated financial ROI claim.

## Storage

KPI datapoints are written per workflow into `workflow_metrics` and aggregated via `/metrics/summary`.

## Interpretation

- high success rate with stable latency indicates robust automation flow
- route distribution helps detect backlog concentration by business area
