---
name: docs-directory-keeper
description: Create and maintain the standard docs/ directory tree on any project — prds/, plans/, decisions/, retros/, progress/, architecture/, postmortems/, qa/, api/. Use when starting a new project, when docs/ is missing or partial, or when the user asks "set up docs", "where should this go", or "make sure the structure is right".
---

# docs-directory-keeper

## Purpose

Every project that uses this skill library has the same `docs/` layout. Predictable structure means humans, QA, and agents can all find the right artifact without asking.

## When to use

- Starting a new project.
- `docs/` is missing or has a non-standard shape.
- User says: "set up docs", "where should this go", "make sure the structure is right", "scaffold the docs".
- Any other skill in this library is about to write a file under `docs/` and the parent directory doesn't exist yet.

## The standard layout

```
docs/
├── README.md              ← index of the docs/ tree itself
├── prds/                  ← Product Requirements Docs (owned by prd-creation)
├── plans/
│   ├── CURRENT.md         ← the live phase/story plan (owned by story-breakdown / phased-implementation)
│   └── archive/           ← prior CURRENT.md snapshots
├── decisions/             ← ADRs, numbered NNNN-*.md (owned by adr-writer)
│   └── log.md             ← lightweight decision log (owned by decision-log)
├── retros/                ← end-of-phase retrospectives (owned by sprint-retrospective)
├── progress/
│   ├── CURRENT.md         ← the current state-of-the-world snapshot
│   ├── handoffs/          ← per-session handoff notes (owned by handoff-prep)
│   └── snapshots/         ← context snapshots (owned by context-snapshot)
├── architecture/
│   ├── system.drawio      ← top-level system diagram (owned by drawio-architect)
│   └── ...                ← additional diagrams as needed
├── postmortems/           ← incident writeups (owned by incident-postmortem)
├── deploys/               ← per-deploy checklists and rollback plans (owned by deploy-checklist / rollback-plan)
├── qa/                    ← QA test plans (owned by qa-test-plan)
├── api/                   ← OpenAPI / Swagger specs (owned by swagger-openapi-spec)
├── bugs/                  ← bug investigation writeups (owned by bug-investigation)
├── security/              ← threat models, audit reports, PII + secrets policy (owned by security/*)
│   ├── threat-models/
│   ├── dependency-audits/
│   ├── pii-inventory.md
│   └── secrets-policy.md
├── standards/             ← code standards docs (owned by code-standards/*)
│   ├── style-guide.md
│   ├── error-handling.md
│   ├── logging.md
│   ├── naming.md
│   ├── typing.md
│   └── linting.md
├── performance/           ← perf budgets, investigations, load tests, DB tuning (owned by performance/*)
│   ├── budgets.md
│   ├── investigations/
│   ├── load-tests/
│   └── db/
├── cicd/                  ← pipeline, branch protection, release strategy, env-parity (owned by cicd/*)
│   ├── pipeline.md
│   ├── branch-protection.md
│   ├── release-strategy.md
│   ├── release-flow.md
│   └── environment-parity.md
├── integration/           ← service map and contract policy (owned by integration/*)
│   ├── service-map.md
│   └── api-contract-policy.md
└── onboarding.md          ← getting-started doc (owned by onboarding-walkthrough)
```

## Process

1. **Scan** the current project for any of the directories above.
2. **For each missing directory**, create it with a `.gitkeep` (so empty dirs survive in git) and a one-line `README.md` describing its purpose.
3. **Create `docs/README.md`** at the top if missing — a 1-screen index pointing to each subdir, linking to the skill that owns it.
4. **Create `docs/progress/CURRENT.md`** if missing with a starter: "Project initialized. No active work yet."
5. **Create `docs/plans/CURRENT.md`** if missing with a starter: "No active plan. Run story-breakdown to create one." (This satisfies the phased-implementation hook for early scaffolding work.)
6. **Don't move existing files.** If a project already has docs in a different shape, surface a migration recommendation but don't silently relocate things.

## What this skill does NOT do

- Invent new top-level directories. If you need one, propose it in a PR to this repo so all projects pick it up consistently.
- Write the actual content of PRDs, plans, ADRs, etc. Other skills own that.

## Output

A populated `docs/` tree.
