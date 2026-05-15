---
name: assumption-surfacing
description: As work proceeds, explicitly flag the inferences and defaults the agent is filling in — so the user can correct in-flight rather than discover the mismatch in the diff. Use continuously during implementation, especially when the user has asked for the work to proceed without upfront clarifying questions, or when requirements-clarification has run and non-load-bearing items remain.
---

# assumption-surfacing

## Purpose

Even with thorough upfront clarification (`requirements-clarification`), implementation surfaces dozens of small decisions: which field is required, what the default looks like, where exactly the new code lives. The agent makes those calls. The cheapest place to catch a wrong call is *while making it*, not when the user reads the diff three commits later.

This skill is the discipline of saying "I assumed X" out loud, briefly and consistently, while the work happens.

## When to use

- Continuously during any implementation or design work.
- Especially when the user has said "just go" / "don't pause for questions."
- When `requirements-clarification` already ran — this is the followthrough for everything that wasn't load-bearing.
- Any time the agent fills in a default the user didn't specify.

## What counts as an assumption worth surfacing

Surface inferences about:

- **Defaults chosen** — value, behavior, format, ordering.
- **Edge cases handled** — what happens on empty input, error path, unauthorized user.
- **Files / locations picked** — where the new code lives.
- **Naming choices** — class / function / field / route names.
- **Inclusions and exclusions** — features that look adjacent but weren't asked for.
- **Validation rules added** — min/max, required-vs-optional, regex.
- **External-facing changes** — anything visible to API consumers, end users, or other services.
- **Reversal cost** — if undoing this would cost more than 5 minutes, surface it.

What NOT to surface (would be noise):

- Renames internal to a single function.
- Whitespace, imports, formatting.
- Idiomatic choices that match existing code in the same file.
- Trivially reversible defaults the user will see in the diff.

The line: would the user, reading just the user-facing summary (not the diff), want to know about this choice? If yes, surface it.

## How to surface

### Inline form (preferred)

When emitting a brief progress update, append the assumption:

> Added the `cancelOrder` endpoint. Assumed cancellation is idempotent (second cancel returns the same response, not 409). Flag if wrong.

Short, ends with "flag if wrong" or similar. One sentence per assumption.

### Batched form (end of response)

For longer turns with many small calls, list at the end:

> **Assumptions I made — say if any are wrong:**
> - Used cursor pagination (not offset) on the new `listOrders` endpoint.
> - Default `page_size = 50`, max 200.
> - Auth required; no public/anonymous access.
> - New table uses `tenant_id` as leading column in the composite PK.
> - Errors return the standard envelope (`{ error: { code, message, request_id } }`).

Keep it terse. 5-10 items max; if more, the work probably needed `requirements-clarification` first.

### Inline-in-code form (for hidden assumptions only)

When the assumption is buried in code where a reader might miss it — and it matters — leave a single-line comment:

```python
# Assumption: cancellation is idempotent — second cancel returns 200, not 409.
```

Sparingly. Don't litter the codebase with assumption commentary. Most assumptions belong in the response, not the source.

## Decision: surface vs. ask

| Situation | Action |
| --- | --- |
| Load-bearing AND not yet started | Ask (`requirements-clarification`) |
| Load-bearing AND mid-work, hit unexpectedly | Stop; ask; flag the half-done state |
| Not load-bearing, easily reversed | Make the call; surface in the response |
| Not load-bearing, hard to reverse | Make the call; surface PROMINENTLY with a "consider before I keep going" |
| Not load-bearing, trivial | Make the call; don't surface (would be noise) |

## Volume calibration

A turn that surfaces *zero* assumptions on non-trivial work is suspicious — almost no work has zero inferred decisions. A turn that surfaces *fifteen* is also wrong — those items needed upfront clarification.

Healthy range: **2-7 surfaced assumptions per non-trivial turn.** Below that, you might be hiding decisions. Above that, you should have paused earlier.

## What to do when the user corrects an assumption

1. Apply the correction immediately.
2. **Look for sibling assumptions** that were wrong for the same reason. If the user said "we don't use cursor pagination here, we use offset," check the other pagination decisions in this turn.
3. Note the correction so it sticks for the rest of the session — if appropriate, save to memory (`user`/`feedback` type).

## Anti-patterns

- **"Done."** No assumptions surfaced; user discovers six misalignments in the diff.
- **Hidden assumption in code without flag.** Future reader has no idea the choice was inferred vs. specified.
- **Surfacing trivia.** "Assumed semicolons at end of statements." Erodes trust faster than silence.
- **Long-winded assumption explanations.** One sentence per item. Brevity is what makes the format scannable.
- **Surfacing AFTER the diff lands without highlighting.** Buried in a paragraph at the bottom; user misses it.
- **Asking after surfacing.** Pick one mode per item — ask OR surface, not both.

## Cross-references

- `requirements-clarification` — upfront pattern; this skill is the continuous one.
- `handoff-prep` — the handoff doc captures assumptions as part of state.
- `decision-log` — when an assumption is "stuck" (we're committing to it), it becomes a one-line log entry.

## Output

Inline-or-batched assumption notes within the response. Occasional code comments for non-obvious choices that future readers need.
