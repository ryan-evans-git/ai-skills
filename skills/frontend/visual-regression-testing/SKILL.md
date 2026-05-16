---
name: visual-regression-testing
description: Set up and maintain visual regression tests — snapshot diffing per component and per page, with discipline around dynamic content masking, baseline updates, and threshold tuning. Use when a design regression slipped past code review, when launching a design system, or when the user says "visual regression", "Percy", "Chromatic", "screenshot test", "snapshot test", "Playwright visual".
---

# visual-regression-testing

## Purpose

Pixel changes are often the regressions code review misses. A 4px padding shift, a button color drifting, a chart axis breaking on long labels — these escape diffs and tests but hit users. Visual regression tests catch them by diffing screenshots against a baseline on every PR.

## When to use

- A design regression made it to production despite passing all tests.
- Launching or maintaining a design system / component library.
- Before / after a refactor that touches CSS.
- User says: "visual regression", "Percy", "Chromatic", "screenshot test", "snapshot test", "Playwright visual comparisons".

## Pick a tool

| Tool | Best for | Notes |
| --- | --- | --- |
| **Chromatic** | Storybook-driven design systems | Tight Storybook integration; cloud-hosted; review UI is best-in-class. Cost grows with snapshot count. |
| **Percy** | Cross-framework, full-page snapshots | BrowserStack-owned; mature; good UI. |
| **Playwright Visual Comparisons** | Existing Playwright suite | `expect(page).toHaveScreenshot()`. Built-in; cheap (no external service). |
| **Lost Pixel** / **BackstopJS** | Self-hosted / open-source | More setup but no per-snapshot cost. |

Default: **Chromatic if you have a Storybook-driven design system; Playwright Visual Comparisons if you have a Playwright test suite and don't want a separate service.**

## What to snapshot

### Per-component (the right level for most cases)
- **Each component** in **each significant variant** (default, hover, focus, error, disabled, loading).
- **Light + dark mode** if both are supported.
- **At a few representative widths** (typically mobile + desktop).
- Lives in Storybook stories with the Chromatic addon, or in Playwright tests of a Storybook URL.

### Per-page (selectively)
- Critical user-facing pages: home, signup, checkout.
- Don't snapshot every page — most are compositions of components, and component snapshots cover them.
- Use page-level for: pages with real layout (not just component composition), landing pages, marketing.

### NOT for
- Pages with heavily dynamic content (live data, timestamps, ads) — too much noise.
- Animations mid-frame — capture states (before / after), not moments.

## Handling dynamic content

The biggest source of flake. Strategies:

1. **Mock the data** — feed fixed fixtures, not real API.
2. **Freeze time** — many tools have `clock.setFixedTime()` or similar.
3. **Mask volatile regions** — most tools let you blur / replace specific selectors.
4. **Skip the dynamic region** as part of the test setup — e.g. hide the timestamp via CSS.

Example (Chromatic):
```js
// .storybook/preview.js
export const parameters = {
  chromatic: {
    delay: 200, // wait for animations to settle
    pauseAnimationAtEnd: true,
  },
};

// per-story:
export const Default = {
  parameters: {
    chromatic: { diffThreshold: 0.2 },
  },
};
```

## Threshold tuning

A pixel-perfect threshold catches font rendering differences across OSes, browsers, GPUs. A loose threshold misses real regressions.

- **Default**: ~0.1-0.2% pixel difference, with anti-aliasing tolerance.
- **Tighter** for design-system primitives (you want to catch a 1px shift in a button).
- **Looser** for full-page snapshots with realistic content.

Don't disable diffing entirely "because it's flaky." Tune the threshold or mask the dynamic part.

## Baseline updates — workflow

The discipline that makes visual regression sustainable:

1. **CI runs against baseline**. Any diff → status check fails on the PR.
2. **Reviewer sees the diff** in the tool's UI.
3. **Three outcomes**:
   - **Intentional change** (the PR redesigned the component): reviewer approves; new screenshots become the baseline.
   - **Unintentional change** (something broke): fail the PR; author fixes.
   - **Flaky** (false positive from dynamic content): fix the masking / mock, don't just keep approving.
4. **Approval is per-snapshot**, not blanket — discourage "just approve all."

**The failure mode to avoid**: a culture of "just approve the changes" without review. Defeats the entire mechanism.

## CI integration

- **Run on every PR.** Block merge on unapproved diffs (or at minimum, surface them prominently).
- **Run on main after merge** to keep the baseline current.
- **For Chromatic / Percy**: GitHub status check + review URL in the PR.
- **For Playwright Visual**: `expect(...).toHaveScreenshot()` fails the build; CI surfaces the diff image.

## Storybook + visual regression — the canonical combo

This combo is so common it deserves explicit setup:

1. Build components with stories covering each variant + state.
2. Chromatic CI publishes Storybook + runs snapshots on each PR.
3. Stories double as: developer docs, design review surface, visual regression specs.
4. Cross-ref `design-system-keeper` — Storybook is part of the design system.

## When NOT to use visual regression

- **Highly dynamic dashboards** — snapshot value is low; flake is high.
- **Marketing pages with live CMS content** — content changes constantly.
- **Pages where business logic dominates** — unit / integration tests cover those better.

For these, rely on component-level snapshots (which DO have stable layouts) plus e2e tests for behavior.

## Process

1. **Pick the tool** based on stack (Chromatic if Storybook-driven, Playwright Visual if Playwright-driven).
2. **Start with the design system primitives** — easiest to snapshot, highest leverage.
3. **Add per-page snapshots** sparingly, for high-traffic pages.
4. **Wire CI** — block (or at minimum, surface) on unapproved diffs.
5. **Establish the approval workflow** with the team.
6. **Document at `docs/frontend/visual-regression.md`** — tool, what's snapshotted, who reviews, how to handle flakes.
7. **Track flake rate** — > 5% flake means tuning is needed.

## Anti-patterns

- **Approving all diffs.** Defeats the purpose.
- **No masking of dynamic content.** Snapshots flake; team stops trusting them.
- **Snapshotting every page.** Cost balloons; review fatigue; signal degrades.
- **Snapshots without Storybook** — variants become hand-rolled in test files; drift from real usage.
- **Cross-OS snapshot comparison.** Font rendering differs; use a consistent CI environment.
- **No baseline-update path.** Intentional design changes block PRs forever.
- **Skipping flaky snapshots permanently** instead of fixing the flake source.

## Cross-references

- `design-system-keeper` — Storybook + visual regression is the canonical pair.
- `frontend-design` — the design that's being protected.
- `flaky-test-management` — same discipline (24h-quarantine, 30d-fix) for visual flakes.
- `qa-test-plan` — visual regression complements behavioral tests.

## Output

Visual regression tests committed, CI wired, baseline established. `docs/frontend/visual-regression.md` documents the workflow.
