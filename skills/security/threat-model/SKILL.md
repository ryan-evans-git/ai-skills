---
name: threat-model
description: Produce a STRIDE-style threat model for a new feature, service, or significant architectural change. Use when starting design on anything that touches auth, payment, PII, third-party integrations, or new data stores — or when the user says "threat model", "STRIDE", "what could go wrong", "security design". Output is a structured doc under docs/security/threat-models/.
---

# threat-model

## Purpose

Make security risks visible at design time, before code is written. Threat models live alongside ADRs and PRDs — they're an input to architectural decisions, not a checkbox.

## When to use

- A PRD or ADR introduces: a new external integration, a new auth flow, a new data store, a new public endpoint, payment / financial / PII handling.
- User says: "threat model", "STRIDE", "what could go wrong", "security design", "attack surface".
- Before significant refactors that change trust boundaries.

## STRIDE checklist (per data flow / trust boundary)

| Letter | Threat | Asks |
| --- | --- | --- |
| **S** | Spoofing | Can an attacker impersonate a user / service / token? |
| **T** | Tampering | Can data be modified in transit, at rest, or in cache? |
| **R** | Repudiation | Can a user deny taking an action; do we have audit trail? |
| **I** | Information disclosure | Can data leak via logs, error messages, side channels, or unauthorized access? |
| **D** | Denial of service | Can the system be overwhelmed; what's the blast radius of one bad caller? |
| **E** | Elevation of privilege | Can a user gain capabilities they shouldn't have? |

## Process

1. **Read the design artifact** — PRD, ADR, or system diagram (`docs/architecture/system.drawio`).
2. **Identify assets** — what's valuable: user data (which fields, classification), money, credentials, integrations, reputation.
3. **Draw or reference a data flow diagram** — components, data flows, trust boundaries (the lines where data crosses from one trust level to another). If the system diagram already shows this, link it.
4. **For each trust boundary**, walk STRIDE. Write down threats that are *plausible*, not all conceivable threats.
5. **For each threat, score** with a simple model:
   - **Likelihood:** Low / Medium / High (given current defenses and realistic attacker).
   - **Impact:** Low / Medium / High (worst plausible outcome).
   - **Risk:** Likelihood × Impact bucketed to Low / Medium / High / Critical.
6. **For each Medium+ risk**, propose a mitigation. Categorize:
   - **Eliminate** (remove the feature / data flow).
   - **Mitigate** (controls reduce likelihood or impact).
   - **Transfer** (e.g. push to a third party with stronger guarantees).
   - **Accept** (with a named owner and a reason).
7. **State residual risk** — what remains after mitigations.
8. **List follow-up stories** to add to `docs/plans/CURRENT.md` for any mitigation that requires implementation work.
9. **Write the doc** to `docs/security/threat-models/YYYY-MM-DD-feature-name.md` using `templates/THREAT-MODEL.md`.
10. **Link from** the originating PRD/ADR and from `docs/progress/CURRENT.md`.

## What good threat models look like

- **Specific.** "An attacker who steals a session cookie can perform any action as the user" beats "auth could be bypassed."
- **Scoped.** One feature or boundary per doc. Don't try to model the whole system in one pass.
- **Honest.** Note risks even if they're inconvenient. Document accepted risks with a name attached.
- **Actionable.** Every Medium+ risk has a mitigation entry or an explicit acceptance.

## What this skill does NOT do

- Replace a real security review by a security engineer for high-risk changes.
- Replace `security-review` of the actual diff. Threat model = design-time; security-review = code-time.

## Output

`docs/security/threat-models/YYYY-MM-DD-feature-name.md`

## Template

See [THREAT-MODEL.md](../../../templates/THREAT-MODEL.md).
