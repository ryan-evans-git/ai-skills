---
name: synthetic-monitoring
description: Run synthetic probes — uptime checks, scripted user journeys, multi-region — that detect outages and degradations from outside the system, before real users complain. Use when setting up monitoring for a user-facing service, after an "outage discovered by Twitter" incident, or when the user says "synthetic monitoring", "uptime check", "Pingdom", "user journey monitoring", "external probe".
---

# synthetic-monitoring

## Purpose

Internal metrics tell you whether your servers think they're healthy. Synthetic probes tell you whether *the actual user experience* works from where users actually are. The two diverge surprisingly often — DNS misconfigured in one region, TLS expired, CDN serving stale, a multi-region routing bug that the prod metrics happily call "100% healthy" because no traffic is reaching the bug.

## When to use

- Setting up monitoring for a user-facing service.
- After an outage that internal monitoring missed.
- Multi-region service where regional outages are possible.
- High-availability SLA (>99.9%) — internal-only monitoring is insufficient.
- User says: "synthetic monitoring", "uptime check", "Pingdom", "user journey monitoring", "external probe", "outside-in monitoring".

## Types of synthetic checks

### Tier 1: Uptime / availability checks
- Hit an endpoint every 1-5 min from N regions, assert 2xx + latency below threshold.
- Cheap, fast, broad coverage.
- Provides a clean SLI: "% of probes that succeeded" across a window.

### Tier 2: Multi-step user journeys
- Scripted browser sessions ("Playwright check": load page → sign in → search → click result → expect outcome).
- Slower, more expensive, catches integration bugs uptime checks miss.
- Run every 5-15 min.
- One per critical user journey (signup, checkout, login, primary feature use).

### Tier 3: API contract probes
- Hit specific endpoints with known inputs, validate the response shape and content.
- Catches: API drift, deserialization bugs, cache poisoning, partial outages.
- Cross-ref `integration-contract-tests` — those run in CI; these run continuously in prod.

### Tier 4: Third-party-dependency probes
- Check the dependencies you rely on (status pages, direct API health probes).
- When `payment-service` is down, you want to know before the next checkout fails — and customer support wants a status page that pulls this.

## Where to probe from

- **Multiple regions** matching your user geography. A US-only probe misses an EU CDN outage.
- **Outside your cloud provider** — same-cloud probes don't catch regional cloud outages from the user's perspective.
- **Managed providers**: Pingdom, UptimeRobot, Better Stack, Datadog Synthetics, Checkly, AWS CloudWatch Synthetics. Don't roll your own unless you have a strong reason.

## What to alert on

| Signal | Tier | Action |
| --- | --- | --- |
| Single-region single-probe failure | Tier 3 | Log; pattern only |
| Multi-region single failure within N min | Tier 1 page | Likely real outage |
| Journey fails | Tier 1 page | User-impacting |
| Latency 3× baseline | Tier 2 ticket | Degradation, investigate |

Don't page on every single missed probe — false positives erode trust (see `alerting-policy`). Require multiple regions or sustained failure.

## Process

1. **Identify the critical journeys** — same set as `qa-test-plan`. The journeys that matter to users.
2. **Pick a provider** — managed unless you have a reason not to.
3. **For each journey**:
   - Write the probe script (Playwright / curl / managed-provider DSL).
   - Set the probe regions (where users are).
   - Set the frequency (1-5 min for Tier 1; 5-15 min for journeys).
   - Set the alert threshold per `alerting-policy`.
4. **Wire into the on-call dashboard** (`dashboard-design`) — green/red per probe.
5. **Wire into the SLI** (`slo-definition`) — "% probes succeeding" can be the availability SLI.
6. **Status page integration** — for customer-facing services, the synthetic probes drive the public status page (don't hand-update the status page during incidents).
7. **Document at `docs/observability/synthetic-checks.md`**:
   - Each check: target, regions, frequency, alert threshold, owner.
   - Status page link.

## Common gotchas

- **Probes that use static credentials that rotate.** Probe stops working; nobody notices for weeks. Either: probe with a long-lived test account, or rotate probe creds along with the system.
- **Authenticated journeys hitting prod**: real user accounts. Pollute analytics, count toward funnel. Use clearly-tagged test accounts; exclude from metrics and billing.
- **Probes triggering rate limits.** Common with aggressive frequency — your own probe is contributing to "outages."
- **Tests that pass when the page partially loads.** Probe checks 200; user sees a half-rendered page. Add content assertions.
- **Probes from your own cloud account.** Same-cloud outages defeat the purpose.

## Cross-references

- `metrics-design` — synthetic results are themselves metrics.
- `slo-definition` — synthetic uptime as an SLI.
- `alerting-policy` — when synthetic failures page.
- `dashboard-design` — surface synthetic status prominently.
- `integration-contract-tests` — contract tests in CI; this is contract probes in prod.

## Output

- Configured synthetic checks (in provider UI / IaC).
- `docs/observability/synthetic-checks.md` — inventory and ownership.
- Status page configured if customer-facing.
