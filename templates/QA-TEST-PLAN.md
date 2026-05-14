# QA test plan: <Feature name>

- **PRD:** [link]
- **Story:** [link to docs/plans/CURRENT.md]
- **PR:** [link]
- **Author:** <name>
- **Last updated:** YYYY-MM-DD

## Feature summary

<One sentence.>

## Prerequisites

- Environment: <env>
- Accounts / roles: <list>
- Feature flags: <flag = value>
- Seed data: <list or script>

## Test data

| Name | Value / source |
| --- | --- |
| <fixture> | <how to obtain or generate> |

## In scope

- ...

## Out of scope

- ...

## Requirements coverage

| Requirement (from PRD) | Test cases |
| --- | --- |
| <req> | TC-001, TC-002 |

## Test cases

### TC-001 — <title>

- **Type:** manual | automated | both
- **Priority:** P0 | P1 | P2
- **Automated test path:** `path/to/test` *(if applicable)*
- **Preconditions:** ...
- **Steps:**
  1. ...
  2. ...
- **Expected result:** ...
- **Notes:** ...

### TC-002 — <title>

...

## Edge cases

- Empty input
- Max-length input
- Unicode / emoji
- Concurrent users
- Network failure mid-flow
- Auth expiry mid-flow
- Browser back / refresh
- Double-submit

## Regression areas

| Area at risk | Covered by |
| --- | --- |
| ... | TC-... |

## Exit criteria

- All P0 cases pass.
- All P1 cases pass or have an accepted-risk note.
- No new P0/P1 bugs in regression areas.
