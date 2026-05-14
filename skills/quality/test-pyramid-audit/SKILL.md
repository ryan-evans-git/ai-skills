---
name: test-pyramid-audit
description: Audit the test suite's shape — ratio of unit / integration / end-to-end tests, mocking patterns, test runtime — and surface imbalances that hurt confidence or speed. Use when the user says "audit our tests", "is our test suite healthy", "why is CI slow", "are we over-mocking", or before a release.
---

# test-pyramid-audit

## Purpose

Test suites that look healthy by line-coverage can still be brittle (over-mocked), slow (too many e2e), or shallow (no integration layer at all). This skill produces a report that tells the team where the suite is weak and what to do.

## When to use

- User says: "audit our tests", "are we testing the right things", "why is CI slow", "are we over-mocking", "what's our test pyramid look like".
- Before a release or major refactor.
- Onboarding to a new codebase.

## Process

1. **Inventory the suite**:
   - Count tests per layer (unit / integration / e2e) using path conventions or test-runner tags.
   - Total runtime per layer.
   - Flakiness — recent test failures by file (from CI logs if accessible).
2. **Sample tests by layer** — read 5–10 from each. Look for:
   - **Unit tests**: are they testing one thing? Are they mocking collaborators or the SUT itself? Do they assert behavior or implementation details (e.g. "method was called once")?
   - **Integration tests**: do they hit real boundaries (DB, queue, HTTP) or are they thinly-disguised unit tests with everything mocked?
   - **E2E tests**: are they testing critical user journeys or doing what an integration test should do? Are they reliable?
3. **Identify gaps**:
   - Public API endpoints with no integration test.
   - Critical flows with no e2e test.
   - Modules with high churn and no unit tests.
   - Error paths with no tests.
4. **Identify excesses**:
   - Tests that only assert mock-call-counts (replace with a higher-level test or delete).
   - Snapshot tests that snapshot too much.
   - E2E tests covering ground a unit test could cover.
   - Tests that haven't failed in 6+ months for non-trivial code (suspect over-fitting or dead test).
5. **Output a report** under `docs/qa/test-pyramid-audit-YYYY-MM-DD.md`:
   - **Numbers**: tests per layer, runtime per layer, flake rate.
   - **Shape**: is it a pyramid, a martini glass, an ice-cream cone, an hourglass.
   - **Gaps** (must-fix): missing tests for high-risk code, with file references.
   - **Excesses** (should-trim): brittle/redundant/slow tests, with file references.
   - **Recommendations**: prioritized, each with rough effort.
6. **Optionally**, file follow-up stories on `docs/plans/CURRENT.md`.

## Healthy pyramid heuristics

- Many fast unit tests (~70% of tests, <30% of runtime).
- A meaningful integration layer (~20–25% of tests, ~40–60% of runtime).
- A small, ruthlessly-curated e2e layer (~5–10% of tests, <30% of runtime).
- Total CI test time: ideally under 10 minutes on the critical path.

These are heuristics, not laws — note when a project has good reasons to differ.

## Output

`docs/qa/test-pyramid-audit-YYYY-MM-DD.md`.
