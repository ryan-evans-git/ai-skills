# Postmortem: <Incident name>

- **Severity:** SEV-1 | SEV-2 | SEV-3
- **Date of incident:** YYYY-MM-DD
- **Duration of user impact:** HH:MM – HH:MM UTC (<duration>)
- **Author:** <name>
- **Status:** Draft | Reviewed | Action items in progress | Closed
- **Related:** runbook, dashboards, related ADRs

## Summary

<2–4 sentences. Any exec or new hire can understand what happened.>

## Impact

<Who was affected, how, for how long. Quantify: X% of users, Y requests failed, $Z revenue impact.>

## Timeline (UTC)

| Time | Event |
| --- | --- |
| HH:MM | <event> |
| HH:MM | Detection: <how, by whom> |
| HH:MM | Escalation to <on-call / role> |
| HH:MM | Mitigation attempt: <what> — <worked / didn't, why> |
| HH:MM | Resolution / all-clear |

## Root cause

<The actual underlying problem.>

## Trigger

<What made it surface at this moment.>

## Contributing factors

<Things that made it worse, slower to detect, or harder to fix. Monitoring gaps, alert noise, runbook gaps, on-call confusion, documentation gaps.>

- ...

## What went well

- ...

## What went poorly

- ...

## Lessons

<Generalizable insights, beyond this specific incident.>

- ...

## Action items

| Action | Why (which factor it addresses) | Owner | Due | Story link |
| --- | --- | --- | --- | --- |
| <action> | <factor> | <role/name> | YYYY-MM-DD | [link] |

## Blameless reminder

This document critiques systems, processes, monitoring, and defaults — not people. Any individual making the same decisions with the same information would have arrived at the same outcome.
