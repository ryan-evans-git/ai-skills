---
name: dependency-cache-cleanup
description: Find and reclaim space from language-level dependency caches — node_modules, .venv, target/, .gradle, .cargo, .npm, pip cache, pnpm store — across many projects on the user's machine. Use when the user says "node_modules everywhere", "venv cleanup", "target directory", "clear pip cache", or notices broad disk pressure.
---

# dependency-cache-cleanup

## Purpose

Per-project dependency dirs (especially `node_modules`, Rust `target/`, Python `.venv/`) cost hundreds of MB to several GB each. Multiplied across 50 cloned repos = real money. This skill finds them, decides which are safe to remove (re-creatable from lockfiles), and clears them with the user's go-ahead.

## When to use

- Disk pressure.
- User just cloned + abandoned several repos.
- After language version upgrades (old per-version caches stranded).
- User says: "node_modules everywhere", "venv cleanup", "target directory huge", "clear pip cache", "where is all my disk going".

## What's safe vs. risky

| Resource | Safe to clear? | Cost to restore |
| --- | --- | --- |
| `node_modules/` | Yes — if lockfile committed | One `npm install` (minutes) |
| `.venv/` (per-project) | Yes — if requirements pinned | One `pip install` (seconds-minutes) |
| `target/` (Rust) | Yes | One `cargo build` (slow — full rebuild) |
| `dist/`, `build/` | Yes | One build command |
| `.gradle/`, `.m2/` (per-project) | Yes | Re-resolve from lockfile |
| `.next/`, `.nuxt/` build outputs | Yes | One dev server start |
| `~/.cache/pip/` | Yes (user-level) | Re-download on next install |
| `~/.cache/pnpm/store/` | Yes — but expensive to refill | Re-resolve all deps; slow |
| `~/.cargo/registry/cache/` | Yes — registry cache | Re-download crates |
| `~/.npm/` | Yes — user-level | Re-download from registry |
| **Global Python installs** | NO — leave alone | Breaks system tools |
| **System package managers** (apt, brew installs) | NO — out of scope | — |

## Process

### Step 1 — find them
- Project-level caches (recursive scan):
  ```sh
  # Find node_modules dirs, sorted by size
  find ~/code ~/projects ~/Documents -name "node_modules" -type d -prune 2>/dev/null \
    | xargs -I {} du -sh {} | sort -rh | head -50
  ```
  Adjust the search roots to where the user's projects live.
- Same pattern for: `target`, `.venv`, `venv`, `__pycache__`, `.gradle`, `build`, `dist`, `.next`, `.nuxt`, `.parcel-cache`, `.turbo`.
- User-level caches:
  ```sh
  du -sh ~/.cache/* 2>/dev/null | sort -rh | head -20
  du -sh ~/Library/Caches/* 2>/dev/null | sort -rh | head -20    # macOS
  ```

### Step 2 — score by safety + recency
- For each candidate, check:
  - Has a lockfile next to it (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Pipfile.lock`, `Cargo.lock`)? If yes, fully restorable → safe.
  - When was the parent project last touched? `git log -1 --format=%ai` in the parent dir. Recently-active projects: skip; rarely-active: prime cleanup target.
  - Is the parent dir even a git repo at the expected path, or has it been deleted? Orphaned cache → safe.

### Step 3 — present and confirm
- Show the user a table:
  ```
  Path                                  Size   Last touched   Lockfile?  Safety
  ~/code/old-prototype/node_modules     1.2G   2025-09        yes        safe
  ~/code/active-app/node_modules        450M   2026-05-12     yes        skip (active)
  ~/code/legacy/target                  3.4G   2024-11        yes        safe
  ```
- Get explicit go-ahead per group.

### Step 4 — remove
- Per-project caches: `rm -rf <dir>` (after confirmation).
- User-level caches: prefer the tool's own cleanup if available:
  - `npm cache clean --force`
  - `pnpm store prune`
  - `cargo cache --autoclean` (requires `cargo install cargo-cache`)
  - `pip cache purge`
  - `yarn cache clean`

### Step 5 — verify and report
- Re-run `du` on the parent dirs.
- Report: removed N caches, reclaimed M GB.
- Note: next build / install will be slower on touched projects. That's the tradeoff.

## What to NEVER do

- Remove caches inside actively-changed directories without confirming with the user (especially `target/` for Rust — a full rebuild can be 5+ minutes).
- Remove a `.venv` that has hand-installed packages not in `requirements.txt`. Check `pip freeze` against the lockfile first if uncertain.
- Touch system Python / system package manager state.
- Bulk-`rm -rf` from a glob across the whole home dir.

## Cross-references

- `docker-cleanup` — Docker is often the biggest single hog.
- `worktree-cleanup` — git worktrees compound the per-checkout cost.
- `dev-storage-audit` — start there if "I don't know what's eating disk."

## Output

Reclaimed disk + summary of caches removed.
