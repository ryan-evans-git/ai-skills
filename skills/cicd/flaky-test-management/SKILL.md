---
name: flaky-test-management
description: Detect, quarantine, root-cause, and re-enable flaky tests — without the "just retry it" anti-pattern that lets flakes live forever. Use when a test fails inconsistently, when CI has a flake rate above threshold, when the user says "flaky test", "flake", "retry CI", "intermittent failure".
---

# flaky-test-management

## Purpose

A flaky test is worse than a missing test: it teaches the team to ignore CI. "Just rerun it" is the start of a slow slide where every red is dismissed as a flake — including the real bug. This skill gives flakes a finite lifespan.

## When to use

- A test fails sometimes, passes other times, on the same code.
- CI flake rate trending up.
- A test was "just rerun until green" by someone today.
- User says: "flaky test", "flake", "retry CI", "intermittent failure", "test is unreliable".

## The lifecycle

```
1. Detect      → 2. Triage immediately → 3. Quarantine     →
4. Root-cause  → 5. Fix                → 6. Re-enable      → 7. Burn-in
```

Never skip step 4. "Add a retry" is not a fix; it's quarantine wearing a costume.

## Process

### 1. Detect
- Run the test enough times to confirm flakiness, not transient-real-failure. Tools: `pytest --count=20`, `cargo test -- --test-threads=1 --skip` loops, GitHub Actions matrix with rerun.
- If CI has flake-tracking (Datadog CI Visibility, BuildPulse, Trunk Flaky Tests), use the data.

### 2. Triage immediately
- **File an issue.** Title: `flaky: <test name>`. Include: stack traces from multiple runs, frequency, first observed.
- **Owner assigned within 1 day.** If no owner, the test owner (CODEOWNERS) is on the hook.
- **Severity**: P0 if blocking releases or hiding real failures; P1 if just noisy.

### 3. Quarantine (within 24h of detection)
- Mark the test with the platform's quarantine mechanism:
  - Python pytest: `@pytest.mark.flaky` or `@pytest.mark.skip(reason="quarantined: <link>")`.
  - JS Jest: `test.skip` or `test.failing`.
  - Rust: `#[ignore]` with a comment referencing the issue.
  - JUnit: `@Disabled("flaky: <link>")`.
- Quarantine ≠ delete. The test still runs (optionally, in a separate suite) so flake rate is trackable.
- **Required**: link to the tracking issue from the quarantine annotation.

### 4. Root-cause
Common causes (in approximate order of frequency):
- **Time / ordering**: test depends on `now()` near a boundary; sleep-based waits; ordering of parallel tests.
- **Shared mutable state**: tests share a DB / global / temp dir without cleanup.
- **Hidden network / IO**: test hits a real network or filesystem when it should mock.
- **Resource exhaustion**: port already in use; out of memory; disk full.
- **Race condition in the code under test**: this is the most valuable kind — finding it improves prod.
- **Real bug**: the test is correctly catching a bug that's intermittent.

Reproduce locally with the failing seed/order if possible. If not reproducible locally, run it in CI in isolation or with verbose tracing.

### 5. Fix
- Fix the underlying cause, not the symptom.
- **Retry is NOT a fix.** A retry hides flake; it doesn't remove flake. Reserve retries for genuinely-external dependencies the test can't mock.
- If the test can't be made deterministic, consider whether it should be a test at all (some end-to-end behaviors are inherently non-deterministic; better covered by load tests / monitoring).

### 6. Re-enable
- Remove the quarantine annotation.
- Close the tracking issue with a link to the fix.

### 7. Burn-in
- Run the test 100+ times in CI on the fix branch to confirm.
- Watch the flake-tracking dashboard for the next 7 days. If it re-flakes, back to step 3.

## Policies

- **Quarantine maximum**: 30 days. After that, the test is auto-deleted (with notice) — keeping a quarantined test forever is admitting the team will never fix it.
- **Flake budget**: target <1% flake rate across the suite. If above, freeze new tests until the budget is restored.
- **No retry as default config.** Retries are per-test, opt-in, with a comment explaining why.

## Anti-patterns

- **`--rerun-failed`** as the global CI default. Hides everything.
- **Quarantine with no issue link.** Nobody will ever fix it.
- **Quarantine forever.** The test becomes a fossil; the code it covered drifts; it's worse than not having it.
- **"I'll fix it later."** Later doesn't come unless calendared.
- **Adding `sleep(5)` to fix flake.** Either the test needs an event-based wait or the system has a race.

## What this skill does NOT do

- Replace good test hygiene (`tdd-enforcer`, `test-pyramid-audit`). Flakes often come from test-suite design problems upstream.

## Output

- Quarantine annotations with issue links.
- Tracking issues with root-cause + fix + burn-in evidence.
- Closed loop: zero forever-quarantined tests.
