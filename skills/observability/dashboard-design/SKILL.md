---
name: dashboard-design
description: Build dashboards that answer specific questions — service health, incident triage, business funnel — rather than "all metrics in one place." Use when creating dashboards, when the user says "Grafana", "dashboard", "what should the dashboard show", "service health dashboard", or after an incident exposed dashboard gaps.
---

# dashboard-design

## Purpose

A good dashboard answers a question in seconds. A bad one is "here are 47 charts" — useless when an incident is happening. This skill is the design framework that produces the small set of dashboards that actually get used.

## When to use

- Creating a new dashboard for a service.
- Existing dashboard isn't useful during incidents.
- User says: "Grafana", "Datadog dashboard", "dashboard", "service health view", "what should the dashboard show".

## Dashboards by purpose (not by service)

Build dashboards for specific audiences answering specific questions:

### 1. Service health (on-call dashboard)
**Question**: "Is my service healthy right now? If not, where?"

Standard layout (top → bottom):
- **Header**: service name, owning team, on-call rotation, SLO status.
- **The four golden signals** (`metrics-design`): latency p50/p95/p99, traffic rate, error rate, saturation. One row.
- **Per-endpoint breakdown**: top N endpoints by error rate or latency. Lets you see WHICH endpoint is unhealthy.
- **Dependency health**: per downstream — call rate, error rate, p95 latency. Lets you see if the problem is yours or theirs.
- **Resource saturation**: CPU, memory, pool depth, queue lag.
- **Recent deploys overlay** on every chart — instantly correlates "started getting worse" with "deploy at 14:32."

### 2. Funnel / business
**Question**: "Are users completing the journeys we care about?"

- Each step of the funnel as a separate panel.
- Conversion rate panel showing % between steps.
- Time-shifted comparison (vs. last week / last month) to see trends.
- Note: business charts at the top of the on-call dashboard too — sometimes "everything looks fine but signups dropped to zero."

### 3. Capacity / scaling
**Question**: "Will we run out of headroom in N hours / days?"

- Saturation per resource, with thresholds drawn.
- Projected exhaustion based on growth rate.
- Used to make scaling decisions, not for live incidents.

### 4. Cost
**Question**: "Where is the money going?"

- See `cost-attribution` in finops.

### 5. Per-feature deep-dive
**Question**: "What's happening inside feature X?" Used during investigation; not a daily-driver dashboard.

## Design rules

### Layout
- **Top of dashboard = highest-signal** info. The on-call's eye lands there first.
- **Left → right, top → bottom** — eye flow. Don't bury critical info on the bottom-right.
- **Rows are categories**: golden signals, endpoints, deps, resources. Don't randomly interleave.
- **No more than one screen** for the primary dashboard. Scrolling = nobody scrolls.

### Charts
- **Pick the right chart type**:
  - Time series for everything-over-time.
  - Single-stat for current value (SLO budget remaining, error rate now).
  - Heatmap for distributions (latency).
  - Avoid pie charts.
- **Y-axis labels with units**. Every chart.
- **Consistent time range** across the dashboard (don't have one chart on 1h and another on 24h side by side).
- **Annotations**: deploys, incidents, feature flag changes. Critical for "what changed?"

### Thresholds
- **Draw SLO thresholds on charts** — visual: "are we in budget?"
- **Color carefully** — green/yellow/red works but is overused; high-contrast (one accent color) often reads better.
- **Avoid red walls** — if everything is red all the time, nothing is red.

### Filters
- **Top-of-dashboard variables**: environment, region, tenant. Same dashboard, different scopes.
- **Default to the most-used scope** (typically prod, all regions).

### Single source of truth
- **One canonical dashboard per service.** Multiple "v2/v3/v_alex_test" dashboards = confusion during incidents.
- **Version-control the dashboard JSON** where the platform supports it (Grafana, Datadog).

## Process

1. **Identify the question(s)** the dashboard answers.
2. **Pick the audience** — on-call / business / capacity / cost. One dashboard, one audience.
3. **List the panels** that answer the question(s). Group by row.
4. **Build it**, then **rehearse**: pretend an incident is happening — can you triage from this dashboard alone, in <60s?
5. **Iterate after every incident**: did the dashboard answer the questions you had? If not, add the panel.
6. **Version-control** the dashboard. Make changes via PR where the platform supports.
7. **Link it from**:
   - The service's `README.md`.
   - The runbook for every alert (`alerting-policy`).
   - On-call's "starting shift" checklist.

## Anti-patterns

- **"Everything dashboard."** 60 panels; useless in an incident.
- **No deploy annotations.** Half of "what changed" investigations stall here.
- **Dashboards as art.** Pretty but doesn't answer questions.
- **Per-host charts.** Useful at small scale; pathological at large scale. Aggregate first.
- **No SLO overlay.** Charts disconnected from "is this OK or not?"
- **Dashboard not used by on-call.** Either it's wrong, or nobody knows it exists. Fix both.
- **Editing in the UI without version control.** Drift; lost work; can't reproduce.

## Cross-references

- `metrics-design` — what's measured determines what dashboards can show.
- `slo-definition` — overlay SLO thresholds.
- `alerting-policy` — alerts link to dashboards.
- `incident-postmortem` — dashboards iterate from each incident's gaps.

## Output

- Dashboards (in platform UI / JSON / IaC).
- `docs/observability/dashboards.md` — index of canonical dashboards + their purpose.
