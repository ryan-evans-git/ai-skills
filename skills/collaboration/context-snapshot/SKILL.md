---
name: context-snapshot
description: Capture a structured snapshot of the current state of the work — what's been explored, what's been decided, what was tried and rejected, where current files stand — into docs/progress/ so a future agent or human can pick up without rediscovering everything. Use when the user says "snapshot", "save state", "checkpoint", "summarize what we've done", or mid-session when context is heavy.
---

# context-snapshot

## Purpose

Different from `handoff-prep` — a handoff says "here's what to do next." A snapshot says "here's what we've learned, including paths we tried and rejected, so you don't repeat them."

Snapshots compound: read enough of them and a future agent has the same intuition the previous agent built up.

## When to use

- User says: "snapshot", "save state", "checkpoint", "summarize what we've done", "capture context".
- Mid-session when context is getting heavy and a future you (or another agent) might pick this up.
- After a long investigation where several approaches were tried.
- Before swapping models or starting a fresh session.

## Process

1. **Filename**: `docs/progress/snapshots/YYYY-MM-DD-HHMM-topic.md`.
2. **Capture, in order**:
   - **What we were trying to do** — the goal, in one paragraph. Reference the active story.
   - **What we know now that we didn't at the start** — facts learned about the codebase, the bug, the constraints. Cite files / line numbers.
   - **What we tried that worked** — approaches that produced progress, with PR/commit links.
   - **What we tried that didn't work, and why** — the dead ends. Be specific about *why* it didn't work, so the future agent doesn't repeat.
   - **What we explicitly didn't try, and why** — paths considered and ruled out.
   - **Current state of files** — `git status` summary, what's committed vs. uncommitted, what's in-progress.
   - **Open questions** — what we still don't know.
   - **Working hypothesis** — current best guess of the right path forward (and confidence level).
3. **Link from `docs/progress/CURRENT.md`** so it's discoverable.
4. **Commit the snapshot** — snapshots are versioned artifacts, like ADRs.

## What this skill does NOT do

- Make decisions. A snapshot describes the state; a decision belongs in an ADR or the decision-log.
- Replace `handoff-prep`. Snapshots are richer and less action-oriented; handoffs are sharper and more actionable.

## What good snapshots look like

- Concrete. "We confirmed via experiment Z that hypothesis Y is false because of evidence X."
- Honest about uncertainty.
- Specific about what *not* to do. The most valuable information is "we already tried that."

## Output

`docs/progress/snapshots/YYYY-MM-DD-HHMM-topic.md`
