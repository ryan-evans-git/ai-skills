#!/usr/bin/env bash
# install.sh — symlink every skill in this repo into ~/.claude/skills/
#
# Usage:
#   ./install.sh            # personal install: symlinks into ~/.claude/skills/
#   ./install.sh --project  # project install: symlinks into ./.claude/skills/
#   ./install.sh --dry-run  # show what would happen, don't link

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"

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
  TARGET="$HOME/.claude/skills"
else
  TARGET="$PWD/.claude/skills"
fi

echo "Installing skills from: $SKILLS_SRC"
echo "Into:                   $TARGET"
$dry_run && echo "(dry run — no changes will be made)"
echo

mkdir -p "$TARGET"

count=0
while IFS= read -r -d '' skill_dir; do
  name="$(basename "$skill_dir")"
  dest="$TARGET/$name"

  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "SKIP  $name (exists and is not a symlink)"
    continue
  fi

  if $dry_run; then
    echo "LINK  $name -> $skill_dir"
  else
    ln -sfn "$skill_dir" "$dest"
    echo "LINK  $name"
  fi
  count=$((count + 1))
done < <(find "$SKILLS_SRC" -mindepth 2 -maxdepth 2 -type d -print0)

echo
echo "Linked $count skill(s)."
echo
echo "To enable enforcement hooks (TDD, phased-implementation), see hooks/README.md."
