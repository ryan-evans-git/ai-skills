---
name: drawio-architect
description: Create and maintain draw.io (.drawio) architecture diagrams for the project. Use when starting a new project, when the system structure changes (new service, new integration, new data flow), or when the user says "diagram this", "architecture diagram", "draw.io", "update the diagram". Diagrams live under docs/architecture/.
---

# drawio-architect

## Purpose

Every project has at least one current architecture diagram in draw.io format (`.drawio` XML, also viewable as `.drawio.svg`). The diagram is the fastest onboarding artifact and the most-skipped one. This skill keeps it current.

## When to use

- Starting a new project — create `docs/architecture/system.drawio`.
- A structural change is being made: new service, new external integration, new data flow, new auth boundary, new queue/topic, new datastore.
- User says: "diagram this", "architecture diagram", "draw.io", "update the diagram", "show me the system".
- A PRD or ADR describes a new component — the diagram needs to reflect it.

## Process

1. **Confirm `docs/architecture/` exists.** If not, run `docs-directory-keeper` first.
2. **Identify or create the right diagram**:
   - `system.drawio` — top-level: all services, external systems, data stores, users.
   - `<area>.drawio` — focused diagrams for a subsystem (auth, ingestion, etc.) when the top-level gets too dense.
   - Don't keep more than one diagram per concern.
3. **Edit the .drawio XML directly.** draw.io files are plain XML and can be edited with Edit/Write. For non-trivial changes, generate the XML using the conventions below and tell the user how to open it in draw.io for review.
4. **Follow the style guide**:
   - **Left-to-right** data flow when possible.
   - **External systems** at the edges, in dashed/grey boxes.
   - **Data stores** as cylinders or labeled DB shapes.
   - **Async** (queues, topics, events) drawn with dashed arrows.
   - **Sync** (HTTP, gRPC) drawn with solid arrows.
   - **Auth boundaries** drawn as dashed regions.
   - **Every arrow labeled** with the protocol or event name.
   - **No more than ~12 top-level nodes** per diagram. If you need more, split.
5. **Also export a `.drawio.svg`** alongside the source — many viewers (GitHub, IDEs) render SVG inline but not draw.io. If `drawio-desktop` is available, export it; otherwise note in `docs/architecture/README.md` that SVG export is manual.
6. **Update `docs/architecture/README.md`** with a one-line description of every diagram in the folder.
7. **Link the diagram** from `docs/README.md` and from any ADR that drove the change.

## Minimal starter diagram

A blank `.drawio` to start from lives at `templates/architecture.drawio`. Copy it, then iterate.

## What this skill does NOT do

- Replace prose architecture docs. The diagram complements the README/ADRs, doesn't replace them.
- Diagram implementation details (class hierarchies, internal function calls). It's a system diagram.

## Output

`docs/architecture/system.drawio` (and optionally `.drawio.svg`).

## Template

See [architecture.drawio](../../../templates/architecture.drawio).
