---
name: service-map
description: Maintain a living service map at docs/integration/service-map.md — who calls this service, what this service calls, the contracts in play, and who owns each side. Use when starting a new service, when a new integration is added, when ownership changes, or when the user says "service map", "who calls this", "what does this depend on", "integration overview".
---

# service-map

## Purpose

In a multi-service world, the most expensive mistake is a change that breaks something you didn't know was calling you. The service map is the durable answer to "what would break if we changed this?" — maintained by humans, consulted by agents, and always read before any cross-service change.

## When to use

- Starting a new service.
- Adding a new upstream caller or downstream dependency.
- Ownership of a calling/called service changes.
- Before any API change (the [upstream-callers](../upstream-callers/SKILL.md) skill reads this).
- User says: "service map", "who calls this", "what does this depend on", "integration overview", "what would break if".

## Process

1. **Locate or create `docs/integration/service-map.md`.** One file per service repo.
2. **Populate two tables**:

   **Upstream callers** — services that call this one:

   | Caller | Endpoints called | Contract | Owner | Priority | Notes |
   | --- | --- | --- | --- | --- | --- |
   | `web-frontend` | `GET /v1/orders`, `POST /v1/orders` | `docs/api/openapi.yaml` v1.4 | @team-web | P0 | Customer-facing checkout |
   | `mobile-api` | `GET /v1/orders` | same | @team-mobile | P0 | Hits this on every app launch |
   | `analytics-pipeline` | `GET /v1/orders/changes` | streaming, JSON-lines | @team-data | P2 | Async; tolerates delay |

   **Downstream dependencies** — services this one calls:

   | Dependency | Endpoints used | Contract | Owner | Failure mode | Notes |
   | --- | --- | --- | --- | --- | --- |
   | `payment-service` | `POST /v2/charges` | `payment-service/docs/api/openapi.yaml` v2.1 | @team-payments | Block checkout | Idempotency-Key required |
   | `inventory-service` | `GET /v1/availability` | gRPC `inventory.v1.AvailabilityService` | @team-fulfillment | Show stale stock | 200ms timeout |
   | `Stripe` | charges, customers | external | (Stripe support) | Block checkout | PCI scope |

3. **Required fields per row**:
   - **Endpoints** — the specific operations involved, not just "the service."
   - **Contract** — the contract document (OpenAPI version, gRPC proto, etc.).
   - **Owner** — the team or person responsible on the *other* side.
   - **Priority** (for upstream) — P0 (breaks user flow) / P1 (degrades) / P2 (async or non-critical).
   - **Failure mode** (for downstream) — what happens to this service when the dependency is unhealthy.
4. **Add a "Contact for breaking changes" block** at the top — one row per caller team with how to reach them (Slack channel, email list, on-call rotation). Breaking changes start with a message to this list.
5. **Keep the date current.** `Last updated: YYYY-MM-DD` at the top. Stale maps are dangerous — a section more than 90 days unchanged should be reviewed.
6. **Cross-link**:
   - From `README.md` to the service map.
   - From `docs/architecture/system.drawio` if it shows the same relationships.
   - From every PRD / ADR that adds an integration.

## When to refresh proactively

- After a quarter passes (review for staleness).
- After any new endpoint is exposed publicly.
- After a new external SDK / API call is introduced.
- After a team reorg that may have changed owners.

## What this skill does NOT do

- Auto-discover callers/dependencies. Static analysis can help (grep for HTTP clients, OpenAPI consumers) but this map is *intentional* — it represents what the team is committed to supporting, not just what happens to be wired up.
- Replace runtime observability (request graph from traces). Both are useful; the map is the *contract*, traces are the *reality*.

## Output

`docs/integration/service-map.md` (single living doc per service repo).
