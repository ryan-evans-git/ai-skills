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
- [data-retention-policy](skills/security/data-retention-policy/SKILL.md) — Per-class retention rules + enforcement; living `docs/security/retention-policy.md`.
- [right-to-delete](skills/security/right-to-delete/SKILL.md) — End-to-end user-deletion procedure spanning primary stores, derived data, caches, third parties, and backups. Map at `docs/security/deletion-map.md`.
- [audit-log-retention](skills/security/audit-log-retention/SKILL.md) — Separate retention + integrity policy for compliance / audit logs; spec at `docs/security/audit-log-spec.md`.

## code-standards

- [style-guide-keeper](skills/code-standards/style-guide-keeper/SKILL.md) — Maintain `docs/standards/style-guide.md` pointing at the authoritative external guide per language plus project deviations.
- [error-handling-standards](skills/code-standards/error-handling-standards/SKILL.md) — Typed errors at boundaries, no silent swallow, log-once-at-the-top; doc at `docs/standards/error-handling.md`.
- [logging-standards](skills/code-standards/logging-standards/SKILL.md) — Structured logging, required context fields, no PII; doc at `docs/standards/logging.md`.
- [naming-conventions](skills/code-standards/naming-conventions/SKILL.md) — File / function / variable / test / branch / commit naming; doc at `docs/standards/naming.md`.
- [typing-strictness](skills/code-standards/typing-strictness/SKILL.md) — Enable strict type checking (mypy/pyright/TS strict/clippy); doc at `docs/standards/typing.md`.
- [linter-config](skills/code-standards/linter-config/SKILL.md) — Pick and configure linters/formatters; doc at `docs/standards/linting.md`.

## performance

- [performance-budget](skills/performance/performance-budget/SKILL.md) — Define and CI-enforce budgets (latency, page weight, build time); living `docs/performance/budgets.md`.
- [performance-investigation](skills/performance/performance-investigation/SKILL.md) — Measure → profile → hotspot → fix → benchmark → write up. Per-investigation doc under `docs/performance/investigations/`.
- [load-test-plan](skills/performance/load-test-plan/SKILL.md) — Realistic steady/ramp/spike/soak load tests with thresholds; output to `docs/performance/load-tests/`.
- [query-performance](skills/performance/query-performance/SKILL.md) — Read EXPLAIN plans, fix N+1, add the right indexes, add regression guards; writeups under `docs/performance/db/`.
- [caching-strategy](skills/performance/caching-strategy/SKILL.md) — Five-question framework before adding a cache; living `docs/architecture/caching.md`.

## architecture

- [api-design](skills/architecture/api-design/SKILL.md) — Opinionated conventions for REST resource modeling, status codes, pagination, errors, idempotency, money/time.
- [resilience-patterns](skills/architecture/resilience-patterns/SKILL.md) — Timeouts, retries, idempotency keys, circuit breakers, bulkheads, graceful degradation, backpressure, health checks.
- [service-boundaries](skills/architecture/service-boundaries/SKILL.md) — Force-based decision framework for when to extract a new service vs. keep as a module.
- [data-modeling](skills/architecture/data-modeling/SKILL.md) — Schema conventions: PKs, naming, nullability, FKs, soft deletes, JSON columns, multi-tenancy.
- [twelve-factor-checklist](skills/architecture/twelve-factor-checklist/SKILL.md) — Audit a service against the twelve-factor app principles; report at `docs/architecture/twelve-factor-audit.md`.

## cicd

- [pipeline-design](skills/cicd/pipeline-design/SKILL.md) — Stages, parallelization, caching, fail-fast, required vs. optional checks; doc at `docs/cicd/pipeline.md`.
- [branch-protection](skills/cicd/branch-protection/SKILL.md) — Standard branch protection rule set + CODEOWNERS; doc at `docs/cicd/branch-protection.md`.
- [artifact-promotion](skills/cicd/artifact-promotion/SKILL.md) — Build once, promote the same artifact through environments; release flow at `docs/cicd/release-flow.md`.
- [release-strategy](skills/cicd/release-strategy/SKILL.md) — Cadence, versioning scheme, tagging, release notes, authority; doc at `docs/cicd/release-strategy.md`.
- [environment-parity](skills/cicd/environment-parity/SKILL.md) — Parity matrix across dev/CI/staging/prod; living `docs/cicd/environment-parity.md`.
- [flaky-test-management](skills/cicd/flaky-test-management/SKILL.md) — Detect → quarantine → root-cause → fix → re-enable lifecycle with budget and time limit.

