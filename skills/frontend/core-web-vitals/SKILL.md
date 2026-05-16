---
name: core-web-vitals
description: Optimize and maintain Core Web Vitals — LCP, INP, CLS — plus the related metrics (TTFB, FCP, total bundle size, image weight, font loading). Use when a page is slow, before launching a public site, when the user says "Core Web Vitals", "LCP", "INP", "CLS", "PageSpeed", "Lighthouse score", "page weight", or when Search Console flags issues.
---

# core-web-vitals

## Purpose

Core Web Vitals are how Google (and increasingly users + business teams) measure whether a page is actually fast. Generic "lighthouse green" isn't enough — you need to track p75 in real-user-monitoring, set budgets, and hold the line. This skill is the playbook.

Pairs with `performance-budget` (general) and `performance-investigation` (any-tier perf debugging). This skill is the frontend-specific siblings.

## When to use

- A page is slow / Lighthouse score is mediocre.
- Search Console / Real User Monitoring flagged a metric as poor.
- Before launching a public-facing site.
- User says: "Core Web Vitals", "LCP", "INP", "CLS", "PageSpeed", "Lighthouse score", "page weight", "TTFB", "font loading", "image optimization".

## The metrics — what each measures, how to fix

### LCP — Largest Contentful Paint
**What**: Time from navigation to the largest content element rendering.
**Target**: < 2.5s at p75.

**Most common causes when bad**:
- Hero image not optimized (huge, no priority hint, no proper format).
- Slow TTFB (server response — see backend perf).
- Render-blocking CSS / JS in `<head>`.
- Fonts loading the LCP text late.
- Slow DNS / TLS / redirects.

**Fixes (in order of impact)**:
1. **Optimize the LCP element** — usually the hero image:
   - Modern formats (AVIF / WebP) with fallback.
   - Proper dimensions; don't ship 4000px for a 600px slot.
   - `srcset` + `sizes` for responsive serving.
   - `fetchpriority="high"` on the LCP image.
   - Preload it: `<link rel="preload" as="image" href="...">`.
2. **Reduce TTFB**:
   - SSR/SSG at the edge if possible.
   - CDN for static assets + cacheable HTML.
   - Eliminate redirect chains.
3. **Eliminate render-blocking**:
   - Inline critical CSS; defer rest.
   - `defer` / `async` on non-critical JS.
4. **Font strategy**:
   - `font-display: swap` so text renders with fallback while custom loads.
   - Preload critical fonts; subset to characters used.
   - Or self-host with proper caching.

### INP — Interaction to Next Paint
**What**: Latency of user interactions (clicks, taps, key presses). Replaced FID.
**Target**: < 200ms at p75.

**Most common causes when bad**:
- Long JavaScript tasks (>50ms) blocking the main thread.
- Heavy third-party scripts (analytics, A/B test, chat widgets).
- Expensive re-renders on input.
- Synchronous layout / forced reflow.

**Fixes**:
1. **Break up long tasks** — `setTimeout`, `requestIdleCallback`, `scheduler.yield()`.
2. **Defer / lazy-load third-party scripts.** Especially: chat widgets, ad code, A/B test scripts. Use `<script defer>` or load on interaction.
3. **Memoize / virtualize lists** so input doesn't re-render thousands of nodes.
4. **Debounce expensive handlers** (search-as-you-type, autosave). 200-300ms typical.
5. **Web workers** for genuinely-CPU-heavy work (parsing, calculation).
6. **Avoid forced layout** — read DOM properties before writing in animation frames.

### CLS — Cumulative Layout Shift
**What**: Visual stability — how much content shifts unexpectedly during page life.
**Target**: < 0.1 at p75.

**Most common causes when bad**:
- Images without dimensions → reflow when they load.
- Web fonts swapping → text reflow.
- Ads / embeds / iframes injected without reserved space.
- Banners / cookie notices appearing late and pushing content.

**Fixes**:
1. **Set width / height on images and videos** (or `aspect-ratio` CSS).
2. **Reserve space for embeds / ads / banners**. Use `min-height` or skeleton boxes.
3. **Font loading**: use `size-adjust`, `ascent-override`, etc. to minimize swap-induced shift.
4. **Avoid inserting content above existing content** after page load.
5. **Animate `transform` / `opacity`** (compositor-only), not properties that trigger layout.

## Supplementary metrics

- **TTFB** — Time to First Byte. < 800ms target. Backend / CDN concern.
- **FCP** — First Contentful Paint. < 1.8s. Faster than LCP; same fix patterns.
- **Total Blocking Time** (TBT, lab equivalent of INP). < 200ms.
- **Total page weight** — set a budget; pre-launch hardstop.
- **JS bundle size** — < 200KB gzipped on critical path is a reasonable bar.

## Measurement

### Lab (synthetic) — for development iteration
- **Lighthouse** in DevTools or `lighthouse` CLI.
- **WebPageTest** for detailed waterfall.
- **PageSpeed Insights** (combines lab + field).

Lab is reproducible but doesn't reflect real users.

### Field (real-user monitoring) — for ground truth
- **Chrome User Experience Report (CrUX)** — public, aggregated.
- **`web-vitals` JS library** — send to your own analytics.
- **Vercel Speed Insights**, **Cloudflare Speed**, **Datadog RUM**, **SpeedCurve** — managed.

**P75 in the field is the metric that matters.** Lab tells you the page's potential; field tells you the user's reality.

## Process

1. **Measure current state** in both lab (Lighthouse) and field (RUM if available; PageSpeed Insights otherwise).
2. **Identify which metric(s) are failing** and on which routes.
3. **Profile the failing metric** with Chrome DevTools Performance tab.
4. **Pick the highest-impact fix** per the fixes-list above. One at a time.
5. **Measure delta** — both lab and field (field updates daily/weekly).
6. **Set CI thresholds** so regressions block merges:
   - Lighthouse CI on critical routes.
   - Bundle-size check (`bundlesize`, `size-limit`, or framework-native).
7. **Document at `docs/frontend/web-vitals.md`** — current numbers + targets + active optimizations + budget thresholds.

## Anti-patterns

- **Optimizing lab Lighthouse score with no field signal.** Lab measures the optimistic case.
- **Adding the analytics / chat / ad scripts that broke perf without questioning them.** Each new script has a real cost.
- **Image without dimensions because "we'll fix it later."** CLS.
- **All fonts loaded blocking.** Pick critical; defer or system-fallback the rest.
- **Single big JS bundle.** Split by route.
- **`prefers-reduced-motion` ignored.** Both an a11y issue AND a perf opportunity (heavy animations are expensive).
- **No regression guard.** Performance is the easiest thing to silently regress.

## Cross-references

- `performance-budget` — frontend budgets are part of the overall budget.
- `performance-investigation` — backend + frontend, this is the frontend specialist.
- `frontend-design` — design with perf in mind (image weight is design choice).
- `responsive-design` — `srcset` / image sizes belong to responsive too.
- `rendering-strategy` — SSR/SSG/ISR/CSR choice affects TTFB and LCP.

## Output

- Code changes implementing fixes.
- `docs/frontend/web-vitals.md` — current numbers + targets + budget.
- CI checks (Lighthouse CI, bundle-size).
