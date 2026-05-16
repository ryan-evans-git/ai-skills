---
name: design-system-keeper
description: Establish and maintain a design system — tokens (color, typography, spacing, motion, radii, shadows), component primitives, naming conventions, Storybook discipline. Use when starting a new frontend project, when colors/spacing are inconsistent across the app, or when the user says "design system", "design tokens", "Storybook", "component library", "Figma tokens".
---

# design-system-keeper

## Purpose

Without a design system, every new component picks slightly-different colors, spacing, and behavior. The drift is invisible at first and impossible to fix after twelve months. This skill establishes the tokens + component primitives early, then keeps them durable.

## When to use

- Starting a new frontend project.
- Existing project where colors / spacing / shadows are inconsistent.
- Migrating from one design language to another.
- Before scaling a UI team beyond 2-3 engineers.
- User says: "design system", "design tokens", "Storybook", "component library", "Figma tokens", "consistency".

## What a design system is (minimum viable)

1. **Tokens** — primitive values: colors, type scale, spacing, radii, shadows, motion durations & easings, breakpoints.
2. **Semantic tokens** — names for *intent*: `color.text.primary`, `color.bg.elevated`, `space.gap.dense`. Reference primitives but used everywhere in the app.
3. **Component primitives** — Button, Input, Card, Modal, Tooltip, etc. with all states designed.
4. **Documentation** — Storybook (or equivalent) showing every component, every state, every prop.
5. **Naming + usage rules** — written so the next person doesn't re-invent.

## Tokens — the foundation

### Color
- **Primitive palette**: a brand color (with shade ramp), a neutral ramp, semantic colors (success/warning/danger/info), each with shades.
- **Semantic tokens**:
  - `color.text.primary`, `color.text.secondary`, `color.text.disabled`, `color.text.inverse`.
  - `color.bg.app`, `color.bg.elevated`, `color.bg.muted`.
  - `color.border.default`, `color.border.subtle`, `color.border.focus`.
  - `color.action.primary`, `color.action.primary.hover`, `color.action.primary.active`, `color.action.primary.disabled`.
- **Light + dark modes**: semantic tokens shift; primitive palette doesn't. Test both at every step.

### Typography
- **Type scale**: 6-10 sizes, named by purpose (`display.lg`, `display.md`, `heading.lg`, `body.md`, `body.sm`, `caption`).
- **Per size**: font-size, line-height, letter-spacing, font-weight.
- **Font stack**: a primary (often custom), a fallback (system), a mono.
- **Numerals**: tabular for data; default lining for everything else.

### Spacing
- **Scale**: usually a 4px or 8px base, with steps (2, 4, 8, 12, 16, 24, 32, 48, 64, 96).
- **Semantic spacing**: `space.gap.tight`, `space.gap.default`, `space.gap.loose`, `space.section`.

### Radii
- Usually 4-6 values (`radius.sm`, `radius.md`, `radius.lg`, `radius.pill`, `radius.circle`).
- Pick one or two for cards / buttons; resist "different radius per surface."

### Shadows
- **Elevation ramp**: `shadow.subtle`, `shadow.raised`, `shadow.overlay`, `shadow.sticky`.
- Each combines blur + spread + tint. Don't reuse the same shadow on every surface.

### Motion
- **Durations**: `motion.fast` (~120ms), `motion.default` (~200ms), `motion.slow` (~400ms).
- **Easings**: `motion.standard` (cubic-bezier), `motion.emphasized`, `motion.decelerate`, `motion.accelerate`.
- Tie to `prefers-reduced-motion` at the component level.

### Breakpoints
- Usually 3-5 (`xs`, `sm`, `md`, `lg`, `xl`). Container queries are often a better choice than viewport queries — see `responsive-design`.

## Storage + tooling

- **Where tokens live**: a single source-of-truth file. Common patterns:
  - CSS variables (`:root { --color-bg: ... }`).
  - Tailwind config (`tailwind.config.js` extending the theme).
  - Style Dictionary (cross-platform: web, iOS, Android).
  - Figma tokens (synced to code via plugin or Style Dictionary).
- **Pick one** and don't fork. Tokens duplicated in Figma and code is the most common drift source.

## Component primitives

Build these first; everything else composes from them:

- **Button** (primary, secondary, tertiary, ghost, danger; sizes; with-icon variants; loading state).
- **Input / Textarea** (with label, helper text, error, success states).
- **Select / Combobox**.
- **Checkbox / Radio / Switch**.
- **Modal / Dialog** (see `modal-and-dialog-design`).
- **Tooltip / Popover**.
- **Card / Surface** (with elevation variants).
- **Avatar / Badge / Tag / Chip**.
- **Spinner / Skeleton** (see `loading-and-error-states`).
- **Toast / Alert / Banner**.
- **Tabs / Accordion**.
- **Table** (sortable, dense / comfortable, with row actions).

Each must be:
- Designed in all states (default, hover, focus, active, disabled, loading, error).
- A11y-correct (cross-ref `a11y-audit`; many of these have WAI-ARIA patterns).
- Documented in Storybook with controls for every prop.

## Storybook discipline

- One story file per component.
- A story per significant state / variant.
- A `Default` story that's the most-common usage.
- Controls (args) exposed for every prop.
- Visual regression hooked up (cross-ref `visual-regression-testing`).
- A11y addon enabled and findings tracked.

## Process

1. **Audit current state** — sample 10-20 components in the app; tally color values, spacing values, radii, shadows. Surface the drift.
2. **Define primitives** — pick the scales you'll use. Resist "let's keep our options open" — fewer tokens is better.
3. **Define semantic tokens** — name by intent, not appearance. Once `color.action.primary` exists, the app uses *that*, not `blue-500`.
4. **Migrate components** — replace hardcoded values with semantic tokens, one component at a time.
5. **Set up Storybook** if not already; document each primitive.
6. **Write `docs/frontend/design-system.md`** — the canonical reference:
   - Tokens (with usage examples).
   - Component primitives (with links to Storybook).
   - Naming rules.
   - "Don't reach for X; reach for Y" guidance.
7. **Cross-link** from `README.md`, `CLAUDE.md` / `AGENTS.md`.

## Anti-patterns

- **Tokens defined separately in Figma and code.** Drift guaranteed.
- **Naming by appearance** (`color.blue.500`) instead of intent (`color.action.primary`). When you rebrand, every usage breaks.
- **Too many tokens.** Twelve shades of grey nobody can tell apart.
- **Components that override the system "just this once."** Either fix the system to accommodate, or push back on the design.
- **No "what NOT to use" guidance.** Engineers reach for the wrong token without it.
- **Storybook abandoned.** Six months in, half the components aren't in it; new joiners can't trust it.
- **Design system as a separate repo no one updates.** Co-locate or auto-sync.

## Cross-references

- `frontend-design` — uses the tokens you establish here.
- `a11y-audit` — every component's a11y attributes belong in the system.
- `responsive-design` — breakpoints are tokens.
- `loading-and-error-states` / `modal-and-dialog-design` — primitives.
- `visual-regression-testing` — Storybook + snapshots.

## Output

- Token files (CSS vars / Tailwind config / Style Dictionary).
- Storybook with primitives.
- `docs/frontend/design-system.md` — single living doc.
