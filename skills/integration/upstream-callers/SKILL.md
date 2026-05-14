---
name: upstream-callers
description: Before changing any public API in this service, consult the service-map to identify upstream callers, classify the change as breaking vs. non-breaking, and decide rollout (versioning, deprecation window, comms). Use whenever the user wants to change a public route, response shape, error code, header, or behavior — or says "change the API", "rename this field", "deprecate this endpoint", "breaking change".
---

# upstream-callers

## Purpose

The number-one cause of cross-service outages is a change that *looked* safe in this repo but broke a caller in another repo. This skill forces the agent to consult the [service-map](../service-map/SKILL.md) and classify every public-API change before the code is written.

## When to use

- About to change a public HTTP route, gRPC method, event topic, or any other published contract.
- User says: "change the API", "rename this field", "deprecate this endpoint", "breaking change", "remove this route", "tighten validation".
- Reviewing a PR that touches anything reachable from a caller.

## Process

1. **Identify what is changing.** Be precise about *exactly* which:
   - Route / path / method.
   - Field name, type, presence (required ↔ optional).
   - Status code, error envelope shape.
   - Headers (request or response).
   - Behavior (default values, ordering, side effects, idempotency).
   - Auth requirements (newly requiring a scope is breaking).
2. **Classify the change**:
   | Class | Examples |
   | --- | --- |
   | **Non-breaking** (additive) | New optional field in response; new endpoint; new optional query param |
   | **Subtly breaking** | New required request field; tighter validation; new auth scope; changed default |
   | **Breaking** | Renamed/removed field; status code change; URL change; semantic change |

   If in doubt, treat as breaking. "Subtly breaking" is breaking in production.
3. **Open `docs/integration/service-map.md`** and read every row in the **Upstream callers** table. For each caller:
   - Do they use the endpoint being changed? (Check the "Endpoints called" column.)
   - What's their priority? (P0 callers gate everything.)
   - Who owns them?
4. **For non-breaking changes**: proceed. Update the OpenAPI spec (`swagger-openapi-spec` skill), bump the minor version, mention in `CHANGELOG`.
5. **For breaking changes**: do not just change. Choose a rollout:
   - **Versioned coexistence** — keep v1 working; add v2 with the new shape. Callers migrate on their schedule. Preferred for any P0 caller.
   - **Deprecation window** — keep both shapes responding; mark v1 deprecated in OpenAPI; log a deprecation warning header on v1 calls; commit a sunset date.
   - **Coordinated change** — only when all callers are within your control and willing to deploy in lock-step. Document the order.
   - **Hard break** — only with explicit go-ahead from every P0/P1 caller owner, recorded in writing.
6. **Communicate before merging**:
   - Post in the channel(s) listed in the service-map's "Contact for breaking changes" block.
   - Open issues/tickets on caller repos so it lands in their backlog.
   - Get a written acknowledgement from each P0/P1 caller owner.
7. **Update artifacts**:
   - `docs/api/openapi.yaml` — bump version, mark deprecated where applicable, add `x-sunset-date`.
   - `CHANGELOG.md` — under a `Deprecated` or `Breaking` heading.
   - `docs/decisions/log.md` or a full ADR if the change is significant.
   - `docs/integration/service-map.md` if the contract version changed.
8. **Monitor the deprecation**:
   - Emit metrics on use of the deprecated path: `deprecated_path_hits{endpoint="/v1/foo"}`.
   - Alert if usage doesn't trend to zero before the sunset date.

## Anti-patterns

- "It's just renaming a field; the diff is tiny." Rename = breaking. Always.
- Removing a field because "nobody uses it" without metrics to prove zero use.
- Trusting a recent grep over the service map — your grep doesn't see the mobile-app repo you forgot about.
- Sunset-date in the future, then forgetting about it. Calendar the date when you ship the deprecation.

## What this skill does NOT do

- Maintain the service map itself (see `service-map`).
- Design the new API shape (see `api-design` in the architecture category).
- Write the OpenAPI changes (see `swagger-openapi-spec`).

## Output

A classification + rollout decision recorded in the PR description or commit message, plus updates to the artifacts listed above.
