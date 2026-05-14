---
name: data-retention-policy
description: Define and enforce per-data-class retention rules — how long primary data, logs, backups, and derived data live before automatic deletion. Use when starting a new project that handles user data, before a compliance review (GDPR / CCPA / SOC2 / HIPAA), when adding new data fields, or when the user says "data retention", "retention policy", "TTL", "data lifecycle", "how long do we keep X".
---

# data-retention-policy

## Purpose

Without a retention policy, data accumulates forever — costing storage, expanding the breach blast radius, and creating compliance exposure. This skill writes the policy, anchors each class to a justification, and wires enforcement so retention isn't aspirational.

Complements `pii-data-handling` (which classifies fields) and `audit-log-retention` (which handles the special-case longer retention for audit/compliance logs).

## When to use

- Starting a new project that handles user data.
- Adding a new data class (e.g. starting to store session recordings, recommendation embeddings).
- Before compliance review (GDPR, CCPA, SOC2, HIPAA, PCI).
- After a "we still have data from 2018" discovery.
- User says: "data retention", "retention policy", "TTL", "data lifecycle", "how long do we keep X", "GDPR retention".

## Retention classes (template)

| Class | Examples | Default retention | Justification |
| --- | --- | --- | --- |
| **Primary user data** | Account info, profile, settings | Lifetime of account + 30d after deletion | Restore window for accidental deletes |
| **Transactional data** | Orders, payments, invoices | 7 years | Financial / tax law minimum |
| **Session data** | Logged-in session records | 30 days | Auth audit; cleared on logout |
| **Operational logs** | Request logs, error logs | 30–90 days | Debugging / incident review |
| **Audit logs** | Auth events, admin actions, data access | 1–7 years | Compliance; see `audit-log-retention` |
| **Derived / analytics** | Aggregates, embeddings, reports | Per use case; default 1 year | Useful but reconstructible |
| **Backups** | DB snapshots, object-store backups | 30 days rolling + monthly for 12 months | Restore + investigation window |
| **Telemetry / RUM** | Frontend performance metrics | 90 days | Trend analysis |
| **Email / notification history** | Sent messages | 90 days | Resend / dispute window |
| **Soft-deleted records** | Rows with `deleted_at` set | 30 days (then hard-delete) | Recovery window after user delete |

These are defaults; adjust per project. The point is to set numbers, anchor each to a justification, and enforce them.

## Process

1. **Inventory the data classes** in the project. Source: `pii-data-handling` PII inventory, DB tables, log destinations, third-party services.
2. **For each class, decide retention** with these inputs:
   - Legal minimum (financial records often 7+ years).
   - Legal maximum (GDPR data-minimization principle).
   - Business need (do we actually use 2-year-old session data? If not, why keep it?).
   - Storage cost.
3. **Document in `docs/security/retention-policy.md`** with the table above filled in for this project. One row per class. Required columns:
   - Class name
   - Examples / which tables/files
   - Retention period (a *number*, not "as long as needed")
   - Justification
   - Enforcement mechanism (TTL on rows / lifecycle policy / cron job)
   - Owner
4. **Wire enforcement** — don't leave retention to discipline:
   - **DB rows**: scheduled job (`DELETE WHERE created_at < now() - interval 'X days'`) OR Postgres `pg_partman` time-partitioned tables (drop partitions) OR row TTL where the engine supports it.
   - **Log retention**: log aggregator's own retention setting (CloudWatch, Loki, Elastic).
   - **Object storage**: S3 / GCS lifecycle rules.
   - **Backups**: backup tool's own retention (AWS Backup, Velero, pgbackrest).
   - **Soft-delete → hard-delete**: scheduled job after the soft-delete window.
5. **Add a deletion audit trail** — when retention triggers a delete, log it (date, class, count) so a future investigator can prove deletions happened on schedule.
6. **Schedule annual review** — laws change, business needs change. Stale policies create compliance gaps.

## Special cases

### Backups vs. primary data
- A user delete request must propagate to backups in a defined timeframe, OR backups must be old enough that they'll naturally expire.
- For GDPR: documented backup retention < user-data retention typically satisfies the "right to delete" obligation (data is gone within the backup-rotation window).

### Pseudonymization
- If you can't delete the data (e.g. it's load-bearing for analytics), can you pseudonymize? Replace identifiers with hashes; keep aggregates.
- Document pseudonymization as a retention strategy, with the de-anonymization risk noted.

### Third-party retention
- Data sent to vendors (analytics, logging, email) is subject to *their* retention.
- Document vendor retention in the same policy.
- For PII vendors, ensure the DPA (data processing agreement) bounds vendor retention.

## Anti-patterns

- **"Retention as long as the law allows."** Maximum retention is rarely the right answer; minimum-needed is.
- **No enforcement.** "We aim for 90-day log retention" with no actual deletion job means logs live forever.
- **Different retention in backups vs. live.** Forgetting backups is how data "comes back" after a user delete.
- **One-size-fits-all retention.** Auth logs and search-history logs have very different retention needs.

## Cross-references

- `pii-data-handling` — classification of fields.
- `right-to-delete` — per-user deletion procedure (GDPR / CCPA).
- `audit-log-retention` — compliance-mandated longer retention.

## Output

`docs/security/retention-policy.md` (single living doc) + enforcement configured in the relevant systems.
