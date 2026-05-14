---
name: downstream-dependencies
description: Before integrating with or relying on a downstream service, audit the contract, the SLA, the failure mode, and the impact on this service when the dependency is unhealthy. Use when adding a new downstream call, when the user says "integrate with X", "call the Y API", "add Z as a dependency", or before merging any code that talks to a new external system.
---

# downstream-dependencies

## Purpose

Every downstream dependency is a part of your reliability contract that you don't control. This skill enforces a checklist before any new dependency is wired in, and documents the relationship in the service map so future agents understand the failure mode without re-deriving it.

## When to use

- About to add a call to another service, internal or external.
- User says: "integrate with X", "call the Y API", "add Z as a dependency", "consume the W service", "we need data from V".
- Reviewing a PR that introduces a new HTTP / gRPC client, SDK, or webhook subscription.

## Checklist (before wiring it in)

### Contract
- [ ] **The contract is documented and stable** — OpenAPI / proto / pact / etc. Saved or linked in `docs/integration/`.
- [ ] **Versioning policy is understood** — semver? URL-versioned? Endpoint-versioned? Will breaks be announced?
- [ ] **Authentication mechanism documented** — what tokens, how rotated, where stored.
- [ ] **Rate limits known** — requests per minute / burst / cost. Will we hit them?
- [ ] **Idempotency support documented** — if we retry, what guarantees does the API give?

### Reliability
- [ ] **SLA / SLO is stated** — uptime target, latency target. (For internal: ask the owning team. For external: cite their status page.)
- [ ] **Status page or incident channel identified** for the service.
- [ ] **Historical reliability surveyed** — past 90 days of incidents reviewed if available.

### Failure mode
- [ ] **What happens to this service when the dependency is unhealthy?** Choose deliberately:
   - **Block** — fail the request, return error. Appropriate only for truly required dependencies.
   - **Degrade** — return partial / cached / default response. Document the user-visible behavior.
   - **Async / queue** — write to local store, retry later.
   - **Fire-and-forget** — accept loss; usually wrong unless explicitly OK.
- [ ] **Timeout configured** — never use the client default. Set a value tied to this service's own latency budget.
- [ ] **Retry policy decided** — limited attempts, exponential backoff, jitter, max budget. Don't retry on non-idempotent calls unless idempotency keys.
- [ ] **Circuit breaker considered** — for high-volume dependencies, prevent thundering herd on dependency recovery.
- [ ] **Bulkhead considered** — does one slow dependency tie up the request pool for unrelated traffic?

### Security
- [ ] **Data classification of what we send/receive** — does this leak PII to a third party? (Cross-ref `pii-data-handling`.)
- [ ] **Credentials stored correctly** — secret manager, not env file. (Cross-ref `secrets-hygiene`.)
- [ ] **TLS validated** — not disabled "to make it work."

### Observability
- [ ] **Metrics** — request count, latency, error rate, retries — broken out per dependency.
- [ ] **Distributed tracing** — pass trace context across the call.
- [ ] **Logging** — log dependency call failures with enough context to triage (but no secrets / no PII).

### Cost
- [ ] **Cost per call understood** for paid APIs (LLM providers, payment processors, mapping APIs, SMS).
- [ ] **Caching considered** for repeat reads of stable data (cross-ref `caching-strategy`).
- [ ] **Spending alert configured** in the provider's console.

### Documentation
- [ ] **Service map updated** — add the new dependency row in `docs/integration/service-map.md` with its failure mode.
- [ ] **ADR if significant** — `adr-writer` skill.

## Process

1. Walk the checklist above. Mark each item `[x]` confirmed / `[~]` partial / `[ ]` no / `[n/a]`.
2. **For any `[ ]`**, either resolve before wiring up, or explicitly accept the risk (with a named owner) in the PR description.
3. **Write the dependency row** into `docs/integration/service-map.md` under "Downstream dependencies".
4. **Code the integration** following the decisions above (timeout, retries, failure mode, etc.).
5. **Add a contract test** if reasonable (see `integration-contract-tests`).

## Anti-patterns

- "Just call it; we'll add a timeout later." A call without a timeout will eventually hang the whole service.
- Wrapping someone else's SDK without reading its retry/timeout defaults. They are often wrong for your use case.
- Treating an internal service as more reliable than an external one. Internal services routinely have *worse* SLAs than well-known SaaS.
- Adding a paid API without a budget alarm.

## Output

- Checklist resolved in the PR description.
- Service map updated.
- Code with the agreed timeout / retry / failure-mode behavior.
