#!/usr/bin/env python3
"""PreToolUse hook: block edits to production source unless a sibling test file was touched recently.

Wired in via .claude/settings.json. Reads the tool-call payload on stdin, decides whether
the edit is allowed, exits 0 (allow) or non-zero with a message on stderr (block).

Bypass: set AI_SKILLS_BYPASS_TDD=1.

Heuristic:
  - Edits to docs/, tests/, test/, __tests__/, .claude/ are allowed.
  - Edits to non-code files (.md, .yaml, .json, .drawio, etc.) are allowed.
  - Edits to test files themselves are allowed.
  - Otherwise, look for a plausible test file. If found and its mtime is newer than the
    target file's mtime OR within MAX_GAP_MINUTES, allow. Otherwise block.

This is intentionally a "vibes-based TDD" hook — it nudges toward test-first without
actually running tests. For stricter enforcement, extend this to invoke pytest/jest and
require a failing test.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

MAX_GAP_MINUTES = 15
ALWAYS_ALLOWED_DIRS = ("docs/", "tests/", "test/", "__tests__/", ".claude/", "migrations/")
ALWAYS_ALLOWED_SUFFIXES = (".md", ".drawio", ".yaml", ".yml", ".json", ".toml", ".cfg", ".ini")
CODE_SUFFIXES = (".py", ".ts", ".tsx", ".js", ".jsx", ".rs", ".go", ".rb", ".java", ".kt", ".swift")
TEST_FILE_PATTERNS = (
    re.compile(r"(^|/)test_[^/]+\.py$"),
    re.compile(r"(^|/)[^/]+_test\.py$"),
    re.compile(r"(^|/)[^/]+\.test\.(ts|tsx|js|jsx)$"),
    re.compile(r"(^|/)[^/]+\.spec\.(ts|tsx|js|jsx)$"),
    re.compile(r"(^|/)tests?/"),
    re.compile(r"(^|/)__tests__/"),
)


def is_test_file(rel_str: str) -> bool:
    return any(p.search(rel_str) for p in TEST_FILE_PATTERNS)


def find_test_for(target: Path, cwd: Path) -> Path | None:
    stem = target.stem
    candidates: list[Path] = []
    if target.suffix == ".py":
        candidates += [
            target.with_name(f"test_{target.name}"),
            target.parent / "tests" / f"test_{target.name}",
            cwd / "tests" / f"test_{target.name}",
        ]
    else:
        for ext in (".test", ".spec"):
            candidates += [
                target.with_name(f"{stem}{ext}{target.suffix}"),
                target.parent / "__tests__" / f"{stem}{ext}{target.suffix}",
            ]
    for c in candidates:
        if c.exists():
            return c
    # Last-resort fuzzy match: any file in tests/ with the stem in its name.
    tests_dir = cwd / "tests"
    if tests_dir.exists():
        for p in tests_dir.rglob(f"*{stem}*"):
            if p.is_file():
                return p
    return None


def main() -> int:
    if os.environ.get("AI_SKILLS_BYPASS_TDD") == "1":
        return 0

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not file_path:
        return 0

    cwd = Path(payload.get("cwd") or os.getcwd())
    target = Path(file_path)
    try:
        rel = target.resolve().relative_to(cwd.resolve())
    except ValueError:
        rel = target
    rel_str = str(rel).replace(os.sep, "/")

    if any(rel_str.startswith(d) for d in ALWAYS_ALLOWED_DIRS):
        return 0
    if target.suffix.lower() in ALWAYS_ALLOWED_SUFFIXES:
        return 0
    if target.suffix.lower() not in CODE_SUFFIXES:
        return 0  # unknown file type — don't block
    if is_test_file(rel_str):
        return 0

    # New file being written? Block — write the test first.
    if not target.exists():
        print(
            "tdd-enforcer hook: blocked.\n"
            f"  About to create new code file {rel_str} without a test.\n"
            "  Write a failing test first (see skill: tdd-enforcer),\n"
            "  or set AI_SKILLS_BYPASS_TDD=1 to bypass.",
            file=sys.stderr,
        )
        return 1

    test_file = find_test_for(target, cwd)
    if test_file is None:
        print(
            "tdd-enforcer hook: blocked.\n"
            f"  No test file found for {rel_str}.\n"
            "  Create one (e.g. tests/test_{stem}.py) and write a failing test first,\n"
            "  or set AI_SKILLS_BYPASS_TDD=1 to bypass.".format(stem=target.stem),
            file=sys.stderr,
        )
        return 1

    target_mtime = target.stat().st_mtime
    test_mtime = test_file.stat().st_mtime
    gap_minutes = (target_mtime - test_mtime) / 60

    # Test is older than target by more than MAX_GAP_MINUTES — likely not test-first.
    if gap_minutes > MAX_GAP_MINUTES:
        print(
            "tdd-enforcer hook: blocked.\n"
            f"  Test file {test_file} is {gap_minutes:.0f} min older than {rel_str}.\n"
            "  Update the test (preferably with a new failing case) before editing production code,\n"
            "  or set AI_SKILLS_BYPASS_TDD=1 to bypass.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
