---
name: performance-budget
description: Define and commit performance budgets for the project — p95/p99 API latency, page weight, render budget, memory ceiling, build time — and wire CI enforcement so regressions fail the build. Use when starting a new project, defining SLOs, before a release, or when the user says "perf budget", "performance SLO", "Core Web Vitals targets", "latency target", "page weight budget".
---

# performance-budget

## Purpose

A budget is a number the team is willing to defend. Without one, "fast enough" drifts. With one, every PR knows whether it took or gave back budget. This skill establishes the budgets, commits them as code, and wires CI to enforce them.

## When to use

- Starting a new project or service.
- Defining SLOs / SLAs.
- Before a release (sanity-check budgets are still met).
- After an incident caused by perf regression.
- User says: "perf budget", "performance SLO", "Core Web Vitals", "latency target", "page weight budget", "how fast should this be".

## Process

1. **Identify the user-visible perf surfaces** that matter for this project:
   - **HTTP API**: p50, p95, p99 latency per endpoint or per endpoint group; error rate; throughput ceiling.
   - **Web frontend**: LCP, INP, CLS (Core Web Vitals); TTFB; total page weight; JS bundle size; render time on the slowest supported device.
   - **Background jobs**: per-job p95 duration; queue lag SLO.
   - **Build / dev loop**: cold build time; hot reload time; test-suite runtime.
   - **Resources**: memory ceiling per instance; DB connection count.
2. **Set numbers, not adjectives.** "Fast" is not a budget. `p95 < 200ms`, `LCP < 2.5s on Moto G4 / 4G`, `bundle < 200KB gzipped`, `cold build < 30s` — those are budgets.
3. **Anchor budgets to the user / business** where possible:
   - "Search endpoint p95 < 200ms" because user research shows abandonment >300ms.
   - "LCP < 2.5s" because Core Web Vitals "good" threshold.
   - "Build < 30s" because PR cycle time matters.
4. **Commit the budgets**:
   - **API**: as thresholds in the load-test config (`k6`, `vegeta`, `locust`).
   - **Frontend**: in `lighthouserc.json` / `lighthouse-ci`, `bundlesize.config.js`, or framework-native budget files.
   - **Build / test time**: a CI check that fails if `time` exceeds X.
   - **Memory**: container resource limits; an OOM alert.
5. **Wire CI to fail on breach** — not just warn. A non-blocking budget is not a budget.
6. **Write `docs/performance/budgets.md`** (living single doc, refreshed when budgets change) with:
   - Each budget, the number, the rationale, the enforcement mechanism.
   - **Date of last review** + owner per budget.
   - **Exceptions** with named owner and sunset date.
7. **Schedule a quarterly review** — budgets that aren't revisited become aspirational.

## Anti-patterns

- **Budgets without enforcement.** "We aim for <200ms" with no CI check is a wish.
- **Aggregate budgets only.** Setting just an overall p95 hides slow long-tail endpoints. Set per-area budgets.
- **Budgets from nowhere.** If the rationale is "feels right", document that explicitly and revisit. Better: anchor to user research or industry baselines.
- **No mobile / slow-network budget.** A site that's fast on the dev's M2 Max is not necessarily fast.

## What this skill does NOT do

- Investigate why something is slow (see `performance-investigation`).
- Design specific load tests (see `load-test-plan`).
- Decide *what* to cache (see `caching-strategy`).

## Output

`docs/performance/budgets.md` plus CI config changes.
