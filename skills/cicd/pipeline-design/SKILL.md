---
name: pipeline-design
description: Design or audit a CI/CD pipeline — stages, parallelization, caching, fail-fast, required vs. optional checks, time budget, artifact handoff. Use when setting up CI for a new project, when CI is slow or unreliable, or when the user says "CI pipeline", "GitHub Actions", "build pipeline", "speed up CI", "why is CI slow".
---

# pipeline-design

## Purpose

A good pipeline is fast, fail-fast, and informative: it tells you within minutes whether a change is safe, and exactly what's broken when it isn't. This skill is the design playbook — tool-agnostic, with specific snippets for common runners.

## When to use

- Setting up CI for a new project.
- Existing CI is slow (>10 min) or flaky.
- Adding new stages (e.g. security scan, contract tests).
- User says: "CI pipeline", "GitHub Actions", "build pipeline", "speed up CI", "why is CI slow", "pipeline design".

## Default stage layout

A PR pipeline should run these in roughly this order, parallel where possible:

```
[ trigger: PR opened/updated ]
       │
       ├── lint / format check           (fastest, ~30s)
       ├── type check                    (~1m)
       ├── unit tests                    (~1-3m)
       │      │
       │      ├── coverage report
       │      └── junit upload
       │
       ├── build artifact                (~1-5m)
       │      │
       │      └── upload to registry/cache
       │
       ├── security scan                 (parallel with build)
       │      ├── dependency audit
       │      ├── SAST (semgrep/bandit/codeql)
       │      └── secret scan (gitleaks)
       │
       └── integration / contract tests  (depends on build artifact)
              │
              └── e2e tests              (only if other stages green)
```

Production deploy pipeline (post-merge) adds:
```
└── deploy to staging
       ↓
└── smoke tests + canary perf check
       ↓
└── promote to prod (manual gate for now; automated when SLOs allow)
```

## Principles

### Fail fast
- **Order stages cheap → expensive.** Lint runs before unit tests, which run before e2e. A formatting error fails in 30 seconds, not 20 minutes.
- **Fail the whole pipeline on first required-stage failure.** Don't keep running optional stages just for "more info" if a required stage has already failed.

### Parallelize aggressively
- Lint, type check, unit tests, security scans can all run in parallel.
- Within a stage, shard tests (`pytest-xdist`, `jest --workers`, `cargo nextest`, `go test -parallel`).
- Cap parallelism at runner capacity to avoid starvation.

### Cache
- **Dependency caches** (`pip`, `npm`, `cargo`, `go mod`) keyed on lockfile hash — restore from cache, install missing.
- **Build caches** where the toolchain supports (`turbo`, `nx`, `sccache`, `bazel`).
- **Layer caches** for container builds (Buildkit cache, registry cache).
- Invalidate when you must, but be deliberate — cache invalidation is the #1 cause of mysterious CI slowness.

### Time budget
- PR pipeline target: **under 10 minutes** on the critical path.
- If you're over, profile: which stage dominates? Speed it up (shard, cache, drop redundancy).
- A 20-minute pipeline means developers context-switch away → real cost.

### Required vs. optional
- **Required checks** (block merge): lint, type, unit tests, security scans, build.
- **Optional checks** (informational): coverage delta, perf benchmark, e2e if flaky.
- Don't block on flaky stages — quarantine and fix the flake (`flaky-test-management`).

### Reproducibility
- A green PR pipeline should produce the same result for the same SHA every time.
- No "rerun until it works." If a stage needs that, it's a bug to fix, not a button to press.

### Visibility
- Every failing stage links to logs that point at the actual error within 3 clicks.
- Test output is in the platform's native test reporter, not just stdout.
- Build artifacts (logs, screenshots, traces) are uploaded for failed runs.

## Process

1. **Map the project's actual checks**: what currently runs, in what order, taking how long.
2. **Profile**: which stages dominate runtime? (Most CI runners surface this.)
3. **Identify the critical path** — the longest serial chain. That's the floor on pipeline time.
4. **Apply the principles** to flatten/parallelize/cache.
5. **Define required vs. optional** — move flaky or low-signal checks to optional.
6. **Commit the config** under `.github/workflows/` (or equivalent). One workflow per logical pipeline.
7. **Write `docs/cicd/pipeline.md`** with a high-level diagram + rationale for non-default choices. Keep it short.
8. **Pair with `branch-protection`** — required CI checks listed there must match the pipeline's required stages.

## Anti-patterns

- **Sequential by default.** Stages that don't depend on each other should run in parallel.
- **Re-running everything on every PR commit** without caching. Most pushes change one file.
- **One giant workflow.** Hard to reason about; rerun granularity is poor. Split per concern.
- **Untriaged failures.** "It's flaky" without a tracking issue means it'll be flaky forever.
- **Building twice** — once in CI, once in deploy. Build once; promote.

## What this skill does NOT do

- Pick a specific runner (GH Actions, CircleCI, BuildKite, Jenkins). The principles transfer.
- Cover deployment specifics — see `deploy-checklist`, `artifact-promotion`.

## Output

- CI config files at the repo root.
- `docs/cicd/pipeline.md` documenting the design.
