---
name: rendering-strategy
description: Decide between SSR / SSG / ISR / CSR / streaming / edge rendering for each route or surface, based on user need, data freshness, SEO requirements, and operational cost. Use when designing a new page / feature, when "the page is slow" or "Google isn't indexing this", or when the user says "SSR", "SSG", "ISR", "static", "client-side rendering", "streaming", "edge", "PPR".
---

# rendering-strategy

## Purpose

Modern web frameworks support a handful of rendering strategies. Picking the wrong one is one of the most expensive mistakes — it bakes in tradeoffs that are painful to reverse. This skill is the decision framework.

## When to use

- Designing a new page or feature.
- Existing route is slow / not indexed by search / cost-heavy.
- Migrating between frameworks.
- User says: "SSR", "SSG", "ISR", "static", "client-side rendering", "streaming", "edge", "PPR" (Partial Prerendering), "rendering strategy".

## The options — what each is

| Strategy | What | TTFB | LCP | Freshness | Cost |
| --- | --- | --- | --- | --- | --- |
| **SSG** (Static Site Generation) | HTML generated at build time, served from CDN | Best | Best | Stale until rebuild | Lowest |
| **ISR** (Incremental Static Regeneration) | SSG + revalidate-after-N-seconds in background | Best | Best | Eventually fresh | Low |
| **SSR** (Server-Side Rendering) | HTML generated per request, fresh data | Medium | Good | Always fresh | Medium |
| **Streaming SSR** | SSR but flushes HTML as it's ready | Good (early flush) | Good | Always fresh | Medium |
| **PPR** (Partial Prerendering, Next.js) | Static shell + streamed dynamic holes | Best (shell) | Best | Hybrid | Medium |
| **CSR** (Client-Side Rendering) | Skeleton HTML; JS fetches + renders in browser | Best (skeleton only) | Worst | Always fresh | Lowest (server) |
| **Edge SSR** | SSR running on edge (Cloudflare Workers, Vercel Edge, etc.) | Best | Good | Always fresh | Medium |

## Pick by surface

### Marketing pages (home, pricing, about, blog posts)
- **SSG** is the default.
- Pages rebuild on content change (CMS webhook or scheduled build).
- Maximizes SEO + performance + cost-efficiency.
- Exception: heavy personalization → ISR or SSR with edge caching.

### Documentation
- **SSG**. Same logic.
- Cross-content search benefits from a separate index (Algolia, FlexSearch).

### Product / dashboard (auth-required, per-user data)
- **SSR** (or streaming SSR) for first paint with real data.
- Avoid CSR-only — slow LCP, white screen, bad on mobile.
- Edge SSR if latency matters and the data store is geo-replicated.

### Product listing pages (e-commerce)
- **ISR** is the sweet spot — fast like SSG, fresh enough for inventory updates.
- Revalidate aggressively (e.g. every 60s) so prices/stock stay reasonable.
- Or PPR (Next.js) for the static catalog shell + per-request dynamic price/inventory.

### Search results
- **SSR / streaming SSR** — needs current data.
- Edge if latency matters.
- The search box itself is typically CSR (client-side reactivity).

