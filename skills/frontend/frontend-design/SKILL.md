---
name: frontend-design
description: Build distinctive, production-grade frontend interfaces — pages, components, full applications — with high design quality that avoids the generic "AI aesthetic" defaults. Use when the user asks to design or build any web UI, when they say "design this", "build a page for X", "make this look good", "improve the design", "redesign", or whenever a frontend component or screen is being created or rebuilt.
---

# frontend-design

## Purpose

Default LLM-generated UI looks the same: white background, blue primary button, grey card with subtle shadow, centered hero with gradient, generic illustration. This is the "AI aesthetic" — competent but immediately recognizable as generated, and forgettable. This skill is permission and pattern to do better.

The goal is interfaces that feel **considered, opinionated, and specific** — like a designer with taste made deliberate choices rather than a model reaching for the median.

## When to use

- Any request to design or build a web UI (page, component, dashboard, app).
- "Make this look good" / "improve the design" / "more polished."
- Greenfield design — there's no design system yet and you're making the choices.
- Redesigning an existing surface.
- Building a marketing page, landing page, product UI, internal tool, dashboard.

## The anti-pattern list — things to NOT default to

If the design has any of these and it's not deliberate, it's drifting toward generic:

- **Single accent color (usually blue) on white**. Pick a real palette.
- **`text-gray-500` everywhere** for "subtle" text. Use a real typographic hierarchy.
- **`rounded-2xl shadow-lg` on every card**. Decide what's elevated and what isn't, intentionally.
- **Generic hero**: centered headline, two-line subhead, two buttons, illustration to the right.
- **Equal-height feature grids** (3 columns of identical cards with icon + heading + body).
- **Tailwind defaults untouched** — same shade scale, same border radii, same shadow ramp as every other shipped LLM-generated UI.
- **Gradient backgrounds with two colors** as the "interesting" choice. Almost never the right move.
- **Stock-illustration vibes** — figures with oversized heads, monochrome line drawings of laptops.
- **All sans-serif at the same weight**. Type contrast is free quality.
- **Inflated whitespace** to fake luxury. Spacing should be load-bearing, not decorative.
- **Buttons without states**. Hover, focus, active, disabled, loading — design each.
- **Emoji as iconography**. Use a proper icon set or commission/design icons.
- **Body text below 14px or above 18px** without a reason.

## The principles

### 1. Make a real palette
- Pick **one or two** brand colors that feel specific, not Material defaults. Cyan-600 and indigo-600 are not a brand.
- Build a neutral ramp with actual contrast. Pure black on pure white is fine if the design supports it; otherwise pick a near-black and an off-white with character (warm vs. cool deliberately).
- Define semantic colors separately (success / warning / danger / info) — don't reuse brand colors for them.
- Test in dark mode if dark is supported. Don't just invert.

### 2. Build typographic hierarchy
- **Sans + serif** mixed, or a single high-contrast typeface (variable fonts make this cheap).
- **Display sizes** that feel like display — 48-96px for hero headings. Don't shrink everything to 32px because that's "safe."
- **Tracking and leading** adjusted per size. Big text gets tighter tracking; small text gets looser.
- **Numerals**: tabular for data, lining or old-style by context.
- **Quotes, dashes, em-dashes** correct. Smart quotes, en/em dashes — not `--`.

### 3. Use spacing as composition
- Spacing should *say something*. Two related items get tight spacing; unrelated items get generous spacing. Read the design and tell what's grouped without looking at borders.
- Avoid evenly-spaced everything. Variation creates rhythm.
- 8pt grid is fine as a starting baseline. Don't worship it.

### 4. Show personality in details
- Specific cursor on interactive elements.
- A real selection color, not the default.
- Custom scrollbars on the right surfaces (sparingly).
- Focus rings that match the design language (not the browser default blue).
- 404 / empty / error states with care. They get more attention from real users than expected.
- Microinteractions that earn their keep — a button that subtly responds, a chart that draws in, a toggle that feels good.

### 5. Layout discipline
- Asymmetric layouts where appropriate; centered ones where the symmetry is meaningful.
- Generous whitespace at the right places, tight at others.
- Real grid use — columns that line up across sections, not arbitrary widths.
- Constrain max widths for readability (60-75ch for body; wider for tabular / dashboard data).

### 6. Color contrast that respects users
- WCAG AA minimum (4.5:1 body text, 3:1 large/icons). AAA where you can. See `a11y-audit`.
- Test in colorblind simulators.
- Don't rely on color alone to convey meaning.

### 7. Motion with intent
- Motion communicates: state change, hierarchy, causality.
- Default to 150-250ms for UI feedback, 400-600ms for entrances.
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` for in-and-out; avoid linear.
- Respect `prefers-reduced-motion`. Required, not optional. See `a11y-audit`.

### 8. Density per surface
- Marketing: low density, large type, expressive.
- Product UI: medium density, readable, restrained.
- Dashboards / data tables: high density, tabular numerals, dense rows, generous on horizontal scan.
- Match the density to the user's task, not to "modern."

## Process

1. **Establish the design language** before writing components:
   - Palette (brand + neutral ramp + semantic).
   - Typography (display, body, mono).
   - Spacing scale.
   - Border radii.
   - Shadow ramp (often: none, soft, elevated, sticky).
   - Motion vocabulary.
2. **For each component**, design states explicitly:
   - Default, hover, focus, active, disabled, loading, error, success, empty.
   - Light and dark mode if supported.
3. **Cross-ref `design-system-keeper`** — formalize the tokens early; everything below depends on them.
4. **Review against this skill's anti-pattern list.** If a default would land you in those, change it.
5. **Test** the result against `a11y-audit` (mandatory) and `core-web-vitals` (perf).

## What good output looks like

- A reviewer should be able to tell, at a glance, that this is THIS product — not a generic dashboard / marketing template / SaaS clone.
- The design tells a user where to look, what to do, and what just happened. Hierarchy is doing the work, not decoration.
- Every element has a reason for being the way it is. Spacing, weight, color — defensible.
- Edge cases (loading, error, empty, long content, short content) are handled.

## Cross-references

- `design-system-keeper` — formalize tokens and components as you go.
- `a11y-audit` — every UI passes a11y; design for it, don't bolt on.
- `core-web-vitals` — perf budget includes the design (image weight, font weight, animation cost).
- `responsive-design` — design at every breakpoint, not just one.
- `component-architecture` — composition patterns for the components you build.
- `loading-and-error-states` — the states the design must handle explicitly.
- `ui-copy` — the words are part of the design.

## Output

Code (TSX / Vue / Svelte / HTML+CSS) implementing the design, with the design rationale documented in `docs/frontend/design-rationale.md` if the project is non-trivial.
