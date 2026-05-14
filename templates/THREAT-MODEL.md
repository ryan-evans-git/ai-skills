# Threat model: <Feature / Service name>

- **Status:** Draft | Reviewed | Accepted
- **Date:** YYYY-MM-DD
- **Author:** <name>
- **Reviewers:** <names>
- **Source PRD / ADR:** [link]
- **Related diagrams:** [docs/architecture/...]

## System summary

<One paragraph: what this feature/service does, who calls it, what it depends on.>

## Assets

| Asset | Classification | Why it matters |
| --- | --- | --- |
| <e.g. user PII> | Confidential | GDPR scope; breach → notification |
| <e.g. payment tokens> | Sensitive | Direct financial loss possible |
| ... | | |

## Trust boundaries

<List the lines where data crosses from one trust level to another. Reference the system diagram. Examples:>

- Public internet → load balancer (untrusted → semi-trusted).
- Web → API service (authenticated user → internal service).
- API → Database (service identity → trusted store).
- API → External provider (service → third-party).

## Data flows

<Bullet list of significant data flows that cross boundaries. Each: source → sink, what data, sync/async, encryption.>

- ...

## STRIDE walk

For each trust boundary, plausible threats:

### Boundary: <name>

| ID | Threat | STRIDE | Likelihood | Impact | Risk |
| --- | --- | --- | --- | --- | --- |
| T1 | <e.g. attacker forges a session cookie> | S | M | H | High |
| T2 | <e.g. SQL injection via search field> | T | L | H | Medium |

Repeat per boundary.

## Mitigations

| Threat ID | Mitigation | Type (Eliminate / Mitigate / Transfer / Accept) | Owner | Status |
| --- | --- | --- | --- | --- |
| T1 | Bind sessions to client fingerprint + IP-class | Mitigate | <name> | Planned |
| T2 | All queries parameterized; lint rule added | Mitigate | <name> | Implemented |

## Residual risk

<After mitigations, what risk remains? Explicit accept-risk notes here, each with a named owner.>

- ...

## Out of scope

<What this threat model deliberately does NOT cover, and why.>

- ...

## Follow-ups

<Action items to add to docs/plans/CURRENT.md.>

- [ ] ...
