---
name: responsive-design
description: Design and implement responsive layouts — breakpoint strategy, container queries, fluid type, touch targets, mobile-first vs. desktop-first defaults, viewport handling. Use when building any UI that should work across screen sizes, when an existing UI breaks at a particular width, or when the user says "responsive", "mobile", "breakpoints", "container query", "fluid type", "tablet".
---

# responsive-design

## Purpose

A site that "works on mobile" and a site designed for mobile look very different. This skill is the patterns that produce the second: layouts that breathe across sizes, components that adapt to their container (not the viewport), type that scales fluidly, and interactions that work for thumb-on-glass.

## When to use

- Building any UI that should work across phones, tablets, laptops, large monitors.
- Existing UI breaks at a specific width or device class.
- Greenfield design where the breakpoint strategy needs to be set.
- User says: "responsive", "mobile", "breakpoints", "container query", "fluid type", "tablet", "small screen", "mobile-first".

## Principles

### 1. Mobile-first by default — but think it through
- **Mobile-first**: base styles target mobile; `min-width` media queries layer on for larger screens.
- Rationale: mobile usually has more constraints (smaller viewport, slower network, touch input). Designing under constraint then expanding is easier than the reverse.
- **Counterexample**: a complex dashboard / admin tool whose primary use is desktop. Don't pretend mobile is primary; design desktop first, then decide what mobile sees (often: a simplified subset, or "use desktop for the full experience").

### 2. Container queries > viewport queries for most components
- **Viewport queries** (`@media (min-width: 768px)`) — based on screen width. Right for top-level layout.
- **Container queries** (`@container (min-width: 400px)`) — based on the component's container. Right for components used in different layout contexts (sidebar vs. main column vs. modal).
- Container queries are now widely supported. Default to them for component-internal responsive behavior.

### 3. Fluid type
- **`clamp()`** for fluid sizing: `font-size: clamp(1rem, 0.5rem + 1vw, 1.25rem);`
- Set min and max; let the middle interpolate.
- Avoids the "too small on desktop OR too big on mobile" tradeoff.
- Pair with line-height that also scales (often as a unitless ratio that adapts).

### 4. Fluid spacing
- Same principle for gaps and padding: `padding: clamp(1rem, 2vw, 2rem);`
- Section padding especially benefits — small on mobile, larger on desktop.

### 5. Breakpoint strategy
- **Fewer is better**: 3-5 breakpoints, not 12. Common set: `sm` (480), `md` (768), `lg` (1024), `xl` (1280), `2xl` (1536).
- **Name by purpose** internally if the names map to design decisions ("layout-shift", "two-column", "wide").
- **Set breakpoints from the design**, not from device sizes. Don't try to match the iPhone-X-Pro-Max viewport — there are too many. Set breakpoints where YOUR layout needs to change.

### 6. Touch targets
- **Minimum 44×44px** for touch (Apple guideline) — 48×48 in Material.
- **Spacing between targets** ≥ 8px so thumbs don't mishit.
- Hover states still useful but **don't rely on hover for important info** — touch devices don't hover.
- `:focus-visible` for keyboard; `:hover` for mouse; design for both.

### 7. Viewport meta tag
Required at the top of every responsive page:
```html
<meta name="viewport" content="width=device-width, initial-scale=1" />
```
Don't add `user-scalable=no` or `maximum-scale=1` — breaks zoom for low-vision users. (Cross-ref `a11y-audit`.)

### 8. Image responsiveness
- `srcset` + `sizes` for multiple resolutions. Browser picks the best.
- `<picture>` for art direction (different crop / image entirely at different sizes).
- Modern formats (AVIF, WebP) with fallback.
- Cross-ref `core-web-vitals`.

### 9. Layout primitives
Build on these instead of media queries when possible:
- **Flexbox** with `flex-wrap` for "as many as fit, wrap the rest."
- **CSS Grid** with `repeat(auto-fit, minmax(MIN, 1fr))` — auto-responsive without media queries.
- **`min()` / `max()` / `clamp()`** in widths, paddings, columns.
- **Aspect-ratio** to preserve proportions across sizes.

### 10. The "tablet awkward middle"
- Tablet sizes (768-1024) are where most responsive designs break down.
- Common bug: 3-column grid that looks great on desktop, becomes 1-column on phones, but stays 3-column on tablet — and looks cramped.
- Test explicitly at iPad / iPad Pro widths.

## Common patterns

### Sidebar layout
- Desktop: persistent sidebar + main.
- Tablet: collapsible sidebar.
- Mobile: hidden behind a menu trigger; full-screen drawer.

### Card grid
- Desktop: 3-4 columns.
- Tablet: 2 columns.
- Mobile: 1 column.
- Often `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` removes the need for media queries entirely.

### Navigation
- Desktop: horizontal nav with all items visible.
- Mobile: hamburger menu OR bottom tab bar (for app-like experiences).
- Tablet: pick — usually follow desktop unless the nav has > 5 top-level items.

### Tables
- Desktop: full table.
- Mobile: either horizontal scroll (with sticky first column) OR card-per-row (each row as a labeled card).
- Choose deliberately; depends on data.

### Modals
- Desktop: centered overlay with backdrop.
- Mobile: full-screen takeover OR bottom sheet (slides up from bottom). Bottom sheets feel native; pick based on context.

## Process

1. **Identify the screen sizes that matter** for the audience. Usually: phone (small + large), tablet, laptop, desktop. Maybe ultra-wide.
2. **Pick the breakpoint strategy** — viewport for top-level layout, container queries for components.
3. **Design at the smallest size first** (or the primary size — see "mobile-first counterexample" above).
4. **Layer on for larger sizes**: where does the layout change? What gets added vs. just repositioned?
5. **Use fluid sizing** (type, spacing) for in-between sizes instead of stepping at every breakpoint.
6. **Test on real devices** — emulators lie about touch behavior, scroll behavior, and on-screen keyboard impact.
7. **Verify**:
   - Touch targets ≥ 44px (`a11y-audit`).
   - Zoom 200% works without horizontal scroll.
   - Bottom of viewport accessible when on-screen keyboard is up (mobile form bug).
8. **Document at `docs/frontend/responsive.md`** — breakpoint strategy, layout patterns, common gotchas.

## Anti-patterns

- **Designing only for one width.** "Looks great on my MacBook."
- **Hiding important content on mobile.** Users on phones don't deserve less.
- **Trying to match every device size** with media queries instead of fluid sizing.
- **Touch targets 24×24** because "they look better." Unusable for many fingers.
- **Hover-only interactions.** Hidden on touch devices.
- **Bottom-of-screen CTAs covered by browser chrome / on-screen keyboard.**
- **Fonts that shrink below 14px on mobile.** Body text minimum is 16px on touch; 14px caption max.
- **Container width = viewport width** at every size, no max-width. Body text becomes unreadable on wide monitors.
- **`user-scalable=no`** in viewport meta. Breaks zoom.

## Cross-references

- `frontend-design` — design at every breakpoint.
- `a11y-audit` — touch targets, zoom, focus visible at all sizes.
- `core-web-vitals` — responsive images / CLS.
- `design-system-keeper` — breakpoints are tokens.

## Output

Responsive components / pages, tested at relevant sizes. For complex apps, `docs/frontend/responsive.md` documenting the strategy.
