---
name: adr-writer
description: Capture an Architecture Decision Record (ADR) for a significant technical choice. Use whenever a non-trivial decision is being made — choosing between frameworks, libraries, patterns, data stores, integration approaches, API designs, deployment topologies — or when the user says "ADR", "let's document this decision", "should we use X or Y". Produces a numbered ADR under docs/decisions/.
---

# adr-writer

## Purpose

Make significant technical decisions legible — what was decided, why, what was considered, what we're giving up. ADRs are append-only history; superseded decisions get a follow-up ADR, not an edit.

Lightweight decisions (file structure, naming, in-the-moment design) belong in `decision-log` instead. Use this skill when the decision will outlive any one engineer's memory.

## When to use

- User says: "ADR", "let's document this decision", "should we use X or Y", "what are the tradeoffs".
- A non-trivial decision is being made: framework, library, data store, pattern, integration approach, API design, deployment topology, security model.
- A previous ADR is being superseded.

## Process

1. **Determine the next number.** Look at `docs/decisions/` and find the highest `NNNN-*.md`. Use `NNNN+1`, zero-padded to 4 digits.
2. **Choose a kebab-case title** that names the decision, not the topic: `0007-use-postgres-for-event-store.md`, not `0007-event-storage.md`.
3. **Author the ADR** with sections (Michael Nygard format, plus a few additions):
   - **Status** — Proposed / Accepted / Superseded by ADR-NNNN / Deprecated.
   - **Date.**
   - **Context** — what's the situation, what forces are at play. No solution yet.
   - **Decision** — what we're doing. Active voice: "We will use Postgres for the event store."
   - **Alternatives considered** — at least two, each with why-not. (An ADR with no alternatives is a press release.)
   - **Consequences** — positive AND negative, including what becomes harder.
   - **Out of scope** — explicitly not addressed by this decision.
4. **If superseding** an existing ADR, update the old ADR's status to `Superseded by ADR-NNNN` (this is the only retroactive edit allowed).
5. **Write the ADR** using `templates/ADR.md`.
6. **Link from `docs/progress/CURRENT.md`** and from any related plan/PRD.

## Output

`docs/decisions/NNNN-decision-title.md`

## Template

See [ADR.md](../../../templates/ADR.md).
