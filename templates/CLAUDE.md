# {{project_name}}

<!--
  CLAUDE.md is loaded into Claude's context on every session in this repo.
  Keep it short — every line costs context budget.

  This file has two regions:
    1. Hand-written (the sections OUTSIDE the BEGIN/END ai-skills markers below)
       — project-specific facts. Edit freely.
    2. Managed (the section BETWEEN the markers) — regenerated each session by
       the ai-skills SessionStart hook. Do NOT hand-edit inside the markers;
       changes will be overwritten on the next session.
-->

## About this project

<One paragraph. What this project is, who uses it, what makes it different from a generic project. If you don't know yet, leave this and fill in later.>

## Stack

<Languages, frameworks, key libraries. e.g. "Python 3.12, Flask, LangChain, LangGraph, LangSmith on the backend; TypeScript + React on the frontend.">

## Project-specific conventions

<Anything Claude needs to know about THIS repo that overrides or extends the defaults in the managed section below. Examples:
  - Preferred patterns ("all DB access goes through the repository layer in src/repos/").
  - Areas to ask about before touching ("don't change anything under src/legacy/ without asking").
  - Owners ("billing code: ask @alice; ingestion: ask @bob").
  - Non-obvious gotchas ("tests/test_e2e/ requires LOCAL_DOCKER=1; skip otherwise").>

<!-- BEGIN ai-skills MANAGED — do not edit by hand; refreshed at session start by refresh_claude_md.py -->

## House rules

