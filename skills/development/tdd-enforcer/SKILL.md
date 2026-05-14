---
name: tdd-enforcer
description: Enforce test-driven development — no production code is written without a failing test first. Activates on any request to modify, add, or refactor production code: "implement X", "add a function for Y", "fix this bug", "refactor Z". Pairs with hooks/require_failing_test.py to block edits that skip the test-first step.
---

# tdd-enforcer

## Purpose

Make TDD the default, not an aspiration. Every production change starts with a failing test that locks in the behavior change. Refactors start with a passing test that locks in current behavior so the refactor can prove it preserved it.

This skill ships with a `PreToolUse` hook (`hooks/require_failing_test.py`) that **blocks edits** to production code unless a corresponding test file has been touched recently. See `hooks/README.md` for wiring.

## When to use

- User requests any code change to a non-test file.
- User says: "implement", "add", "fix", "refactor", "make it do X".
- The TDD hook just blocked an edit and you need to write a test first.

## The TDD loop

For new behavior:

1. **Red** — Write the smallest failing test that captures the desired behavior. Run it. See it fail. Confirm the failure is the *expected* failure (right test, right reason).
2. **Green** — Write the smallest amount of production code that makes the test pass. Run all tests. They pass.
3. **Refactor** — With the safety net in place, improve names, structure, duplication. Run tests after every meaningful change.
4. **Commit** — One commit per Red → Green → Refactor cycle is ideal, but at minimum commit per Green. Don't commit Red.

For bug fixes:

1. **Reproduce** — Write a test that fails because of the bug. (If the bug isn't reproducible as a test, that's the first thing to fix.)
2. **Fix** — Make the test pass.
3. **Don't delete the test** — it's now a regression test.

For refactors:

1. **Confirm coverage exists** for the behavior you're about to change the shape of. If not, write characterization tests first.
2. Refactor in small steps, running tests between each.

## What this skill does NOT allow

- Writing production code before a failing test exists for the change.
- Mocking the system under test. Mock collaborators, not the thing you're testing.
- "I'll add tests after" — that is not TDD; it's TAD (test-after development), and it produces tests that match the implementation instead of the spec.
- Tests that only assert "no exception was thrown". A test must assert behavior.

## When TDD doesn't apply cleanly

- **Exploratory spikes** — branch off a `spike/*` branch, label the work, throw the code away when done. Spikes are not subject to TDD; *production code derived from a spike* is.
- **Pure refactors with full existing coverage** — no new test needed; the existing tests are the spec.
- **Config / docs / migrations** — not subject to this skill.

In any of those cases, use the `AI_SKILLS_BYPASS_TDD=1` env var to allow the hook to pass, and note the reason in the commit message.

## Output

Code + tests, with tests authored before (or in the same commit as) the production code change. No standalone artifact.
