---
name: right-to-delete
description: Implement a complete user-data deletion procedure that covers primary data, derived data, caches, backups, third-party processors, and produces a verifiable audit trail. Use when implementing GDPR / CCPA compliance, when designing account deletion, when the user says "right to delete", "right to be forgotten", "data subject deletion", "DSR", "account deletion".
---

# right-to-delete

## Purpose

"Delete my account" is one of the hardest features to implement correctly. Forgetting a single derived table or cache means the data isn't gone — and a regulator or auditor will find it. This skill is the systematic checklist of every place a user's data lives, with a verification step that proves the deletion happened.

## When to use

- Building a user-account-deletion feature.
- Preparing for GDPR / CCPA / similar compliance.
- After a deletion request was received but the procedure isn't yet automated.
- User says: "right to delete", "right to be forgotten", "DSR" (data subject request), "account deletion", "delete my account flow", "data erasure".

## The map — where user data actually lives

For each system on this list, the deletion procedure must address it (or explicitly note why it doesn't apply).

### Primary stores
- [ ] User row in the users / accounts table.
- [ ] Owned resources (orders, posts, uploads, files in object storage).
- [ ] Foreign-key referenced rows (comments by this user, audit log entries about this user).
- [ ] Soft-deleted rows from earlier deletes (covered by `data-retention-policy` hard-delete window).

### Derived / aggregated
- [ ] Materialized views referencing the user.
- [ ] Data warehouse / analytics DB copies.
- [ ] Embedding / vector stores keyed on user content.
- [ ] Search indexes (Elastic, Algolia, Meilisearch).
- [ ] Cached query results (`caching-strategy` cache layer).

### Logs
- [ ] Operational logs containing the user's ID / email / IP.
- [ ] Audit logs — **usually exempt from deletion** for compliance; see `audit-log-retention`. Document this exemption.

### Backups
- [ ] DB snapshots — typically NOT individually mutated; rely on natural backup rotation (must be documented in `data-retention-policy`).
- [ ] Document the maximum window before a restored backup would still contain the deleted user's data.

### Third-party processors
- [ ] Email / SMS providers (SendGrid, Twilio, Postmark).
- [ ] Analytics (Segment, Mixpanel, Amplitude, GA).
- [ ] Error tracking (Sentry, Rollbar).
- [ ] Customer support tools (Intercom, Zendesk, Front).
- [ ] Payment processor (Stripe, Adyen — usually has its own deletion API).
- [ ] CDN logs.
- [ ] Marketing automation.

### Auth & sessions
- [ ] Identity provider (Auth0, Cognito, Firebase, Clerk).
- [ ] Active sessions / refresh tokens revoked.
- [ ] MFA secrets / WebAuthn credentials.

### App-specific
- [ ] Frontend localStorage / IndexedDB — guidance to the user (we can't clear theirs from the server).
- [ ] Mobile-app on-device cache — same.

## Process

### Phase 1 — discovery (one-time)
1. Walk the map above. Build a per-system inventory of where the project actually stores user data.
2. Write to `docs/security/deletion-map.md` — one row per system with:
   - System name
   - What user data lives there
   - Deletion API / mechanism
   - Owner
   - Tested? (yes/no/date)

### Phase 2 — implement deletion flow
1. **User-initiated trigger** — the account-deletion endpoint.
2. **Confirm intent** — re-auth, type-the-username, 24-hour grace period (optional but recommended).
3. **Emit `user.deletion_requested` event** — let downstream systems (warehouse, analytics) react.
4. **Mark account "deletion pending"** — block login, suspend access.
5. **Run the deletion workflow** — either sync (small data) or queued (typical):
   - Delete primary store entries (cascade or explicit).
   - Trigger third-party deletion APIs (each vendor's pattern).
   - Invalidate caches.
   - Remove from search indexes.
   - Revoke sessions.
6. **Wait for natural-expiry items** (backups, logs) — document the window.
7. **Emit `user.deletion_completed`** event after sync deletions; emit `user.deletion_finalized` after the natural-expiry window.
8. **Record an audit log entry** — "User X deleted on YYYY-MM-DD; finalized YYYY-MM-DD" — for the compliance trail. (Yes, this means a record of the user existing remains; that's fine and necessary.)

### Phase 3 — verify
1. **Automated tests**: a "delete-then-search" test for each system — after deletion, try to find the user's data. Should fail.
2. **Manual periodic spot-check** — pick a test account, delete it, walk the map, confirm.
3. **Deletion confirmation to the user** — email confirming completion (sent at `deletion_completed`).

### Phase 4 — handle SLA
- GDPR: 30 days to fulfill, with one 60-day extension allowed.
- CCPA: 45 days, with one 45-day extension.
- Document the project's commitment (often "within X business days, faster than law requires").

## Common gotchas

- **Forgetting search indexes.** Deletion deletes the row but Elastic/Algolia still serves results.
- **Forgetting derived data.** Recommendations / embeddings derived from user content can still expose them.
- **Foreign-key constraints.** A user owns 1000 orders — `ON DELETE` strategy must be intentional (cascade vs. anonymize vs. transfer to a "deleted user" sentinel).
- **Audit logs leaking PII.** Audit logs may need to retain the action but not the PII — log user IDs and roles, not emails.
- **Backups undoing deletion.** A restore from a 90-day-old backup brings the user back. Test the restore-then-redelete procedure.
- **Email provider history.** Deleting the user in your DB doesn't delete the emails you've sent them via SendGrid's API — that's a separate call.

## What this skill does NOT do

- Decide what to retain for legal / accounting reasons (consult legal).
- Replace a Data Protection Impact Assessment for high-risk processing.

## Cross-references

- `data-retention-policy` — the overall retention framework.
- `pii-data-handling` — what data is classified as personal.
- `audit-log-retention` — the deliberately-exempt audit trail.

## Output

- `docs/security/deletion-map.md` — the per-system inventory.
- The deletion endpoint + workflow + tests in code.
- An entry in the `audit-log` of every deletion request and completion.
