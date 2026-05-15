---
name: cost-attribution
description: Attribute cloud / LLM / SaaS spend to features, customers, teams, or tenants — and produce a regular report that connects spend to value. Use when launching a new product line, when the cost-per-customer question comes up, when justifying engineering investment, or when the user says "cost per feature", "cost per customer", "unit economics", "showback", "chargeback", "cost attribution".
---

# cost-attribution

## Purpose

"Where does the money go?" splits into two harder questions: "which feature spends it" and "which customer / use case generates the spend." Without attribution, you can't decide whether a feature pays for itself, whether a customer is profitable, or where the team's investment should go.

## When to use

- Launching a new product line — what's the cost per use?
- Cost-per-customer (or per-tenant) question comes up.
- Justifying engineering investment (which expensive feature is most-used?).
- Negotiating contracts with vendors (need to know your dependency cost per X).
- User says: "cost per feature", "cost per customer", "unit economics", "showback", "chargeback", "cost attribution", "is this customer profitable".

## Two flavors

- **Showback** — give each team / feature a report of their spend. No money changes hands; visibility drives change.
- **Chargeback** — actually charge the team / business unit for their spend (real ledger entries). Heavier process; only for large orgs that need it.

Start with showback. Chargeback usually comes later.

## What to attribute

| Cost source | Attribution method |
| --- | --- |
| **Cloud compute** | Cost-allocation tags + cloud-provider billing API |
| **Cloud storage** | Tags + lifecycle reports |
| **Databases** | Schema-level allocation (per service / per tenant) — harder; often a single resource has many consumers |
| **LLM API spend** | Per-request logging with `feature` field (see `llm-cost-management`) |
| **Third-party SaaS** (Stripe, SendGrid, Twilio) | Vendor-side metering + your own per-feature instrumentation |
| **Networking** | Egress per service via VPC flow logs + tags |

## Attribution dimensions

Pick the dimensions that match the decisions you'll make:

- **Feature** — for product investment / kill decisions.
- **Customer / tenant** — for unit economics, pricing decisions, large-customer profitability.
- **Team** — for capacity planning, FinOps accountability.
- **Environment** — dev/staging/prod (often dev surprise-dominates).
- **Region** — for multi-region cost analysis.

Don't try to attribute every dollar perfectly to every dimension on day one. Start with feature + team; add customer attribution when business asks.

## Process

### Phase 1 — Foundations (do these before reporting)
1. **Required tags enforced** on all resources (cross-ref `cloud-cost-budget`).
2. **Per-LLM-call attribution logged** (cross-ref `llm-cost-management`).
3. **Per-request feature attribution** in app code: every notable request emits `feature_used` (or via traces — cross-ref `distributed-tracing`).
4. **Vendor APIs ingested** — Stripe, SendGrid, etc. with per-customer metering (where possible) into the analytics warehouse.

### Phase 2 — Build the attribution model
1. **Cloud spend → feature**: cost-allocation tag `feature` → cloud-provider cost-explorer / billing-export.
2. **Cloud spend → customer**: harder; usually proportional allocation based on usage (e.g. % of requests per tenant).
3. **LLM spend → feature → customer**: per-call logs aggregated by `feature` and `tenant_id`.
4. **Shared infrastructure**: if 3 features share a DB, allocate the DB cost by query share (rows queried, query time, table size by tenant).
5. **Document the allocation rules** — others need to trust the numbers.

### Phase 3 — Report
- **Per-feature monthly** — cost trend per top features, broken out by spend type (compute / DB / LLM / vendor).
- **Per-customer monthly** — top customers by cost, alongside revenue (when revenue data is available).
- **Per-team** — surface to the team; bake into their dashboards (`dashboard-design`).
- **Anomaly callouts** — what changed week over week.

### Phase 4 — Drive change
- **Per-feature**: feature owners see their spend; they own optimization.
- **Per-customer**: surface unprofitable customers to product / sales — pricing or feature gating.
- **Per-team**: ties to team budgets (`cloud-cost-budget`).

## Unit economics

The closing of the loop: **cost per X / revenue per X**.

- **Cost per active user** = total cost / active users.
- **Cost per request** = LLM + infra cost / requests served.
- **Cost per feature use** = feature-attributed cost / feature uses.

These numbers drive: pricing decisions, feature kill decisions, scaling investment decisions. They are the most useful FinOps output.

## Where this lands organizationally

- Engineering owns the **instrumentation + report generation.**
- Finance owns the **vendor-spend ingestion + chart of accounts mapping.**
- Product owns the **per-feature decisions** the data drives.

FinOps as a practice is the intersection of these three; this skill builds the data.

## Process documentation

Write `docs/finops/cost-attribution.md` with:
- The attribution model (how each cost flows to each dimension).
- Where data lives (warehouse table, dashboard).
- Refresh cadence.
- Limitations / known gaps in attribution.
- Owners per system.

## Anti-patterns

- **Attribution without action.** Reports nobody reads.
- **Trying for 100% attribution.** ~80% attributed + clearly-labeled "unallocated" is fine. Chasing the last 20% costs more than the insight returns.
- **Spreadsheets as source of truth.** Use a warehouse table; let dashboards query it.
- **Customer-level attribution without consent / contract clarity** for chargeback. Showback is safe; chargeback needs the business mechanics in place first.
- **Allocating shared costs evenly** when usage is wildly uneven. "All teams pay 1/N for the DB" doesn't reflect reality.

## Cross-references

- `cloud-cost-budget` — attribution lets budgets be set at the right granularity.
- `idle-resource-audit` — attribution surfaces what's expensive AND unowned.
- `resource-right-sizing` — feature-level cost views show which workloads to target.
- `llm-cost-management` — LLM-spend attribution is a key subset.
- `metrics-design` / `distributed-tracing` — per-feature instrumentation lives here.

## Output

- Attribution data in a warehouse / cost-explorer-equivalent.
- `docs/finops/cost-attribution.md` — model + ownership.
- Per-feature / per-customer / per-team monthly reports.
