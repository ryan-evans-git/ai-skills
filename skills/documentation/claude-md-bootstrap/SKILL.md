---
name: claude-md-bootstrap
description: Create or refresh a project's root CLAUDE.md using the ai-skills template — installing house rules (TDD, phased delivery, docs/ layout, security defaults) into the file Claude loads on every session in that repo. Use when starting a new project, when an older project doesn't yet have CLAUDE.md, when the user says "set up CLAUDE.md", "bootstrap CLAUDE.md", "install house rules", or after pulling a new version of the ai-skills library.
---

# claude-md-bootstrap

## Purpose

`CLAUDE.md` is loaded into Claude's context **every** session in a repo, unconditionally — unlike skills, which only fire when their description matches the user's request. This skill writes (or updates) the CLAUDE.md at a project root so the ai-skills "house rules" are always in Claude's context for that project: phased implementation, TDD, the standard `docs/` layout, security defaults, and a pointer back to the full skills library.

The file has two regions:
- **Hand-written** — project name, stack notes, repo-specific conventions, anything custom.
- **Managed** — between `<!-- BEGIN ai-skills MANAGED -->` and `<!-- END ai-skills MANAGED -->` markers. The companion SessionStart hook (`hooks/refresh_claude_md.py`) regenerates only this region each session, so the file stays current as the ai-skills library evolves.

## When to use

- A new project where the SessionStart hook isn't wired in yet (manual bootstrap).
- An older project where the user wants to refresh CLAUDE.md right now rather than waiting for the next session start.
- The user says: "set up CLAUDE.md", "bootstrap CLAUDE.md", "install house rules", "give this repo the ai-skills baseline".
- After pulling a new version of ai-skills and wanting the changes visible immediately.

**Note:** when the `refresh_claude_md.py` SessionStart hook is wired into `.claude/settings.json`, it automatically creates CLAUDE.md from the template the first time it runs in any git repo and refreshes the managed section every session after. This skill is for explicit, on-demand creation/refresh; the hook is for the steady state.

## Process

1. **Locate the project root.** Use the cwd; if cwd is inside a subdirectory, walk up to the nearest directory containing a `.git/`.
2. **Check for an existing CLAUDE.md.**
   - If it exists with the BEGIN/END markers → say so, and offer to refresh just the managed section (call `hooks/refresh_claude_md.py` directly, or update inline).
   - If it exists *without* the markers → don't overwrite. Surface the existing content and offer to either (a) wrap it with markers + insert the managed section, or (b) leave it alone.
   - If it doesn't exist → create it from `templates/CLAUDE.md`.
3. **Substitute placeholders** in the template:
   - `{{project_name}}` → directory basename of project root.
   - `{{commit_sha}}` → short SHA of the ai-skills library (from `git rev-parse --short HEAD` inside the library checkout).
   - `{{date}}` → today's date, ISO format.
   - `{{skill_count}}` → count of `SKILL.md` files under the library's `skills/` tree.
   - `{{index_url}}` → URL of the library's INDEX.md.
4. **Write the file** at `<project-root>/CLAUDE.md`.
5. **Recommend** (don't auto-add) wiring the SessionStart hook into `.claude/settings.json` so future sessions auto-refresh the managed section. The wiring snippet is in `hooks/settings.snippet.json`.
6. **Don't auto-stage or commit** — leave it to the user. The file is per-repo and they may want to review.

## What goes in the managed vs. unmanaged regions

| Region | Contents | Who edits |
| --- | --- | --- |
| Hand-written (above and below markers) | Project name, what it does, stack, project-specific conventions, owners | Humans |
| Managed (inside markers) | House rules from ai-skills (TDD, phased, docs/, code standards, security defaults), library version, skill count, pointers | The SessionStart hook |

The hand-written sections are where project-specific facts go: "we use framework X", "the auth flow lives at Y", "ask before touching the Z config." Those facts never get clobbered.

## What this skill does NOT do

- Edit any other file — only CLAUDE.md.
- Pull from git remotes. The library SHA reflects whatever is currently checked out wherever ai-skills is installed.
- Replace project-specific guidance that already lives in the hand-written sections.

## Output

`<project-root>/CLAUDE.md`

## Template

See [CLAUDE.md](../../../templates/CLAUDE.md).
