---
name: service-boundaries
description: Decide whether to split a service, merge services, or keep an extraction inside the current process — using a deliberate set of forces (team ownership, deploy cadence, data ownership, scaling profile) rather than micro-services-by-default. Use when proposing a new service, when an existing one is getting too big, or when the user says "should this be its own service", "split this up", "extract this", "monolith vs microservice".
---

# service-boundaries

## Purpose

The cost of a service is not the code — it's the operational surface (deploy pipeline, monitoring, on-call, network calls, distributed-system bugs). This skill resists "new feature, new service" reflex and only extracts when the forces actually warrant it.

## When to use

- Proposing a new service in a PRD/ADR.
- An existing service has grown big and someone says "should we split this?"
- A new domain is being added.
- User says: "should this be its own service", "split this up", "extract this", "monolith vs microservice", "service boundary".

## The forces (extract when *most* are true)

| Force | Pull to extract | Pull to keep together |
| --- | --- | --- |
| **Team ownership** | A different team will own it long-term | Same team owns both |
| **Deploy cadence** | This component ships multiple times/day; the rest weekly | Both ship together |
| **Scaling profile** | Wildly different (e.g. 100x more CPU per request) | Similar |
| **Failure isolation** | An outage here MUST not take down the rest | Coupled failure is OK |
| **Tech stack** | Genuinely needs a different language/runtime | Same stack serves both |
| **Data ownership** | Owns its own write-path data others should NOT touch directly | Shares the same write-path data |
| **Regulation / blast radius** | Subject to different compliance regime (e.g. PCI) | Same regime |
| **Team size** | More than 1 Pizza team would work on it independently | One team can own |

**Heuristic**: if fewer than ~3–4 forces clearly point to extraction, keep it together as a module / package within the existing service. Reverse the decision later if forces strengthen.

## Costs you take on per service

Every service adds, minimum:
- A deploy pipeline.
- A CI matrix entry.
- Metrics, logs, traces, dashboards.
- On-call rotation entry.
- An entry in the service map (`service-map`).
- A network call (latency + failure mode).
- A contract that has to be maintained (`api-contract-evolution`).
- Auth / authz setup.
- Secret management.

Multiply by N services to estimate ongoing cost.

## Process

1. **Capture the proposed boundary** in one paragraph: what's on each side, and why this seam?
2. **Score the forces** above. List which point to extract, which to keep together. Be specific (cite real evidence).
3. **Decide**:
   - **Extract** if most forces point that way AND the team is willing to absorb the costs above.
   - **Module/package within current service** if forces are weak or mixed. Most "should we split this?" answers are this.
   - **Defer** if forces are strong but the team hasn't sized the cost; revisit when there's capacity.
4. **Write an ADR** (`adr-writer`) capturing the decision, the forces, and the consequences.
5. **If extracting**:
   - Draft the contract first (`api-design`, `swagger-openapi-spec`).
   - Plan the data ownership transition (who owns which tables).
   - Plan the deploy / migration order (strangler pattern is the default — both old and new in production, traffic shifts gradually).
   - Update `service-map`.
6. **If keeping together but isolating** as a module:
   - Define a clear internal interface (function signatures, no shared mutable state).
   - Move it to its own package / directory.
   - Add a comment / `OWNERS` file naming who maintains it.
   - Periodically revisit — internal modules that grow strong forces become candidates for extraction.

## Anti-patterns

- **Micro-services by default.** "Each feature gets a service" with no force analysis. Operational cost compounds.
- **Big-ball-of-mud by default.** Refusing to extract even when forces strongly support it ("we'll just keep adding code").
- **Extracting based on code organization alone.** Modules solve that. Services solve different problems.
- **Extracting before the contract is stable.** A new service with a thrashing contract creates churn for everyone.
- **Distributed monolith.** Multiple services that deploy together, share a DB, and can't be released independently. You took the costs without the benefits.

## What this skill does NOT do

- Decide the specific extraction sequence — that's a plan / migration ADR.
- Design the new contract itself — see `api-design`.

## Output

An ADR capturing the boundary decision, force analysis, and consequences.
