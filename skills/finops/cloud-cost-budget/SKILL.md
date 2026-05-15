---
name: cloud-cost-budget
description: Define per-service / per-team / per-feature cloud budgets with alerts that fire before bills surprise anyone — and document the response when budgets breach. Use when setting up cloud accounts, after a "the bill is HOW much" moment, or when the user says "cost budget", "spending alert", "AWS budget", "FinOps", "cost guardrails".
---

# cloud-cost-budget

## Purpose

Cloud spend grows quietly. By the time the invoice arrives, a runaway resource has burned $40K and nobody knows which feature caused it. This skill puts budgets + alerts in place at the right granularity, with a response policy so an alert means action.

## When to use

- Setting up a new cloud account or new service.
- After a "the bill is HOW much" surprise.
- Before launching anything with autoscaling.
- LLM features going to production (cross-ref `llm-cost-management`).
- User says: "cost budget", "spending alert", "AWS budget", "GCP budget", "Azure budget", "FinOps", "cost guardrails", "cost ceiling".

## Budget granularity (apply at every level)

| Level | What | Who responds |
| --- | --- | --- |
| **Account / project** | Total monthly spend ceiling | Finance + engineering leadership |
| **Service** | Per service / per workload | Service owner |
| **Feature** | Per LLM feature / per new product | Feature owner |
| **Team** | Per team's owned resources | Team lead |
| **Tag-based** | Per cost-allocation tag (`environment`, `tenant`, `feature`) | Resource owner |

Budgets at multiple levels catch different failures: a runaway workload trips the service budget; sustained growth across a team trips the team budget; both feed the account budget.

## Tagging — the foundation

Without tags, budgets are guesses. Required tags on every resource:

| Tag | Why | Example |
| --- | --- | --- |
| `environment` | Separate dev/staging/prod | `prod` |
| `service` | Per-service attribution | `orders-api` |
| `team` | Owner team | `platform` |
| `cost-center` | Finance reporting | `eng-shared` |
| `feature` (optional) | Per-feature attribution | `ai-summarize` |

- **Enforce tagging via policy.** AWS Service Control Policy / GCP organization policy / Azure Policy can refuse-untagged-resource at create time.
- **Audit untagged resources** monthly. Untagged resources are typically the biggest unattributed spend.
- **Auto-tag where possible** — Terraform / Pulumi defaults; CI-provisioned tags; cloud-native automation.

## Setting the budget

For each level:

1. **Baseline**: pull the last 3 months of spend. Use the trend.
2. **Set the budget at ~1.1-1.5× recent baseline** — buys headroom without losing signal.
3. **For new workloads**: estimate based on rough resource needs; set conservatively; tighten after 2 weeks of real data.
4. **Document the rationale** — without it, future-you can't tell "is this number right?"

## Alerts (the policy is what makes budgets matter)

### Standard alert thresholds
- **At 50% of budget** — informational; ticket to the owner.
- **At 80% of budget** — warning; on the team's radar.
- **At 100% of budget** — owner notification + ticket; review what changed.
- **At 120% of budget** — escalation; engineering leadership notified.

For **fast-burn alerts** (the cloud-equivalent of SLO burn rate):
- **Daily spend > 2× expected**: ticket the same day.
- **Hourly spend > 5× expected**: page (for accounts where this matters — e.g. LLM API costs that can spike fast).

### Forecast alerts (better than threshold alerts)
- Cloud providers offer forecast-based budget alerts: alert if *projected* end-of-month spend exceeds budget, even if you're not there yet.
- This is the single most useful FinOps signal — gives warning before threshold is hit.

## Response policy

When a budget breaches:
1. **Identify the cause** — which service / feature / resource is over.
2. **Decide**: is this a transient (one-time backfill), a permanent shift (legitimate growth), or a leak (idle resource / runaway)?
3. **For transient**: log it, raise budget temporarily if needed.
4. **For permanent**: raise budget deliberately; update the rationale doc.
5. **For leak**: dispatch to `idle-resource-audit` / `resource-right-sizing` / shut down the runaway.
6. **Update budget docs** with what was found.

Without a policy, alerts get acknowledged-and-ignored.

## Process

1. **Tagging coverage** — audit current resources for required tags; remediate untagged.
2. **Enforce tags going forward** via policy.
3. **Set up budgets at each level** (account, service, team, optionally feature).
4. **Set alert thresholds** per the standard above.
5. **Wire alerts to a real channel** — not just email. Service-owner Slack channel for service alerts; finance + leadership channel for account-level.
6. **Document at `docs/finops/budgets.md`**:
   - Each budget: amount, scope, owner, rationale, last reviewed.
   - The response policy.
   - Where alerts go.
7. **Monthly review** — what breached, why, action taken. 30-min meeting.

## LLM-specific

LLM costs deserve their own budget granularity:
- **Per LLM-feature budget** with daily-not-monthly alerts (LLM costs can spike 100× faster than infrastructure).
- See `llm-cost-management` for the optimization patterns.

## Anti-patterns

- **One account-level budget.** Tells you the bill is up, not why.
- **No tagging.** Budgets without attribution are just numbers.
- **Alerts to a shared inbox no one reads.** Route to the owner.
- **Budget = 100% of current spend.** Always over budget; alert fatigue.
- **No response policy.** Alert acknowledged, nothing changes.
- **No forecast alerts.** First time you know is the day you breach.
- **Setting budgets once, never reviewing.** Spend reality changes; budgets must too.

## Cross-references

- `idle-resource-audit` — find what to remove when budget breaches.
- `resource-right-sizing` — adjust capacity instead of cutting features.
- `cost-attribution` — per-feature visibility.
- `llm-cost-management` — LLM-specific cost tactics.
- `alerting-policy` — budget alerts follow the same tier discipline.

## Output

- Cloud provider budgets configured.
- Tag-enforcement policies in place.
- `docs/finops/budgets.md` — single living doc of all budgets, owners, rationale.
