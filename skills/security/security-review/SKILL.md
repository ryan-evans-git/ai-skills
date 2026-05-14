---
name: security-review
description: Review a diff or PR for security issues — OWASP Top 10, injection, broken auth, secrets, unsafe deserialization, SSRF, IDOR, race conditions. Use before merging anything that touches auth, user input, file uploads, external calls, or sensitive data; or when the user says "security review", "OWASP", "vulns in this", "is this safe".
---

# security-review

## Purpose

Catch security defects in the code BEFORE they ship. Complements `self-review` with a security-specific lens. Triggered per-diff; the diff-level companion to design-time `threat-model`.

## When to use

- Before merging a PR that touches: auth, sessions, password / token handling, user input, file uploads, SQL/NoSQL queries, shell commands, deserialization, redirects, file paths, external HTTP calls, crypto primitives.
- User says: "security review", "OWASP review", "is this safe to merge", "vulns in this", "security check".
- After `self-review` for anything user-facing.

## Process

1. **Pull the diff**: `git diff <base>...HEAD`.
2. **Walk the checklist below** against the diff, hunk by hunk. Don't summarize — actually read.
3. **For each finding**, cite `file:line` with severity (Critical / High / Medium / Low) and a suggested fix.
4. **Output a structured review** with sections: Critical, High, Medium, Low, plus Verdict.

## Checklist (OWASP Top 10 + common code-level issues)

### A01 Broken access control
- [ ] Every new endpoint enforces authn AND authz.
- [ ] No object-level IDs in URLs without ownership check (IDOR).
- [ ] No reliance on client-side authz checks alone.
- [ ] Admin-only routes are gated server-side, not just hidden in UI.

### A02 Cryptographic failures
- [ ] No hand-rolled crypto. Use the language's vetted lib.
- [ ] No MD5/SHA1 for security. No ECB mode. No fixed IVs.
- [ ] Secrets / tokens generated with a CSPRNG.
- [ ] TLS required for any sensitive transmission.
- [ ] Passwords stored with a slow hash (bcrypt/argon2/scrypt), never plain or fast-hash.

### A03 Injection
- [ ] SQL uses parameterized queries / prepared statements. No string concatenation.
- [ ] No shell commands with user input. If unavoidable, use argv arrays, never `shell=True`/string commands.
- [ ] HTML output is escaped by default (template engine in autoescape mode).
- [ ] LDAP/XPath/NoSQL injection: same rules — parameterize.
- [ ] No `eval`, `exec`, `pickle.load` on untrusted input.

### A04 Insecure design
- [ ] Rate limits exist on sensitive endpoints (login, password reset, signup).
- [ ] Idempotency keys on financial / state-changing operations where appropriate.
- [ ] Error messages don't reveal whether a user exists (no "user not found" vs "wrong password" leak).

### A05 Security misconfiguration
- [ ] No debug mode / verbose stack traces in production.
- [ ] Default credentials changed; example/seed data not in prod.
- [ ] CORS scoped narrowly; not `*` for credentialed endpoints.
- [ ] Security headers set: HSTS, CSP, X-Content-Type-Options, X-Frame-Options / frame-ancestors.

### A06 Vulnerable & outdated components
- [ ] New deps added are not on a CVE list (`dependency-audit` skill).
- [ ] No copy-pasted code from random gists.

### A07 Identification & authentication failures
- [ ] Sessions invalidated on logout AND password change.
- [ ] Session cookies: HttpOnly, Secure, SameSite=Lax/Strict.
- [ ] MFA challenges can't be skipped.
- [ ] Password reset tokens are single-use, time-limited, and bound to the user.

### A08 Software & data integrity failures
- [ ] No deserializing untrusted data with `pickle`, `yaml.load` (use `safe_load`), unsafe XML.
- [ ] Integrity-check downloads (checksum / signature).
- [ ] CI/CD doesn't trust workflow files from forks for secrets.

### A09 Security logging & monitoring failures
- [ ] Auth failures, authz failures, and admin actions are logged.
- [ ] Logs do NOT include secrets, passwords, full tokens, full PAN, or unredacted PII.
- [ ] Alerting exists for spikes in auth failures / 5xx / unusual access patterns.

### A10 Server-side request forgery (SSRF)
- [ ] User-provided URLs are validated against an allowlist before fetch.
- [ ] No fetching from `localhost`, `169.254.169.254`, RFC1918, or `file://` based on user input.
- [ ] Redirects from user URLs are bounded.

### Project-specific (always check)
- [ ] No new secrets committed (api keys, tokens, private URLs).
- [ ] No PII added to log statements (cross-ref `logging-standards`).
- [ ] No raw HTML or markdown from user input rendered without sanitization.
- [ ] File uploads have type/size limits and are stored outside the webroot.
- [ ] Redirects use an allowlist or only relative paths.

## Output format

```
# Security review: <PR title>

## Critical
- `file.py:42` — <issue>. <suggested fix>.

## High
- ...

## Medium
- ...

## Low / nits
- ...

## Verdict
<one of: BLOCK — fix Critical/High before merge | APPROVE WITH NOTES | APPROVE>
```

## What this skill does NOT do

- Replace a security engineer for high-risk changes.
- Run dynamic analysis (DAST). For static analysis, optionally invoke `semgrep`, `bandit`, etc.
