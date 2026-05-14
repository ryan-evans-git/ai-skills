---
name: coverage-gap-finder
description: Identify untested code paths, especially error and edge cases, using coverage reports plus reading the code. Use when the user says "what's not tested", "coverage gaps", "where are we missing tests", "is X covered". Outputs a prioritized list of gaps with suggested test cases.
---

# coverage-gap-finder

## Purpose

Line coverage tells you what was *executed* by tests, not what was *verified*. This skill goes deeper: combine coverage tooling with reading the code to find branches, error paths, and edge cases that no test asserts behavior on.

## When to use

- User says: "what's not tested", "coverage gaps", "where are we missing tests", "is X covered".
- Before signing off on a feature for QA.
- After a bug — surface sibling untested paths.

## Process

1. **Run the project's coverage tool** if one is configured:
   - Python: `pytest --cov`, `coverage report --show-missing`.
   - JS/TS: `jest --coverage`, `vitest --coverage`, `c8`.
   - Rust: `cargo tarpaulin`, `cargo llvm-cov`.
   - Go: `go test -cover -coverprofile`.
   If no tool is configured, note that and proceed with code-reading only.
2. **For each file under audit**, identify gap types:
   - **Untouched branches** — `if/else`, `match`/`switch`, ternaries where one arm is never hit.
   - **Untouched error paths** — `except`/`catch` blocks, error returns, `Result::Err` arms.
   - **Edge-case inputs**:
     - Empty collections, single-element collections, very large collections.
     - Unicode, emoji, RTL text, zero-width chars.
     - Negative numbers, zero, max int, NaN, infinity.
     - Empty strings, very long strings, strings with control chars.
     - Null/None/undefined where the type allows it.
     - Concurrent access where mutable state is involved.
     - Timezone-sensitive paths around DST and day/month boundaries.
   - **Boundary conditions** — off-by-one in loops, range bounds, pagination first/last page.
   - **Untested public API surfaces** — exported functions with no test calling them.
3. **Prioritize** gaps:
   - **P0** — gaps in security, auth, billing, data-loss paths.
   - **P1** — gaps in core user flows.
   - **P2** — gaps in less-critical code paths.
   - **P3** — gaps in helper / utility code.
4. **For each gap**, suggest a specific test case (one sentence). Don't just say "test this function" — say "test that `parseAmount('')` returns an error rather than 0."
5. **Output** the gap list inline or under `docs/qa/coverage-gaps-YYYY-MM-DD.md` if it's substantial. Optionally file follow-up tasks on `docs/plans/CURRENT.md`.

## What this skill does NOT do

- Treat 100% line coverage as the goal. Branch coverage and assertion quality matter more.
- Write the tests itself. That's a separate task (and may be blocked by `tdd-enforcer` rules if you're adding tests to satisfy a past commit — that's fine, write them as characterization tests).

## Output

A prioritized list of gaps, each with a suggested test case. Saved to `docs/qa/` if substantial.
