---
name: a11y-audit
description: Audit a web interface against WCAG 2.1/2.2 AA — keyboard navigation, screen-reader support, color contrast, focus management, ARIA correctness, motion safety — and produce a prioritized findings report. Use when reviewing any UI for accessibility, when shipping a user-facing feature, when the user says "a11y", "accessibility", "WCAG", "screen reader", "keyboard nav", or before a release of any customer-facing surface.
---

# a11y-audit

## Purpose

Accessibility is not a checklist completed once; it's an attribute that decays without active maintenance. This skill walks WCAG 2.1/2.2 AA systematically, combines automated tools with manual checks, and produces a prioritized findings list. Designed so both developers and QA can drive it.

## When to use

- Reviewing any UI before merging.
- Auditing an existing app for the first time.
- After a feature that introduced new interactive components (modals, dropdowns, custom inputs).
- Before launching to external users.
- User says: "a11y", "accessibility", "WCAG", "screen reader", "keyboard nav", "ARIA", "508 compliance".

## The audit layers (run all of them)

### Layer 1 — Automated scan
Catches ~30-40% of issues. Necessary but not sufficient.

- **axe-core** — gold standard. Run via `@axe-core/cli`, `@axe-core/playwright`, browser extension (axe DevTools), or Storybook `@storybook/addon-a11y`.
- **Lighthouse** — accessibility section. Easy to run; less thorough than axe.
- **pa11y** — CI-friendly CLI.
- **WAVE** — browser extension; visual report.

Run on every page / major component. Capture results; track over time.

### Layer 2 — Keyboard-only review
The single most-revealing manual test. Unplug your mouse and:

- [ ] Every interactive element reachable via Tab.
- [ ] Tab order matches visual reading order.
- [ ] Focus indicator visible and high-contrast on every interactive element.
- [ ] Skip-to-content link present at the top.
- [ ] No keyboard traps — you can always Tab out (especially modals).
- [ ] Modals: Tab cycles within; ESC closes; focus returns to opener.
- [ ] Menus / dropdowns: arrow keys navigate; Enter/Space activates; ESC closes.
- [ ] Custom controls (toggle, slider, tabs, accordion) implement their ARIA pattern's keyboard interactions.

### Layer 3 — Screen-reader pass
Use VoiceOver (macOS Cmd+F5), NVDA (Windows free), or TalkBack (Android). Don't skip just because automated says pass.

- [ ] Page has a meaningful title (per route).
- [ ] Headings (h1-h6) form a logical outline.
- [ ] Images: meaningful `alt`; decorative images `alt=""`.
- [ ] Form fields associated with labels (NOT placeholder-as-label).
- [ ] Errors announced when they appear (`aria-live="polite"` or proper form-level alerts).
- [ ] Live regions for dynamic updates (toasts, results loading).
- [ ] Icons-only buttons have accessible names (`aria-label` or visually-hidden text).
- [ ] Tables have proper `<th>` and scope attributes.
- [ ] Lists are `<ul>`/`<ol>`, not div soup.
- [ ] Custom widgets announce role + state correctly.

### Layer 4 — Visual / sensory
- [ ] **Color contrast**: AA = 4.5:1 body text, 3:1 large/icons. AAA = 7:1 / 4.5:1. Test with axe / WebAIM Contrast Checker.
- [ ] **Color alone never conveys meaning**. Error states have an icon AND red, not just red.
- [ ] **Text resizable to 200%** without horizontal scroll or content loss.
- [ ] **No motion-triggered seizures** — no flashing > 3 times/second.
- [ ] **`prefers-reduced-motion` respected** — large motions disabled or reduced.
- [ ] **No content shifts** on focus / hover that confuse focus tracking.

### Layer 5 — Semantic / structural
- [ ] Page uses `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>` landmarks correctly.
- [ ] One `<h1>` per page (with rare exceptions for landmark sub-h1s).
- [ ] Buttons that look like links use `<button>`; links that act like buttons use `<a>`. Match semantics to behavior.
- [ ] Form structure: `<form>`, `<fieldset>`, `<legend>` where grouping helps.
- [ ] Language declared on `<html>` (`lang="en"`).
- [ ] Avoid ARIA where native HTML works. Bad ARIA is worse than no ARIA.

### Layer 6 — Pattern-specific (component-level)
For each interactive pattern in the UI, verify it follows the WAI-ARIA Authoring Practices Guide:

- Modal dialog (focus trap, ESC, aria-modal, aria-labelledby).
- Combobox / autocomplete (very fiddly; consider using a vetted library).
- Tabs (arrow keys, aria-selected, aria-controls).
- Disclosure / accordion (aria-expanded, button trigger).
- Menu / menubar (arrow keys, Home/End, aria-activedescendant pattern OR roving tabindex).
- Tooltip (focus-visible trigger, dismissible, doesn't move keyboard focus).
- Slider, switch, tree, listbox, carousel — each has its WAI-ARIA pattern.

See https://www.w3.org/WAI/ARIA/apg/patterns/ for the canonical patterns.

## Severity classification

- **Critical** — blocks core task for assistive-tech users (form unusable, modal traps focus, important content not announced).
- **High** — violates WCAG AA on a key surface (low contrast on primary CTA, missing labels on shipping form).
- **Medium** — violates WCAG AA on non-critical surface, or significantly degrades UX.
- **Low** — best-practice issue; nice to fix.

## Process

1. Run **Layer 1** (axe) — capture findings.
2. Walk **Layer 2** (keyboard) — record each broken interaction.
3. Walk **Layer 3** (screen reader) — at least one screen reader, on the critical user journeys.
4. Verify **Layer 4-6** systematically.
5. Compile findings into `docs/frontend/a11y-audit-YYYY-MM-DD.md`:
   - Counts by severity.
   - Each finding: location (file + selector), severity, WCAG criterion, description, fix.
   - Coverage notes (what was audited; what wasn't).
6. **File P0/P1 findings** as stories on `docs/plans/CURRENT.md`.

## Anti-patterns

- **Automated scan == passing.** It catches a minority of issues.
- **`role="button"` on a `<div>`** instead of using `<button>`. Native semantics first.
- **`aria-label` overriding visible text**. The visible text IS the label.
- **`tabindex="-1"`** to hide things from keyboard nav, then forgetting to manage focus elsewhere.
- **Custom focus indicators with low contrast** so the default blue ring is replaced with something prettier-and-unreadable.
- **Placeholder as label** — fails for screen readers and disappears on input.
- **Toast notifications without `aria-live`** — invisible to screen readers.
- **Disabling browser zoom** — never. Users zoom.

## Cross-references

- `frontend-design` — design for a11y; don't bolt on later.
- `form-design` — forms are the highest-stakes a11y surface.
- `modal-and-dialog-design` — focus management is the dialog's a11y core.
- `ui-copy` — labels and error messages are a11y artifacts.
- `qa-test-plan` — include a11y cases in every test plan for UI features.

## Output

`docs/frontend/a11y-audit-YYYY-MM-DD.md` — prioritized findings + WCAG criterion citations + suggested fixes.
