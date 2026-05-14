---
name: audit-log-retention
description: Define and enforce a separate retention policy for audit / compliance logs — typically longer than operational logs, often legally required, and exempt from user-deletion requests. Use when implementing audit logging, before compliance review, or when the user says "audit log", "audit trail", "SOX log", "compliance log retention", "tamper-evident log".
---

# audit-log-retention

## Purpose

Audit logs are different from operational logs: they exist to prove who did what when, for regulatory, security-incident, and dispute-resolution purposes. They typically need longer retention, stronger integrity guarantees, and explicit exemption from user-deletion requests. This skill makes those properties deliberate rather than accidental.

Pairs with `data-retention-policy` (the general retention framework) and `right-to-delete` (where audit logs are intentionally NOT deleted).

## When to use

- Implementing audit logging for the first time.
- Before SOC2 / SOX / HIPAA / PCI / ISO27001 review.
- After an incident where "who did this" couldn't be answered.
- User says: "audit log", "audit trail", "SOX log", "compliance log", "tamper-evident log", "WORM storage".

## What IS an audit log (vs. what isn't)

| Is | Isn't |
| --- | --- |
| Auth events (login, logout, failed login, MFA challenge) | Page-view tracking |
| Authz decisions (especially denies) | Performance metrics |
| Admin actions (config changes, user impersonations) | Application errors |
| Data access on sensitive records (PHI reads, financial reads) | Search queries |
| Permission grants / revokes | Cache hits |
| Account lifecycle events (create, delete, suspend) | Request body details |
| Security-policy decisions (rate-limit triggers, WAF blocks) | Background-job durations |

If the line "operator action on user data / system config" applies, it's audit. Otherwise it's operational.

## Required properties

### Content
- **Who** — actor identity (user ID, service ID, system).
- **What** — the action verb + target (e.g. `account.delete` on user X).
- **When** — UTC timestamp with millisecond precision.
- **Where** — source IP / region / device fingerprint.
- **How** — auth method (password / MFA / SSO / API key ID).
- **Result** — success / failure / partial.
- **Correlation** — request ID / trace ID for cross-referencing.

### Storage
- **Append-only** — no UPDATE / DELETE in the application path. Use append-only schemas, WORM object storage, or a managed audit service.
- **Tamper-evident** — at minimum, periodic integrity checksums; ideally hash-chained entries.
- **Separate from operational logs** — different sink, different retention, often different access controls.
- **Encrypted at rest.**
- **Replicated** — single-region storage is a single point of loss.

### Access
- **Limited reads** — auditing is a sensitive permission; not every engineer has it.
- **Reads are themselves audited.** Querying the audit log is an audit-worthy action.
- **No edits, ever.** Corrections happen by *appending* a new entry, not modifying the prior one.

## Retention defaults

These vary by regime; use as starting points and confirm with legal.

| Regime / use case | Typical retention |
| --- | --- |
| **SOX** (financial controls) | 7 years |
| **HIPAA** | 6 years (US federal); longer in some states |
| **PCI-DSS** | 1 year, last 3 months immediately available |
| **SOC2** | 1 year typical; org-defined |
| **GDPR** | "As long as necessary"; balance against right-to-delete |
| **Default for general audit** | 2 years online + 5 years cold storage |

Document the project's actual number, with a citation to why.

## Process

1. **Define which events count as audit-worthy** — list them in `docs/security/audit-log-spec.md`. One row per event type with the required fields per event.
2. **Pick a storage approach**:
   - **Database table** with INSERT-only role + immutable schema (cheap, simple, integrity via app discipline).
   - **Append-only object storage** with bucket versioning + object lock (S3 Object Lock, GCS retention policies).
   - **Managed audit service** (Datadog Audit Trail, AWS CloudTrail, Splunk, Panther).
3. **Implement emission** — a single audit-emit helper used everywhere, NOT scattered `logger.info("user logged in")` calls. The helper enforces the required fields.
4. **Set retention** matching the regulatory floor. Configure at the storage layer (lifecycle policy / object lock / DB partition expiry).
5. **Configure access**:
   - Read role separate from operational log role.
   - Reads to the audit log themselves audited.
   - No service-account write access to *modify* — INSERT only.
6. **Document the right-to-delete exemption** in `docs/security/retention-policy.md`:
   - Audit logs are retained for [period] for [reason: SOX / HIPAA / SOC2 / fraud-investigation].
   - User-deletion requests do NOT remove audit log entries (only PII fields are minimized where possible).
   - User-facing privacy notice must say this.
7. **Test integrity** periodically:
   - Run an integrity check on a sample of records (checksum / hash-chain verify).
   - Confirm no engineer has been able to DELETE / UPDATE in the past period (review IAM logs of the audit store).
8. **Test retrievability** — pull a record from N years ago in a tabletop exercise. If you can't, the retention is theoretical.

## Anti-patterns

- **Audit events in the same log stream as request logs.** Different retention, different access controls — separate them.
- **`logger.info("admin changed config")`** as the audit mechanism. Will drift; not enforced; no required fields.
- **App-controlled deletion of audit records.** Defeats the purpose. Use platform-level retention, not app DELETEs.
- **PII in audit logs that shouldn't be there.** Log user IDs (and minimal context to identify the actor), not emails / names. Audit logs survive deletion; PII in them creates a "right to delete" conflict.
- **No alerting on audit-log tampering.** A successful tamper attempt without alerts is invisible.

## Cross-references

- `data-retention-policy` — the overall framework.
- `right-to-delete` — exempts audit logs.
- `logging-standards` — separate set of rules for operational logs.
- `security-review` — checks that auth/authz events are logged.

## Output

- `docs/security/audit-log-spec.md` — list of audit-worthy event types + required fields.
- Audit log infrastructure (table / bucket / managed service) configured with retention.
- Audit-emit helper in code, used everywhere audit events arise.
