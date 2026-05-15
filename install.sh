#!/usr/bin/env bash
# install.sh — symlink every skill AND subagent in this repo into the Claude config.
#
# Usage:
#   ./install.sh            # personal install: ~/.claude/skills/ + ~/.claude/agents/
#   ./install.sh --project  # project install: ./.claude/skills/ + ./.claude/agents/
#   ./install.sh --dry-run  # show what would happen, don't link

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
AGENTS_SRC="$REPO_ROOT/agents"

mode="personal"
dry_run=false
for arg in "$@"; do
  case "$arg" in
    --project) mode="project" ;;
    --dry-run) dry_run=true ;;
    -h|--help)
      sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) echo "unknown arg: $arg" >&2; exit 1 ;;
  esac
done

if [[ "$mode" == "personal" ]]; then
  BASE="$HOME/.claude"
else
  BASE="$PWD/.claude"
fi
SKILLS_TARGET="$BASE/skills"
AGENTS_TARGET="$BASE/agents"

echo "Installing from: $REPO_ROOT"
echo "  Skills → $SKILLS_TARGET"
echo "  Agents → $AGENTS_TARGET"
$dry_run && echo "(dry run — no changes will be made)"
echo

link_dir_items() {
  local src="$1" target="$2" min_depth="$3" max_depth="$4" kind="$5"
  [[ -d "$src" ]] || { echo "(no $kind directory at $src; skipping)"; echo; return; }

  mkdir -p "$target"
  local count=0
  while IFS= read -r -d '' item; do
    local name dest
    name="$(basename "$item")"
    dest="$target/$name"

    if [[ -e "$dest" && ! -L "$dest" ]]; then
      echo "SKIP  $kind/$name (exists and is not a symlink)"
      continue
    fi

    if $dry_run; then
      echo "LINK  $kind/$name -> $item"
    else
      ln -sfn "$item" "$dest"
      echo "LINK  $kind/$name"
    fi
    count=$((count + 1))
  done < <(find "$src" -mindepth "$min_depth" -maxdepth "$max_depth" "$@" -print0 2>/dev/null \
            || find "$src" -mindepth "$min_depth" -maxdepth "$max_depth" -print0)

  echo "Linked $count $kind(s)."
  echo
}

# Skills live two levels down: skills/<category>/<skill-name>/
echo "== Skills =="
count=0
while IFS= read -r -d '' skill_dir; do
  name="$(basename "$skill_dir")"
  dest="$SKILLS_TARGET/$name"
  mkdir -p "$SKILLS_TARGET"

  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "SKIP  skills/$name (exists and is not a symlink)"
    continue
  fi

  if $dry_run; then
    echo "LINK  skills/$name -> $skill_dir"
  else
    ln -sfn "$skill_dir" "$dest"
    echo "LINK  skills/$name"
  fi
  count=$((count + 1))
done < <(find "$SKILLS_SRC" -mindepth 2 -maxdepth 2 -type d -print0)
echo "Linked $count skill(s)."
echo

# Agents are one level down: agents/<agent-name>.md
echo "== Agents =="
if [[ -d "$AGENTS_SRC" ]]; then
  mkdir -p "$AGENTS_TARGET"
  count=0
  while IFS= read -r -d '' agent_file; do
    name="$(basename "$agent_file")"
    dest="$AGENTS_TARGET/$name"

    if [[ -e "$dest" && ! -L "$dest" ]]; then
      echo "SKIP  agents/$name (exists and is not a symlink)"
      continue
    fi

    if $dry_run; then
      echo "LINK  agents/$name -> $agent_file"
    else
      ln -sfn "$agent_file" "$dest"
      echo "LINK  agents/$name"
    fi
    count=$((count + 1))
  done < <(find "$AGENTS_SRC" -mindepth 1 -maxdepth 1 -type f -name "*.md" ! -name "README.md" -print0)
  echo "Linked $count agent(s)."
else
  echo "(no agents/ directory at $AGENTS_SRC; skipping)"
fi
echo

echo "To enable enforcement hooks (TDD, phased-implementation, CLAUDE.md refresh), see hooks/README.md."
