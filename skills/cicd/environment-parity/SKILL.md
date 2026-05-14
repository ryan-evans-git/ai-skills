---
name: environment-parity
description: Audit how similar dev, CI, staging, and production are — same runtime versions, same backing services, same config shape, same data shape — so "works in staging" implies "works in prod." Use when setting up environments, after a "works on my machine" / "works in staging" incident, or when the user says "environment parity", "dev/prod parity", "why does it work in staging but not prod".
---

# environment-parity

## Purpose

Every difference between environments is a place a bug can hide. This skill audits the differences explicitly so the team knows what they're betting on when they say "staging is green."

Complements `twelve-factor-checklist` (which calls out parity as one factor) with a much deeper concrete checklist.

## When to use

- Setting up environments for a new project.
- After a "passed staging, broke in prod" incident.
- Onboarding a service to a new environment.
- User says: "environment parity", "dev/prod parity", "why does it work in staging but not prod", "environments drifting", "staging matches prod".

## What environments to audit

At minimum:
- **Local dev** — engineer's laptop.
- **CI** — wherever tests run.
- **Staging / pre-prod** — last gate before prod.
- **Production**.

For some projects: ephemeral preview envs (per-PR), per-customer envs (for on-prem), etc.

## Parity dimensions (the audit)

For each dimension, score each environment. Flag drifts.

### Runtime
- Language version (down to the patch level — Python 3.12.3 ≠ 3.12.7).
- OS / container base image.
- Architecture (ARM vs. x86 — this catches more people than expected).
- System libraries that affect behavior (locale, timezone, OpenSSL version).

### Application
- Same artifact across envs (see `artifact-promotion`). If "different builds per env," parity is automatically broken.
- Same config *shape* (same env-var names; different values are fine).
- Same feature flags shape; states may differ.

### Backing services
- Same DB engine + major version across envs (Postgres 16 everywhere, not SQLite in dev + Postgres in prod).
- Same cache (Redis everywhere, not in-memory in dev).
- Same queue / event bus.
- Same object storage (real S3-API in dev, not local filesystem — use MinIO / LocalStack if needed).
- Same external services (sandbox/mock for paid APIs, but the *protocol* the same).

### Data
- Same schema (migrations applied consistently).
- Representative data volume in staging (not 1000 rows when prod has 100M).
- Representative data shape (long strings, unicode, edge cases — not just clean fixtures).
- PII-safe — staging shouldn't have prod PII unless explicitly anonymized.

### Configuration
- Same env-var keys defined in all envs.
- Different *values* are fine and expected (dev uses dev DB; prod uses prod DB).
- No env-only code paths (`if ENV == "dev": skip_auth()` is a parity violation AND a security bug).

### Time / region
- Document the timezone each env runs in. Recommendation: UTC everywhere.
- Document the region / data residency for each env.

### Network
- Egress rules — can the service reach what it needs in each env?
- Ingress — same routing / TLS / load balancer in staging as prod?

## Process

1. **Build the parity matrix** — environments as columns, dimensions as rows. One cell per intersection.
2. **Fill in actual values** by reading the env config / infra-as-code / runtime.
3. **Flag drifts** as either:
   - **Acceptable** — different values, same kind (DB URL differs; both are Postgres).
   - **Unacceptable** — different kind (SQLite vs. Postgres; in-memory queue vs. real one).
4. **For each unacceptable drift**, file a follow-up: how to fix or how to mitigate (e.g. "staging gets prod-like data volume monthly").
5. **Write to `docs/cicd/environment-parity.md`** — the matrix + drift status + last reviewed date.
6. **Schedule a quarterly review.** Environments drift silently; a quarterly audit catches it before an incident does.

## Anti-patterns

- **SQLite in dev, Postgres in prod.** Different SQL dialects, different concurrency model, different indexes. Will bite eventually.
- **Mocking external services in dev with hand-rolled mocks** that drift from the real protocol. Use the vendor's sandbox / a generated mock.
- **No staging data refresh policy.** Staging works against month-old data and never finds today's edge cases.
- **`if env == "dev"` code paths.** Use config / feature flags, never branch on env name.
- **"It's just staging, we'll fix it for prod."** That's how parity dies.

## What this skill does NOT do

- Configure environments. This is the audit; provisioning is platform-specific.
- Replace ephemeral preview envs (which can be a *replacement* for some staging — but only if they have parity to prod, which is the same question).

## Output

`docs/cicd/environment-parity.md` (living matrix + drift status).
