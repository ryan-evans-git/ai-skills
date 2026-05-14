# Enforcement hooks

Two skills in this library are designed to **block edits** when their preconditions aren't met:

- **tdd-enforcer** — refuses to modify production code unless a corresponding test file has been touched more recently than the production file, or the edit is to a test file itself.
- **phased-implementation** — refuses to modify source files unless `docs/plans/CURRENT.md` exists and has been updated recently (default: within the last 7 days).

Both are enforced via Claude Code `PreToolUse` hooks. They are **opt-in per project** — you add them to a project's `.claude/settings.json` if you want enforcement.

## Wiring them up

Copy the snippet from `settings.snippet.json` into your project's `.claude/settings.json` (merge with any existing `hooks` block).

```jsonc
{
  "hooks": {
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

Adjust the path if you installed the library somewhere other than `.claude/skills/ai-skills`.

## How blocking works

Each hook script:
1. Receives the tool input on stdin as JSON.
2. Decides whether the edit is allowed.
3. Exits 0 to allow, or exits non-zero with a message on stderr to block.

When a hook blocks, Claude sees the stderr message and can adjust — typically by writing the missing test or updating the plan, then retrying.

## Bypass mechanisms

Both hooks honor an env var escape hatch for emergencies:

- `AI_SKILLS_BYPASS_TDD=1` — skip the TDD check
- `AI_SKILLS_BYPASS_PLAN=1` — skip the plan-required check

Use bypasses sparingly; the skills are designed to be the default.

## What the hooks DON'T do

- They don't run your tests. They check that a test file was *touched* recently — they don't verify it failed. The intent is to make TDD friction-free for engineers who already work that way and surface the requirement to those who don't.
- They don't validate the plan content. They check that `docs/plans/CURRENT.md` exists and is recent. Quality of the plan is on you.

Both are intentionally lightweight. If you want stricter enforcement (actually run the test and require it to fail first), extend the scripts.
