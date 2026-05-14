---
name: pii-data-handling
description: Inventory the project's PII / sensitive data fields, classify them, and document handling rules — encryption, logging, retention, deletion, access. Use when adding new data fields, before a release, when preparing for GDPR / CCPA / SOC2 / HIPAA review, or when the user says "PII", "data classification", "GDPR", "privacy review".
---

# pii-data-handling

## Purpose

Most data-handling failures come from "we didn't realize that field was sensitive." This skill maintains a living inventory of every PII / sensitive field and the handling rules for each — so logging, storage, retention, and deletion decisions are made deliberately.

## When to use

- Starting a new project that handles user data.
- Adding any new field that might be PII or sensitive.
- Before a release.
- Preparing for compliance review (GDPR / CCPA / SOC2 / HIPAA).
- User says: "PII", "data classification", "GDPR", "privacy review", "right to delete", "data retention".

## Classification levels

| Level | Examples | Default handling |
| --- | --- | --- |
| **Public** | Marketing copy, public usernames | No special handling. |
| **Internal** | User-agent, request paths, IDs not tied to identity | Logged freely, retained per default. |
| **Confidential — PII** | Name, email, IP address (in many jurisdictions), phone, address, DOB | Encrypted at rest, not in logs by default, retention bounded. |
| **Sensitive — special category** | Health, financial, biometric, government ID, sexual orientation, religion | Encrypted at rest with field-level encryption where possible. NEVER in logs. Access logged. Retention strict. |
| **Authentication material** | Passwords, tokens, secrets, keys | Hashed (passwords) or referenced (tokens). Never logged. Never returned to client. Rotation policy in place. |

## Process

1. **Inventory every field** the system collects, derives, stores, or transmits. Sources:
   - DB schemas.
   - API request/response schemas (`docs/api/openapi.yaml`).
   - Logging statements (grep for `log.info`, `logger.`, etc., near user data).
   - Third-party services (analytics, error trackers, customer support).
2. **For each field, record**:
   - Field name + storage location (table.column, schema property).
   - Classification level (Public / Internal / Confidential / Sensitive / Auth).
   - Source — how does it enter the system.
   - Sinks — where does it go (DB, logs, third-party, exports).
   - Encryption — at rest, in transit, field-level.
   - Retention — how long, who decides, when it's deleted.
   - Deletion path — what happens on a "delete my data" request.
   - Access — who/what can read it; is access logged.
3. **Check for violations**:
   - PII / Sensitive fields appearing in logs.
   - PII shared with third parties not in the privacy policy.
   - Fields with no defined retention.
   - Sensitive fields without field-level encryption.
   - Auth material returned by any API (even to "self").
   - No deletion path (right to be forgotten).
4. **Compliance hooks** — note which fields are subject to:
   - **GDPR** — anyone in the EU/EEA: requires consent, access, deletion, portability.
   - **CCPA/CPRA** — California residents.
   - **HIPAA** — if PHI applies.
   - **PCI-DSS** — payment data.
5. **Write to `docs/security/pii-inventory.md`** (single living doc — UPDATE, don't append new files per audit). Date-stamp the doc at the top: `Last updated: YYYY-MM-DD`.
6. **For violations**, file action items on `docs/plans/CURRENT.md`.

## Logging rule (worth highlighting separately)

A simple rule that prevents most leaks:

> Default to redacting any field at Confidential or above when logging. Use structured logging with explicit field allowlists, not stringly-interpolated messages.

See `logging-standards` skill for the implementation pattern.

## What this skill does NOT do

- Make legal determinations. "Is this PII under GDPR" is a legal question with regional answers — flag for legal review when uncertain.
- Replace a DPIA (Data Protection Impact Assessment) for high-risk processing.

## Output

`docs/security/pii-inventory.md` (living, single doc)
