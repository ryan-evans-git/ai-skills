---
name: swagger-openapi-spec
description: Author and maintain an OpenAPI 3.x (Swagger) specification for every HTTP route in the project, with operationIds, summaries, and descriptions formatted for direct conversion into MCP tool definitions. Use when adding/changing an HTTP route, when the user says "swagger", "openapi", "API spec", "document the API", "MCP tools from the API", or when an OpenAPI file is missing for an HTTP service.
---

# swagger-openapi-spec

## Purpose

Every HTTP route in the project is described in an OpenAPI 3.x spec that is *good enough to feed directly to an MCP server*. The spec is treated as the source of truth for tool generation, client generation, and human onboarding — not as a chore done after the fact.

## When to use

- Adding, changing, or removing an HTTP route.
- The project exposes HTTP routes but has no OpenAPI spec.
- User says: "swagger", "openapi", "API spec", "document the API", "I want MCP tools from this".
- A PRD or ADR is being implemented that introduces new endpoints.

## Process

1. **Locate or create the spec**:
   - Default location: `docs/api/openapi.yaml` (or `docs/api/openapi.json`).
   - One spec per deployable service. Don't merge unrelated services into one file.
2. **For every route, populate every required field below.** Missing fields are not optional — they directly degrade MCP tool quality.
3. **Validate** the spec with a linter (`redocly lint`, `spectral lint`, or `openapi-spec-validator`) before merging.

## Required per-operation fields (MCP-ready)

Every operation MUST have:

- **`operationId`** — camelCase, action verb + noun, unique across the spec. This becomes the MCP tool name. Examples: `getUserById`, `listOrders`, `createInvoice`, `cancelSubscription`. Never reuse, never rename without a deprecation path.
- **`summary`** — under 60 characters, action-oriented. Shown as the short label in tool pickers.
- **`description`** — 1–3 sentences explaining *when an agent should call this tool*, not just what it does. This is the load-bearing field — an LLM uses it to decide whether to invoke the tool. Write it in user-need terms.
  - Bad: "Returns user object by ID."
  - Good: "Fetch a single user's profile (name, email, status) by their numeric ID. Use when you have a user ID and need any user-attribute information. Do not use to search by email — see `findUserByEmail`."
- **`tags`** — for grouping related operations (e.g. `users`, `billing`). MCP servers use tags to organize tool listings.
- **`parameters`** — every path/query/header parameter has a `description` (also LLM-facing), `required`, and a typed `schema`.
- **`requestBody`** (where applicable) — `description`, `required`, and a `content` schema with at least one example.
- **`responses`** — every documented status code (success + errors) has a `description` and a typed schema. At minimum: 200/201, 400, 401/403, 404, 500. Don't document statuses the API doesn't actually return.
- **`x-mcp-side-effects`** — custom extension. One of `none`, `read-only`, `write`, `destructive`. Lets MCP wrappers decide which operations to gate behind confirmation.

## Required global fields

- `info.title`, `info.version`, `info.description` — `description` should explain what the service is for, in agent-facing terms.
- `servers` — list every environment the spec applies to (dev, staging, prod).
- `components.schemas` — every type used in request/response bodies, named and reusable. No inline schemas more than 3 fields deep.
- `components.securitySchemes` — every auth method (bearer, OAuth2, API key) explicitly defined.

## Naming rules for operationIds

- camelCase, single identifier (no spaces, no hyphens).
- Verb + noun: `getX`, `listX`, `createX`, `updateX`, `replaceX`, `deleteX`, `cancelX`, `searchX`.
- Plural for collections (`listOrders`), singular for items (`getOrder`).
- Scope when ambiguous: `listOrdersForUser`, `getInvoicePdf`.
- One operationId per route+method. Never two operations with the same id.

## Sync with code

- If the framework supports it (FastAPI, NestJS, drf-spectacular, etc.), generate the spec from code rather than hand-writing it — and configure the framework to emit the MCP-required fields. Hand-written specs drift.
- Add a CI check that fails if the deployed spec doesn't match the committed spec.

## What this skill does NOT do

- Replace REST design review. Bad endpoints documented well are still bad endpoints. Run an ADR if route design is non-obvious.
- Generate the MCP server itself. This skill produces a spec good enough for one — the MCP server is separate tooling.

## Output

`docs/api/openapi.yaml` (or per-service `docs/api/<service>.openapi.yaml`).

## Template

See [openapi.yaml](../../../templates/openapi.yaml) for a minimal MCP-ready starter.
