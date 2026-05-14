---
name: resilience-patterns
description: Apply core resilience patterns — timeouts, retries with backoff, circuit breakers, bulkheads, idempotency, graceful degradation — to any code that calls a network dependency or runs under load. Use when adding a downstream call, when designing a request path, when the user says "resilience", "retry", "timeout", "circuit breaker", "bulkhead", "fault tolerance".
---

# resilience-patterns

## Purpose

The unhappy-path patterns are well-known and chronically under-applied. This skill is the checklist that turns "the call could fail" into a defined behavior the system can be reasoned about.

## When to use

- Any code path that calls a network dependency (HTTP, gRPC, DB, queue, cache, external API).
- Designing a new request handler.
- After an incident where a partial dependency outage cascaded.
- User says: "resilience", "retry", "timeout", "circuit breaker", "bulkhead", "fault tolerance", "graceful degradation".

## The patterns

### 1. Timeout — *always*
- **Never use default client timeouts.** They're either too long (Python `requests` default is no timeout) or unknown.
- Pick a timeout based on this service's own latency budget for that operation. If your p95 budget is 500ms and the dependency claims p99 200ms, set timeout to 200ms.
- Distinguish **connect timeout** from **read timeout** when the library supports it.
- Timeout = the call gives up. Combine with retries or fallback to define what happens next.

### 2. Retry with backoff — *for transient failures only*
- **Retry only on**: network errors, 5xx, 429 (with `Retry-After`).
- **Never retry**: 4xx (other than 429), 408 timeouts on non-idempotent calls without idempotency keys.
- **Backoff** — exponential (e.g. 100ms, 200ms, 400ms, 800ms) **with jitter** (random factor) to prevent synchronized retries.
- **Max attempts** — usually 2–4. More buys little; just adds latency.
- **Retry budget** — limit total retry rate as a percentage of base traffic (e.g. retries ≤ 10% of base requests). Prevents retries from amplifying an outage.

### 3. Idempotency keys — *for mutations that retry*
- Generate a UUID on the client; pass as `Idempotency-Key` header; server stores result for N hours.
- Without this, retries on POST can charge a card twice / send two emails / create two orders.
- See also `api-design` for how to expose idempotency on your own endpoints.

### 4. Circuit breaker — *for hot, fail-fast paths*
- Track recent failure rate per dependency. When it crosses a threshold, "open the circuit" — fail immediately for a cool-off period instead of waiting for timeouts.
- After cool-off, "half-open" — let a probe through; if it succeeds, close. If it fails, stay open longer.
- Implementations: `pybreaker`, `tenacity`, `resilience4j`, Polly, Istio mesh-level.
- **Don't add for low-volume dependencies** — circuit breakers thrash on small request volumes.

### 5. Bulkhead — *to contain blast radius*
- Limit resources (connection pool slots, thread/coroutine count) per dependency. Slow dependency A can't starve the pool that handles dependency B.
- For HTTP: per-host connection pools.
- For request handling: separate worker pools per critical path.

### 6. Graceful degradation — *when failure is recoverable*
- Define what "degraded but useful" means per dependency.
- Cache-fallback: serve last-good response when the source is down.
- Default-value fallback: skip a non-critical enrichment; serve the core result.
- Async retry: queue the failed operation, return a partial response, retry later.
- **Document the user-visible degraded behavior** in the service map.

### 7. Backpressure — *upstream protection*
- Reject early when downstream queues are full, instead of accepting work that will time out.
- Return 503 with `Retry-After`.
- Better to fail fast than to fail slow.

### 8. Health checks — *separate liveness from readiness*
- **Liveness**: am I running? (Restart if false.)
- **Readiness**: am I ready to take traffic? (Removed from load balancer if false — e.g. during dependency outage if you can't serve.)
- Don't conflate. A failing dependency should make you NOT ready, but it shouldn't restart you.

## Process per code path

1. **Identify every network call** in the path.
2. **For each, decide and document**:
   - Timeout value.
   - Retry policy (or "no retry").
   - Idempotency strategy (if mutating).
   - Failure behavior (block / degrade / async).
   - Circuit breaker (yes if high volume + failure-prone).
3. **Verify the call is wrapped** in code accordingly. Reject reviews that skip this.
4. **Cross-ref `downstream-dependencies`** — same checklist, from the new-integration angle.
5. **Test the failure path** — chaos test or fault-injection. A retry policy with no test of the retry path is theoretical.

## Anti-patterns

- "Retry forever" — turns a 5-minute outage into an unrecoverable cascade.
- Same retry policy regardless of error code — retrying a 400 makes no one happy.
- Long timeouts to "give the dependency a chance" — chains the user request to a struggling system.
- No jitter — every client retries at the same moment, hammering the recovering service.
- Catching all exceptions and treating them identically — see `error-handling-standards`.

## What this skill does NOT do

- Specify a single library to use. Pick what fits the stack.
- Cover failure handling in batch / event-stream contexts in depth.

## Output

Inline decisions on each network call, captured in code + `docs/integration/service-map.md` failure-mode column.
