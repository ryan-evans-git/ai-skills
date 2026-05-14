---
name: incident-postmortem
description: Author a blameless postmortem for a production incident — timeline, root cause, contributing factors, action items. Use when there has been a user-visible outage, data issue, or significant degradation, or when the user says "postmortem", "writeup the incident", "what went wrong on X".
---

# incident-postmortem

## Purpose

Make incidents into durable learning. Blameless, specific, action-oriented. Lives under `docs/postmortems/` so future engineers can search for "have we seen this before" and find a real answer.

## When to use

- A production incident occurred (outage, degradation, data issue, security event, customer-impacting bug in prod).
- User says: "postmortem", "writeup the incident", "what went wrong on X", "RCA for X".

## Process

1. **Gather facts before writing**:
   - Alert / detection time and source.
   - User-impact window: start, end, scope.
   - Mitigation: what was done, when, by whom.
   - Logs, dashboards, code commits in the window.
   - Customer reports.
2. **Decide severity** based on team conventions: SEV-1 / SEV-2 / SEV-3. Note it at the top.
3. **Choose filename**: `docs/postmortems/YYYY-MM-DD-short-incident-name.md`.
4. **Draft the postmortem** with sections:
   - **Summary** — 2–4 sentences any exec or new hire can understand.
   - **Impact** — who was affected, how, for how long, quantified where possible (X% of users, Y requests failed, $Z revenue impact).
   - **Timeline** — bullets in UTC, every notable event. Detection, escalation, mitigations attempted (working AND not), resolution, all-clear.
   - **Root cause** — the actual underlying issue.
   - **Trigger** — what made it surface at this moment.
   - **Contributing factors** — things that made it worse, slower to detect, or harder to fix (monitoring gaps, alert noise, runbook gaps, on-call confusion).
   - **What went well** — keep doing.
   - **What went poorly** — change.
   - **Lessons** — generalizable insights.
   - **Action items** — every action has owner + due date + linked story. No anonymous "we should".
5. **Stay blameless.** Critique systems, processes, monitoring, defaults — not people. Replace names with roles where possible.
6. **Link the postmortem from**:
   - `docs/progress/CURRENT.md`.
   - The next sprint retro.
   - Any ADR or process change that follows from it.
7. **File action items as stories** on `docs/plans/CURRENT.md` (or a follow-up plan).

## Action item discipline

- Each action has: **what**, **why** (which contributing factor it addresses), **owner**, **due date**, **link to story**.
- Track them to completion. A postmortem with unaddressed action items 6 months later means the incident will repeat — surface it.

## Output

`docs/postmortems/YYYY-MM-DD-short-incident-name.md`

## Template

See [POSTMORTEM.md](../../../templates/POSTMORTEM.md).
