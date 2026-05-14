---
name: integration-contract-tests
description: Add contract tests that verify both sides of an integration agree on the contract — provider-side schema tests that fail when the service drifts, and consumer-side tests that fail when the consumer's expectations drift. Use when integrating with a new dependency, when adding a public API, after a breaking-change incident, or when the user says "contract test", "pact", "consumer-driven", "schema test".
---

# integration-contract-tests

## Purpose

Unit tests prove your code works in isolation. End-to-end tests prove the whole stack works in one configuration. Contract tests fill the gap: they prove the *interface* between two services hasn't drifted, even when each side tests independently and deploys independently.

## When to use

- Adding a new integration (either direction).
- Promoting an internal API to "public" (consumed by other services).
- After a postmortem where one side changed and the other broke.
- User says: "contract test", "pact", "consumer-driven contract", "schema test", "spec test".

## Two flavors — pick the right one

### Schema contract tests (lighter weight)

The contract is the OpenAPI spec / proto / JSON schema. Tests verify each side conforms.

- **Provider side**: a test runs against the running service for each operation in the spec, asserting the actual response matches the schema (status, headers, body shape, types). Tools: `schemathesis` (Python), `dredd`, `openapi-validator`, `spectator` (Ruby).
- **Consumer side**: tests use a mock generated from the spec, so the consumer's tests can never diverge from the documented contract.

**When to use**: most cases. Lower overhead than pact-style, catches most regressions. Required when the contract is OpenAPI/proto.

### Consumer-driven contract tests (heavier, more precise)

Each consumer publishes a "pact" describing what it actually relies on. The provider runs every consumer's pact against itself. Tools: `pact-foundation/pact-*` for many languages, with a Pact Broker for orchestration.

**When to use**: when you have multiple internal consumers with diverging needs, and the OpenAPI spec is too loose to catch real regressions. Worth the operational overhead for high-blast-radius services.

## Process

1. **Decide the flavor** for this integration. Default to schema contract tests; escalate to pact when there are 3+ active consumers with diverging contracts.
2. **Wire it into CI** — contract tests run on every PR and fail the build if the contract is violated.
3. **For provider-side schema tests**:
   - Start the service in CI (or use a docker-compose).
   - Run the schema test tool against the OpenAPI spec.
   - Test every operation, every documented response code.
   - Use property-based testing where the tool supports it (random valid inputs).
4. **For consumer-side**:
   - Tests against the API use a mock derived from the spec, NOT a hand-rolled mock that can drift.
   - Re-fetch / re-generate the mock when the upstream version is bumped.
5. **For pact**:
   - Consumer publishes pact to Pact Broker on every consumer build.
   - Provider verifies all known pacts on every provider build.
   - "Can-i-deploy" check in CI before promoting either side.
6. **Track which contract version was last verified** in `docs/integration/service-map.md` — a row that's been verified recently is far more trustworthy than one that "should" still work.

## What to NOT do with contract tests

- **Don't test business logic** in contract tests. Those are integration / unit tests. Contract tests verify *shape* and *protocol*, not behavior depth.
- **Don't test the dependency.** Their tests are their problem. Test your assumptions about their contract.
- **Don't hand-write the mock.** Generate it from the spec / pact. Hand-rolled mocks drift the day after you write them.
- **Don't skip when failing.** A flaky contract test is hiding a real misalignment — fix the test or fix the contract; don't quarantine.

## Output

- Contract test files committed in the repo, runnable via the standard test command.
- CI wired to run them on every PR.
- `docs/integration/service-map.md` updated with the contract verification date per row.

## What this skill does NOT do

- Replace integration tests with realistic data flows.
- Replace load tests (`load-test-plan`).
- Replace runtime monitoring (you still need to detect drift in production, not just in CI).
