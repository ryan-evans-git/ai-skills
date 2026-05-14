---
name: story-breakdown
description: Break a PRD (or feature description) into vertical-slice phases, then stories per phase, then tasks per story. Use whenever the user asks "how should we build this", "break this down", "what are the phases", "create stories", or before starting implementation on anything non-trivial. Produces docs/plans/CURRENT.md, which the phased-implementation hook checks for.
---

# story-breakdown

## Purpose

Turn a PRD into an executable, phased plan. Each phase is a vertical slice that delivers user-visible value end-to-end (not a horizontal layer). Each story is independently shippable. Each task is small enough to estimate.

## When to use

- User says: "break this down", "what are the phases", "create stories", "make a plan", "how should we build this", "let's start on X".
- A PRD exists but `docs/plans/CURRENT.md` doesn't.
- The `phased-implementation` hook just blocked an edit and you need a plan.
- Starting any non-trivial work (more than one PR's worth).

## Process

1. **Read the PRD.** If no PRD exists, run `prd-creation` first.
2. **Read the codebase enough** to understand integration points and constraints.
3. **Define phases** — 2–5 of them, each a vertical slice. A phase is not "build the backend then build the frontend"; it's "deliver feature X for a single user type, end-to-end, behind a flag."
4. **For each phase**, list:
   - Goal (one sentence)
   - User-visible outcome
   - Stories (each independently shippable, ~1–5 PRs)
   - Risks / unknowns
   - Exit criteria (how we know the phase is done)
5. **For each story**, list:
   - Goal
   - Tasks (concrete units of work, ideally <1 day each)
   - Test plan (what tests must exist before merge)
   - Dependencies on other stories
6. **Write to `docs/plans/CURRENT.md`** using `templates/PLAN.md`. Mark current phase + story with `[ACTIVE]`.
7. **Archive prior plans** by moving the previous `CURRENT.md` to `docs/plans/archive/YYYY-MM-DD-previous-plan-name.md` before overwriting.
8. **Update `docs/progress/CURRENT.md`** with a pointer to the new plan.

## Status markers

Each phase/story/task gets a status:

- `[ ]` not started
- `[~]` in progress
- `[x]` done
- `[ACTIVE]` current focus (only one at a time at each level)
- `[BLOCKED: reason]`
- `[DROPPED: reason]`

## Output

`docs/plans/CURRENT.md`

## Template

See [PLAN.md](../../../templates/PLAN.md).
