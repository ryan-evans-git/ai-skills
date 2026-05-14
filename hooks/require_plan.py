#!/usr/bin/env python3
"""PreToolUse hook: block edits to source files unless docs/plans/CURRENT.md exists and is recent.

Wired in via .claude/settings.json. Reads the tool-call payload on stdin, decides whether
the edit is allowed, exits 0 (allow) or non-zero with a message on stderr (block).

Bypass: set AI_SKILLS_BYPASS_PLAN=1.

Rules:
  - Edits to files inside docs/, tests/, test/, or __tests__ are always allowed.
  - Edits to .md, .drawio, .yaml/.yml, .json (config) are always allowed.
  - Otherwise, require docs/plans/CURRENT.md to exist and have been modified within MAX_AGE_DAYS.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

MAX_AGE_DAYS = 7
ALWAYS_ALLOWED_DIRS = ("docs/", "tests/", "test/", "__tests__/", ".claude/")
ALWAYS_ALLOWED_SUFFIXES = (".md", ".drawio", ".yaml", ".yml", ".json", ".toml")


def main() -> int:
    if os.environ.get("AI_SKILLS_BYPASS_PLAN") == "1":
        return 0

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # malformed input — don't block real work

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not file_path:
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd())
    try:
        rel = Path(file_path).resolve().relative_to(cwd.resolve())
    except ValueError:
        rel = Path(file_path)
    rel_str = str(rel).replace(os.sep, "/")

    if any(rel_str.startswith(d) for d in ALWAYS_ALLOWED_DIRS):
        return 0
    if rel.suffix.lower() in ALWAYS_ALLOWED_SUFFIXES:
        return 0

    plan = cwd / "docs" / "plans" / "CURRENT.md"
    if not plan.exists():
        print(
            "phased-implementation hook: blocked.\n"
            f"  No plan found at {plan}.\n"
            "  Create one (see skill: phased-implementation) before editing source files,\n"
            "  or set AI_SKILLS_BYPASS_PLAN=1 to bypass.",
            file=sys.stderr,
        )
        return 1

    age_days = (time.time() - plan.stat().st_mtime) / 86400
    if age_days > MAX_AGE_DAYS:
        print(
            "phased-implementation hook: blocked.\n"
            f"  Plan at {plan} hasn't been updated in {age_days:.1f} days (max {MAX_AGE_DAYS}).\n"
            "  Refresh the plan with the current phase/story before editing,\n"
            "  or set AI_SKILLS_BYPASS_PLAN=1 to bypass.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
