---
name: api-contract-evolution
description: Govern how this service evolves its public contract over time — versioning policy, deprecation procedure, sunset timelines, and the migration playbook for callers. Use when defining versioning policy, when planning a v2, when the user says "API versioning", "deprecation policy", "how do we deprecate", "v1 to v2", "sunset this endpoint".
---

# api-contract-evolution

## Purpose

Versioning isn't a tactic; it's a *policy* the team commits to and callers can rely on. This skill defines that policy once, documents it, and references it from every subsequent breaking change. Without the policy, every change becomes a debate.

Pairs with [upstream-callers](../upstream-callers/SKILL.md) (which is per-change) — this skill defines the rules upstream-callers applies.

## When to use

- Defining versioning policy for a service for the first time.
- Planning a major version (v1 → v2).
- User says: "API versioning", "deprecation policy", "how do we deprecate", "v1 to v2", "sunset this endpoint", "should we go to v2".

## Decisions to make once, document forever

1. **Versioning style**:
   - **URL versioned** (`/v1/...`, `/v2/...`) — easiest for callers; explicit.
   - **Header versioned** (`Accept: application/vnd.foo.v2+json`) — clean URLs; lower discoverability.
   - **Media-type versioned** — heavy ceremony; rarely worth it.
   - **Date-versioned** (Stripe-style: `Stripe-Version: 2024-03-01`) — granular; complex on the server.
   Pick one; don't mix.
2. **Semver alignment**:
   - **MAJOR** for breaking contract changes.
   - **MINOR** for additive non-breaking.
   - **PATCH** for bug fixes, no contract change.
3. **Deprecation procedure**:
   - **Step 1 — Announce**: post to the channels listed in `service-map.md`. Add `Deprecation` and `Sunset` HTTP headers (RFC 8594).
   - **Step 2 — Document**: mark the operation `deprecated: true` in OpenAPI; add `x-sunset-date`.
   - **Step 3 — Instrument**: emit a metric on calls to the deprecated path: `deprecated_path_hits{endpoint="..."}`.
   - **Step 4 — Wait**: at least N months of deprecation (state the minimum; common values 3, 6, 12).
   - **Step 5 — Verify**: usage metric trends to zero, or remaining users have been individually contacted.
   - **Step 6 — Remove**: only after step 5, and never on a Friday.
4. **Sunset minimum**: state the floor (e.g. "no public endpoint is removed in less than 6 months from deprecation announcement"). Exceptions must be approved by a named role.
5. **Coexistence rules**: when v2 is released, how long does v1 live? Common: until usage trends to zero or sunset minimum has passed, whichever is later.

## Process

1. **Author `docs/integration/api-contract-policy.md`** with the decisions above. Single living doc.
2. **Link it from**:
   - `README.md`.
   - The OpenAPI spec's top-level `info.description`.
   - `docs/integration/service-map.md`.
3. **Reference it** in every PR that introduces a breaking change or deprecation. The PR template should ask: "Does this follow the API contract policy? Link it."
4. **For each deprecation in flight**, maintain a row in `docs/integration/api-contract-policy.md`:

   | Operation | Replacement | Deprecated on | Sunset date | Current callers | Owner |
   | --- | --- | --- | --- | --- | --- |
   | `GET /v1/orders` | `GET /v2/orders` | 2026-04-15 | 2026-10-15 | web-frontend, mobile-api | @platform-team |

5. **Calendar the sunset dates**. Each sunset gets a reminder on the day deprecation is announced (e.g. a recurring task / calendar invite). Otherwise sunsets slip indefinitely.

## Anti-patterns

- Versioning policy that's "whatever feels right at the time" — every deprecation becomes a one-off negotiation.
- No instrumentation on deprecated paths — you have no idea whether anyone migrated.
- Sunsetting on the calendar date regardless of remaining callers. The sunset date is necessary but not sufficient; usage must also have trended to zero.
- Releasing v2 with no plan for v1 retirement. Now you maintain two forever.
- Bumping major versions for non-breaking changes (semver violation; callers stop trusting your version numbers).

## What this skill does NOT do

- Make a single change (see `upstream-callers`).
- Maintain the service map (see `service-map`).

## Output

`docs/integration/api-contract-policy.md` (single living doc).
