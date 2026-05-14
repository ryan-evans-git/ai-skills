---
name: deploy-checklist
description: Walk through a pre-deploy verification checklist — tests, migrations, rollback plan, feature flag, monitoring, comms. Use when the user says "ready to deploy", "ship this", "deploy checklist", "production push". Generates / updates a deploy plan if the change is non-trivial.
---

# deploy-checklist

## Purpose

Every production deploy of non-trivial scope clears a checklist before it ships. Stops the predictable failures: forgotten migration, missing flag, no rollback plan, no one watching the dashboards.

## When to use

- User says: "ready to deploy", "ship this", "deploy", "production push", "deploy checklist".
- A PR is about to be merged that involves: DB migration, new feature behind a flag, infra change, dependency upgrade, anything user-visible.

## The checklist

For each item, mark `[x]` confirmed / `[~]` partial / `[ ]` no / `[n/a]` doesn't apply. Don't deploy until every item is `[x]` or `[n/a]`.

### Code & tests
- [ ] All required tests passing in CI on the merge commit.
- [ ] No `[~]` or `[ ]` items in `docs/plans/CURRENT.md` for this story.
- [ ] `self-review` skill completed.
- [ ] Code review approved by the right reviewers.

### Migrations & data
- [ ] DB schema changes are backward-compatible with the previous app version (additive first, drop later).
- [ ] Migrations run in <X minutes for production data volume (state X).
- [ ] If long-running, migration is online / chunked / behind a flag.
- [ ] Data backfill (if any) is idempotent and resumable.
- [ ] Rollback path for the migration is documented (see `rollback-plan`).

### Feature flags
- [ ] Risky behavior is behind a feature flag, default off.
- [ ] Flag rollout plan documented (% / cohort / region).
- [ ] Flag has a kill-switch separate from a code revert.

### Configuration
- [ ] New env vars / secrets added to all environments BEFORE deploy.
- [ ] Config changes versioned alongside the code that needs them.
- [ ] No hardcoded URLs / secrets / customer-specific values.

### Observability
- [ ] Logs for the new code path are structured and useful.
- [ ] Metrics added for any new critical path.
- [ ] Alerts updated for new failure modes.
- [ ] Dashboard exists for the post-deploy watch window.

### Rollback
- [ ] `rollback-plan` skill output committed for this deploy.
- [ ] One-command rollback verified in a non-prod env.
- [ ] Anyone on call knows where the rollback plan is.

### Communications
- [ ] Stakeholders notified if user-visible.
- [ ] Status page / changelog entry prepared if applicable.
- [ ] Support team briefed on new behavior.

### Post-deploy plan
- [ ] Owner identified to watch the deploy.
- [ ] Watch window length defined (e.g. 30 min for low-risk, 2h+ for risky).
- [ ] Success criteria defined (e.g. "error rate < baseline + 5% for 30 min").

## Process

1. **Read the diff and PR description** to understand scope.
2. **Walk the checklist**, marking each item with evidence (link to passing CI run, link to flag, etc.). Don't just check boxes — cite the evidence inline.
3. **Output** as a markdown checklist in the conversation OR commit to `docs/deploys/YYYY-MM-DD-release-name.md` for substantial deploys.
4. **If any item is `[ ]`, stop the deploy** and either resolve or explicitly accept the risk in the doc with a name attached.

## Output

A filled-in checklist, either inline or under `docs/deploys/`.
