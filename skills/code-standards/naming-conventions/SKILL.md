---
name: naming-conventions
description: Define naming rules for files, directories, modules, functions, variables, constants, tests, branches, and identifiers across the project's languages. Use when starting a project, when a naming disagreement comes up, or when the user says "naming", "what should I call this", "rename convention", "branch names".
---

# naming-conventions

## Purpose

Names are read more than they're written. Consistent naming reduces cognitive load across modules, helps grep, and prevents the slow drift into `utils.py` / `helpers.ts` / `misc/` chaos.

## When to use

- Starting a new project.
- A naming disagreement comes up in PR review.
- User says: "naming", "what should I call this", "rename convention", "branch names".

## Process

1. **Author `docs/standards/naming.md`** with the conventions below.
2. **Wire enforceable rules into the linter** where possible (file naming, function casing, constant casing).
3. **Cross-link** with `style-guide-keeper` (it points here).

## Conventions

### Files & directories

- Lowercase, hyphen-separated (`order-service.ts`, `user-repository.py`) — UNLESS the language convention says otherwise (Python uses underscores: `order_service.py`).
- One concept per file. If you'd struggle to name a file with one noun, it's doing too much.
- No `utils`, `helpers`, `misc`, `common` directories. Each utility lives near what it serves, or in a named module that says what it does.
- Tests mirror source: `src/foo.py` → `tests/test_foo.py`; `src/Bar.ts` → `src/Bar.test.ts` or `__tests__/Bar.test.ts`.

### Functions

- **Verb + noun.** `fetchUser`, `parsePayload`, `validateEmail`. Functions are actions.
- **Booleans use `is`, `has`, `should`, `can`.** `isActive`, `hasPermission`, `shouldRetry`. No `flag` / `check` / `bool`.
- **No "Manager", "Handler", "Helper", "Util" suffixes** unless they mean something specific in your framework.
- **No abbreviations** unless universally understood (`url`, `id`, `json`, `db`). `usr`, `cfg`, `prsr` are forbidden.
- **Side-effect signaling:** prefer pure functions; when a function mutates or does I/O, the verb should make it obvious (`save`, `update`, `delete`, `send`, `fetch`).

### Variables

- **Descriptive over short.** `userId` not `uid`, `accountBalance` not `bal`.
- **No single letters** except loop indices (`i`, `j`) and lambda placeholders (`x` in `xs.map(x => ...)`). Even those should grow up to real names if the body is more than one line.
- **Plurals for collections.** `users`, not `userList`.
- **Avoid type-encoded names** (`strName`, `arrUsers`) — types are types.

### Constants

- `SCREAMING_SNAKE_CASE` for module-level constants in Python / JS.
- `kCamelCase` only if your language convention demands it (Google C++).
- Constants near their use, not in a global `constants.py` unless they're truly shared.

### Classes & types

- `PascalCase` everywhere except in languages that say otherwise.
- **Noun phrases**, not verbs. `OrderProcessor`, `UserRepository`, `BillingError`. Never `OrderProcessing` (gerund) or `ProcessOrder` (verb).
- **Interfaces / abstract types** — don't prefix with `I` (Java/.NET-style) unless the team explicitly chose to.

### Tests

- Test names describe behavior: `test_user_signup_with_existing_email_returns_409`.
- Not `test_signup_1`, `test_works`.
- Pattern: `test_<subject>_<scenario>_<expected_outcome>`.

### Branches

- `<type>/<short-description>` where type is `feat` / `fix` / `chore` / `refactor` / `docs` / `spike`.
- Example: `feat/order-cancellation-flow`, `fix/idor-on-user-endpoint`.
- Lowercase, hyphen-separated, no ticket numbers in the branch name unless required by tooling.

### Commits

- Conventional commits: `type(scope): description`.
  - `feat(orders): support partial cancellation`
  - `fix(auth): close session on password change`
- Imperative voice ("add", "fix" — not "added", "fixes").

### Identifiers (UUIDs, slugs, IDs)

- IDs are surfaced as opaque strings in APIs, never auto-increment integers in URLs (IDOR risk; see `security-review`).
- Slugs are lowercase, hyphen-separated, stable.
- UUIDs are v7 (time-ordered) where supported, v4 otherwise.

## Process when renaming

- Use the IDE's rename refactor; verify across the whole repo.
- Update tests, docs, and any string references (config keys, log event names, schema fields).
- Deprecate old names with a sunset date, don't just delete (especially for public API surfaces).
- Capture the rename in the changelog if user-visible.

## What this skill does NOT do

- Cover URL design / REST resource naming — those belong in `swagger-openapi-spec`.
- Cover database naming — that's a separate concern (recommend snake_case for tables/columns).

## Output

`docs/standards/naming.md`
