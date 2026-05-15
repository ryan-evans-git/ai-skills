---
name: idle-resource-audit
description: Find and decommission resources that are unused or barely used — orphan volumes, idle instances, untagged-and-untouched databases, abandoned dev environments, dormant load balancers. Use periodically, when a budget breaches, or when the user says "idle resources", "orphan resources", "unused", "abandoned", "what can we delete", "cost optimization".
---

# idle-resource-audit

## Purpose

The biggest FinOps wins usually aren't right-sizing busy resources — they're finding the resources that *do nothing*. Old test environments, orphaned volumes from terminated instances, load balancers fronting nothing, dev DBs nobody connects to. This skill systematically finds and removes them.

## When to use

- Periodically (monthly is reasonable).
- After a budget breach (`cloud-cost-budget`).
- After team reorgs (people leave, their resources don't).
- Before announcing cost cuts.
- User says: "idle resources", "orphan resources", "unused", "abandoned", "what can we delete", "cost optimization", "zombie resources".

## What to audit

### Compute
- **Stopped instances** — paying for storage; rarely intentional long-term.
- **Running instances with near-zero CPU** for the last 2 weeks (often abandoned dev / staging).
- **Auto-scaling groups with idle baseline** (`min=2` for a service that needs 0 when idle).

### Storage
- **Unattached EBS / managed disks** — instance terminated, volume orphaned. Pure waste.
- **Old snapshots** — snapshots without a retention policy multiply forever.
- **Empty / nearly-empty object buckets** that still pay for replication / lifecycle / inventory features.

### Databases
- **DBs with no recent connections** — managed DBs charge regardless of use.
- **Dev / staging DBs sized like prod** — see `resource-right-sizing`.
- **Read replicas with low query rate** — possibly unused.

### Networking
- **Unattached Elastic IPs / static IPs** — charged when not associated.
- **Load balancers with no targets** or zero traffic.
- **NAT Gateways** in environments that don't need them (cheap mistake; sneaky cost).
- **VPCs / subnets in unused regions.**

### Logs / metrics / traces
- **Old log groups** with no recent writes but ongoing storage charges.
- **CloudWatch / monitoring agent on terminated instances** (rare but happens).

### Identity / access
- **Cost-of-API-call services** with unused API keys still rotating.

### Old experiments
- **Sandbox / experiment accounts** without owners.
- **PR preview environments** that never got cleaned up.

## Discovery commands / tools

| Cloud | Built-in finder |
| --- | --- |
| AWS | Trusted Advisor (paid), Compute Optimizer, Cost Explorer "Resource Optimization" |
| GCP | Recommender, Active Assist |
| Azure | Advisor, Cost Management |
| Multi-cloud | CloudHealth, Spot.io, Cloudability, Vantage |

Custom queries are often more thorough — e.g. for AWS:
- `aws ec2 describe-volumes --filters Name=status,Values=available` — unattached volumes.
- `aws ec2 describe-addresses --query 'Addresses[?InstanceId==null]'` — unattached EIPs.
- CloudWatch metrics with 2-week 0-utilization filters for instance idleness.

## Process

1. **Run the discovery** across compute, storage, networking, DB, logs.
2. **For each candidate, capture**:
   - Resource ID and type.
   - Tags (cross-ref `cloud-cost-budget` — untagged resources are nearly always idle).
   - Created date / last-used date (where measurable).
   - Estimated monthly cost.
   - Owner (from tags or git history).
3. **Classify** each:
   - **Orphan** — definitely unused (no owner, no traffic, no recent access). Safe to delete after confirmation.
   - **Idle but owned** — owner exists but resource isn't doing anything. Confirm with owner before action.
   - **Active but oversized** — dispatch to `resource-right-sizing`.
4. **Confirm with owners** before deleting anything that isn't clearly orphaned. The first time you delete someone's "old" prototype that turned out to be the demo for tomorrow's investor pitch will teach this lesson permanently.
5. **Delete in stages**:
   - Stop / detach first (reversible).
   - Wait 2 weeks (catches "wait, that thing was needed").
   - Then delete.
6. **Snapshot databases / volumes** before destructive deletion if in doubt.
7. **Document at `docs/finops/idle-audits.md`** — per-audit row: date, resources deleted, estimated monthly savings.

## When you can't find owners

This is the typical hard case. Approaches:
- **Tag-then-track** policy: untagged resources get a `pending-delete-YYYY-MM-DD` tag; warn in the resource via tag or description; if nobody claims by date, delete.
- **Account-level review**: the team that owns the account adjudicates. Sometimes the answer is "delete it; if I'm wrong I'll redeploy from infra-as-code."
- **Cost-attribution** investigation (cross-ref) — even untagged resources often have a Terraform-state owner or a name that gives away origin.

## What to NEVER do silently

- **Delete data without a snapshot** when uncertain.
- **Delete a resource without telling its likely owner**, even if a tag is missing.
- **Bulk-delete via API across many accounts** without per-resource confirmation.
- **Delete a "test" resource without checking it isn't actually load-bearing** — names lie.

## Anti-patterns

- **Periodic audits but no enforcement.** Same resources appear in the audit every month.
- **No tag-enforcement upstream.** Untagged resources keep proliferating.
- **Auto-delete everything idle for N days.** Catches load-bearing infrequent infrastructure (DR replicas, monthly batch jobs).
- **Audit only in prod.** Dev / staging accounts are usually 60-80% of waste in young teams.

## Cross-references

- `cloud-cost-budget` — budgets fire; this skill finds what to cut.
- `resource-right-sizing` — sister skill for resources that ARE used but oversized.
- `cost-attribution` — finds owners and feature origins.
- `worktree-cleanup` / `dev-storage-audit` — local version of this for dev machines.

## Output

- Decommissioned resources (after confirmation).
- `docs/finops/idle-audits.md` — audit history + savings.
- Open follow-up: tag-enforcement gaps if many orphans were untagged.
