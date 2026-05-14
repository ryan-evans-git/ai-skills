---
name: phased-implementation
description: Require an active phase plan before writing or editing production code. Activates on any request to implement, build, fix, or refactor when docs/plans/CURRENT.md is missing or stale. Pairs with hooks/require_plan.py to block edits when no current plan exists.
---

# phased-implementation

## Purpose

Code is the last step, not the first. This skill ensures every implementation session is anchored to a written plan — a phase, a current story, a clear definition of done — so that progress is legible across sessions, agents, and team members.

Ships with a `PreToolUse` hook (`hooks/require_plan.py`) that **blocks edits** to source files when `docs/plans/CURRENT.md` is missing or stale (>7 days old by default). See `hooks/README.md`.

## When to use

- User asks to implement, build, fix, or refactor anything non-trivial.
- The phased-implementation hook just blocked an edit.
- Starting a new session and `docs/plans/CURRENT.md` doesn't reflect the current work.

## Process

1. **Check for a current plan.** Read `docs/plans/CURRENT.md`. If missing or stale, run `story-breakdown` before anything else.
2. **Confirm the active phase + story.** Exactly one phase and one story should be marked `[ACTIVE]`. If multiple are, that's a problem — resolve before editing.
3. **Locate the task** the current edit advances. If the edit doesn't correspond to a listed task, either:
   - Add it as a task under the active story (small, scoped), or
   - Stop — what you're doing is out of phase. Either re-prioritize the plan or open a new story.
4. **Edit code** in scope of the active story. Don't drift into adjacent stories ("while I'm here..."). Capture out-of-scope finds as new tasks/stories on the plan.
5. **Update `docs/plans/CURRENT.md` as you go**:
   - Mark tasks `[~]` when started, `[x]` when complete.
   - When a story is done, mark the next story `[ACTIVE]`.
   - When a phase is done, run `sprint-retrospective`.
6. **Touch `docs/plans/CURRENT.md`** at the end of each working session so the staleness check passes. Even a status update keeps the plan current.

## Phase exit criteria

Each phase has explicit exit criteria listed in the plan. A phase is not done until:

- All `[ACTIVE]` / `[~]` items are resolved (done or explicitly dropped/deferred).
- The exit criteria are demonstrably met.
- A retrospective has been written.
- The plan has been updated to mark the phase `[x]` and queue the next phase.

## What this skill does NOT allow

- Writing code with no plan in place.
- Letting a single session sprawl across multiple stories — finish one or split it.
- Marking a phase `[x]` without a retro.

## Output

Updated `docs/plans/CURRENT.md` plus the implementation work itself.

## Template

See [PLAN.md](../../../templates/PLAN.md) for plan structure (owned by `story-breakdown`).
