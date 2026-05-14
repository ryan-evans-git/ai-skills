---
name: performance-investigation
description: Systematically investigate a performance problem — reproduce the slow behavior, measure baseline, profile to find the hotspot, fix, benchmark to prove the fix, then write up. Use when the user says "X is slow", "perf regression", "spike in latency", "investigate the slowness", "why is Y taking so long", or when an alert fires on a latency SLO.
---

# performance-investigation

## Purpose

Performance fixes that skip steps fix the wrong thing. This skill enforces a loop similar to `bug-investigation` but tuned for "behavior is correct but too slow": measure first, profile second, change third, benchmark fourth, write up fifth.

Use `bug-investigation` for incorrect behavior. Use this skill for correct-but-slow behavior.

## When to use

- User reports slowness: "X is slow", "Y takes forever", "regression on Z", "spike in latency".
- A latency / perf budget alert fired (see `performance-budget`).
- Profiling reveals a hotspot worth investigating.
- A user-facing metric (LCP, INP, p95 latency) has degraded.

## Process

1. **Capture the report** verbatim:
   - What's slow, in what scenario, on what device / data / load.
   - Expected vs. observed (with numbers if available).
   - Frequency: always / under load / once / certain inputs only.
   - Recent changes that might correlate.
2. **Reproduce.** Don't optimize anything until you can reproduce — and reproduce reliably enough to measure. If you can't reproduce, the first task is *make this reproducible*.
3. **Measure the baseline.** Get a number before changing anything:
   - For an endpoint: latency distribution (p50, p95, p99) under representative load.
   - For a page: LCP / INP / TTFB on a representative device + network.
   - For a job: duration on representative data volume.
   - **Take multiple samples.** Single measurements lie. Use a load-test tool or a quick loop.
4. **Set a target.** What does "fixed" mean? Tie to the perf budget if one exists. Don't open-endedly chase faster.
5. **Profile.** Use the right tool for the layer:
   - **App-level**: `py-spy` / `cProfile` (Python), `clinic` / `0x` (Node), `pprof` (Go), Chrome DevTools Performance (frontend), Linux `perf` (native).
   - **Database**: `EXPLAIN ANALYZE`, slow query log, query plan visualizer. See `query-performance`.
   - **Network**: browser DevTools network tab, `tcpdump`, RUM data.
   - **System**: `htop`, `iostat`, `vmstat` for CPU/IO/memory contention.
6. **Identify THE hotspot.** Not three. One. The thing the profile says is taking the most time / cycles / bytes. Resist the urge to optimize on guess.
7. **Form a hypothesis.** "I think the hotspot is `X` because the profile shows Y." Write it down — when the fix doesn't work, this is what you check.
8. **Fix the hotspot.** Smallest change that addresses it. Don't bundle other improvements.
9. **Benchmark.** Re-measure with the same methodology as step 3. Did it actually improve, and by how much? If improvement < 20%, ask whether the hotspot was actually the bottleneck — Amdahl's law applies.
10. **Check for regressions.** Faster on the hot path is sometimes slower on a cold path. Run the full perf-relevant test suite, not just the hot scenario.
11. **Commit a regression test / benchmark** so this doesn't silently get reverted later. For endpoints: a load-test threshold; for code-level work: a microbenchmark.
12. **Write up** under `docs/performance/investigations/YYYY-MM-DD-short-name.md`:
    - **Report** — original observation.
    - **Repro** — final steps + setup.
    - **Baseline numbers** — p50/p95 or whatever metric, with sample size.
    - **Hypothesis explored** — including the ones that turned out wrong.
    - **Root cause** — the hotspot.
    - **Fix** — what changed (PR/commit links).
    - **Result** — before / after numbers.
    - **Regression guard** — link to the benchmark / load test / alert that prevents recurrence.
    - **Sibling risks** — other places with the same anti-pattern; what was checked.
    - **Lessons** — feed forward.

## What this skill does NOT allow

- Optimizing before measuring.
- Changing multiple things at once and claiming credit for the speedup.
- Closing an investigation without a regression guard if the fix was non-trivial.
- "Looks faster now" instead of numbers.

## Output

- Code change + regression guard.
- `docs/performance/investigations/YYYY-MM-DD-short-name.md`.
