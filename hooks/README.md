# Hooks

This library ships three hooks. All are **opt-in per project** — you add them to a project's `.claude/settings.json` if you want them.

## PreToolUse — blocking enforcement

These two refuse edits when their preconditions aren't met:

- **`require_plan.py`** (skill: `phased-implementation`) — refuses to modify source files unless `docs/plans/CURRENT.md` exists and has been updated within the last 7 days.
- **`require_failing_test.py`** (skill: `tdd-enforcer`) — refuses to modify production code unless a corresponding test file has been touched more recently than the production file, or the edit is to a test file itself.

## SessionStart — auto-refresh CLAUDE.md

- **`refresh_claude_md.py`** (skill: `claude-md-bootstrap`) — at the start of every session:
  - If `CLAUDE.md` exists with the `<!-- BEGIN ai-skills MANAGED -->` / `<!-- END ai-skills MANAGED -->` markers → regenerates just the managed section; hand-written content outside the markers is preserved.
  - If `CLAUDE.md` exists *without* the markers → skipped (the user wrote their own; we don't clobber).
  - If `CLAUDE.md` doesn't exist *and* the cwd is inside a git repo → auto-creates it from the full template so older projects pick up house rules automatically.
  - If `CLAUDE.md` doesn't exist *and* there's no `.git/` walking up → skipped (avoid creating files in ad-hoc / scratch dirs).

## Wiring them up

Copy the snippet from `settings.snippet.json` into your project's `.claude/settings.json` (merge with any existing `hooks` block).

```jsonc
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": ".claude/skills/ai-skills/hooks/refresh_claude_md.py" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "hooks": [
          { "type": "command", "command": ".claude/skills/ai-skills/hooks/require_plan.py" },
          { "type": "command", "command": ".claude/skills/ai-skills/hooks/require_failing_test.py" }
        ]
      }
    ]
  }
}
```

Adjust the path if you installed the library somewhere other than `.claude/skills/ai-skills` (e.g. for a personal install, use the absolute path to your ai-skills checkout).

## How blocking works

Each hook script:
1. Receives the tool input on stdin as JSON.
2. Decides whether the edit is allowed.
3. Exits 0 to allow, or exits non-zero with a message on stderr to block.

When a hook blocks, Claude sees the stderr message and can adjust — typically by writing the missing test or updating the plan, then retrying.

## Bypass mechanisms

All three hooks honor env var escape hatches:

- `AI_SKILLS_BYPASS_TDD=1` — skip the TDD check
- `AI_SKILLS_BYPASS_PLAN=1` — skip the plan-required check
- `AI_SKILLS_NO_REFRESH_CLAUDE_MD=1` — skip the CLAUDE.md refresh

Use bypasses sparingly; the skills are designed to be the default.

## What the hooks DON'T do

- The PreToolUse hooks don't run your tests. They check that a test file was *touched* recently — they don't verify it failed. The intent is to make TDD friction-free for engineers who already work that way and surface the requirement to those who don't.
- The plan-required hook doesn't validate plan content. It checks that `docs/plans/CURRENT.md` exists and is recent. Quality of the plan is on you.
- `refresh_claude_md.py` doesn't pull from a remote. It uses whatever version of the ai-skills library is currently checked out wherever the hook script lives. To get newer library content, `git pull` (or `git submodule update --remote`) the ai-skills checkout — the next session start picks it up automatically.

The PreToolUse hooks are intentionally lightweight. If you want stricter enforcement (actually run the test and require it to fail first), extend the scripts.
