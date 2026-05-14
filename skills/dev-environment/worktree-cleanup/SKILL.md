---
name: worktree-cleanup
description: Find and safely remove stale git worktrees, abandoned branches, and orphaned checkouts — without destroying uncommitted work. Use when the user says "git worktree cleanup", "too many worktrees", ".claude/worktrees", "old branches", "abandoned checkouts", or notices disk pressure from git state.
---

# worktree-cleanup

## Purpose

Git worktrees, abandoned feature branches, and orphaned shallow clones accumulate. Each worktree is a full checkout — multiply by 20 stale ones and that's gigabytes. This skill cleans them safely, with explicit checks against losing uncommitted work.

Especially relevant when using AI-agent worktrees (e.g. `.claude/worktrees/<random-id>`) that get created and forgotten.

## When to use

- User reports disk pressure.
- User says: "git worktree cleanup", "too many worktrees", ".claude/worktrees", "old branches", "abandoned checkouts".
- After a long stretch of AI-agent-driven work that created many worktrees.

## Process

### Step 1 — inventory
- List all worktrees:
  ```sh
  git worktree list
  ```
- For each worktree, capture: path, branch, HEAD SHA, last-commit date.
- For the main repo, also list local branches:
  ```sh
  git for-each-ref --format='%(refname:short) %(committerdate:iso) %(authorname)' refs/heads/
  ```

### Step 2 — categorize
For each worktree, classify:

| Category | Criteria | Action |
| --- | --- | --- |
| **Active** | Has uncommitted changes OR last commit within 7 days | KEEP |
| **Recent, idle** | Clean, last commit 7–30 days ago | Confirm with user; safe to remove |
| **Stale** | Clean, last commit > 30 days | Likely safe; confirm and remove |
| **Orphaned** | Branch deleted or merged; checkout still exists | Safe to remove |
| **Broken** | Path no longer exists / corrupted | Prune via `git worktree prune` |

### Step 3 — check uncommitted work
- For each worktree being considered for removal:
  ```sh
  cd <worktree-path>
  git status --short                  # any uncommitted changes?
  git stash list                      # any stashes?
  git log @{u}..HEAD                  # commits ahead of upstream not pushed
  ```
- **Never remove a worktree with uncommitted, stashed, or unpushed work** without explicit user confirmation AND a recovery plan.

### Step 4 — show the user, then act
- Present the categorization as a table.
- For each removal candidate, show: path, branch, HEAD SHA, last-commit-date, is-clean, is-pushed.
- Wait for explicit go-ahead per group ("remove all stale ones" / "skip the orphaned-branch one").

### Step 5 — remove safely
- For each confirmed:
  ```sh
  git worktree remove <path>          # removes the worktree (fails if dirty)
  git worktree remove --force <path>  # forces removal — only after explicit confirmation
  ```
- For branches abandoned with the worktree (if the user confirms):
  ```sh
  git branch -d <branch>              # only deletes if merged
  git branch -D <branch>              # force delete — requires explicit confirmation
  ```
- Prune the worktree metadata:
  ```sh
  git worktree prune
  ```

### Step 6 — also consider
- **Old PR branches** that were merged: usually safe to delete locally with `git branch -d`. Don't auto-delete branches you can't confirm are merged on the remote.
- **`.claude/worktrees/` directory** (Claude Code's per-agent worktrees) — these are *frequently* abandoned and safe to clean up via the standard worktree commands. Don't manually `rm -rf` — git won't know they're gone.
- **Shallow clones / submodule state** — usually small, skip unless audited as large.

### Step 7 — report
- Worktrees removed: count + total size reclaimed (compare `du -sh` before/after).
- Branches removed.
- Anything skipped + why.

## What to NEVER do

- `rm -rf` a worktree directory directly. Use `git worktree remove`. Direct removal leaves git metadata pointing at a phantom worktree.
- Force-remove a worktree with uncommitted changes without user confirmation.
- Delete an unmerged branch without user confirmation.
- Bulk-remove without showing the user what's being removed.

## Cross-references

- `docker-cleanup` — Docker also eats disk.
- `dev-storage-audit` — find what's biggest before reaching here.

## Output

Reclaimed disk + a summary of removed worktrees / branches.
