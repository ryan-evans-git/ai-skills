---
name: pr-description
description: Author a thorough pull request description. Use when the user opens a PR, says "write the PR description", "create a PR", or after running gh pr create. Covers summary, motivation, changes, test plan, screenshots, and breaking changes.
---

# pr-description

## Purpose

A PR description is the durable artifact a future engineer will read when bisecting, debugging, or onboarding. It should explain *why* this change exists, not restate the diff.

## When to use

- User asks to open a PR.
- User says "write the PR description", "draft the PR body", "create a PR".

## Process

1. **Gather context**:
   - The diff (`git diff <base>...HEAD`).
   - The commit messages (`git log <base>..HEAD`).
   - The active story in `docs/plans/CURRENT.md`.
   - Any related PRD, ADR, or issue.
2. **Draft the title** — under 70 chars, imperative voice, conventional-commits prefix if the repo uses them (`feat:`, `fix:`, `refactor:`, etc.). Title is for skimming; details go in the body.
3. **Draft the body** with sections (all of them, even if "n/a"):
   - **Summary** — 1–3 bullets, the *why* not the *what*.
   - **Motivation / Context** — link the PRD, ADR, story, or issue this advances.
   - **What changed** — bullet list grouped by area; mention non-obvious choices.
   - **Test plan** — checklist of how this was verified. Manual + automated.
   - **Screenshots / recordings** — for UI changes, mandatory. Note "n/a" otherwise.
   - **Breaking changes** — explicit `None` if there are none.
   - **Rollout / rollback notes** — flags, migrations, data backfills, ordering with other deploys.
   - **Out of scope / follow-ups** — what was deliberately left undone.
4. **Verify before submitting**:
   - Linked artifacts exist and are publicly accessible (or at least within the org).
   - Screenshots actually attached.
   - Test plan reflects what was actually run.

## What to avoid

- Restating the diff in prose. Reviewers can read the diff.
- "Various changes" / "small fixes" — write what they were.
- Emoji-heavy descriptions unless the team convention demands it.
- "Closes #123" without saying what the change does.

## Output

PR body, typically passed to `gh pr create --body "$(cat <<'EOF' ... EOF)"`.
