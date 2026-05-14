---
name: estimation-helper
description: Produce a three-point time estimate for a story, task, or feature — accounting for testing, docs, code review, and unknown-unknowns. Use when the user asks "how long will this take", "estimate this", "story points for X", or when populating effort fields on a plan.
---

# estimation-helper

## Purpose

Most estimates are too small because they only count happy-path coding. This skill produces estimates that include the work everyone forgets: tests, docs, review, integration, edge cases, and the unknowns you haven't surfaced yet.

## When to use

- User says: "how long will this take", "estimate this", "story points", "rough estimate".
- Populating effort fields in `docs/plans/CURRENT.md`.
- Pushing back on a deadline.

## Process

1. **Decompose** the work into concrete pieces. Refuse to estimate anything bigger than ~2 days as a single item — break it down.
2. **For each piece, identify**:
   - Code change (the obvious part).
   - Tests (unit + integration; default ~50–75% of code time for greenfield, more for legacy).
   - Docs (PRD/plan updates, ADR if applicable, README, OpenAPI updates).
   - Code review + revision (typically 20–30% of code time).
   - Integration & manual verification.
   - Known unknowns — list them. Each gets buffer.
3. **Three-point estimate** per piece:
   - **Best case** — everything works first try.
   - **Most likely** — your honest gut estimate.
   - **Worst case** — realistic worst, not catastrophic.
   - **Expected = (best + 4·likely + worst) / 6** (PERT formula).
4. **List unknowns separately** — they aren't included in the three points until they're resolved into knowns. Each unknown gets a "time to resolve" estimate.
5. **Output a table**:
   ```
   | Piece | Best | Likely | Worst | Expected |
   | --- | --- | --- | --- | --- |
   ```
   Plus an "Unknowns to resolve first" list with each unknown's resolution-time estimate.
6. **Roll up** total expected time, total unknowns budget, and a single sentence: "Best case X, likely Y, worst case Z."

## What to never do

- Don't give a single number unless the user asks for one after seeing the range.
- Don't estimate in story points unless the team has a calibrated points-to-time mapping. Hours/days are clearer.
- Don't pad invisibly; if you're adding buffer, label it.

## Output

Inline in the conversation, or appended to the relevant story in `docs/plans/CURRENT.md`.
