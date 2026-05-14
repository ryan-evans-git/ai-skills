---
name: branch-protection
description: Configure branch protection rules — required status checks, required reviewers, no direct pushes to main, signed commits, linear history — so quality gates actually gate. Use when setting up a new repo, when CI checks aren't being enforced, when the user says "branch protection", "required reviews", "block direct push", "force push protection".
---

# branch-protection

## Purpose

CI checks that aren't *required* to pass are advisory. Branch protection turns the pipeline from "we hope you ran it" into "you can't merge without it." This skill defines the standard rule set and documents it so every repo in the org looks the same.

## When to use

- Setting up a new repo.
- Auditing existing repos for inconsistent protection.
- After a "how did that merge?" incident.
- User says: "branch protection", "required reviews", "block direct push", "force push protection", "merge rules".

## Standard rule set (for `main`)

### Required
- [ ] **Require pull requests.** No direct pushes to `main`.
- [ ] **Require at least 1 approving review** (2 for high-blast-radius repos: platform, security, billing).
- [ ] **Dismiss stale reviews when new commits are pushed.** Otherwise reviewers approve, author force-pushes, change ships unreviewed.
- [ ] **Require review from CODEOWNERS** if a `CODEOWNERS` file exists.
- [ ] **Require status checks to pass.** Specify each required check by name — matching the required stages in `pipeline-design`. Common set:
  - `lint`
  - `type-check`
  - `unit-tests`
  - `build`
  - `security-scan`
  - `dependency-audit`
- [ ] **Require branches to be up to date with `main` before merging.** Prevents "passed CI on a stale base" merges.
- [ ] **Require conversation resolution.** Open review comments must be marked resolved.
- [ ] **Block force pushes to `main`.**
- [ ] **Block deletion of `main`.**
- [ ] **Apply rules to administrators.** (No bypass.)

### Recommended
- [ ] **Require signed commits.** GPG / sigstore / SSH. Prevents commit-impersonation attacks.
- [ ] **Require linear history.** Squash or rebase merges only — no merge commits. Cleaner history; easier `git bisect`.
- [ ] **Restrict who can push.** Team-based; revoke broad org-wide write where possible.
- [ ] **Lock the branch** for read-only repos / archived projects.

### Optional / contextual
- [ ] Require deployment to staging to succeed before allowing merge (when the pipeline does this).
- [ ] Auto-merge enabled (only after all checks pass; only on auto-approved PRs).

## Process

1. **Identify the default branch** (usually `main`).
2. **Set the rules** via the platform's UI / API / IaC:
   - GitHub: Repo Settings → Branches → Branch protection rules, OR `terraform-github` resource `github_branch_protection`, OR a `repository-rulesets` ruleset.
   - GitLab: Settings → Repository → Protected Branches + Merge request approvals.
   - Bitbucket: Repository settings → Branch restrictions.
3. **Verify required checks match pipeline stages.** When the pipeline gains/loses a stage, this list updates too. Drift here is the most common cause of "the check disappeared and nobody noticed."
4. **CODEOWNERS** if applicable — one file at repo root. Format:
   ```
   # Owners by area
   /api/         @platform-team
   /billing/     @billing-team @security-team
   /infra/       @platform-team
   ```
   CODEOWNERS triggers review-required from the named teams when files in their path change.
5. **Document** the active rules in `docs/cicd/branch-protection.md` — one-page table of what's enforced + rationale + exceptions.
6. **For multi-repo orgs**, prefer a *ruleset* applied across repos so they don't drift. Document the org-level baseline.

## Anti-patterns

- **Required checks list doesn't match pipeline.** A new check added but not "required" means it can be bypassed. A required check that was removed from pipeline means PRs sit forever waiting for a check that never runs.
- **Administrators bypass.** "I'll just push to main this once." Sets the tone; norm collapses.
- **No CODEOWNERS for sensitive paths.** Security / billing changes can slip past the right reviewer.
- **Merge commits allowed alongside squash.** History becomes inconsistent.

## What this skill does NOT do

- Configure CI itself (`pipeline-design`).
- Decide release / deploy gating beyond merge (see `artifact-promotion`).

## Output

- Branch protection rules configured (UI or IaC).
- `CODEOWNERS` file at repo root (if applicable).
- `docs/cicd/branch-protection.md` documenting the active rules.
