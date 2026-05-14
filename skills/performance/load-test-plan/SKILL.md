---
name: load-test-plan
description: Design realistic load tests for a service or endpoint — pick scenarios (steady, ramp, spike, soak), set thresholds against the perf budget, choose a tool, identify dependencies, and write a runnable plan. Use before releases of latency-sensitive features, when capacity planning, or when the user says "load test", "stress test", "k6", "locust", "capacity test".
---

# load-test-plan

## Purpose

Most production perf surprises come from "we never tested it under realistic load." This skill designs load tests that exercise the system the way real users actually will — not just one happy-path endpoint hammered as fast as possible.

## When to use

- Before a release of any latency-sensitive feature.
- Capacity planning for an expected traffic increase (marketing event, customer ramp, integration go-live).
- After scaling infrastructure (new region, new instance class, new DB tier).
- User says: "load test", "stress test", "capacity test", "k6", "locust", "vegeta", "gatling", "how much load can it handle".

## Process

1. **Define what success means.** Pull from `docs/performance/budgets.md`:
   - p95 / p99 latency targets per endpoint group.
   - Error rate ceiling (e.g. < 0.1% 5xx).
   - Throughput floor (e.g. 200 req/s sustained).
   - Resource ceiling (e.g. CPU < 70% per instance).
2. **Pick the scenarios.** Don't run one. Run a mix:
   - **Steady-state** — expected production load, sustained for 10–30 min. Validates the system runs fine in normal times.
   - **Ramp** — start at 0, increase to 2x expected peak over 10–15 min. Finds the breaking-point load.
   - **Spike** — instantaneous jump from baseline to 2–5x peak. Tests autoscaling, connection-pool sizing, queue depths.
   - **Soak** — expected load for 4–12 hours. Surfaces memory leaks, connection-pool exhaustion, log-disk fill.
3. **Use a realistic workload mix**, not just one endpoint:
   - Map traffic by endpoint: which routes get what % of real traffic. Use access logs.
   - Mix authn flows: a real user hits login, then does many other things, then logs out — not just 1000 logins.
   - Include caching realistically: warm cache vs. cold cache produce very different numbers.
   - Use realistic data sizes (pagination boundaries, large payloads, varied input lengths).
4. **Identify environmental dependencies** the test will hit:
   - DB — is it a prod-equivalent instance, or a tiny dev one?
   - External APIs — mocked, sandboxed, or real?
   - Caches — warm, cold, or skipped?
   - Rate limits — disabled for the test, or part of what's being measured?
   - **Document each.** Otherwise the test result is unprovable.
5. **Pick the tool** per stack:
   | Need | Tool |
   | --- | --- |
   | HTTP scriptable, modern UX | `k6` |
   | Python-scripted scenarios | `locust` |
   | Simple high-throughput | `vegeta`, `wrk` |
   | JVM, complex scenarios | `gatling` |
   | gRPC | `ghz`, `k6` with the gRPC extension |
   | Browser-driven (real-browser) | `Playwright` + a load-test harness, or `k6 browser` |
6. **Set thresholds in the test config** so the test fails when the budget breaks. A green load test with no thresholds is no signal.
7. **Decide where it runs**:
   - **Locally** — for development iteration. Not for go/no-go.
   - **Pre-prod env that matches prod** — for release sign-off.
   - **Production with feature flags** — for shadow / canary tests when pre-prod can't be made representative.
8. **Write the plan** to `docs/performance/load-tests/YYYY-MM-DD-feature-or-service.md` with:
   - **Goal** — what question this answers.
   - **Targets** — citing the perf budget.
   - **Scenarios** — each with shape (steady / ramp / spike / soak), duration, concurrency profile, traffic mix, thresholds.
   - **Environment** — instance sizes, DB tier, caches state, rate limits, monitoring.
   - **Run command(s)** — exact commands so someone can reproduce.
   - **What to watch during the run** — dashboards, log streams, alerts.
   - **Exit criteria** — when the run is "done".
   - **Result template** — table to fill in after the run.
9. **After running**, append actual results + observations to the same doc.
10. **File follow-up stories** on `docs/plans/CURRENT.md` for any threshold breach.

## Anti-patterns

- **One endpoint hammered.** Doesn't represent real users; misses contention with other paths.
- **Tiny dataset.** Test DB with 1000 rows; prod has 100M. Result tells you nothing.
- **No warmup.** First-N-requests cold-start skew the numbers.
- **No assertions / thresholds.** Test passes if the tool exits 0, even when latency is awful.
- **Run once, never again.** Without scheduled re-runs, the test is a snapshot, not a guard.

## What this skill does NOT do

- Set the budgets themselves (see `performance-budget`).
- Investigate why a load test failed (see `performance-investigation`).

## Output

`docs/performance/load-tests/YYYY-MM-DD-feature-or-service.md` plus the load-test script committed in-repo.
