# Skills index

One-line catalog of every skill in this library.

## planning

- [prd-creation](skills/planning/prd-creation/SKILL.md) — Author a Product Requirements Doc with problem, users, goals, non-goals, success metrics, milestones.
- [story-breakdown](skills/planning/story-breakdown/SKILL.md) — Turn a PRD into vertical-slice phases → stories → tasks, written to `docs/plans/CURRENT.md`.
- [sprint-retrospective](skills/planning/sprint-retrospective/SKILL.md) — Run a structured retro at the end of a phase/sprint; output to `docs/retros/`.
- [adr-writer](skills/planning/adr-writer/SKILL.md) — Capture architectural decisions in numbered ADRs under `docs/decisions/`.
- [estimation-helper](skills/planning/estimation-helper/SKILL.md) — Three-point estimates that include testing, docs, and unknown-unknowns.

## development

- [tdd-enforcer](skills/development/tdd-enforcer/SKILL.md) — Red/green/refactor. No production code without a failing test first. **Ships with a blocking hook.**
- [phased-implementation](skills/development/phased-implementation/SKILL.md) — Refuse to write code unless a current phase plan exists. **Ships with a blocking hook.**
- [pr-description](skills/development/pr-description/SKILL.md) — Generate PR descriptions with summary, motivation, changes, test plan, screenshots, breaking changes.
- [self-review](skills/development/self-review/SKILL.md) — Pre-PR diff review against a checklist (dead code, debug statements, secrets, coverage).

## documentation

- [docs-directory-keeper](skills/documentation/docs-directory-keeper/SKILL.md) — Enforce the standard `docs/` layout and keep `docs/progress/CURRENT.md` up to date.
- [claude-md-bootstrap](skills/documentation/claude-md-bootstrap/SKILL.md) — Create / refresh the project's `CLAUDE.md` with managed house rules; pairs with the `refresh_claude_md.py` SessionStart hook.
- [drawio-architect](skills/documentation/drawio-architect/SKILL.md) — Every project has `docs/architecture/system.drawio`; update on structural changes.
- [swagger-openapi-spec](skills/documentation/swagger-openapi-spec/SKILL.md) — Every HTTP route is in an OpenAPI spec with MCP-ready `operationId`s and tool-style descriptions.
- [decision-log](skills/documentation/decision-log/SKILL.md) — Append-only lightweight log for decisions that don't merit a full ADR.
- [changelog-keeper](skills/documentation/changelog-keeper/SKILL.md) — Maintain `CHANGELOG.md` per Keep-a-Changelog convention.
- [readme-generator](skills/documentation/readme-generator/SKILL.md) — Generate or refresh a README with a known structure.

## quality

- [qa-test-plan](skills/quality/qa-test-plan/SKILL.md) — Author manual + automated QA test plans per feature; for QA resources to drive directly.
- [bug-investigation](skills/quality/bug-investigation/SKILL.md) — Repro → minimize → root cause → fix → regression test, written up under `docs/bugs/`.
- [test-pyramid-audit](skills/quality/test-pyramid-audit/SKILL.md) — Audit unit/integration/e2e ratio and over-mocking.
- [coverage-gap-finder](skills/quality/coverage-gap-finder/SKILL.md) — Identify untested paths, especially error and edge cases.

## operations

- [incident-postmortem](skills/operations/incident-postmortem/SKILL.md) — Blameless postmortem with timeline, contributing factors, action items.
- [deploy-checklist](skills/operations/deploy-checklist/SKILL.md) — Pre-deploy verification: tests, migrations, rollback plan, feature flag, monitoring.
- [rollback-plan](skills/operations/rollback-plan/SKILL.md) — Document how to roll back every deploy (code, migrations, flags, config).

## collaboration

- [handoff-prep](skills/collaboration/handoff-prep/SKILL.md) — Write a handoff doc for the next dev or agent: state, blockers, next steps.
- [onboarding-walkthrough](skills/collaboration/onboarding-walkthrough/SKILL.md) — Generate / maintain `docs/onboarding.md` for new team members.
- [context-snapshot](skills/collaboration/context-snapshot/SKILL.md) — Capture current session state into `docs/progress/` so a future agent or human can pick up cold.

## security

- [threat-model](skills/security/threat-model/SKILL.md) — STRIDE-style threat model for a new feature, service, or significant change; output under `docs/security/threat-models/`.
- [security-review](skills/security/security-review/SKILL.md) — Diff-level review against OWASP Top 10 + common code-level vulnerabilities.
- [dependency-audit](skills/security/dependency-audit/SKILL.md) — Scan deps for CVEs and abandoned packages; report under `docs/security/dependency-audits/`.
- [secrets-hygiene](skills/security/secrets-hygiene/SKILL.md) — Scan for committed secrets, audit `.env` and `.gitignore`, maintain `docs/security/secrets-policy.md`.
- [auth-checklist](skills/security/auth-checklist/SKILL.md) — Verify every HTTP route enforces authn + authz; cross-checks OpenAPI spec against route handlers.
- [pii-data-handling](skills/security/pii-data-handling/SKILL.md) — Maintain `docs/security/pii-inventory.md` — classification + handling rules per field.

## code-standards

- [style-guide-keeper](skills/code-standards/style-guide-keeper/SKILL.md) — Maintain `docs/standards/style-guide.md` pointing at the authoritative external guide per language plus project deviations.
- [error-handling-standards](skills/code-standards/error-handling-standards/SKILL.md) — Typed errors at boundaries, no silent swallow, log-once-at-the-top; doc at `docs/standards/error-handling.md`.
- [logging-standards](skills/code-standards/logging-standards/SKILL.md) — Structured logging, required context fields, no PII; doc at `docs/standards/logging.md`.
- [naming-conventions](skills/code-standards/naming-conventions/SKILL.md) — File / function / variable / test / branch / commit naming; doc at `docs/standards/naming.md`.
- [typing-strictness](skills/code-standards/typing-strictness/SKILL.md) — Enable strict type checking (mypy/pyright/TS strict/clippy); doc at `docs/standards/typing.md`.
- [linter-config](skills/code-standards/linter-config/SKILL.md) — Pick and configure linters/formatters; doc at `docs/standards/linting.md`.