### User profile pages (auth-required, personal)
- **SSR** for first paint.
- Updates after that are CSR (don't reload the page on every change).

### Highly interactive (editor, drawing tool, IDE)
- **CSR** is fine — the user is in the app for minutes. Initial load can be slower; ongoing performance is what matters.
- Often SSR a minimal shell, then hand off to client.

### Real-time (chat, live data, notifications)
- **SSR** for the initial state + WebSocket / SSE for updates.
- Don't poll if you can subscribe.

### LLM / streaming responses
- **Streaming SSR** is purpose-built for this. Show response tokens as they arrive.

## The decision flow

```
Is the page content the same for every user (anonymous)?
├── Yes → Does the content change?
│         ├── Rarely (< daily)   → SSG
│         ├── Sometimes (hourly) → ISR
│         └── Frequently (per-min) → SSR (or ISR with short revalidate)
└── No → Is SEO needed (search-indexed)?
          ├── Yes  → SSR (or streaming SSR / PPR)
          └── No   → Is initial paint important?
                    ├── Yes → SSR (or PPR)
                    └── No  → CSR
```

**Edge vs. region**: orthogonal to the above. Use edge when:
- The data is in an edge-replicated store (KV, edge config, geo-replicated DB).
- Latency from the user's geography matters.
- Don't use edge if you're going to call back to a single-region DB anyway — you've added a hop without benefit.

## SEO considerations

If the page must rank in search:
- **Content must be in the initial HTML** that crawlers receive.
- Pure CSR pages (with content rendered after JS hydration) are now indexed by Google but **less reliably** and **slower-ranking** than SSR/SSG.
- For SEO-critical surfaces, **default to SSG/SSR**. CSR only if the page intentionally isn't indexed.

## Data fetching tied to rendering

The rendering strategy interacts with data fetching:

- **SSG**: fetch at build time only. `getStaticProps` / equivalent.
- **ISR**: same as SSG + a revalidate window.
- **SSR**: fetch per request, server-side. `getServerSideProps` / equivalent.
- **Streaming SSR**: stream chunks as data resolves. React Suspense, Next.js loading.tsx.
- **CSR**: fetch client-side. SWR / React Query / Apollo client.

Most modern frameworks let you mix per-component within a page (server components for static parts, client components for interactivity). Use the mix; don't pick one universally.

## Performance implications

- **LCP** improves dramatically with SSG/SSR + edge over CSR. The hero is rendered before JS even loads.
- **INP** depends mostly on hydration cost (size of client JS) regardless of rendering strategy.
- **CLS** is independent — depends on layout discipline (cross-ref `core-web-vitals`).
- **TTFB** is best for SSG (CDN serve), worst for unoptimized SSR (waiting on DB).

## Cost implications

- **SSG**: lowest. Build once, serve from CDN forever.
- **ISR**: low. Builds when triggered; serves cached otherwise.
- **SSR**: per-request compute. Costs scale with traffic.
- **CSR**: lowest server cost; pushes work to the client (so degrades on slow devices).
- **Edge SSR**: medium; cheaper per-request than regional, but slower-cold-start without proper warmth.

## Process

1. **For each route / surface, walk the decision flow above.**
2. **For sites with many surfaces, build a table** in `docs/frontend/rendering-strategy.md`:

   | Route | Strategy | Why | Data sources | Revalidation |
   | --- | --- | --- | --- | --- |
   | `/` | SSG | Marketing; rebuild on CMS publish | CMS | Webhook-triggered build |
   | `/products` | ISR | Inventory changes hourly | Postgres | 60s revalidate |
   | `/products/[id]` | ISR | Same | Postgres | 60s revalidate |
   | `/checkout` | SSR | Per-user state | Session + Postgres | n/a |
   | `/dashboard` | SSR + CSR | Auth + per-user | Auth + API | n/a |
   | `/app/*` | CSR | Heavy interactivity | API | n/a |

3. **Cross-check with `core-web-vitals`** — the rendering strategy must support the perf budget.
4. **Document any deviations** from the obvious default with a reason — these are the choices future engineers will second-guess.
5. **Wire monitoring** per strategy:
   - SSG / ISR: build times + revalidation rates.
   - SSR: per-route latency.
   - CSR: client-side perf RUM.

## Anti-patterns

- **Picking one strategy for the whole app.** Modern frameworks let you mix per route.
- **CSR for SEO-critical pages.** Slower indexing; sometimes not indexed at all.
- **SSR for static marketing pages.** Wasted compute; worse latency than SSG.
- **ISR with stale-for-hours revalidation on price/inventory.** Customers see wrong info.
- **Edge SSR that calls a single-region DB.** Added latency, no benefit.
- **Streaming without `prefers-reduced-motion`** consideration — incremental layout can be jarring.
- **No fallback for build failures.** ISR with revalidation can serve a stale page; that's fine. CSR can't fallback if the API is down without a clear error UI.

## Cross-references

- `core-web-vitals` — rendering strategy directly affects LCP / TTFB.
- `caching-strategy` — ISR is a cache; same five-question discipline.
- `performance-investigation` — slow pages: rendering strategy is one of the levers.
- `frontend-design` — design needs to handle the strategy's loading patterns.
- `loading-and-error-states` — CSR + streaming need rich loading patterns.

## Output

Per-route rendering choices implemented + `docs/frontend/rendering-strategy.md` documenting them.
