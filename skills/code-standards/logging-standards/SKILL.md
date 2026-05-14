---
name: logging-standards
description: Define structured logging conventions — log levels, what to log, what NEVER to log (PII, secrets), required context fields (request_id, trace_id, user_id), and how to log errors. Use when starting a project, when adding observability, or when the user says "logging standards", "what to log", "structured logs", "log format".
---

# logging-standards

## Purpose

Logs are the cheapest observability you have — and the easiest place to leak data or generate unsearchable noise. This skill puts a thin, opinionated standard in place so logs are structured, searchable, and safe.

## When to use

- Starting a new project / service.
- Adding observability to existing code that prints.
- After an incident where missing or noisy logs slowed diagnosis.
- User says: "logging standards", "what to log", "structured logs", "log format", "log levels".

## The rules

### Format

1. **Structured.** JSON for prod, key=value or JSON for dev. Never pure prose strings as the only content.
2. **One event per call.** Don't span events across `log` calls. If a single operation has phases, emit a start and an end with a shared correlation id.
3. **Required fields on every log line:**
   - `timestamp` (ISO-8601, UTC, with microseconds).
   - `level` (DEBUG / INFO / WARN / ERROR / CRITICAL).
   - `service` (which service / module).
   - `request_id` and/or `trace_id` (propagated from the inbound request or job).
   - `event` — short snake_case name describing what happened (`user_signup_succeeded`, `payment_authorized`).
4. **Encouraged fields when applicable:**
   - `user_id` (NOT email/name — see PII rules below).
   - `tenant_id`.
   - `duration_ms` for timed operations.
   - `error_type` and `stack` for ERROR.

### Levels

| Level | Use |
| --- | --- |
| **DEBUG** | Developer-only detail. Should be safely silenceable in prod. |
| **INFO** | Notable events that explain what the system did. One per significant operation, not per loop iteration. |
| **WARN** | Something unusual but handled (retry succeeded, fallback used, deprecated endpoint hit). |
| **ERROR** | Unhandled failure or operator-actionable problem. Includes stack trace. |
| **CRITICAL** | System unable to serve. Pages on-call. |

INFO is not a free-for-all. If your INFO logs scroll faster than a human can skim them, half of them should be DEBUG.

### What NEVER to log

- Passwords, tokens, API keys, OAuth codes — even truncated.
- Full credit card numbers, full SSNs, full government IDs.
- PII or sensitive data per `pii-data-handling` classification (Confidential and above).
- Full request/response bodies on sensitive endpoints. Log shape + size, not content.
- Internal stack traces in WARN-level logs (use ERROR or DEBUG).

### What to log

- Inbound request: method, path, status, duration, user_id (if authenticated), `request_id`.
- Significant state changes: created/updated/deleted with subject IDs.
- External calls: target, duration, success/failure, retries.
- Authn/authz outcomes (success + failure — security signal).
- Backend errors with their wrapped chain (see `error-handling-standards`).

### PII redaction

- Apply a redaction filter at the logging-framework level. Don't rely on every dev remembering.
- Allowlist what's loggable per field, rather than denylisting what isn't.
- For values that must be partially visible (last 4 of a card, masked email), use a single standard helper.

## Process

1. **Write `docs/standards/logging.md`** with the rules above and language-specific examples (Python `structlog` / `logging`, JS `pino`, Rust `tracing`, etc.).
2. **Configure the logging framework** to emit structured output and inject required fields automatically (request_id middleware, trace propagation).
3. **Add a redaction filter** for the classified fields from `pii-data-handling`.
4. **Set log-level conventions per environment** (DEBUG locally, INFO in staging, INFO+ in prod, ERROR pages).
5. **Add to the code-review checklist** (cross-ref `self-review`, `security-review`): no PII in logs, no `print`/`console.log` left behind.

## Anti-patterns

- `logger.info(f"user {user}")` with `__str__` returning the email. Use explicit IDs.
- One giant log message with a JSON blob inside a string. Use structured fields.
- DEBUG logs that include data the company isn't allowed to retain — the level doesn't change the storage policy.
- "Just to be safe" logs at every function entry. They're noise, not safety.

## What this skill does NOT do

- Specify tracing (OpenTelemetry / distributed tracing). That's a separate observability skill if you add one.
- Set up a log aggregator. The format must work with whatever you pick; configuration is separate.

## Output

`docs/standards/logging.md`
