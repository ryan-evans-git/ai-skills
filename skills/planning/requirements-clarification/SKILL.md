---
name: requirements-clarification
description: Detect load-bearing ambiguity in a user request and ask the 1-3 questions whose answers would actually change the design — before writing code, a PRD, or a plan. Use whenever a request lands that's vague about scope, users, success criteria, or constraints, especially before prd-creation, story-breakdown, or implementation. Resists the over-asking failure mode by requiring each question to pass a "would this change the design?" filter.
---

# requirements-clarification

## Purpose

The two failure modes around ambiguous requirements are equally bad:

1. **Charging ahead** — Claude makes assumptions, writes code, and the user discovers half the work missed the mark.
2. **Over-asking** — Claude bombards the user with 15 questions before any work starts; the user gives up and writes the code themselves.

The middle path is **load-bearing questions only**: a small set (typically 1-3) whose answers would *actually change the design*. Everything else is an inline assumption (see `assumption-surfacing`) that can be corrected mid-flight.

## When to use

- A request arrives that's vague about scope, users, success criteria, constraints, or boundaries.
- Before `prd-creation` (gather the load-bearing facts first).
- Before `story-breakdown` (need a clear-enough goal).
- Before non-trivial implementation work.
- User says: "build me X", "we need Y", "fix Z" — and X/Y/Z isn't fully specified.

## When NOT to use

- The user has explicitly said "just go" / "don't ask clarifying questions" / "make the reasonable call." Honor that — use `assumption-surfacing` instead to surface decisions inline.
- The request is small and reversible (a 5-line change). Just do it; the diff is the conversation.
- The user has already provided a PRD / spec / detailed brief that answers the load-bearing questions.

## The load-bearing filter

A question is load-bearing if and only if its answer would change at least one of:

- **Scope** — what's in vs. out of this work.
- **Users / consumers** — who is this for; what are their constraints.
- **Architecture** — service / module boundaries, sync vs. async, data ownership.
- **API surface** — public contracts, breaking changes, versioning needs.
- **Data model** — schema shape, identifiers, multi-tenancy, retention.
- **Security posture** — auth model, PII handling, audit requirements.
- **Success criteria** — how the user will judge "done."
- **Constraints** — deadline, compliance, integration boundaries, headcount.

A question is NOT load-bearing if it's about:

- Naming (renamable later).
- Default values (configurable later).
- Internal implementation choice (refactorable later).
- Formatting / styling (visible in diff; user can redirect).
- Library / package version pick within reason.
- Anything where the user would see the diff and easily redirect.

For non-load-bearing items, make the reasonable call AND surface the assumption inline (`assumption-surfacing`).

## Process

1. **Read the request fully.** Don't react to the first sentence.
2. **Sketch what you'd build** if you proceeded with no clarification. This is where ambiguity surfaces — you'll naturally hit decision points.
3. **For each decision point, run the filter:**
   - Would changing this answer cause significant rework? → Load-bearing. Candidate question.
   - Could the user redirect after seeing the result? → Not load-bearing. Make the call.
4. **Group + dedupe** candidate questions. Often two surface-level questions resolve to one underlying question.
5. **Cap at 3 questions** for the first pass. If you have more, prioritize ruthlessly:
   - Which would cause the most rework if wrong?
   - Which blocks the most other decisions?
   - Which can't be answered by reading the codebase?
6. **Ask the questions** — concrete, options-where-useful, format that's fast to answer:
   - Bad: "How should we handle errors?" (open-ended; user has to write an essay)
   - Good: "For invalid input, prefer (a) return 400 with field-level errors, (b) silent fallback to defaults, or (c) reject the whole request? — happy to default to (a)."
7. **Offer a default** for each question so the user can just confirm. "Reasonable default" beats "open question" for response speed.
8. **For anything you didn't ask about**, write a one-line list at the end: "Assuming X, Y, Z — say if any of these are wrong." (This is the handoff to `assumption-surfacing`.)
9. **Wait for the answer before significant code work.** Other work (reading code, drafting plans, scaffolding non-load-bearing files) can proceed.

## Question format

```
Before I dive in, [N] question[s] where the answer would change the design:

1. <question> — default: <reasonable choice>
2. <question> — options: (a) ..., (b) ..., (c) ...

Assuming the following — flag if any are wrong:
- <non-load-bearing assumption 1>
- <non-load-bearing assumption 2>
```

This format respects the user: shows you've thought, offers defaults, makes answers cheap.

## Examples

### Example 1 — load-bearing surfaces clearly

User: "Add a feature so users can export their data."

Load-bearing questions:
1. Which user types — end users only, or admins exporting any user's data? (changes auth model + data scope)
2. Sync (download) or async (email link)? (changes architecture — async needs job + storage)
3. Format(s) — CSV / JSON / both / configurable? (changes UX + implementation)

Non-load-bearing (just decide + surface):
- File naming convention.
- Where the download button lives in the UI.
- Field order in the export.

### Example 2 — appears ambiguous, isn't really

User: "Rename `getOrder` to `fetchOrder` everywhere."

Looks ambiguous but isn't load-bearing. Just do it; surface afterward: "Renamed in N files; left the public API alias for backward compatibility. Remove the alias?"

### Example 3 — appears clear, isn't

User: "Add caching to the dashboard endpoint."

Looks clear, but `caching-strategy` flags five questions. The load-bearing ones:
1. Staleness tolerance — is real-time required, or is "up to 60s stale" OK?
2. Per-user or shared across users? (changes cache key + memory cost)

The rest (Redis vs. in-process, TTL exact number, etc.) — make the call + surface.

## Anti-patterns

- **Question-bombing.** "I have 15 questions before I can start." User disengages.
- **Asking unanswerable questions.** "What's the right architecture?" — that's your job to propose.
- **Asking what's in the codebase.** Go read it.
- **Asking after charging ahead.** Questions belong before significant work, not after.
- **No defaults offered.** Forces the user to do all the thinking.
- **Asking about non-load-bearing details** to look thorough. Erodes trust faster than guessing wrong.

## Cross-references

- `assumption-surfacing` — inline pattern for everything not load-bearing.
- `prd-creation` — when the answer set is broad enough to need a written PRD.
- `story-breakdown` — clarification feeds the plan; plan needs answers.
- `estimation-helper` — load-bearing unknowns are the things that wreck estimates.

## Output

- 1-3 high-leverage questions in the response (or zero, if nothing is truly load-bearing).
- A short list of assumptions you made for the non-load-bearing decisions.
