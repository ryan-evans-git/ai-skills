#!/usr/bin/env python3
"""SessionStart hook: create or refresh CLAUDE.md from the ai-skills template.

Wired in via .claude/settings.json. Reads the SessionStart event payload on stdin
and ensures the project's CLAUDE.md is current.

Behavior:
  - If CLAUDE.md exists AND contains BEGIN/END ai-skills markers → regenerate the
    managed section in place. Hand-written content outside markers is preserved.
  - If CLAUDE.md exists WITHOUT markers → do nothing (the user wrote their own
    file and we don't want to clobber it). Surface a one-line hint on stderr.
  - If CLAUDE.md doesn't exist AND the cwd is inside a git repo → create it
    from the full template, with placeholders rendered. Older projects that
    never had a CLAUDE.md get one automatically.
  - If CLAUDE.md doesn't exist AND no .git/ is found walking up from cwd →
    do nothing. Avoids creating CLAUDE.md in ad-hoc / scratch directories.

Always exits 0 — failures here must never block a session from starting.

Bypass: set AI_SKILLS_NO_REFRESH_CLAUDE_MD=1.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

BEGIN_MARKER = "<!-- BEGIN ai-skills MANAGED"
END_MARKER = "<!-- END ai-skills MANAGED -->"
INDEX_URL = "https://github.com/ryan-evans-git/ai-skills/blob/main/INDEX.md"

HOOK_DIR = Path(__file__).resolve().parent
LIB_ROOT = HOOK_DIR.parent
TEMPLATE_PATH = LIB_ROOT / "templates" / "CLAUDE.md"


def lib_short_sha() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=LIB_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return (result.stdout or "").strip() or "unknown"
    except Exception:
        return "unknown"


def skill_count() -> int:
    skills_dir = LIB_ROOT / "skills"
    if not skills_dir.exists():
        return 0
    return sum(1 for _ in skills_dir.rglob("SKILL.md"))


def extract_managed_block(text: str) -> str | None:
    pattern = re.compile(
        rf"({re.escape(BEGIN_MARKER)}.*?{re.escape(END_MARKER)})",
        re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


def render(text: str, project_name: str) -> str:
    return (
        text.replace("{{project_name}}", project_name)
        .replace("{{commit_sha}}", lib_short_sha())
        .replace("{{date}}", date.today().isoformat())
        .replace("{{skill_count}}", str(skill_count()))
        .replace("{{index_url}}", INDEX_URL)
    )


def find_project_root(start: Path) -> tuple[Path, bool]:
    """Walk up from `start` looking for a .git/ directory.

    Returns (root, found): root is the directory containing .git/ if found,
    else `start` resolved. `found` indicates whether we actually located a
    git repo — used to decide whether auto-creating CLAUDE.md is appropriate.
    """
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate, True
    return cur, False


def main() -> int:
    if os.environ.get("AI_SKILLS_NO_REFRESH_CLAUDE_MD") == "1":
        return 0

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    cwd = Path(payload.get("cwd") or os.getcwd())
    project_root, in_git_repo = find_project_root(cwd)
    claude_md = project_root / "CLAUDE.md"

    if not TEMPLATE_PATH.exists():
        print(
            f"refresh_claude_md: template missing at {TEMPLATE_PATH}; skipping.",
            file=sys.stderr,
        )
        return 0

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")

    if not claude_md.exists():
        if not in_git_repo:
            return 0  # ad-hoc dir; don't create
        try:
            rendered = render(template_text, project_root.name)
            claude_md.write_text(rendered, encoding="utf-8")
            print(
                f"refresh_claude_md: created {claude_md} from ai-skills template.",
                file=sys.stderr,
            )
        except OSError as e:
            print(f"refresh_claude_md: failed to create CLAUDE.md: {e}", file=sys.stderr)
        return 0

    current = claude_md.read_text(encoding="utf-8")
    if BEGIN_MARKER not in current or END_MARKER not in current:
        print(
            "refresh_claude_md: CLAUDE.md has no ai-skills markers; skipping refresh. "
            "Run the claude-md-bootstrap skill to add managed house rules.",
            file=sys.stderr,
        )
        return 0

    new_block_raw = extract_managed_block(template_text)
    if new_block_raw is None:
        print(
            "refresh_claude_md: template has no managed block; skipping.",
            file=sys.stderr,
        )
        return 0

    new_block = render(new_block_raw, project_root.name)

    pattern = re.compile(
        rf"{re.escape(BEGIN_MARKER)}.*?{re.escape(END_MARKER)}",
        re.DOTALL,
    )
    updated = pattern.sub(lambda _m: new_block, current, count=1)

    if updated == current:
        return 0

    try:
        claude_md.write_text(updated, encoding="utf-8")
    except OSError as e:
        print(f"refresh_claude_md: failed to write CLAUDE.md: {e}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
