---
name: docker-cleanup
description: Reclaim disk space from Docker — stopped containers, dangling images, unused volumes, builder cache — with a dry-run-first, confirm-before-delete pattern that never silently destroys data. Use when the user says "docker is taking too much space", "Docker.raw is huge", "clean up containers", "docker prune", or notices disk pressure with Docker installed.
---

# docker-cleanup

## Purpose

Docker accumulates state quickly during dev/testing — abandoned containers, dangling images, build cache that ballooned. This skill reclaims the space safely, with a dry-run-first / confirm-before-delete pattern so test fixtures and intentional state aren't lost.

## When to use

- The user reports disk pressure on a machine with Docker.
- Docker Desktop's `Docker.raw` / VM disk image is large.
- After a long testing session that ran many containers.
- User says: "docker is taking too much space", "Docker.raw is huge", "clean up docker", "docker prune", "free disk".

## Process — always in this order

### 1. Measure first
- Show what's using space:
  ```sh
  docker system df              # high-level: images, containers, volumes, build cache
  docker system df -v           # detailed per-resource
  ```
- On macOS Docker Desktop, also note the size of the VM disk image (`~/Library/Containers/com.docker.docker/Data/vms/0/data/Docker.raw`).

### 2. Show what would be removed (dry-run mentally — Docker has no `--dry-run`)
- List candidates before removing:
  ```sh
  docker ps -a --filter "status=exited" --filter "status=dead"           # stopped containers
  docker images --filter "dangling=true"                                  # dangling images (no tag)
  docker images                                                           # all images — for tagged-but-unused check
  docker volume ls --filter "dangling=true"                               # anonymous volumes
  docker builder du                                                       # build cache size
  ```

### 3. Decision tree per resource type

**Stopped containers**
- Almost always safe to remove. Stopped containers preserve filesystem layers; rarely intentional to keep.
- Exception: containers stopped *recently* during active debugging. Filter `--filter "until=24h"` to be conservative.
- Command: `docker container prune --filter "until=24h"` (review prompt; type `y`).

**Dangling images** (`<none>:<none>`)
- Always safe. These are layers left from rebuilds.
- Command: `docker image prune` (NO `-a` flag — that prunes tagged images too; be careful).

**Tagged but unused images**
- More dangerous. An image you pulled for testing that isn't currently running but you'll want again costs bandwidth/time to re-pull.
- Audit first: `docker images --format "{{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}"`.
- Remove specific ones: `docker rmi <image>`. Don't bulk-prune tagged images without review.

**Anonymous volumes**
- These hold data. Removing them deletes data.
- **Check what they hold first**: a volume from a postgres container has real DB state. Test data that took an hour to seed is in here.
- Audit: `docker volume ls -q -f "dangling=true"` then `docker volume inspect <vol>` to see mountpoints and the container that created it.
- Only prune anonymous volumes the user explicitly confirms.

**Named volumes**
- NEVER auto-prune. Named volumes are intentional.

**Networks**
- Custom networks left from `docker-compose down` runs. Safe to prune unused.
- Command: `docker network prune`.

**Build cache**
- Can be huge (especially with BuildKit). Usually safe to clear, costs rebuild time.
- Audit: `docker builder du`.
- Command: `docker builder prune` (or `docker builder prune --filter "until=168h"` to keep last week).

### 4. The "big hammer" — `docker system prune`
- `docker system prune -a --volumes` removes: stopped containers, all images not used by a container, all build cache, all unused volumes.
- **Confirm with the user explicitly before running this.** It will remove tagged images and volumes.
- Recommended only when the user has confirmed they're OK losing everything not currently running.

### 5. macOS Docker Desktop — reclaiming the VM disk
- `docker system prune` reclaims space *inside* the VM but the `Docker.raw` file may not shrink.
- Docker Desktop now has an "Optimize disk image" button in Settings → Resources → Advanced. Recommend that to the user.
- Or restart Docker Desktop after prune — it can trigger compaction.

### 6. Report after
- Show `docker system df` before and after.
- Summarize: "Reclaimed X GB. Removed Y containers, Z images, W volumes."

## What to NEVER do silently

- Run `docker system prune -a --volumes` without explicit confirmation.
- Remove named volumes.
- Remove running containers (Docker won't anyway, but don't `-f` past that).
- Skip the "what's in this volume" check before removing anonymous volumes.

## Output

Reclaimed disk space + a summary of what was removed.

## Cross-references

- `worktree-cleanup` — git worktrees can also eat disk.
- `dependency-cache-cleanup` — language-level caches.
- `dev-storage-audit` — find what's actually using the disk before reaching for Docker.
