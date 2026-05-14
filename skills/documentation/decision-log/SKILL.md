---
name: decision-log
description: Append a one-line entry to a lightweight decision log for decisions that don't merit a full ADR — choices made in passing, conventions adopted, tools picked. Use when a small but real decision is made: file naming, library choice, default values, formatting conventions. Output appends to docs/decisions/log.md.
---

# decision-log

## Purpose

Most decisions don't deserve an ADR but they shouldn't be invisible either. The decision log is an append-only, one-line-per-entry record of "we decided X today because Y." Future engineers stop asking "why is this like this" because the answer is one grep away.

Use `adr-writer` for architecturally-significant decisions. Use this skill for everything else worth recording.

## When to use

- A decision is made in passing — convention, default, tool choice, naming pattern.
- User says: "let's go with X", "decided to use Y", "we'll do it this way", "noting that".
- A choice gets debated and resolved, even briefly.

## Process

1. **Confirm `docs/decisions/log.md` exists.** If not, create it with a header.
2. **Append one line** in this format:

   ```
   - YYYY-MM-DD — <decision>. (Reason: <why>. <Optional: link to context>.)
   ```

   Example:

   ```
   - 2026-05-14 — Use httpx over requests for new HTTP clients. (Reason: built-in async support, consistent API across sync/async paths.)
   - 2026-05-14 — Default pagination size = 50. (Reason: matches existing endpoints; reviewed in PR #142.)
   ```
3. **One line per decision.** If you want more space than one line, you probably want an ADR — escalate.
4. **Newest at the bottom.** Append-only. Don't reorder, don't edit prior entries (decisions can be superseded by a new entry, not by editing the old one).

## What this skill does NOT do

- Replace ADRs for significant decisions. If you find yourself writing a paragraph, stop and run `adr-writer` instead.
- Track to-dos or action items. Use the plan for those.

## Output

Appended line in `docs/decisions/log.md`.