## integration

- [service-map](skills/integration/service-map/SKILL.md) — Living service map of upstream callers and downstream dependencies; `docs/integration/service-map.md`.
- [upstream-callers](skills/integration/upstream-callers/SKILL.md) — Consult the service map and classify breaking-vs-additive before any public API change.
- [downstream-dependencies](skills/integration/downstream-dependencies/SKILL.md) — Pre-integration checklist covering contract, SLA, failure mode, observability, and cost.
- [api-contract-evolution](skills/integration/api-contract-evolution/SKILL.md) — Versioning, deprecation, sunset policy; living `docs/integration/api-contract-policy.md`.
- [integration-contract-tests](skills/integration/integration-contract-tests/SKILL.md) — Schema or pact-style contract tests wired into CI.

## dev-environment

- [dev-storage-audit](skills/dev-environment/dev-storage-audit/SKILL.md) — Find where disk is *actually* going across Docker, project caches, worktrees, IDE caches, downloads. Run this first.
- [docker-cleanup](skills/dev-environment/docker-cleanup/SKILL.md) — Reclaim Docker disk safely; per-resource decision tree; never silently destroy data.
- [worktree-cleanup](skills/dev-environment/worktree-cleanup/SKILL.md) — Find stale git worktrees and orphan branches; check for uncommitted work before removing.
- [dependency-cache-cleanup](skills/dev-environment/dependency-cache-cleanup/SKILL.md) — Per-project (`node_modules`, `target`, `.venv`) and user-level caches; safety + recency scoring.

## ai-engineering

- [prompt-engineering](skills/ai-engineering/prompt-engineering/SKILL.md) — Prompts as code: structure, versioning, eval-gating; under `prompts/` with frontmatter.
- [llm-evals](skills/ai-engineering/llm-evals/SKILL.md) — Golden sets, graders, regression gating; suites under `tests/evals/`.
- [llm-cost-management](skills/ai-engineering/llm-cost-management/SKILL.md) — Visibility-first; prompt caching, routing, batch, context trimming. Living `docs/ai/cost-management.md`.
- [hallucination-guardrails](skills/ai-engineering/hallucination-guardrails/SKILL.md) — Schema, grounding, refusal, verification; layered defense per feature.
- [rag-design](skills/ai-engineering/rag-design/SKILL.md) — Chunking, hybrid retrieval, reranking, citation grounding, eval discipline.
- [agent-design](skills/ai-engineering/agent-design/SKILL.md) — Justify the agent; design tools, control flow, safety scope, observability, evals.
- [llm-safety](skills/ai-engineering/llm-safety/SKILL.md) — Prompt-injection defense, jailbreak resistance, scoped tool use, adversarial evals.

## observability

- [metrics-design](skills/observability/metrics-design/SKILL.md) — RED + USE + golden signals; metric inventory at `docs/observability/metrics-inventory.md`.
- [slo-definition](skills/observability/slo-definition/SKILL.md) — SLI / SLO / error budget + policy that triggers on depletion.
- [alerting-policy](skills/observability/alerting-policy/SKILL.md) — Three tiers (page / ticket / log); runbook-gated paging; symptom-based.
- [dashboard-design](skills/observability/dashboard-design/SKILL.md) — Dashboards answer one question; service-health, funnel, capacity, cost.
- [distributed-tracing](skills/observability/distributed-tracing/SKILL.md) — OTel, context propagation, sampling, log/metric linkage.
- [synthetic-monitoring](skills/observability/synthetic-monitoring/SKILL.md) — Outside-in probes for uptime, journeys, contracts.

## finops

- [cloud-cost-budget](skills/finops/cloud-cost-budget/SKILL.md) — Per-service / team / feature budgets + alerts + response policy; `docs/finops/budgets.md`.
- [resource-right-sizing](skills/finops/resource-right-sizing/SKILL.md) — Quarterly audit; downsize / change family / change tier with measured savings.
- [idle-resource-audit](skills/finops/idle-resource-audit/SKILL.md) — Find unused resources (orphan volumes, idle instances, dormant LBs); safe staged decommission.
- [cost-attribution](skills/finops/cost-attribution/SKILL.md) — Per-feature / per-customer / per-team showback; unit economics.
