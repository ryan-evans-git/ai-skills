---
name: onboarding-walkthrough
description: Create or maintain docs/onboarding.md — a getting-started doc for new team members joining the project, covering setup, key concepts, where things are, who owns what. Use when the user says "onboarding doc", "for new joiners", "getting started guide", or when the doc is missing/stale and someone new is joining.
---

# onboarding-walkthrough

## Purpose

Get a new engineer (or QA, or agent) productive within day one. Onboarding is the README for people who are *staying*, not just visiting — deeper, opinion-having, and ruthlessly current.

## When to use

- New team member joining and there's no onboarding doc, or the existing one hasn't been touched in months.
- User says: "onboarding doc", "for new joiners", "getting started guide", "what do new people need to know".
- Significant change to setup or architecture invalidates the existing onboarding doc.

## Process

1. **Locate** or create `docs/onboarding.md`. One file for the whole project.
2. **Draft sections**, each as short as possible:
   - **First day — get it running.**
     - Required tooling versions (state exact versions, not "latest").
     - Cloning instructions, including submodules / LFS if any.
     - Local setup commands, in order, copy-pasteable.
     - How to seed local data.
     - How to run tests.
     - How to run the app locally end-to-end.
     - Common first-day errors and their fixes.
   - **Key concepts.**
     - Domain glossary (3–10 terms) — the words this team uses that an outsider wouldn't recognize.
     - System overview — link to `docs/architecture/system.drawio` rather than duplicating.
     - Important invariants and constraints (e.g. "all money is stored in cents as integers", "tenant ID is required on every query").
   - **Where things are.**
     - Map of top-level directories with one-line descriptions.
     - Where to find: PRDs, plans, retros, ADRs, postmortems (link to `docs-directory-keeper`-style layout).
     - Where logs / dashboards / metrics live (link the actual URLs).
   - **How we work.**
     - Branching / PR conventions.
     - TDD expectation (link `tdd-enforcer`).
     - Phase / story workflow (link `phased-implementation`).
     - Code review norms.
   - **People & ownership.**
     - Who owns what area (use roles, not just names, so the doc ages better).
     - Who's the right reviewer for X.
     - Where to ask for help.
   - **Common tasks** — short recipes for things every team member will need to do (add a route, add a migration, add a feature flag, deploy a hotfix).
3. **Verify every command** by reading the source, not from memory. If a command is in CI or a Makefile, cite where.
4. **Date the doc** at the top: `Last updated: YYYY-MM-DD`. Stale doc is worse than no doc — if you can't verify, mark a section `[STALE — verify before trusting]`.

## What this skill does NOT do

- Replace pairing. The doc gets someone unblocked; humans get them productive.
- Become a wiki for everything. If a section grows past one screen, link out to a dedicated `docs/...md`.

## Output

`docs/onboarding.md`
