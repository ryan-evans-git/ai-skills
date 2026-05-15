---
name: distributed-tracing
description: Instrument a service for distributed tracing — span creation, context propagation, attribute discipline, sampling — so cross-service questions like "why is this one request slow" can be answered. Use when setting up tracing for a new service, when "we can't tell where time is going" comes up, or when the user says "tracing", "OpenTelemetry", "OTel", "Jaeger", "spans", "distributed trace".
---

# distributed-tracing

## Purpose

Metrics tell you something is wrong; logs tell you what happened to one component; **traces tell you the path of one request across all components**. Without tracing, "why is this slow" requires hand-correlating logs across services. With tracing, it's a UI click.

## When to use

- Setting up a new service in a multi-service system.
- An investigation where "where did the time go" took hours.
- Adding a new external dependency.
- User says: "tracing", "OpenTelemetry", "OTel", "Jaeger", "spans", "distributed trace", "trace ID".

## The OpenTelemetry default

Adopt OpenTelemetry (OTel) as the instrumentation standard:
- **Vendor-neutral** — switch backends (Jaeger, Tempo, Datadog, Honeycomb, Lightstep, Dynatrace) without re-instrumenting.
- **Language-native SDKs** for Python, JS/TS, Go, Rust, Java, etc.
- **Automatic instrumentation** for popular frameworks/libraries (Flask, FastAPI, Express, gRPC, requests, http, common DB drivers).

## What to span

Create a span (a timed operation) for:

### Always
- **Inbound request handler** — auto-instrumented by web framework integrations.
- **Outbound dependency calls** — DB queries, HTTP calls, queue publishes, cache lookups. Auto-instrumented for most.
- **Background jobs / tasks** — each job is a top-level span.

### Often
- **Significant in-process operations** — image processing, complex computation, batch processing. Manual spans.
- **LLM calls** — cross-ref `agent-design`; each model call + each tool call.

### Rarely / never
- **Tight loops** — one span per iteration of a 10k-element loop is span spam.
- **Trivial function calls** — only span what's worth a row in the trace UI.

## Context propagation

The whole point of distributed tracing is the trace following a request *across* services.

- **HTTP**: standard `traceparent` and `tracestate` headers (W3C Trace Context). Auto-injected by OTel HTTP clients; auto-extracted by server middlewares.
- **gRPC**: same context, metadata-based.
- **Queues / messaging**: serialize the trace context in the message headers; deserialize on consume. Most OTel instrumentations handle this for common brokers.
- **Background work** triggered from a request: explicitly pass the context (don't drop it).

**The most common bug**: a service downgrades context to a fresh trace, breaking the chain. Visible as: traces stop at a service boundary. Audit with: "do my traces reach all the way through?"

## Attributes (the searchable / filterable fields on spans)

Attach to spans:
- **HTTP**: method, path template (NOT raw path with params), status code.
- **DB**: operation type (`SELECT`/`INSERT`), table/collection, *parameterized* statement (never the full statement with values — PII risk + cardinality).
- **External APIs**: target service, operation, status.
- **User context**: `user.id`, `tenant.id` (hash if needed; never email/name).
- **Custom**: feature flags active, route variant, etc.
- **LLM**: model name, input/output token counts, cached tokens, cost.

**Avoid as attributes**: full request/response bodies, secrets, unbounded-cardinality fields (request IDs go on the span itself, not as filterable attributes).

## Sampling

100% sampling is expensive for high-volume services; storage cost / query speed degrade.

- **Head-based sampling**: decide at trace start. Cheap; can miss interesting traces (errors after the head decided to drop).
- **Tail-based sampling**: collect all spans, decide after the trace completes whether to keep. Preferred — keep all error traces, all slow traces, sample healthy traces. Requires a collector that supports it (OTel Collector, vendor agents).
- **Always-on for**: errors, slow requests (above latency threshold), and a baseline sample (~1-5%) of healthy traces for distribution analysis.

## Linking with logs and metrics

The "three pillars" are most powerful when linked:
- **Logs**: include `trace_id` in every log line (`logging-standards` mentions it). Click from a slow trace to its logs.
- **Metrics**: emit metrics with exemplar trace IDs — click from a latency spike on a chart to a representative slow trace.

This is where observability becomes engineering, not archaeology.

## Process

1. **Pick the backend** — what the org uses, or default to a managed provider (Honeycomb, Tempo+Grafana, Datadog).
2. **Adopt OTel SDK** for the service's language.
3. **Enable auto-instrumentation** for the framework + libraries.
4. **Add manual spans** for significant in-process work (per the list above).
5. **Verify context propagation** — open a trace; confirm it crosses every boundary.
6. **Add critical attributes** (tenant, user, feature flag).
7. **Configure sampling** — tail-based preferred.
8. **Wire trace IDs into logs** (`logging-standards`).
9. **Document at `docs/observability/tracing.md`**:
   - Backend + access.
   - Span conventions (what gets spans, what attributes).
   - Sampling policy.
   - Key trace queries: "slow checkout traces last hour", "errors per service".

## Anti-patterns

- **Tracing disabled in prod "for performance."** Modern sampling reduces overhead to <1%. The cost of NOT having traces in an incident dwarfs the runtime cost.
- **Manual spans on every function.** Span spam; expensive; hard to read.
- **Spans without attributes.** Trace shows duration but not what.
- **PII in attributes.** Traces are searched broadly; PII leaks.
- **No link from logs to traces.** Trace shows the path; logs show the why. Without `trace_id` in logs, you can't bridge.
- **High-cardinality attributes** — `path: /users/abc-123` blows up backend storage. Use the path template.

## Cross-references

- `metrics-design` — emit metrics with exemplar trace IDs.
- `logging-standards` — `trace_id` in every log line.
- `performance-investigation` — traces are the primary tool.
- `resilience-patterns` — instrument retry / circuit-breaker decisions as span attributes.
- `agent-design` — LLM agent steps as spans.

## Output

- OTel instrumentation in code.
- `docs/observability/tracing.md` — conventions + sampling policy.
