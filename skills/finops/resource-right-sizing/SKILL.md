---
name: resource-right-sizing
description: Audit compute, memory, storage, and database tier choices against actual utilization — and right-size to match real demand instead of pessimistic guesses. Use periodically, after a budget breach, before scaling decisions, or when the user says "right-size", "instance size", "over-provisioned", "are we using all this CPU", "scale down".
---

# resource-right-sizing

## Purpose

Cloud resources are sized at the moment of "let's just be safe." Six months later, nobody remembers the rationale and the workload is using 12% of what it's paying for. This skill is the periodic audit that brings spend back in line with real demand.

## When to use

- Periodically (recommend quarterly).
- Right after a budget breach (`cloud-cost-budget`).
- Before scaling out — make sure scaling isn't masking a sizing problem.
- After a workload change (deploy that significantly reduced CPU need; feature removed).
- User says: "right-size", "instance size", "over-provisioned", "scale down", "are we using all this CPU", "memory is unused".

## Resources to audit

| Resource | Right-size check |
| --- | --- |
| **Compute** (VMs, containers) | CPU & memory utilization vs. requested; p95 over 2-week window |
| **Database tier** | CPU, memory, IOPS, connection count; consider lower tier or serverless |
| **Storage volumes** | Provisioned vs. used; IOPS provisioned vs. used |
| **Object storage** | Storage class tier (hot vs. cold) vs. actual access pattern |
| **Caches** (Redis, Memcached) | Memory usage, eviction rate, hit rate |
| **Message queues** | Throughput, retention, partition / shard count |
| **Load balancers** | Are you paying for HA you don't need (single-AZ?) |
| **Reserved capacity** | Coverage vs. actual usage; opportunity for further commitments |

## The right-sizing rules

### Compute
- **CPU**: target p95 utilization ~50-70%. Below ~30%, downsize. Above ~80% sustained, upsize (or scale out).
- **Memory**: target p95 ~70-80%. Memory-bound apps can run higher; latency-sensitive lower.
- **Don't right-size based on p99 alone.** A 1-min spike per day shouldn't dictate 24/7 sizing — solve with scaling, not bigger instances.
- **Match the instance family to the workload**: CPU-bound → compute-optimized; memory-bound → memory-optimized; balanced → general-purpose. Wrong family at right size still wastes money.

### Database
- **CPU + memory** as above.
- **Connection count** — many DBs have per-tier connection limits. If 80% saturated, consider connection pooling before upsizing.
- **IOPS** — if provisioned IOPS are unused, drop the tier.
- **Serverless / autoscaling tiers** — for variable workloads, can dramatically beat fixed sizing.
- **Read replicas** — often added "for safety" then under-used. Audit replica utilization.

### Storage
- **Object storage classes** — hot (S3 Standard) vs. infrequent-access vs. archive (Glacier). Migrate by access pattern. Lifecycle policies automate this.
- **Volumes** — over-provisioned EBS / managed disks are common; check actual usage vs. provisioned.

### Caches
- **Memory headroom** — if usage is steady well below capacity, downsize.
- **Eviction rate** — if cache is constantly evicting, upsize OR reduce what you cache.
- **Hit rate** — low hit rate on an expensive cache = remove the cache (cross-ref `caching-strategy`).

### Reserved capacity / commitments
- Most cloud providers offer 30-72% discount for 1-3 year commitments.
- Coverage target: ~70-80% of baseline; leave headroom for variance.
- Don't over-commit — wasted reservations are worse than on-demand for that capacity.

## Process

1. **Pull utilization data** for the audit window (2-4 weeks):
   - AWS: Compute Optimizer, Trusted Advisor, CloudWatch.
   - GCP: Recommender, Cloud Monitoring.
   - Azure: Advisor, Monitor.
   - Plus your own metrics (`metrics-design`).
2. **List candidates** for change (per-resource recommendation: downsize / upsize / change-family / change-tier).
3. **For each candidate, decide**:
   - Estimated monthly savings (or cost).
   - Risk of the change (performance regression? capacity headroom for spikes?).
   - Effort.
4. **Sort by savings × (1 / risk).** Do the high-savings low-risk ones first.
5. **Test in staging if the change is non-trivial** — load test (`load-test-plan`) on the smaller size.
6. **Apply the change.**
7. **Monitor for 2 weeks** — if performance degrades, revert.
8. **Document at `docs/finops/right-sizing-audits.md`** — append a row per audit: date, changes made, estimated monthly savings, observed savings.

## When NOT to right-size

- **Right before a known traffic event** (launch, marketing campaign, seasonal spike) — wait until after.
- **For inherently bursty workloads** without auto-scaling in place — fixing scaling is the better intervention.
- **Resources with strong SLOs at risk** — measure twice; ideally on a parallel canary.

## Anti-patterns

- **Sizing on peak load** with no plan for off-peak. Schedules / scaling-by-time-of-day catch the common pattern.
- **Right-sizing without metrics**. "Looks too big" is not data.
- **Optimizing for cost over reliability without explicit acceptance.** A right-size that causes incidents is a false win.
- **Doing it once.** Workloads change; right-sizing is recurring.
- **Right-sizing dev to production levels.** Dev usually doesn't need prod sizing — but production DOES need prod sizing.

## Cross-references

- `cloud-cost-budget` — triggers right-sizing reviews when budgets breach.
- `idle-resource-audit` — sister skill for resources used 0%.
- `cost-attribution` — find expensive features as right-sizing targets.
- `load-test-plan` — validate after downsizing.
- `metrics-design` — utilization metrics are the input.

## Output

- Resource changes applied (via IaC where possible).
- `docs/finops/right-sizing-audits.md` — audit history + savings.
