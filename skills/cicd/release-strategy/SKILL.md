---
name: release-strategy
description: Define how this project versions, tags, and ships releases — semver alignment, release cadence, tagging convention, release notes generation, who can cut a release. Use when setting up a new project, when "when do we cut a release?" is unclear, or when the user says "release strategy", "semver", "release cadence", "tagging", "release notes".
---

# release-strategy

## Purpose

Releases without a strategy oscillate between "ship every PR to prod" (good for some products, terrifying for others) and "we ship when someone remembers" (always bad). This skill makes the choice deliberate, documents it, and wires the tooling so the strategy is the default path.

## When to use

- Setting up a new project.
- "When do we release?" comes up.
- Versioning is inconsistent.
- User says: "release strategy", "semver", "release cadence", "tagging", "release notes", "version bump".

## Decisions to make once

### 1. Release cadence
Pick one and commit:
- **Continuous to prod** — every merge to `main` deploys. Best for: tightly-tested SaaS with strong CI + feature flags + small blast radius. Hardest to do safely.
- **Continuous to staging, manual prod promote** — `main` always deployable to staging; prod promotion is on a schedule (daily / weekly) or on-demand with a checklist. Default for most teams.
- **Versioned releases** — cut a release every N weeks / per milestone, tagged and announced. Best for: libraries, SDKs, anything consumed by external integrators.

### 2. Versioning scheme
- **Semver** (`X.Y.Z`) for libraries / packages / public APIs.
- **CalVer** (`2026.05.0` or `YYYY.MM.MICRO`) for products / SaaS where "major version" doesn't mean much.
- **Sequential** (`r1`, `r2`, …) for internal services where versioning is just a deploy counter.
- For semver, align with `api-contract-evolution`: major = breaking, minor = additive, patch = fixes.

### 3. Tagging convention
- Tag releases as `vX.Y.Z` (semver) or `YYYY.MM.MICRO` (CalVer).
- Tags are immutable — never move them.
- Sign tags (`git tag -s`) for libraries / public releases.

### 4. Release notes
- Driven by `CHANGELOG.md` (see `changelog-keeper`).
- Auto-generated from PR titles / labels? Acceptable as a starting point if PR titles are disciplined; better to hand-curate the "added / changed / fixed" summary.
- For user-facing releases, include screenshots / migration notes.

### 5. Authority
- Who can cut a release: roles, not names, so it ages well. ("Members of @team-release" or "any maintainer.")
- Required approvers for prod deploys.
- On-call presence required for the deploy window.

### 6. Pre-releases
- `vX.Y.Z-rc.1`, `-beta.1`, `-alpha.1` for tested-but-not-blessed builds.
- Document when each is used and what the support guarantees are.

## Process

1. **Make each decision above** in a session, considering the project's risk profile.
2. **Write `docs/cicd/release-strategy.md`** with the decisions.
3. **Wire the tooling**:
   - Tag-on-merge or tag-on-command, per cadence choice.
   - Release-please / changesets / cargo-release / semantic-release if useful for auto-versioning + changelog.
   - GitHub Releases / equivalent to publish notes.
4. **Document the release procedure** as a runnable checklist — anyone with authority should be able to execute it cold:
   ```
   1. Verify CI green on the commit to release.
   2. Update CHANGELOG.md — Unreleased → vX.Y.Z (changelog-keeper).
   3. Bump version in package metadata (pyproject.toml / package.json / Cargo.toml).
   4. PR the version bump + changelog. Merge.
   5. Tag the merge commit: git tag -s vX.Y.Z -m "Release X.Y.Z".
   6. Push the tag. CI publishes / deploys.
   7. Create GitHub Release from the tag with the changelog excerpt.
   8. Announce in the agreed channel(s).
   ```
5. **Cross-link** with `changelog-keeper`, `deploy-checklist`, `rollback-plan`.

## Anti-patterns

- **No documented strategy.** Each release reinvents the wheel; some skip steps.
- **Versioning by gut feel.** "Feels like a minor, I'll bump 1.4 → 1.5" with no clear breaking-change definition. Use semver discipline OR pick a different scheme; don't pretend to follow semver while violating it.
- **Tag-then-fix.** Tagging `v1.2.0`, finding a bug, force-pushing the tag. Tags are immutable; cut `v1.2.1`.
- **Skipping CHANGELOG.** Users / downstream consumers won't know what changed.
- **No rollback plan referenced from the procedure.** Releases without rollback plans are bets.

## What this skill does NOT do

- Decide deployment strategy itself (blue/green, canary, rolling) — that's a platform-level decision.
- Replace `deploy-checklist` for the per-deploy verification.

## Output

`docs/cicd/release-strategy.md` + tooling configuration.
