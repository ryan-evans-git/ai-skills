---
name: changelog-keeper
description: Maintain CHANGELOG.md per the Keep a Changelog convention. Use when shipping a release, cutting a version, merging a user-visible change, or when the user says "update the changelog", "what's in this release", "changelog entry".
---

# changelog-keeper

## Purpose

A `CHANGELOG.md` written for humans, following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Every user-visible change goes in the `[Unreleased]` section when merged, and `[Unreleased]` becomes a version on release.

## When to use

- Merging a user-visible change (feature, bugfix, breaking change, deprecation).
- Cutting a release / tagging a version.
- User says: "update the changelog", "what's in this release", "changelog entry".

## File layout

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New thing.

### Changed
- Updated thing.

### Deprecated
- Thing being phased out.

### Removed
- Gone.

### Fixed
- Bug.

### Security
- Vuln addressed.

## [1.2.0] - 2026-04-12
...
```

## Process

### On a user-visible merge

1. Open `CHANGELOG.md`. If missing, create it with the header above.
2. Under `[Unreleased]`, append a line to the appropriate subsection (`Added`/`Changed`/`Deprecated`/`Removed`/`Fixed`/`Security`).
3. **Write for the user, not the developer.** "Added: filter orders by date range" beats "Added: new `date_filter` param on `/orders`."
4. Reference the PR/issue at the end: `... ([#142](link))`.

### On release

1. Decide the version per semver:
   - **MAJOR** if `Removed` or breaking `Changed` entries exist.
   - **MINOR** if `Added` entries exist (and no breaking).
   - **PATCH** if only `Fixed` / non-breaking changes.
2. Rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`.
3. Create a fresh empty `[Unreleased]` section at the top.
4. Add comparison links at the bottom of the file:
   ```
   [Unreleased]: https://github.com/org/repo/compare/vX.Y.Z...HEAD
   [X.Y.Z]: https://github.com/org/repo/compare/vX.Y.W...vX.Y.Z
   ```
5. Tag the release in git (`git tag vX.Y.Z`).

## What to skip

- Internal refactors with no user-visible effect. Those belong in commit messages, not the changelog.
- "Updated deps" lines unless a dep update changed user-visible behavior.

## Output

Updated `CHANGELOG.md`.
