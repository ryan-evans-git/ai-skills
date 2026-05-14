---
name: dev-storage-audit
description: Audit the developer machine for where disk space is actually going — top-level home directories, common large-file offenders (Docker, IDE caches, downloads, Library/Caches), with actionable findings ranked by reclaim potential. Use when the user says "disk full", "where did my disk go", "200GB used and I don't know why", "free up space", or any vague disk-pressure complaint.
---

# dev-storage-audit

## Purpose

Most "my disk is full" sessions chase the wrong target (clearing pip cache while 200GB of old Docker images sit untouched). This skill systematically finds where the space *actually* is, ranks the offenders, and points at the right cleanup skill (or manual action).

This is the **entry point** — run this first, then dispatch to `docker-cleanup`, `worktree-cleanup`, `dependency-cache-cleanup`, or a manual recommendation.

## When to use

- User says: "disk full", "where did my disk go", "free up space", "200GB used and I don't know why", "what's eating my disk", "running out of space".
- Before reaching for a specific cleanup skill — find the biggest target first.

## Process

### Step 1 — get the high-level picture
- Total disk:
  ```sh
  df -h /                            # macOS / Linux
  ```
- Where is the user spending bytes at the top level?
  ```sh
  # macOS: largest items at home root
  du -sh ~/* ~/.[!.]* 2>/dev/null | sort -rh | head -20
  ```

### Step 2 — drill into common offenders by category

Show top consumers in each category, even if not in the home-dir top 20 (some are hidden).

**Docker / VMs**
- macOS Docker Desktop: `du -sh ~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw 2>/dev/null`
- Linux: `du -sh /var/lib/docker 2>/dev/null` (may need sudo)
- VirtualBox / VMware / Parallels VM disk images in `~/`
- Lima / Colima / Podman state

**IDE & editor caches**
- macOS: `du -sh ~/Library/Caches/JetBrains 2>/dev/null`, `du -sh ~/Library/Caches/com.microsoft.VSCode 2>/dev/null`
- `~/.config/Code/Cache`, `~/.vscode-server/data` (Linux / WSL)

**Browser caches & profiles**
- Chrome / Firefox / Brave profile directories — can be tens of GB
- macOS Mail downloads, attachments

**Language ecosystems** (user-level)
- `~/.cache/pip`, `~/.cache/uv`, `~/.cache/pnpm`, `~/.npm`, `~/.cargo`, `~/.rustup`, `~/go`, `~/.gradle`, `~/.m2`

**Per-project caches** (recursive — see `dependency-cache-cleanup`)
- `node_modules`, `.venv`, `target/`, `__pycache__`, `.next`, `.turbo`

**git worktrees & old clones** (see `worktree-cleanup`)
- `git worktree list` and `du -sh` per worktree
- Cloned repos no longer used (look in `~/code`, `~/projects`, `~/src`, etc.)

**Downloads**
- `~/Downloads` is universally huge and full of forgettable installers / disk images / archives.

**Old backups**
- `~/Library/Application Support/MobileSync/Backup` (iOS backups via iTunes/Finder).
- Time Machine local snapshots: `tmutil listlocalsnapshots /` — macOS keeps these on the local disk; can be 50+ GB.

**Logs**
- macOS: `/private/var/log`, `~/Library/Logs` — usually small but check.
- App-specific: `~/Library/Logs/CrashReporter`, `~/Library/Logs/DiagnosticReports`.

### Step 3 — rank and present
Build a table of the top 15 offenders across all categories:

```
Rank  Path                                                Size    Category         Cleanup skill
1     ~/Library/Containers/.../Docker.raw                 187G    Docker           docker-cleanup
2     ~/code/legacy-project/node_modules                  4.2G    Project cache    dependency-cache-cleanup
3     ~/Library/Caches/JetBrains                          3.8G    IDE cache        manual: clear in IDE
4     ~/Downloads                                          3.1G    Downloads        manual: review and remove
...
```

Sort by size. Group nearby items so the user sees the *kind* of thing eating disk, not just one path.

### Step 4 — recommend
For each top entry, surface:
- The size.
- The right cleanup skill or manual action.
- The risk level (safe / data-loss-possible / requires user judgment).
- The one-line command (so the user can run it themselves if they prefer).

### Step 5 — handoff
- For Docker → dispatch to `docker-cleanup`.
- For project caches → dispatch to `dependency-cache-cleanup`.
- For worktrees → dispatch to `worktree-cleanup`.
- For IDE / downloads / browser caches → manual recommendation with exact paths.
- For Time Machine local snapshots: `tmutil thinlocalsnapshots / 9999999999999 4` (frees most). Document the command, don't run silently.

## Tools worth recommending

- **`ncdu`** — interactive disk usage browser. `ncdu ~` then drill in.
- **`dust`** — `du` replacement with better output.
- **`OmniDiskSweeper`** (macOS, free) — GUI for large-file finding.
- **`grandperspective`** / **DaisyDisk** — visual treemaps of disk usage.

If the user doesn't have these, recommend installing one — much better UX than `du` for ongoing audits.

## What to NEVER do

- Auto-delete based on size alone.
- Delete anything under `/System/`, `/Library/` (system, not user), or `/private/var/` without expert confirmation.
- Run `find / -delete` or anything similarly broad.
- Touch the user's Documents, Pictures, Music, Movies without explicit permission.

## Output

A ranked audit + handoff to specific cleanup skills or manual recommendations.
