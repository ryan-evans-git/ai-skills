---
name: bug-investigation
description: Systematically investigate a bug — reproduce, minimize, root-cause, fix, regression-test, write up. Use when the user reports a bug, says "this is broken", "investigate X", "why does Y happen", "debug this", or pastes a stack trace / error. Output is both the fix and a writeup under docs/bugs/.
---

# bug-investigation

## Purpose

Bug fixes that skip steps cause repeat incidents. This skill enforces the full loop: reproduce before fixing, minimize before reasoning, root-cause before patching, regression-test before merging, write up before closing.

## When to use

- User reports a bug, pastes an error or stack trace, says "this is broken", "investigate", "why does X happen", "debug this".
- A production incident has a likely code cause.
- A flaky test is suspected of hiding a real bug.

## Process

1. **Capture the report** verbatim:
   - What the user did / what the system did.
   - What was expected vs. observed.
   - Environment (version, OS, browser, etc.).
   - Frequency (always / sometimes / once).
   - Anything they've already tried.
2. **Reproduce** in a controlled environment:
   - Don't fix anything until you can reproduce it. If you can't reproduce, the first task is "make this reproducible" — add logging, narrow the conditions, ask the reporter for one specific thing.
   - If reproduction is environmental, capture exact steps.
3. **Minimize** the repro:
   - Strip everything not load-bearing. Smaller repro → cleaner root cause.
   - A minimized repro is the seed of the regression test.
4. **Root-cause**, don't symptom-patch:
   - Ask "why does this happen" at least three times.
   - Identify the *commit* that introduced the bug if practical (`git bisect`).
   - Distinguish *trigger* (the thing that made it happen now) from *root cause* (the thing that made it possible).
5. **Write a regression test** that fails because of the bug. Don't fix anything yet — let it fail.
6. **Fix** until the regression test passes and the existing suite stays green.
7. **Check for siblings** — bugs cluster. Search for other places with the same anti-pattern and either fix them in scope or capture them as follow-ups.
8. **Write up** under `docs/bugs/YYYY-MM-DD-short-name.md`:
   - **Report** — original observation.
   - **Reproduction** — final steps.
   - **Root cause** — the actual underlying problem.
   - **Trigger** — what made it surface now.
   - **Fix** — what changed (with PR/commit links).
   - **Regression test** — link to the test file/line.
   - **Sibling risks** — other places at risk; what was checked.
   - **Lessons** — anything to feed forward (process, monitoring, tests).
9. **If the bug had user impact in production**, escalate to `incident-postmortem` — the writeup format is different.

## What this skill does NOT allow

- Fixing before reproducing.
- Patching the symptom without identifying the root cause.
- Closing a bug without a regression test.
- "Fixed" with no writeup if the bug was non-trivial.

## Output

- Code fix + regression test.
- `docs/bugs/YYYY-MM-DD-short-name.md`.

## Template

See [BUG.md](../../../templates/BUG.md).
