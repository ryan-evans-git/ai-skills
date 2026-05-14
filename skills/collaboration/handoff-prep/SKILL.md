---
name: handoff-prep
description: Write a handoff document for the next engineer or agent picking up the work — current state, what's done, what's in progress, blockers, next steps, watch-outs. Use at the end of a working session, when the user says "handoff", "wrap up", "context for the next person", "I'm stopping for the day".
---

# handoff-prep

## Purpose

A handoff is a self-contained brief that lets the next person (human or agent) pick up cold — without reading the full chat, without paging the previous engineer. Lives under `docs/progress/handoffs/` so multiple sessions accumulate a usable history.

## When to use

- End of a working session, especially one that didn't reach a clean stopping point.
- User says: "handoff", "wrap up", "context for the next person", "I'm stopping for the day", "make sure the next agent can pick this up".
- Before swapping ownership of a feature.

## Process

1. **Choose a filename**: `docs/progress/handoffs/YYYY-MM-DD-HHMM-short-name.md`.
2. **Capture the current state**, in order of importance to a cold reader:
   - **Where we are** — the active story from `docs/plans/CURRENT.md`, one paragraph.
   - **What's done since last handoff** — bullets with PR/commit links.
   - **What's in progress** — the exact file/function/test currently being worked on. Include uncommitted-but-saved changes (`git status` summary).
   - **Next steps** — ordered list of concrete actions the next person should take.
   - **Blockers** — anything waiting on a decision, person, or external system. Name them.
   - **Watch-outs** — non-obvious gotchas: flaky test you haven't fixed, weird env state, a path that looks promising but failed.
   - **Open questions** — things to clarify before continuing.
   - **Commands to know** — exact commands to run the relevant test, dev server, etc.
3. **Update `docs/progress/CURRENT.md`** with a one-line "last handoff: <link>" pointer.
4. **Commit the handoff doc** even if other work is uncommitted (the handoff describes the uncommitted state).

## What makes a good handoff

- **Self-contained** — the next reader doesn't need this conversation to act.
- **Specific** — "the test at tests/test_billing.py:42 is currently failing because of X" beats "billing tests are broken".
- **Action-oriented** — next steps are imperative, ordered, runnable.
- **Honest about uncertainty** — flag what you tried and didn't work, not just what worked.

## What to avoid

- Restating things that are in `docs/plans/CURRENT.md` — link to it.
- Restating the diff. The diff is the diff; the handoff explains *intent* and *state*.
- Apologies and meta-commentary about the session itself.

## Output

`docs/progress/handoffs/YYYY-MM-DD-HHMM-short-name.md`

## Template

See [HANDOFF.md](../../../templates/HANDOFF.md).
