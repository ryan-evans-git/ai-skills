---
name: rollback-plan
description: Document how to roll back a specific deploy — code revert path, migration reversal or compatibility plan, feature flag kill, config restore, data-backfill undo. Use when preparing to deploy something non-trivial, when the user says "rollback plan", "what if this breaks", "how do we undo this".
---

# rollback-plan

## Purpose

A deploy without a rollback plan is a deploy that's hard to undo at 3am. Every non-trivial deploy gets a one-page rollback plan that someone unfamiliar with the change can execute under pressure.

## When to use

- Before any non-trivial deploy (DB migration, infra change, risky feature).
- User says: "rollback plan", "what if this breaks", "how do we undo this".
- Required by `deploy-checklist`.

## Process

1. **Identify what's actually being deployed**:
   - Code changes.
   - DB migrations.
   - Config / env var changes.
   - Feature flags toggling.
   - Data backfills.
   - Third-party / infra changes.
2. **For each, document the reversal**:
   - **Code** — usually `git revert <sha>` + redeploy. State the SHA range.
   - **DB migrations** — distinguish two cases:
     - **Backward-compatible (additive)**: no DB rollback needed; just revert the code.
     - **Destructive (drops / renames / type changes)**: spell out the recovery — restore from snapshot, replay, manual fix. If recovery is expensive, the migration shouldn't be destructive in the same deploy as the code change.
   - **Feature flags** — name the flag, state where to toggle it (admin UI, config, env var), state who has access.
   - **Config** — list previous values; commit the rollback config as a separate change ready to apply.
   - **Data backfill** — describe how to undo. If undoable is impossible, that's a flag — escalate.
   - **Third-party / infra** — name the dashboard / CLI / approval path.
3. **State the trigger** — what symptoms cause a rollback (not just "things look bad"): error rate above X, latency above Y, customer reports above Z, alert page.
4. **State the decision authority** — who can call the rollback. On-call by default; named individual for higher-risk changes.
5. **Estimate**: how long does each step take. Total time-to-rollback should be under your incident SLO.
6. **Test the rollback** in a non-prod environment. Document the test result (date + who).

## Format

`docs/deploys/YYYY-MM-DD-release-name-rollback.md` with sections:

- **Deploy summary** (what's being deployed)
- **Rollback triggers** (symptoms that warrant rollback)
- **Authority** (who can call it)
- **Steps**, in order, each with:
  - Action
  - Command / link
  - Expected outcome
  - Time estimate
- **Verification** — how to confirm the rollback worked
- **Tested in non-prod**: date, by whom

## What this skill does NOT do

- Replace `deploy-checklist`. This is one input to it.
- Roll back automatically. Rollback is a human decision in most setups.

## Output

`docs/deploys/YYYY-MM-DD-release-name-rollback.md`
