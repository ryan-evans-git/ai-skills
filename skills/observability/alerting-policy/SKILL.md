---
name: alerting-policy
description: Design an alerting policy that pages humans only when human action is required, routes everything else to tickets, and resists alert fatigue. Use when setting up alerts, after an alert-fatigue incident, when the user says "alerts", "paging", "PagerDuty", "alert fatigue", "false positive alert", "noisy alerts".
---

# alerting-policy

## Purpose

The cost of a noisy alert isn't the false page — it's the muscle memory of dismissing alerts that, eventually, gets applied to the real one. This skill is the discipline that makes "the alert went off" mean something.

## When to use

- Setting up alerts for a new service.
- Alert fatigue / a missed real alert.
- Adding a new dependency or feature.
- User says: "alerts", "paging", "PagerDuty", "alert fatigue", "false positive alert", "noisy alert", "what should page me".

## The three tiers

Every signal goes into exactly one tier. Mixing is the source of fatigue.

### Tier 1 — Page (P1)
- **Criterion**: needs human action *right now*; user-visible impact is happening or imminent.
- **Examples**: SLO error-budget burn-rate over threshold; checkout broken; auth service down.
- **Wakes someone up.** Both metaphorically (Slack / phone / PagerDuty) and literally (off-hours pages).
- **Runbook required** — every Tier 1 alert links to a runbook. No runbook → not a Tier 1.

### Tier 2 — Ticket (P2)
- **Criterion**: needs investigation, but not in the next 5 minutes. Will become Tier 1 if ignored.
- **Examples**: dependency degraded but circuit breaker holding; cost trending over budget; SLO budget at 25%.
- **Creates a ticket / Slack notification in a team channel.** Handled during the next business hours.

### Tier 3 — Log / dashboard only
- **Criterion**: useful to know during investigations; not actionable on its own.
- **Examples**: spike in a single endpoint's latency; one host disk filling slowly.
- **Visible on dashboards** (`dashboard-design`), queryable in logs, but doesn't ping anyone.

## What gates Tier 1 (pageable)

Mandatory before adding any Tier 1 alert:

- [ ] **Has a runbook** — written, accessible, with named owner. Linked from the alert payload.
- [ ] **Is actionable now** — there's a clear thing a human can do at 3am to mitigate. "Alert that something is wrong" without action belongs in Tier 2.
- [ ] **Anchored to a symptom**, not a cause. Page on "checkout failure rate > X%", not "Postgres replication lag > Y." Symptom alerts catch unknown failure modes; cause alerts miss them.
- [ ] **Not flapping** — a stable signal over a meaningful window. "5xx > 1% for 5 minutes" not "any single 5xx."
- [ ] **Cost of false page < cost of missed real alert** for this signal.

## Symptom-based vs. cause-based alerting

**Prefer symptom-based**: alert on what users experience. "Checkout success rate dropped below 99%" catches every failure mode that affects checkout — including ones you didn't anticipate.

**Cause-based alerts**: useful as Tier 2/3 supplements ("DB CPU at 95%") to speed diagnosis once the symptom alert fires. Rarely the right primary alert.

## SLO burn-rate alerting (the right shape for Tier 1 reliability alerts)

Instead of "error rate > 1%" (which can be fine, given budget), alert on **burn rate**: how fast you're spending the error budget over a window.

Standard pattern (Google SRE):
- **Fast burn**: 14.4× burn rate for 1h → page. (Would exhaust 30-day budget in 2 days.)
- **Slow burn**: 6× burn rate for 6h → page. (Catches sustained issues that fast-burn misses.)

These give 6+ hours of warning before total exhaustion, with low false-positive rates.

## Alert payload — required fields

Every alert that pages or tickets includes:
- **Title** — what's wrong, in user-visible terms. "Checkout 5xx rate elevated", not "RedisException count up."
- **Severity** — P1/P2.
- **Service / owner team.**
- **Time started** + **current value of the offending metric**.
- **Runbook link.**
- **Dashboard link** filtered to the relevant service / time.
- **Recent deploys** (the alert system can include the last N deploys).
- **Auto-link to recent related alerts** if available.

A 3am page should let the on-call diagnose without opening 8 tabs.

## Process

1. **Walk the SLOs** (`slo-definition`). For each, set up multi-window burn-rate alerts as Tier 1.
2. **Walk the dependencies** (`service-map`). For each P0 dependency, alert on the integration health (Tier 1 if outage = user impact; Tier 2 if you have a fallback).
3. **Walk the resources**: connection pools, queue depths, disk. Set Tier 2 / Tier 3 thresholds.
4. **Walk the business events** (`metrics-design`). At least one Tier 1 / Tier 2 for the funnel.
5. **Audit existing alerts**:
   - Any Tier 1 without a runbook → demote or write the runbook.
   - Any Tier 1 with high false-positive rate → tune or demote.
   - Any "informational page" — these don't exist. Make it a ticket.
6. **Document at `docs/observability/alerts.md`** — per alert: tier, signal, threshold, runbook, owner.
7. **Schedule quarterly review** — alerts that haven't fired in 6 months may be stale (or solving a fixed problem and worth removing); high-frequency alerts likely need tuning.

## Anti-patterns

- **Pageable alerts without runbooks.** On-call woken up to read source code.
- **Alerts on every metric.** The team learns to mute everything.
- **No symptom alerts** — only cause alerts. Misses new failure modes.
- **Static thresholds set "to be safe"** that never match reality. Tune them.
- **No tier discipline.** Everything pages; nothing is signal.
- **Auto-resolved alerts.** "It went away" alerts: lower-tier them.
- **Same threshold for staging and prod.** Different blast radius.

## Cross-references

- `metrics-design` — the underlying signal.
- `slo-definition` — burn-rate alerts on SLO budgets.
- `dashboard-design` — alert links to dashboards.
- `incident-postmortem` — every page has a postmortem trail (or a tuning ticket).

## Output

- Alert definitions (in code or platform UI).
- `docs/observability/alerts.md` per-alert inventory.
- Runbooks at `docs/operations/runbooks/<alert-name>.md`.