This project uses the [ai-skills](https://github.com/ryan-evans-git/ai-skills) shared skills library.
Library version: `{{commit_sha}}` · refreshed `{{date}}` · {{skill_count}} skills available.
See the [skills index]({{index_url}}) for the full catalog.

### Working with ambiguous requests

- **Ask only load-bearing questions.** Before significant work, scan for ambiguity. Ask 1-3 questions ONLY if the answer would change scope, architecture, API surface, data model, security posture, success criteria, or constraints. Offer a default for every question. (skill: requirements-clarification)
- **Surface everything else inline.** For non-load-bearing inferences (defaults chosen, edge cases handled, names picked), flag them in the response as you go — "Assumed X; flag if wrong." Mid-flight correction is cheaper than diff archaeology. Target 2-7 surfaced assumptions per non-trivial turn. (skill: assumption-surfacing)
- **"Just go" overrides upfront questions** — fall through to inline surfacing instead.

### Specialist subagents available

The library ships 8 subagents (installed under `~/.claude/agents/` or `.claude/agents/`) that the main agent can delegate to via the `Agent` tool. Use them when isolation matters (independent review, parallel audit, write-scoped role) rather than running the work in the main thread:

- `code-reviewer` — independent diff/PR review, read-only.
- `qa-engineer` — test plans, coverage audits, bug writeups.
- `architect` — ADRs, threat models, service-boundary analysis, API design.
- `planner` — clarify requirements + draft PRD + phase/story plan.
- `prompt-evaluator` — run eval suite for a prompt/model change; before/after delta.
- `dependency-auditor` — CVEs, abandoned packages, licenses, secrets.
- `performance-investigator` — reproduce → measure → profile → propose fix.
- `incident-responder` — drive blameless postmortems.

Delegate when the work would pollute the main thread's context or benefits from a fresh, role-scoped agent. For everyday in-thread work, apply the relevant skill directly.

### Default workflow

- **Plan before code.** Work is broken into phases → stories → tasks. The live plan is `docs/plans/CURRENT.md`. (skill: phased-implementation; enforced by `require_plan.py` hook if installed)
- **TDD by default.** Every behavior change starts with a failing test. (skill: tdd-enforcer; enforced by `require_failing_test.py` hook if installed)
- **Capture decisions.** Significant choices become ADRs under `docs/decisions/`. Quick decisions land in `docs/decisions/log.md`. (skills: adr-writer, decision-log)
- **Retros at phase boundaries.** Write to `docs/retros/`. (skill: sprint-retrospective)
- **Handoff before stopping.** Long sessions end with a handoff doc under `docs/progress/handoffs/`. (skill: handoff-prep)

### Standard `docs/` layout

```
docs/
├── prds/           plans/          decisions/      retros/
├── progress/       architecture/   postmortems/    deploys/
├── qa/             api/            bugs/           security/
└── standards/
```

(skill: docs-directory-keeper)

### Documentation expectations

- **Architecture diagram** — `docs/architecture/system.drawio` reflects the current system. (skill: drawio-architect)
- **OpenAPI spec** — every HTTP route is in `docs/api/openapi.yaml` with an MCP-ready `operationId`, summary, and agent-facing description. (skill: swagger-openapi-spec)
- **README** stays current with how to run the project. (skill: readme-generator)
- **CHANGELOG** maintained per Keep-a-Changelog. (skill: changelog-keeper)

### Code standards

- **Errors** — typed at boundaries, no silent swallow, log-once-at-the-top. See `docs/standards/error-handling.md`. (skill: error-handling-standards)
- **Logging** — structured, includes `request_id`/`trace_id`, NEVER includes PII or secrets. See `docs/standards/logging.md`. (skill: logging-standards)
- **Naming** — see `docs/standards/naming.md`. (skill: naming-conventions)
- **Types** — strict-mode checker on (mypy/pyright/TS strict/clippy). See `docs/standards/typing.md`. (skill: typing-strictness)
- **Lint/format** — config committed; pre-commit hook runs locally; CI fails on violations. See `docs/standards/linting.md`. (skill: linter-config)
- **Style** — see `docs/standards/style-guide.md`. (skill: style-guide-keeper)

### Security defaults

- **Authn + authz on every HTTP route**, deny-by-default. (skill: auth-checklist)
- **No secrets in code** — env vars or a secrets manager. Pre-commit secret scan recommended. (skill: secrets-hygiene)
- **PII** — see `docs/security/pii-inventory.md` for what's classified as PII / Sensitive and the handling rules. (skill: pii-data-handling)
- **Dependencies audited** before each release. (skill: dependency-audit)
- **Threat model** for any new auth flow, integration, or sensitive feature. (skill: threat-model)
- **Diff-level security review** before merging anything that touches user input, auth, or external calls. (skill: security-review)

### Performance defaults

- **Budgets are numbers, not adjectives.** Committed budgets live in `docs/performance/budgets.md` and are enforced in CI. (skill: performance-budget)
- **Measure before optimizing.** Use `performance-investigation` for "X is slow" — never change code on a guess.
- **DB hot path** — read `EXPLAIN` plans, fix N+1, add the right indexes; writeups under `docs/performance/db/`. (skill: query-performance)
- **Cache only after answering the five questions** in `docs/architecture/caching.md`. No silent staleness. (skill: caching-strategy)
- **Load test latency-sensitive features** before release; plans under `docs/performance/load-tests/`. (skill: load-test-plan)

### Architecture defaults

- **API design** follows the conventions in `api-design` (REST resource modeling, status codes, pagination, errors, idempotency, money/time).
- **Resilience by default** — every network call has a timeout, retry policy, idempotency strategy, and documented failure mode. (skill: resilience-patterns)
- **Don't reach for a new service.** Walk the force analysis in `service-boundaries` before extracting.
- **Schemas follow the conventions** in `data-modeling` (UUIDv7 PKs, FKs always declared, soft deletes deliberate, tenant_id leading in composite indexes).
- **Twelve-factor audit** for any deployable service: `docs/architecture/twelve-factor-audit.md`.

### Integration defaults

- **Consult `docs/integration/service-map.md` before any public-API change.** Classify as additive / subtly-breaking / breaking. (skill: upstream-callers)
- **Run the dependency checklist before adding any downstream call** — contract, SLA, failure mode, timeout, retries, observability, cost. (skill: downstream-dependencies)
- **Versioning + deprecation policy** documented at `docs/integration/api-contract-policy.md`. Sunsets are calendared, never indefinite. (skill: api-contract-evolution)
- **Contract tests** wired into CI for every active integration. (skill: integration-contract-tests)

### CI/CD defaults

- **PR pipeline under 10 min** on the critical path; fail-fast cheap → expensive. (skill: pipeline-design)
- **Required checks match pipeline stages exactly.** Branch protection enforces them. (skill: branch-protection)
- **Build once, promote everywhere.** No `docker build` in deploy steps. (skill: artifact-promotion)
- **Versioning + release strategy** documented at `docs/cicd/release-strategy.md`. (skill: release-strategy)
- **Dev/CI/staging/prod parity** audited and tracked in `docs/cicd/environment-parity.md`. (skill: environment-parity)
- **Flaky tests get quarantined within 24h, fixed within 30d, or deleted.** No forever-quarantine. (skill: flaky-test-management)

### Data lifecycle defaults

- **Retention policy** per data class at `docs/security/retention-policy.md`. Enforced, not aspirational. (skill: data-retention-policy)
- **User-deletion** walks the deletion map at `docs/security/deletion-map.md` — primary store, derived data, caches, third parties, backups. (skill: right-to-delete)
- **Audit logs** are separate from operational logs, append-only, with their own retention. Exempt from user-deletion. (skill: audit-log-retention)

### AI / LLM defaults

- **Prompts are code.** Versioned under `prompts/<name>.md` with frontmatter; eval-gated before merging. (skill: prompt-engineering)
- **Every LLM feature has an eval suite** under `tests/evals/<feature>/`. Prompt or model changes run them. (skill: llm-evals)
- **Cost visibility on day one** — every LLM call logged with feature/model/tokens/cost. Living `docs/ai/cost-management.md`. (skill: llm-cost-management)
- **Prompt caching enabled by default** for any Anthropic-API integration. Stable prefixes first, dynamic content last.
- **Structured output + refusal + confidence** in every user-facing LLM schema. (skill: hallucination-guardrails)
- **Agents only when justified** — single-completion + retrieval is the default; agents add cost, latency, and debug surface. (skill: agent-design)
- **Adversarial evals** for any user-facing LLM feature: prompt injection, jailbreak, exfiltration. (skill: llm-safety)
- **RAG citations are verifiable** — quote-match against retrieved chunks; reject if not in context. (skill: rag-design)

### Observability defaults

- **RED + USE + golden signals** as the metric baseline; inventory at `docs/observability/metrics-inventory.md`. (skill: metrics-design)
- **SLOs anchored to user-visible journeys**, with an explicit error-budget policy at `docs/observability/slos.md`. (skill: slo-definition)
- **Alerts in three tiers** (page / ticket / log); pageable alerts require a runbook. (skill: alerting-policy)
- **Dashboards answer questions**, not "all metrics." Canonical service-health + funnel dashboards per service. (skill: dashboard-design)
- **OpenTelemetry tracing**, with `trace_id` injected into every log line. (skill: distributed-tracing)
- **Synthetic probes** from multiple regions for any user-facing service. (skill: synthetic-monitoring)

### FinOps defaults

- **Required tags on every resource** (`environment`, `service`, `team`, `cost-center`); enforced via policy.
- **Budgets at multiple levels** (account, service, team, feature) with forecast-based alerts. Living `docs/finops/budgets.md`. (skill: cloud-cost-budget)
- **Quarterly right-sizing audit** + monthly idle-resource audit. (skills: resource-right-sizing, idle-resource-audit)
- **Per-feature / per-customer attribution** instrumented; reports at `docs/finops/cost-attribution.md`. (skill: cost-attribution)

### Frontend defaults

- **Design with intent.** Avoid the generic AI aesthetic; build a real palette + type hierarchy + spacing. (skill: frontend-design)
- **Design system anchored on tokens** — `docs/frontend/design-system.md` is the source of truth; Storybook + visual regression keep it honest. (skills: design-system-keeper, visual-regression-testing)
- **Accessibility is required, not a bonus.** WCAG 2.1/2.2 AA at minimum; audit before launch. (skill: a11y-audit)
- **Core Web Vitals budgeted + enforced** — LCP < 2.5s, INP < 200ms, CLS < 0.1 at p75. Lighthouse CI on critical routes. (skill: core-web-vitals)
- **Forms use real labels** (not placeholders), specific error messages, hybrid validation timing, autocomplete attributes. (skill: form-design)
- **Component APIs lean toward composition over configuration** — primitives first, headless second, styled third. (skill: component-architecture)
- **Responsive everywhere** — fluid type with `clamp()`, container queries for components, viewport queries only for top-level layout. (skill: responsive-design)
- **Microcopy is design** — buttons say what happens, errors are specific + blameless, empty states have a next step. (skill: ui-copy)
- **Every async UI handles four states** — idle, loading, success, error — explicitly. (skill: loading-and-error-states)
- **Dialogs follow WAI-ARIA**: focus trap, scroll lock, ESC, focus restoration. Use a vetted headless library. (skill: modal-and-dialog-design)
- **i18n-ready by default** — no hardcoded strings, no concatenation, ICU MessageFormat for plurals. (skill: internationalization-prep)
- **Rendering strategy decided per route**, not picked once globally. (skill: rendering-strategy)
- **Browser automation respects rate limits + robots.txt + ToS.** (skill: browser-use)

### Enforcement hooks (if wired into this project's `.claude/settings.json`)

- `require_plan.py` — blocks edits to source files when `docs/plans/CURRENT.md` is missing or stale.
- `require_failing_test.py` — blocks edits to production code without a recently-touched test file.
- `refresh_claude_md.py` — regenerates this section at session start.
- Bypass env vars: `AI_SKILLS_BYPASS_PLAN=1`, `AI_SKILLS_BYPASS_TDD=1`, `AI_SKILLS_NO_REFRESH_CLAUDE_MD=1`.

<!-- END ai-skills MANAGED -->

## Anything else

<More project-specific notes go below — outside the managed region so they survive refreshes.>
