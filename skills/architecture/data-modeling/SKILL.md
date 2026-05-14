---
name: data-modeling
description: Apply database / persistence design conventions — primary keys, naming, nullability, foreign keys, soft deletes, timestamps, indexes, JSON columns, multi-tenancy — before any new table or significant schema change. Use when designing a new table, when the user says "schema design", "data model", "should this be a column or a table", "JSON column", "soft delete", "multi-tenant data".
---

# data-modeling

## Purpose

Schemas live longer than any application that uses them. Mistakes are expensive to undo. This skill is the checklist to apply *before* the `CREATE TABLE` lands — and the conventions to inherit so every new table looks like every other.

## When to use

- Designing a new table, column, index, or constraint.
- Reviewing a migration PR.
- User says: "schema design", "data model", "should this be a column or a table", "JSON column", "soft delete", "multi-tenant data", "denormalize".

## Default conventions

### Primary keys
- **UUID v7** (time-ordered) as the default PK, OR auto-increment BIGINT if exposed only internally.
- Never expose auto-increment integers in URLs / public APIs (IDOR; enumeration). Surface them as opaque IDs.
- One PK column. Composite PKs only for join tables.

### Naming
- `snake_case` for tables and columns.
- Tables plural (`orders`), columns singular (`order_id`).
- Foreign keys: `<referenced_table_singular>_id` → `user_id` references `users.id`.
- Booleans: `is_*`, `has_*`, `can_*`. No `flag_*` / `bool_*`.
- Timestamps: `created_at`, `updated_at`, `deleted_at` (UTC, `timestamptz` not `timestamp`).
- Enum-like columns: `status`, `kind`, `type` — pair with a CHECK constraint or DB-level enum.

### Required columns on every table
- `id` (PK).
- `created_at` (default `now()`).
- `updated_at` (auto-updated on row update — via trigger or app code; document which).
- `tenant_id` for multi-tenant apps (and an index — see below).

### Nullability
- **Not null by default.** Adding nullability is opt-in with a reason.
- A nullable column should have a clear semantic: "no value vs. unknown vs. not applicable." If you can't articulate the meaning, it shouldn't be nullable.

### Foreign keys
- **Always declare FK constraints.** Without them, data integrity decays silently.
- `ON DELETE` strategy explicit per relationship: `RESTRICT` (default, safest), `CASCADE` (be sure), `SET NULL` (rare, intentional).

### Soft deletes
- Add `deleted_at TIMESTAMPTZ NULL`.
- All queries filter `WHERE deleted_at IS NULL` (consider a view or row-security policy to enforce).
- Soft delete = audit trail + recovery. If you'll never recover, hard-delete is simpler.
- Index `deleted_at` if soft-deleted rows ever query separately.

### JSON columns
- Use for **truly schema-less** payloads (third-party webhooks, user-defined metadata).
- **Don't use for** fields you'll query/filter on. JSON queries are slower and break referential integrity.
- Define the expected shape in `docs/standards/` or as a JSON Schema even if the DB doesn't enforce it.
- If the JSON has stable fields you'd ever filter on, promote them to real columns.

### Indexes
- Every FK gets an index (databases generally don't auto-create one).
- Every column used in a `WHERE`, `JOIN`, or `ORDER BY` of a hot query gets considered for an index.
- Composite indexes match leading column(s) of typical queries (column order matters!).
- **Don't over-index.** Each index slows writes. Drop unused indexes (Postgres: `pg_stat_user_indexes` shows usage).
- Partial indexes for sparse predicates (e.g. `WHERE active = true`).

### Multi-tenancy
- **Pick one model** at project start and stick with it:
  - **Shared schema with `tenant_id` column** — easiest; needs discipline (every query MUST filter by tenant; row-level security helps).
  - **Schema-per-tenant** — strong isolation; harder to migrate.
  - **Database-per-tenant** — strongest isolation, highest cost.
- For shared-schema: `tenant_id` is leading column in most composite indexes. Add a CHECK constraint or DB role to prevent cross-tenant joins.

### Money, time, identifiers (carryover from `api-design`)
- Money in minor units, integer column + currency code column.
- Time as `timestamptz` (Postgres). UTC always.
- Phone numbers, emails: stored normalized (lowercased emails; E.164 phone).

### Encryption at rest
- Sensitive fields (per `pii-data-handling` classification) get column-level encryption *if* the data is sensitive at rest beyond the default disk encryption. Don't reach for it for everything.

## Process

1. **Draft the schema change** (CREATE TABLE / ALTER TABLE).
2. **Walk the conventions** above; flag any deviations with a reason.
3. **Check forward-compat**: can old app code still work with this schema (additive change)? If not, plan a multi-step migration (`deploy-checklist` for migrations).
4. **Add the FK + index** in the same migration as the column.
5. **Update the model code** so it matches the new schema (type hints, validation).
6. **For schemas owned by other code**, update the API/contract too (`swagger-openapi-spec`).
7. **For non-trivial decisions**, write an ADR (`adr-writer`).

## Anti-patterns

- "We'll add the FK later." Later never comes.
- "We'll just store it as JSON for flexibility." Then you query it, find it slow, and have to migrate to columns anyway.
- Adding `metadata JSONB` as a catch-all instead of designing the fields.
- Surrogate keys (`id`) AND natural keys (`email`) both exposed in the API. Pick one externally.
- Forgetting tenant_id on a new table in a multi-tenant app.
- Cascading deletes you didn't think about. ON DELETE CASCADE on a parent of 50 tables, one delete wipes out millions.

## What this skill does NOT do

- Decide between SQL and NoSQL — that's an ADR.
- Optimize specific slow queries — see `query-performance`.

## Output

Schema migration + updated model code; ADR for non-default decisions.
