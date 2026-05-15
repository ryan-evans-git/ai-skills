---
name: slo-definition
description: Define SLIs (service level indicators), SLOs (objectives), and error budgets — anchored to user-visible experience, with explicit consequences when budgets are spent. Use when defining reliability targets, when "is the service reliable enough" is unclear, or when the user says "SLO", "SLI", "error budget", "uptime target", "reliability".
---

# slo-definition

## Purpose

"99.9% uptime" promised to customers, measured against nothing, is theater. SLOs done right are a contract: a measurable indicator, a target, a budget for breakage, and a policy that triggers when the budget runs out. This skill builds that contract.

## When to use

- Defining the reliability bar for a new service.
- Promising SLAs to customers (the SLO is your internal stricter version).
- After an incident where "was this OK or not OK" was debated.
- User says: "SLO", "SLI", "error budget", "uptime target", "reliability target", "five nines".

## The vocabulary

- **SLI** (indicator) — a measurement. "% of requests that completed in <300ms with 2xx status."
- **SLO** (objective) — a target for the SLI. "99.5% over a 30-day rolling window."
- **SLA** (agreement) — a contractual promise to customers, typically *looser* than the internal SLO. If SLA is 99.5%, SLO might be 99.9% so you have warning before you breach SLA.
- **Error budget** — `100% − SLO`. With SLO 99.5% over 30 days, budget is 0.5% × 30 days = ~3.6 hours of failure.

## Designing an SLI

The SLI must reflect **user-visible** experience, not system internals.

| Bad SLI | Good SLI |
| --- | --- |
| CPU < 80% | % requests answered in <300ms with 2xx |
| DB connections healthy | % checkout completions succeeding |
| Pod count == replicas | % page loads with LCP < 2.5s |

Common SLI shapes:
- **Availability**: % requests that succeeded (status < 500, not timeout).
- **Latency**: % requests faster than threshold.
- **Quality**: % responses that met semantic correctness (e.g., %% AI feature responses passing a guardrail check).
- **Freshness**: % data points younger than X.
- **Correctness**: % responses passing a per-response validator.

## Picking the target

- **Anchor to user research / business need.** "Customers tolerate <X% failure" beats "feels reasonable."
- **Be honest about today.** If current performance is 99.2%, setting SLO to 99.99% means perpetual breach. Set the SLO at-or-slightly-above current, then improve.
- **Don't promise five nines without a plan.** Each extra "nine" typically costs 10× in engineering. Most product services don't need >99.9%; many are fine at 99.5%.

## The error budget policy

The budget is meaningless without a policy that triggers when it's depleted. Standard policy:

| Budget remaining | Action |
| --- | --- |
| > 50% | Normal velocity; ship features. |
| 25-50% | Caution; review risky changes more carefully. |
| 0-25% | Freeze non-essential changes; focus on reliability work. |
| < 0% (over budget) | Hard freeze on new features. All capacity to reliability. Postmortem all incidents. |

Without this policy, SLOs are just numbers.

## Process

1. **Pick the user journey** the SLO covers. One SLO per critical journey is better than one composite.
2. **Define the SLI**:
   - Numerator: "good" events.
   - Denominator: total relevant events.
   - Be explicit about what counts as "good" — the boundary cases matter.
3. **Pick the time window**: 30 days rolling is the default. Longer is more lenient.
4. **Set the target**: anchored to current performance + user need + business cost.
5. **Compute the error budget** in human-readable units (e.g. "minutes/month").
6. **Define the policy** — what happens when budget is depleted.
7. **Wire the SLI in metrics** (`metrics-design`) and alerts (`alerting-policy`):
   - **Burn-rate alerts** — alert when budget is spending faster than expected, not when it's already gone.
   - Standard SRE pattern: alert if 14.4× burn rate sustained over 1h (= 2% budget consumed in 1h on a 30-day window) — gives ~6h warning before total exhaustion.
8. **Document at `docs/observability/slos.md`**:
   - Each SLO: SLI definition, target, window, error budget in real units, current consumption.
   - The policy.
   - Last review date + owner.
9. **Quarterly review** — SLOs that aren't reviewed become aspirational. Reduce target if a journey doesn't need it, raise it where the business demands.

## Anti-patterns

- **SLOs on system internals.** Users don't experience CPU; they experience whether the page loads.
- **Composite SLO across many endpoints** — hides a broken endpoint behind healthy ones.
- **SLO == SLA.** No buffer; first breach is also a customer-facing breach.
- **No policy.** SLO is a number nobody acts on.
- **Page on SLO breach.** Page on burn rate, not on already-spent budget.
- **Setting "100%" SLO** — every blip is a breach; team learns to ignore it.

## Cross-references

- `metrics-design` — the SLI is a metric.
- `alerting-policy` — burn-rate alerts.
- `dashboard-design` — surface budget remaining.
- `incident-postmortem` — incidents are charged against the budget.
- `release-strategy` — error-budget policy gates risky releases.

## Output

`docs/observability/slos.md` (single living doc) + metric / alert wiring.
