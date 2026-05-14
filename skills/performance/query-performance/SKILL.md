---
name: query-performance
description: Diagnose and fix slow database queries — read EXPLAIN plans, identify missing indexes, full scans, N+1 patterns, unnecessary joins, type coercion that defeats indexes. Use when the user says "slow query", "N+1", "missing index", "EXPLAIN", "the database is the bottleneck", or when profiling points at DB time.
---

# query-performance

## Purpose

The database is the most common bottleneck in monoliths and the easiest place to make order-of-magnitude wins. This skill walks a single slow query (or a slow endpoint with DB time on the hot path) through a disciplined diagnose-and-fix loop.

DB-engine-agnostic where possible; calls out engine-specific advice (Postgres / MySQL / SQLite) where it matters.

## When to use

- An endpoint is slow and profiling shows DB time dominating.
- A specific query crossed a threshold (slow-query log, ORM warning).
- User says: "slow query", "N+1", "missing index", "EXPLAIN", "the database is the bottleneck", "this query takes forever".
- During `performance-investigation` when the hotspot is a query.

## Process

1. **Isolate the actual query.** ORMs hide what runs:
   - Log the generated SQL (`echo=True` in SQLAlchemy, `Query#to_sql` in ActiveRecord, `--debug` flag in Django, etc.).
   - Capture parameter values, not just placeholders.
2. **Run `EXPLAIN ANALYZE` against representative data.**
   - Postgres: `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <query>;`
   - MySQL: `EXPLAIN ANALYZE <query>;` (8.0+) or `EXPLAIN FORMAT=JSON`.
   - SQLite: `EXPLAIN QUERY PLAN <query>;`
   - **Not on tiny dev data.** Plans flip based on data size; use a prod-shaped dataset.
3. **Read the plan top-down** and look for:
   - **Seq Scan / Full Table Scan** on tables with > a few thousand rows where a filter exists → missing or unusable index.
   - **High Rows Removed by Filter** → an index exists but isn't selective enough, or filter is post-index.
   - **Sort with large data** → consider an index that delivers pre-sorted rows.
   - **Hash Join / Nested Loop on huge sets** → join key may not be indexed.
   - **High Buffers / Reads** in Postgres EXPLAIN → working set doesn't fit in cache.
   - **Function on indexed column** in WHERE → defeats the index (e.g. `WHERE LOWER(email) = ?`). Fix with a functional index or column normalization.
   - **Type coercion** → `WHERE id = '42'` against int column may defeat index. Fix the type.
4. **Check for N+1.** If the slow path runs N queries instead of 1, no amount of per-query tuning fixes it:
   - ORM `query.options(joinedload(...))` / `prefetch_related` / `Include`.
   - Or rewrite as a single query with a join.
   - Look in the ORM log for repeated identical-shape queries during a single request.
5. **Pick the cheapest fix in this order**:
   - **Add an index.** Composite indexes match WHERE+ORDER BY column order. Be wary of over-indexing (writes pay the cost).
   - **Rewrite the query.** Often a CTE / subquery / different join order produces a better plan.
   - **De-N+1.** Single fetch instead of N.
   - **Denormalize or precompute.** Materialized view, summary table, application-side cache. Only after the above are exhausted.
   - **Partition / shard.** Last resort.
6. **Validate the fix**:
   - Re-run `EXPLAIN ANALYZE`. Plan should change (e.g. `Seq Scan` → `Index Scan`).
   - Re-run timing in the same env as the original measurement.
   - **Quantify**: before X ms, after Y ms, on dataset Z.
7. **Add a regression guard**:
   - A test that asserts query count for the endpoint (catches N+1 regression).
   - A perf test threshold for the endpoint (catches re-regression).
   - For critical queries, a slow-query alert in prod.
8. **Write up** under `docs/performance/db/YYYY-MM-DD-short-name.md`:
   - The query.
   - Original plan + key bad signals.
   - Final plan + improvement.
   - Index(es) added (with `CREATE INDEX` statements).
   - Regression guard.
   - Sibling queries with the same anti-pattern.

## Anti-patterns

- **Adding indexes hopefully** without checking the plan. Indexes have write cost — only add what's used.
- **`SELECT *` followed by app-side filtering.** Push the work to the DB.
- **OFFSET pagination on big tables.** Use keyset (cursor) pagination.
- **Tuning a query that nobody runs.** Check actual query frequency before investing.
- **Optimizing in the application layer when the DB has a better plan available.**

## What this skill does NOT do

- Replace a real DBA on truly hard problems (lock contention, replication lag, vacuum/bloat issues).
- Cover schema design from scratch — different concern (ADR territory).

## Output

`docs/performance/db/YYYY-MM-DD-short-name.md` plus the index / query change + regression guard.
