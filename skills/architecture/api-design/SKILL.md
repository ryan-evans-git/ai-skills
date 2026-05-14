---
name: api-design
description: Apply opinionated API design conventions — resource modeling, URL structure, status codes, pagination, errors, idempotency, versioning — before any new endpoint is committed. Use when designing a new endpoint or service, when the user says "design this API", "REST conventions", "how should we structure this endpoint", or when reviewing API design in a PRD/ADR.
---

# api-design

## Purpose

Most "weird" APIs are weird because a hundred small decisions got made one at a time. This skill collects the decisions into an opinionated default so every new endpoint inherits a consistent shape — without re-litigating each one.

Pairs with `swagger-openapi-spec` (which documents the result) and `adr-writer` (which captures intentional deviations from these defaults).

## When to use

- Designing a new endpoint, resource, or service.
- Reviewing a PRD or ADR that includes API design.
- User says: "design this API", "REST conventions", "how should we structure this endpoint", "what's the right URL for", "REST vs gRPC".

## Default conventions

### Resource modeling
- **Nouns, not verbs.** `/orders/{id}/cancel` over `/cancelOrder/{id}` — but prefer `POST /orders/{id}:cancel` for actions on resources, RPC-style only when the action genuinely isn't a resource operation.
- **Pluralized collection names.** `/orders` not `/order`. Consistent.
- **Hierarchy reflects ownership.** `/users/{id}/orders` when an order belongs to one user; `/orders?user_id=X` when not.
- **Opaque IDs in URLs.** Strings, not integers. Prevents enumeration / IDOR.

### HTTP methods
| Method | Use |
| --- | --- |
| **GET** | Read; safe and idempotent; never has side effects, never has body |
| **POST** | Create, or non-idempotent action |
| **PUT** | Full replacement of a resource (idempotent) |
| **PATCH** | Partial update (state-transition or merge semantics — pick one and document) |
| **DELETE** | Remove (idempotent — second delete is 204 or 404, not 500) |

### Status codes (pick a small set, use consistently)
- **200** OK — read or update with body.
- **201** Created — POST that created a resource; include `Location` header.
- **202** Accepted — async work queued; include a status / polling URL.
- **204** No Content — DELETE or update with no body.
- **400** Bad Request — malformed request.
- **401** Unauthorized — no/bad auth.
- **403** Forbidden — authed but not allowed.
- **404** Not Found — resource not found OR (deliberate ambiguity) caller has no access.
- **409** Conflict — state conflict (concurrent edit, duplicate).
- **422** Unprocessable Entity — validation failed.
- **429** Too Many Requests — rate-limited; include `Retry-After`.
- **5xx** — your problem.

Don't invent new codes. Don't return 200 with `{"error": ...}` — use the right code.

### Error envelope (consistent across all endpoints)
```json
{
  "error": {
    "code": "invalid_amount",
    "message": "Amount must be positive.",
    "details": { "field": "amount", "value": -5 },
    "request_id": "req_abc123"
  }
}
```
- **`code`** machine-readable, stable, snake_case. Clients switch on this.
- **`message`** human-readable. Don't expose internals.
- **`details`** optional structured info.
- **`request_id`** ALWAYS included for support / debugging.

### Pagination
- **Cursor pagination** is the default. Returns `next_cursor` (opaque string).
- Offset pagination only for small, bounded collections — OFFSET on big tables kills performance.
- **`page_size`** param; bound it (max 100). Default to a sensible small number (20–50).

### Filtering, sorting
- **Filter** via query params: `?status=active&user_id=X`. Avoid complex query DSLs in URLs; use a POST `/search` for those.
- **Sort** via `?sort=created_at` / `?sort=-created_at`. Document allowed sort fields.

### Idempotency
- Mutations support `Idempotency-Key` header — same key + same payload returns the same result; same key + different payload returns 409 or 422.
- Especially important for: payments, sending messages, creating resources callers might retry.

### Time and money
- **All timestamps in UTC, ISO-8601 with explicit `Z`.** No locale-dependent formats. Never Unix timestamps in JSON (lose precision; ambiguous).
- **Money in minor units as integers.** `"amount": 1250, "currency": "USD"` for $12.50. Never floats for money.

### Versioning
- URL-versioned by default (`/v1/...`). See `api-contract-evolution`.

### Authentication
- Bearer tokens in `Authorization` header. Document scopes per endpoint.
- API keys (if used) go in `X-API-Key` header, never URLs (query params end up in logs).

### Empty / null / absent
- Pick one and stick with it across the API. Recommendation: omit absent optional fields; explicit `null` only when "no value" is semantically distinct from "not provided."

### Rate limiting
- Always include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.
- Differentiate "throttled" (429) from "quota exceeded" (also 429 — use `code` in error envelope to distinguish).

## Process

1. **Read the PRD / story** that motivates the new endpoint.
2. **Walk this skill's conventions**, listing intentional deviations with reasons.
3. **Sketch the endpoint(s)** — path, methods, request shape, response shape, status codes, errors.
4. **Write the OpenAPI** (`swagger-openapi-spec`).
5. **Capture deviations as ADRs** (`adr-writer`).

## What this skill does NOT do

- Cover gRPC / GraphQL design depth. The principles transfer but the conventions need their own skill.
- Replace per-domain modeling choices. Use ADRs for those.

## Output

Inline design notes used by `swagger-openapi-spec`; ADRs for deviations.
