---
name: auth-checklist
description: Verify that every HTTP route enforces authentication and authorization — by walking the OpenAPI spec and the actual route handlers. Use when adding new routes, before a release, when the user says "auth coverage", "is everything protected", "permissions check", "RBAC audit".
---

# auth-checklist

## Purpose

The most common access-control bug is "we forgot to add a check on this one endpoint." This skill audits coverage systematically — every route, every method, every role.

## When to use

- New endpoints added since the last audit.
- Before a release.
- After role / permission model changes.
- User says: "auth coverage", "is everything protected", "permissions check", "RBAC audit", "missing auth".

## Process

1. **Source of truth**: the OpenAPI spec (`docs/api/openapi.yaml`) plus the actual route handlers. If they disagree, the code wins — and the spec must be updated.

2. **Build the coverage matrix** by walking every operation in the spec:

   | Path | Method | operationId | authn | authz (roles) | resource ownership | rate limit | Notes |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | `/users/{id}` | GET | getUserById | required | admin OR self | ownership-checked | yes | |

3. **For each row, verify**:
   - **authn**: spec declares a security requirement (`security: [bearerAuth: []]`) AND the handler enforces it (middleware / decorator / framework guard).
   - **authz**: the role / permission required is documented AND enforced. "Authenticated user" is not authz — every action should have a role or capability gate, even if it's `user`.
   - **resource ownership** (for `:id`-style routes): the handler checks that the authenticated user owns / can access the specific resource. Missing this is the classic IDOR.
   - **rate limit**: state-changing endpoints and auth-sensitive endpoints (login, password reset, signup, MFA challenge) have rate limits.
   - **Public exceptions**: any route explicitly intended to be unauthenticated (health checks, public read APIs) is annotated as such in the spec and intentional in code.

4. **Cross-check role definitions**:
   - List every role / permission used in any endpoint.
   - Each role has a single definition source (not redefined per service).
   - Role grants & revokes are auditable.

5. **Verify "deny by default"** at the framework level:
   - There is a global authn middleware / guard.
   - Routes opt OUT of auth explicitly (allowlist), not opt IN. Opt-in models are how "we forgot" happens.

6. **Output** `docs/security/auth-coverage-YYYY-MM-DD.md`:
   - The full matrix.
   - **Findings** by severity:
     - **Critical**: any route missing authn that should have it.
     - **High**: missing authz, missing ownership check on `:id` routes, missing rate limit on auth-sensitive routes.
     - **Medium**: undocumented public routes, role-definition duplication.
     - **Low**: spec-vs-code drift that doesn't change security posture.
   - Action items onto `docs/plans/CURRENT.md`.

## What this skill does NOT do

- Test for actual bypasses dynamically (DAST). It audits the surface area; pen-testing is separate.
- Audit non-HTTP entry points. Background jobs / webhooks / queue consumers need a separate review — note them as out-of-scope at the top of the report.

## Output

`docs/security/auth-coverage-YYYY-MM-DD.md`
