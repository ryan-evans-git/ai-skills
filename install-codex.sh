#!/usr/bin/env bash
# install-codex.sh — translate this library to OpenAI Codex CLI config.
#
# WHAT TRANSLATES:
#   skills/<category>/<name>/SKILL.md  →  ~/.codex/prompts/<name>.md
#     (Codex invokes prompts as /<name> slash commands. Unlike Claude Code,
#     Codex does NOT auto-trigger on description match — they must be called.)
#   templates/CLAUDE.md                 →  AGENTS.md at the project root
#     (--emit-agents-md flag). AGENTS.md is a cross-tool convention that Codex,
#     Cursor, and several others recognize for project-level instructions.
#
# WHAT DOES NOT TRANSLATE:
#   agents/*.md   — Codex has no direct subagent equivalent. You can run
#                   `codex` recursively or compose via shell, but the
#                   tool-scoping + isolated-context model is Claude Code-specific.
#   hooks/*.py    — Codex's extension model differs from Claude Code's
#                   PreToolUse / SessionStart hooks. The logic in require_plan.py
#                   / require_failing_test.py can be reused as a pre-commit hook
#                   (it's just Python reading a file) — but install-codex.sh
#                   does NOT wire that automatically.
#
# Usage:
#   ./install-codex.sh                  symlink skills into ~/.codex/prompts/
#   ./install-codex.sh --project        symlink into ./.codex/prompts/
#   ./install-codex.sh --emit-agents-md write AGENTS.md to cwd from the template
#   ./install-codex.sh --dry-run        show what would happen
#
# See docs/codex-install.md for the full translation table.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
TEMPLATE="$REPO_ROOT/templates/CLAUDE.md"

mode="personal"
dry_run=false
emit_agents_md=false
for arg in "$@"; do
  case "$arg" in
    --project) mode="project" ;;
    --dry-run) dry_run=true ;;
    --emit-agents-md) emit_agents_md=true ;;
    -h|--help)
      sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "unknown arg: $arg" >&2; exit 1 ;;
  esac
done

if [[ "$mode" == "personal" ]]; then
  TARGET="$HOME/.codex/prompts"
else
  TARGET="$PWD/.codex/prompts"
fi

echo "Installing skills as Codex prompts"
echo "  Source: $SKILLS_SRC"
echo "  Target: $TARGET"
$dry_run && echo "(dry run — no changes will be made)"
echo

mkdir -p "$TARGET"

count=0
skipped=0
while IFS= read -r -d '' skill_md; do
  skill_dir="$(dirname "$skill_md")"
  name="$(basename "$skill_dir")"
  dest="$TARGET/$name.md"

  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "SKIP  $name (exists; not a symlink)"
    skipped=$((skipped + 1))
    continue
  fi

  if $dry_run; then
    echo "LINK  $name -> $skill_md"
  else
    ln -sfn "$skill_md" "$dest"
    echo "LINK  $name"
  fi
  count=$((count + 1))
done < <(find "$SKILLS_SRC" -mindepth 3 -maxdepth 3 -type f -name "SKILL.md" -print0)

echo
echo "Linked $count prompt(s) ($skipped skipped)."
echo

if $emit_agents_md; then
  if [[ ! -f "$TEMPLATE" ]]; then
    echo "warning: template not found at $TEMPLATE; skipping AGENTS.md" >&2
  elif [[ -e "$PWD/AGENTS.md" && ! -L "$PWD/AGENTS.md" ]]; then
    echo "SKIP  AGENTS.md (already exists in $PWD; not overwriting)"
  else
    project_name="$(basename "$PWD")"
    if $dry_run; then
      echo "WRITE AGENTS.md (dry-run preview):"
      head -n 5 "$TEMPLATE"
      echo "  ... (full content rendered from $TEMPLATE with project_name=$project_name)"
    else
      # Render placeholders the same way the Claude Code SessionStart hook does
      lib_sha="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
      today="$(date +%Y-%m-%d)"
      skill_count="$(find "$SKILLS_SRC" -name SKILL.md -type f | wc -l | tr -d ' ')"
      index_url="https://github.com/ryan-evans-git/ai-skills/blob/main/INDEX.md"
      sed \
        -e "s|{{project_name}}|$project_name|g" \
        -e "s|{{commit_sha}}|$lib_sha|g" \
        -e "s|{{date}}|$today|g" \
        -e "s|{{skill_count}}|$skill_count|g" \
        -e "s|{{index_url}}|$index_url|g" \
        -e "s|CLAUDE\\.md|AGENTS.md|g" \
        -e "s|Claude's context|the agent's context|g" \
        -e "s|Claude loads on every session|the AI tool loads on every session|g" \
        -e "s|Anything Claude needs to know|Anything the AI agent needs to know|g" \
        "$TEMPLATE" > "$PWD/AGENTS.md"
      echo "WRITE AGENTS.md in $PWD"
    fi
  fi
  echo
fi

cat <<'EOF'
NOTES on the Claude Code → Codex translation:

  Triggering:
    Claude Code: skills auto-trigger when their description matches the user's request.
    Codex:       prompts are invoked explicitly via slash commands — e.g. /prd-creation.
    Implication: in Codex, the user (or their workflow) decides when to invoke a skill.
                 Treat the description field as documentation rather than a router.

  Subagents (agents/):
    Not translated. Codex has no direct equivalent to Claude Code's Agent tool with
    per-agent tool allowlists and fresh contexts. You can compose via shell or
    recursive codex invocations, but the architecture is meaningfully different.

  Hooks (hooks/):
    Not auto-wired. The Python scripts in hooks/ are portable (they read a file and
    return an exit code) and can be reused as pre-commit hooks, CI checks, or
    custom Codex shell-out commands — but install-codex.sh leaves that to you.

  AGENTS.md:
    Most of the CLAUDE.md template content is tool-agnostic (process expectations,
    docs/ layout, code standards, security defaults). The `(skill: X)` references
    remain useful as hints — they tell any AI agent that there's a playbook of
    that name to apply, regardless of how it's invoked.

  See docs/codex-install.md for the full translation table.
EOF
