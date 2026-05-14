---
name: qa-test-plan
description: Author a QA test plan for a feature — manual and automated cases, prerequisites, data setup, edge cases, regression areas — written so a QA resource (human or agent) can execute it directly. Use when a feature is ready for QA, when the user says "write a test plan", "QA plan", "what should we test for X", or when a PRD/story reaches QA-ready state.
---

# qa-test-plan

## Purpose

Bridge between the PRD and actual verification work. The plan must be executable by a QA engineer or QA agent without having to re-derive what the feature is supposed to do. Lives under `docs/qa/` so it's reviewable and reusable across releases (regression suite).

## When to use

- A feature is ready for QA — story moved to "in review" or "QA" status.
- User says: "write a test plan", "QA plan", "what should we test for X", "regression plan".
- Preparing for a release that bundles multiple features.

## Process

1. **Read inputs** without asking:
   - The PRD (`docs/prds/...`).
   - The story in `docs/plans/CURRENT.md`.
   - The actual diff / PR to know what's actually built.
   - The OpenAPI spec for any API surface affected.
2. **Choose a filename**: `docs/qa/YYYY-MM-DD-feature-name-test-plan.md`.
3. **Structure the plan**:
   - **Feature** — one-sentence summary + link to PRD/story/PR.
   - **Prerequisites** — environment, accounts, data, feature flags, seed state.
   - **Test data** — concrete fixtures, IDs, sample inputs (or scripts to generate them).
   - **In scope** — what this plan covers.
   - **Out of scope** — what it explicitly doesn't.
   - **Test cases**, grouped by area, each with:
     - **ID** (e.g. `TC-001`) — referenceable forever.
     - **Title** — short.
     - **Type** — manual / automated / both.
     - **Priority** — P0 / P1 / P2.
     - **Preconditions.**
     - **Steps** — numbered, action-oriented.
     - **Expected result** — observable, not internal.
     - **Notes** — known flakes, alternate paths, etc.
   - **Edge cases** — pulled out so they're not missed: empty input, max-length input, unicode, concurrent users, network failure mid-flow, auth expiry mid-flow, browser back button, double-submit, refresh during form.
   - **Regression areas** — what existing functionality is at risk and which test IDs cover it.
   - **Exit criteria** — when QA can sign off.
4. **Cover every requirement from the PRD with at least one test case.** Walk the PRD top-down and tag each requirement with the TC-IDs that cover it.
5. **For automated cases**, note where the test lives (path) so a future audit can find it.

## What good test cases look like

- **Observable** — "user sees an error toast that says 'Email already in use'", not "user sees an error".
- **Specific** — "navigate to /signup, enter email 'qa+dup@example.com', click Submit", not "go to signup and try to register".
- **Independent** — each case can run alone given its preconditions.
- **Negative cases included** — at least one per area: invalid input, unauthorized, rate-limited, downstream failure.

## What this skill does NOT do

- Run the tests. That's QA execution.
- Replace automated test code. This document references the automated suite; it isn't a replacement.

## Output

`docs/qa/YYYY-MM-DD-feature-name-test-plan.md`

## Template

See [QA-TEST-PLAN.md](../../../templates/QA-TEST-PLAN.md).
