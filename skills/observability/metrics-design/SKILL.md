---
name: metrics-design
description: Decide what to measure — applying the RED, USE, and four golden signals frameworks — and commit a metric inventory per service. Use when starting a new service, when an incident reveals missing metrics, or when the user says "what should we measure", "metrics design", "RED method", "USE method", "golden signals", "instrumentation".
---

# metrics-design

## Purpose

The most expensive moment in an incident is realizing you can't see what's happening. This skill establishes the minimum metric set per service so that, when something goes wrong, the team has data — not guesses.

## When to use

- Starting a new service.
- An incident revealed missing metrics.
- Adding a new endpoint, dependency, or workload.
- User says: "what should we measure", "metrics design", "RED method", "USE method", "golden signals", "instrumentation", "what metrics".

## The frameworks (use them together, not separately)

### Four Golden Signals (Google SRE)
Apply to any user-facing service:
- **Latency** — how long requests take. Distinguish successful vs. failed (failed requests are often fast).
- **Traffic** — request rate / throughput.
- **Errors** — error rate, broken out by error class.
- **Saturation** — how full the system is (CPU, memory, queue depth, connection pool).

### RED method (for request-driven services)
- **Rate** — requests per second.
- **Errors** — failure rate.
- **Duration** — latency distribution (p50, p95, p99).

### USE method (for resources — CPU, memory, disk, network)
- **Utilization** — % time the resource is busy.
- **Saturation** — degree of queueing / waiting.
- **Errors** — count of error events.

## The minimum metric set per service

Every service ships with at least these:

### Request-path metrics (RED)
- `http_requests_total{endpoint, method, status}` — counter; build rate from it.
- `http_request_duration_seconds{endpoint, method, status}` — histogram for p50/p95/p99.
- `http_in_flight_requests{endpoint}` — gauge of concurrent requests.

### Per-dependency metrics
For each downstream dependency (DB, cache, queue, external API):
- `dep_calls_total{dep, operation, status}`
- `dep_call_duration_seconds{dep, operation, status}`
- `dep_circuit_breaker_state{dep}` if you use them.

### Resource metrics (USE)
Usually emitted by the platform (Kubernetes, cloud metrics), augment with:
- Application-level: thread/coroutine count, connection pool stats, queue depths.

### Business-event metrics
At least one per major user action (signup, checkout, post-published, message-sent). Lets you correlate "the funnel is down" with "the system is fine."
- `business_event_total{event, outcome}` — e.g. `signup_total{outcome="success"}`.

## Conventions

- **Naming**: `<subject>_<verb>_<unit>`. `_total` for counters, `_seconds` / `_bytes` for histograms with units, `_ratio` for gauges 0-1.
- **Labels** (Prometheus-style) — high-cardinality kills your metrics store. NEVER label by user ID, request ID, or anything unbounded. Use traces / logs for high-cardinality.
- **Cardinality budget** — set one. Most series → high cost + slow queries.
- **No business-secret values in metrics** — metrics are often broadly readable.

## Process

1. **List the user journeys** the service supports. (One sentence each.)
2. **List the dependencies** (DB, cache, external APIs).
3. **For each journey**: ensure RED metrics on the entry endpoint, business-event metric on success.
4. **For each dependency**: per-dep call metrics.
5. **For each pooled resource** (DB connections, worker pool): saturation metric.
6. **Cardinality audit** — count series; any label you can't bound, remove or hash.
7. **Write `docs/observability/metrics-inventory.md`** — every metric, its labels, what it answers.
8. **Wire SLOs** (`slo-definition`) and alerts (`alerting-policy`) against the metrics.

## Anti-patterns

- **Adding metrics ad-hoc.** Each new metric should answer a defined question.
- **High-cardinality labels** — `user_id`, `request_id`, `trace_id`. These belong in logs/traces, not metrics.
- **Counters that reset** (gauge masquerading as a counter) — confuses rate calculations.
- **One global "errors" counter** — useless without breakdown by error class.
- **No business metrics** — you can see CPU is fine but not whether the funnel works.
- **Measuring everything; alerting on nothing.** Metrics with no alerts and no dashboard are theater.

## Cross-references

- `slo-definition` — what SLO levels to set against these metrics.
- `alerting-policy` — when do these metrics page someone.
- `dashboard-design` — how to surface them.
- `distributed-tracing` — for the high-cardinality questions metrics can't answer.
- `logging-standards` — same data, different shape, different use.

## Output

- Instrumentation in code.
- `docs/observability/metrics-inventory.md`.
