---
name: error-handling-standards
description: Define and enforce the project's error-handling patterns — no bare excepts, no silent swallow, typed errors at boundaries, log-and-rethrow only at the top, distinguish expected vs. unexpected. Use when starting a project, when designing a new module/service, or when the user says "how should we handle errors", "error standards", "exception policy".
---

# error-handling-standards

## Purpose

Most "weird production behavior" is caused by errors being swallowed, mis-typed, or mis-logged. This skill puts down rules — and a doc engineers reference — so error handling is consistent and traceable.

## When to use

- Starting a new project or service.
- Designing a new module that owns a boundary (HTTP, DB, external API, queue).
- User says: "how should we handle errors", "error standards", "exception policy", "try/except", "should we catch X".

## The rules

1. **Never silently swallow.** If you catch, you must:
   - log it (with enough context to understand later), OR
   - convert and re-raise as a typed domain error, OR
   - explicitly mark it as expected (`# expected: <reason>`) and at least log at DEBUG.
2. **Never `except Exception:` / `catch (Throwable e)` / blanket catch** except at well-defined boundaries: the top of a request handler, a job runner, a CLI entry point. Bare catches everywhere mean nothing is debuggable.
3. **Typed errors at module boundaries.** A module's callers should be able to handle errors by *type*, not by parsing strings. Define a small, finite set of error classes per module.
4. **Distinguish expected from unexpected.**
   - **Expected** (e.g. `UserNotFound`, `InsufficientFunds`): represent as typed errors, returned to callers, logged at INFO, mapped to user-facing messages.
   - **Unexpected** (`KeyError` from a bug, `OperationalError` from a downed DB): logged at ERROR with full context + stack trace, mapped to a generic 5xx for users.
5. **Log once, near the top.** Logging the same exception three times in three layers is noise. Lower layers wrap; the top layer logs.
6. **Preserve context.** When wrapping, include the original exception (Python's `raise X from e`, JS `new Error('...', { cause: e })`, Rust `anyhow!(...).context(...)`).
7. **No `pass` in `except`** unless paired with an explicit `# expected: <reason>` comment AND it's at least a DEBUG log.
8. **No `print` for errors.** Use the logger. See `logging-standards`.
9. **Async errors are not different.** Unawaited promises / unhandled tasks must be caught at the runtime boundary, not lost.
10. **Errors in tests are real.** Tests that pass with logged tracebacks are bugs.

## Process

1. **Author `docs/standards/error-handling.md`** with the rules above, language-specific examples per language in use, and references to the project's typed error classes / error types.
2. **Define the boundary error types** for each major module/service: list them in the doc.
3. **Configure lint rules** that catch violations:
   - Python: `ruff` with rules `BLE001` (blind except), `S110` (try/except/pass), `S112` (try/except/continue), `RET503` (missing return), `E722` (bare except).
   - TS/JS: ESLint rules `no-empty-catch`, `@typescript-eslint/no-throw-literal`, `no-promise-reject-errors`.
   - Rust: clippy `unwrap_used`, `expect_used`, `panic` (in libraries).
4. **Document mapping** from internal error types to user-facing API responses (e.g. `UserNotFound` → HTTP 404, `InsufficientFunds` → HTTP 422). This belongs in the OpenAPI spec too — cross-ref `swagger-openapi-spec`.
5. **Add to the code-review checklist** (cross-ref `self-review`, `security-review`).

## Anti-patterns to call out

- "Belt and suspenders" double-try: catching and rethrowing the same thing in the same layer.
- Catching to print a friendlier message but losing the stack trace.
- `assert` for runtime validation in production code (asserts can be stripped in optimized builds).
- `raise Exception("...")` instead of a typed error.
- Returning `None` / sentinel values from functions that should raise; or raising from functions that should return `Option`/`Result`.

## What this skill does NOT do

- Replace per-module error-design choices. The doc states the rules; ADRs capture specific module designs.

## Output

`docs/standards/error-handling.md`
