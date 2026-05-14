---
name: self-review
description: Review your own diff against a quality checklist before opening a PR. Use whenever the user says "ready to PR", "review my changes", "self-review", "is this ready", or right before pr-description. Catches dead code, debug statements, secrets, missing tests, and incoherent diffs.
---

# self-review

## Purpose

The cheapest review feedback is the one you catch before another human (or agent) has to. This skill walks the diff once with fresh eyes and a checklist.

## When to use

- User says: "ready to PR", "review my changes", "self-review", "is this ready", "look over what we did".
- Right before `pr-description` runs.

## Process

1. **Pull the diff**: `git diff <base>...HEAD` and `git diff --stat <base>...HEAD`.
2. **Walk the diff hunk-by-hunk** against the checklist below. Don't summarize the diff — actually read it.
3. **For each issue found**, either fix it immediately (if trivial and in scope) or note it as a `FOLLOWUP:` item the user must decide on.
4. **Output a structured review**:
   - **Files touched** — count, by area.
   - **Findings** — grouped by severity (must-fix / should-fix / nit), each citing `file:line`.
   - **Coverage** — was the changed code tested. If not, list which functions / branches are missing.
   - **Verdict** — "ready", "ready after the must-fix items", or "not ready — substantial issues."

## Checklist

**Diff coherence**
- Every changed file relates to the active story.
- No drive-by refactors unrelated to the story (capture them as a follow-up instead).
- Renames are atomic — no half-renamed identifiers.

**Dead code & debug remnants**
- No commented-out code blocks left behind.
- No `console.log`, `print`, `dbg!`, `pdb.set_trace`, `debugger`, `TODO/FIXME` added by this change.
- No unused imports, variables, or functions introduced.

**Tests**
- Every new behavior has at least one test.
- Every bug fix has a regression test.
- No test was disabled / skipped / xfailed without a written reason.
- No test asserts only "no exception" — every test asserts behavior.
- Mocks are minimal; the system under test is not itself mocked.

**Security & secrets**
- No API keys, tokens, passwords, or private URLs added to source.
- No user input flows unsanitized into shell, SQL, or HTML.
- No new endpoints lacking authn/authz checks.

**API surface**
- Public function signatures aren't quietly changed (breaking).
- New HTTP routes have OpenAPI entries — see `swagger-openapi-spec` skill.
- Error responses are typed/documented.

**Docs**
- README updated if user-facing behavior changed.
- CHANGELOG updated if the repo uses one.
- ADR exists for any architecturally-significant decision.

**Performance & resources**
- No N+1 queries introduced.
- No unbounded loops or unbounded growth in memory/disk.
- No new dependencies without justification.

## Output

A structured review printed in the conversation. Fixes applied inline as appropriate.
