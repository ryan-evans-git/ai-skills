---
name: sprint-retrospective
description: Run a structured retrospective at the end of a sprint, phase, or significant milestone. Use whenever the user says "let's do a retro", "what went well/badly", "wrap up this phase", or when a phase in docs/plans/CURRENT.md is marked complete. Produces a dated retro document under docs/retros/.
---

# sprint-retrospective

## Purpose

Capture what worked, what didn't, and what to change before momentum (and memory) fade. Output is durable and searchable — future humans and agents read past retros to avoid repeating mistakes.

## When to use

- User says: "let's do a retro", "sprint retrospective", "wrap up this phase", "what did we learn".
- A phase in `docs/plans/CURRENT.md` is marked complete or about to be.
- End of a sprint cycle.

## Process

1. **Gather inputs** without asking the user — read first:
   - `docs/plans/CURRENT.md` — what was the goal, what's the status of stories.
   - Recent commits and PRs (`git log`, `gh pr list`).
   - `docs/progress/` — session notes since the previous retro.
   - `docs/postmortems/` if any incidents happened during the period.
2. **Draft the retro** with sections:
   - **Period covered** — start/end date, phase name, what was the goal.
   - **What shipped** — concrete outcomes; cite PRs/commits.
   - **What went well** — keep doing.
   - **What didn't go well** — be specific; reference real moments, not vibes.
   - **Surprises** — anything that wasn't predicted by the plan.
   - **Action items** — each with an owner and a target date. (Action items without owners are wishes.)
   - **Carry-forward** — items moved to the next phase.
3. **Write to `docs/retros/YYYY-MM-DD-phase-name.md`** using `templates/RETRO.md`.
4. **Link from `docs/progress/CURRENT.md`.**
5. **Update `docs/plans/CURRENT.md`** — mark the closed phase `[x]`, surface action items, and queue the next phase as `[ACTIVE]`.

## Output

`docs/retros/YYYY-MM-DD-phase-name.md`

## Template

See [RETRO.md](../../../templates/RETRO.md).
