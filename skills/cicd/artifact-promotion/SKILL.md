---
name: artifact-promotion
description: Build the deployable artifact once and promote the SAME artifact through environments (dev → staging → prod) by changing only the configuration around it. Use when setting up a deploy pipeline, when "works in staging, fails in prod" happens, or when the user says "promotion", "build once", "artifact registry", "release pipeline".
---

# artifact-promotion

## Purpose

If you build a fresh artifact for each environment, you've shipped a version of the code that was never tested. "Build once, promote everywhere" is the canonical fix: each environment gets the exact same bytes, configured differently.

## When to use

- Setting up a deploy pipeline for a new service.
- After a "passed staging but failed prod" incident.
- When dev/staging/prod artifacts diverge.
- User says: "promotion", "build once", "artifact registry", "release pipeline", "same image to all envs".

## The model

```
[ commit on main ]
       ↓
[ CI runs full pipeline → builds artifact X tagged with the commit SHA ]
       ↓
[ X uploaded to artifact registry — once, immutable ]
       ↓
   ┌─────────────────┬─────────────────┬───────────────┐
   ↓                 ↓                 ↓               ↓
[ deploy X    ]   [ deploy X    ]   [ deploy X    ]
[ to dev      ]   [ to staging  ]   [ to prod     ]
[ with dev    ]   [ with staging]   [ with prod   ]
[ config      ]   [ config      ]   [ config      ]
```

The artifact never changes between environments. Configuration is injected at deploy time.

## Process

1. **Build phase produces an artifact tagged immutably** with the commit SHA (and optionally a semver tag):
   - **Container image**: `registry.example.com/svc/app:<sha>` (and `:1.2.3` for releases).
   - **Binary**: SHA-named binary in object storage.
   - **Package**: published to a registry under a version that matches the SHA / release tag.
2. **Push the artifact to a registry** that all environments read from. One source of truth.
3. **Sign the artifact** if the toolchain supports it (cosign, GPG). Verify the signature before deploying — catches tampering and accidental wrong-image deploys.
4. **Deploy by reference, not by rebuild.** The deploy job pulls `app:<sha>` and starts it with environment-specific config. No `docker build` in the deploy step.
5. **Config injected at deploy time**:
   - Env vars from the platform's secret store.
   - Mounted config files from a config repo (versioned).
   - No baked-in environment names. The artifact doesn't know whether it's running in dev or prod.
6. **Promotion happens by tagging or by deploy event** — not by rebuilding:
   - Add a new tag to the same image: `app:staging-approved` → `app:prod-approved`.
   - Or: trigger the prod deploy with the same `<sha>` the staging deploy used.
7. **Document the promotion path** in `docs/cicd/release-flow.md`:
   - What env is the first stop after build?
   - What gates promote it to the next env?
   - Who can approve a prod promotion?
   - How is rollback handled (`rollback-plan`)?

## Anti-patterns

- **`docker build` in the prod deploy job.** Means prod just got a freshly-built image with potentially-different base layers / deps than staging.
- **Different Dockerfiles per environment.** Multi-stage Dockerfiles with env-specific stages = different artifacts.
- **Mutable tags** (`app:latest`, `app:staging`) used in deploys without recording which SHA they pointed at. You can't reproduce what was deployed.
- **Building from a feature branch for staging, then re-building from `main` for prod.** Different code, different bugs.
- **Promoting by re-running CI.** CI is for build + test, not for promotion.

## Verifying the promotion model

A quick test: for a recent prod deploy, can you produce the exact artifact hash that's running, and run that same artifact locally? If not, the promotion model is broken.

## What this skill does NOT do

- Specify which registry to use. Whatever the platform offers (GHCR, ECR, GCR, Artifact Registry, Quay).
- Define release cadence (`release-strategy`).
- Define what's checked before promotion (`deploy-checklist`).

## Output

- CI / deploy config that produces one artifact and promotes by reference.
- `docs/cicd/release-flow.md` describing the promotion path.
