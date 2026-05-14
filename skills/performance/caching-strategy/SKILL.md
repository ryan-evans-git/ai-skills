---
name: caching-strategy
description: Decide what to cache, where to cache it, how long, and how to invalidate — using a disciplined framework that resists premature caching and surfaces invalidation hazards before they ship. Use when the user says "should we cache this", "Redis", "memcached", "CDN cache", "caching strategy", "stale data", or when a perf investigation points at cacheable repeated work.
---

# caching-strategy

## Purpose

Caching is the most-reached-for and most-mis-applied perf tool. It can produce 100x wins or create the hardest bugs in the system (stale data, thundering herds, cache stampedes, split-brain reads). This skill is a decision framework, not a recipe — it forces you to justify each cache before adding it.

## When to use

- An endpoint or computation is hot and repeats with the same inputs.
- A perf investigation shows repeated work where the inputs rarely change.
- User says: "should we cache this", "Redis", "memcached", "CDN cache", "caching strategy", "stale data", "cache invalidation".

## The five questions

Before adding any cache, answer all five. If you can't, don't add the cache.

1. **What's the cache miss cost vs. hit cost?**
   - Miss is "the expensive thing you're trying to avoid" — e.g. 200ms DB query.
   - Hit is the cache lookup itself — e.g. 1ms Redis GET.
   - If the miss cost isn't 10x+ the hit cost, the cache is probably not worth its complexity. Optimize the original path first.
2. **What's the actual hit rate going to be?**
   - Predict, then validate after deploy. If a key is requested with the same value 99% of the time, great. If different keys are requested with no repetition, a cache adds latency and zero hit rate.
   - Estimate from logs / RUM data, not vibes.
3. **What's the staleness tolerance?**
   - Real-time correctness required (auth tokens, balances, permission checks) → don't cache, or cache with sub-second TTL.
   - Eventual consistency OK (product descriptions, public profiles) → cache freely.
   - In between → state the tolerance explicitly: "stale up to 30s is acceptable because the use case is X."
4. **How will it be invalidated?**
   - **TTL-only** — simplest; user sees stale data for up to TTL. Fine for low-stake data.
   - **Event-based** — invalidate on the write that changes the underlying data. Reliable but couples writes to cache. Tricky across services.
   - **Versioned keys** — write changes a version; reads include the version. Old entries expire naturally. Good for distributed systems.
   - **Manual / admin-triggered** — should be an escape hatch only, not the primary mechanism.
   - **If you cannot answer this**, don't add the cache.
5. **What happens on cache failure?**
   - Cache down → fall through to source of truth, or hard fail? (Almost always: fall through.)
   - Source-of-truth down → serve stale, or fail? Define explicitly.
   - Stampede protection: if 1000 requests miss simultaneously, do they all hit the DB?

## Where to cache (layers)

Pick the layer farthest from the source-of-truth that still meets the staleness tolerance.

| Layer | Good for | Watch out for |
| --- | --- | --- |
| **Browser** (HTTP cache headers, service worker) | Static assets, infrequent-change API responses | Long-lived caches across deploys; use content-hash filenames |
| **CDN / edge** | Public, identical-for-all-users responses | Cookie / auth headers breaking cache key uniformity |
| **Reverse proxy** (Varnish, nginx) | Same as CDN, on-prem | Manual purge complexity |
| **In-process** (LRU in app memory) | Tiny, hot, per-instance | Inconsistency across instances; memory bloat |
| **Distributed** (Redis, memcached) | Cross-instance shared state, sessions, expensive computations | Network latency on miss; single point of failure if not HA |
| **Database query cache / materialized view** | Repeated complex queries | Refresh strategy + space cost |

## Process

1. **Walk the five questions** above for the proposed cache. Write the answers down.
2. **Choose the layer** that meets the staleness tolerance and matches data scope (per-user vs. shared).
3. **Pick the eviction + invalidation strategy.** Be explicit about TTL.
4. **Design the key.** Include enough to make it unique (user ID, locale, version), exclude noise (timestamps, request IDs).
5. **Plan for stampede protection** if miss is expensive:
   - **Single-flight / request coalescing** — N concurrent misses share one fetch.
   - **Background refresh** — refresh before TTL expires, never serving stale.
   - **Jittered TTL** — avoid all keys expiring simultaneously.
6. **Plan observability**:
   - Hit rate metric (must be tracked from day one).
   - Latency metric on hit vs. miss.
   - Cache-failure metric.
7. **Document** in `docs/architecture/caching.md` (living doc — one section per cache):
   - **What** is cached.
   - **Where** (layer + technology).
   - **Key** design.
   - **TTL** and invalidation strategy.
   - **Staleness tolerance** + business justification.
   - **Stampede protection** mechanism.
   - **Owner** + last review date.
8. **If the cache is in front of an external API**, also document rate-limit interaction — caching can hide rate-limit issues until cache expiry creates a flood.

## Anti-patterns

- **Caching without measuring miss cost.** "Just in case it's slow" caches the work needed to know whether you needed the cache.
- **No TTL.** "Forever" caches become source-of-truth without consent.
- **Event-based invalidation across services** without a reliable event bus → silent staleness.
- **Caching mutable user data** in shared keys — instant cross-user leak.
- **No hit-rate telemetry** → no idea whether it's working.
- **Cache as primary store.** If losing the cache loses data, it's not a cache; it's a database with worse durability.

## What this skill does NOT do

- Pick the specific cache technology — that's an ADR (`adr-writer`).
- Diagnose existing cache problems — point at `performance-investigation` for that.

## Output

`docs/architecture/caching.md` (living, one section per cache instance).
