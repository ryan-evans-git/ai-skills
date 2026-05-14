---
name: twelve-factor-checklist
description: Audit a service against the twelve-factor app principles — codebase, dependencies, config, backing services, build/release/run, processes, port binding, concurrency, disposability, dev/prod parity, logs, admin processes. Use when starting a new service, when preparing for cloud deployment, when the user says "twelve factor", "12-factor", "cloud-native readiness", "containerize this".
---

# twelve-factor-checklist

## Purpose

The 12-factor app principles are the closest thing to "deployable hygiene" that the industry agrees on. This skill walks each principle as a checklist and produces a report under `docs/architecture/twelve-factor-audit.md`.

## When to use

- Starting a new service from scratch.
- Preparing an existing service for containerization / cloud deploy.
- Onboarding a service to a new platform (Kubernetes, ECS, Cloud Run, Fly, Render, Vercel).
- User says: "twelve factor", "12-factor", "cloud-native readiness", "containerize this", "ready to deploy".

## The twelve factors (with concrete checks)

### 1. Codebase
One codebase tracked in revision control, many deploys.
- [ ] One repo per service (or a clearly-scoped path in a monorepo).
- [ ] No "production-only" branch divergence — all deploys come from `main` (or a release branch with a clear cherry-pick policy).

### 2. Dependencies
Explicitly declare and isolate dependencies.
- [ ] All deps pinned in a manifest (`pyproject.toml` + lockfile / `package-lock.json` / `Cargo.lock` / `go.sum`).
- [ ] No reliance on system-installed packages.
- [ ] Reproducible install (`pip install -e .` from a clean checkout works).
- [ ] No global tools required to build (or they're in a containerized build).

### 3. Config
Store config in the environment.
- [ ] Config from env vars, NEVER hardcoded.
- [ ] `.env.example` exists with every required variable name + placeholder.
- [ ] Real `.env` is in `.gitignore`.
- [ ] Production secrets via a secrets manager, not env files on disk (`secrets-hygiene`).
- [ ] Config and code are independently swappable — same artifact deploys to dev/staging/prod with different env.

### 4. Backing services
Treat backing services (DB, queue, cache, external APIs) as attached resources.
- [ ] Connection strings come from config; swap-able without code changes.
- [ ] Local dev points at a local backing service; staging at staging's; prod at prod's. Same code.
- [ ] No assumption that a backing service is "always there" — every call has timeout + failure mode (`resilience-patterns`).

### 5. Build, release, run
Strictly separate build and run stages.
- [ ] Build produces an artifact (container image, binary, package).
- [ ] Release combines build + config for a specific environment.
- [ ] Run executes the release.
- [ ] Same build promotes through environments — see `artifact-promotion`.
- [ ] No `npm install` / `pip install` at runtime startup.

### 6. Processes
Execute the app as one or more stateless processes.
- [ ] No in-memory session state. Sessions in Redis / a JWT.
- [ ] No on-disk session state.
- [ ] Uploaded files go to object storage, not local disk.
- [ ] Restarting a process loses nothing important.
- [ ] Multiple replicas can run simultaneously without coordination.

### 7. Port binding
Export services via port binding.
- [ ] App is self-contained; binds to a port via env var (e.g. `PORT`).
- [ ] No reliance on an external web server (Apache mod_php-style).

### 8. Concurrency
Scale out via the process model.
- [ ] Workload types are split into separate process types (`web`, `worker`, `scheduler` — Procfile-style).
- [ ] Horizontal scaling is achievable (add more replicas) without per-replica coordination.

### 9. Disposability
Maximize robustness with fast startup and graceful shutdown.
- [ ] Cold start under 30s (ideally under 10s).
- [ ] Receives `SIGTERM` → drains in-flight requests → exits cleanly within ~30s.
- [ ] Workers handle re-delivery of any task interrupted by a restart (idempotent).
- [ ] Health endpoints respond before serving traffic (`/healthz`, `/readyz`).

### 10. Dev/prod parity
Keep development, staging, and production as similar as possible.
- [ ] Same OS / runtime / language version everywhere.
- [ ] Same backing services (Postgres in dev, not SQLite-in-dev / Postgres-in-prod).
- [ ] Time gap between commit and deploy is hours/days, not weeks (CI/CD enables this).
- [ ] See `environment-parity` for the deeper checklist.

### 11. Logs
Treat logs as event streams.
- [ ] App writes logs to stdout/stderr as structured JSON.
- [ ] No log files on disk that the app manages.
- [ ] Log aggregation happens at the platform level (CloudWatch, Loki, Datadog, etc.).
- [ ] See `logging-standards` for the content requirements.

### 12. Admin processes
Run admin/management tasks as one-off processes.
- [ ] Migrations, REPLs, data-fix scripts run via the same release artifact.
- [ ] No "ssh into the server" workflow — anything that's needed has a documented command.
- [ ] Admin commands are version-controlled and reviewable.

## Process

1. Walk the 12 factors. Mark `[x]` / `[~]` / `[ ]` / `[n/a]` with one-line evidence per item.
2. **For any `[ ]` or `[~]`**, list the gap and the rough fix.
3. **Prioritize gaps**:
   - **P0**: Factors 3, 6, 11 — getting these wrong causes prod incidents.
   - **P1**: Factors 5, 9, 10 — getting these wrong causes deploy/scaling pain.
   - **P2**: the rest.
4. **Write to `docs/architecture/twelve-factor-audit.md`** with the checklist + findings + prioritized backlog.
5. **File follow-up stories** on `docs/plans/CURRENT.md` for the P0/P1 gaps.

## What this skill does NOT do

- Apply zealously to non-app code (CLIs, batch tools, library packages don't all fit 12-factor cleanly).
- Replace platform-specific readiness checks (Kubernetes probes, AWS App Runner constraints, etc.). 12-factor is a baseline; platforms add their own.

## Output

`docs/architecture/twelve-factor-audit.md`
