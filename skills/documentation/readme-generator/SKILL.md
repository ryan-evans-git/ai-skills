---
name: readme-generator
description: Generate or refresh a project README with a consistent structure — what it is, why it exists, how to install, how to run, project layout, contributing. Use when starting a new project, when the README is missing or stale, or when the user says "write a README", "update the README", "what does this repo do".
---

# readme-generator

## Purpose

A README that answers, in this order: *what is this, why does it exist, how do I run it, where's everything, how do I contribute.* No marketing fluff, no badges-as-decoration, no AI-shaped emoji headers.

## When to use

- Starting a new project.
- README missing or only contains `# project-name`.
- User says: "write a README", "update the README", "what does this repo do".
- Project structure changed significantly and the README's layout section is stale.

## Process

1. **Read the project** before writing:
   - `package.json` / `pyproject.toml` / `Cargo.toml` for name, deps, scripts.
   - Entry points and main routes/commands.
   - `docs/architecture/` if it exists.
   - Existing README — preserve any user-written sections; replace only the parts you can verify.
2. **Draft sections in this order**:
   - **Title + one-line description.**
   - **What it is** — 2–4 sentences. What problem does this solve, for whom.
   - **Why it exists** — 1–2 sentences of motivation. Skip if obvious.
   - **Status** — alpha / beta / stable, plus any "not for production" caveats.
   - **Getting started** — copy-pasteable install + run. Test it mentally; if a command would fail on a fresh clone, it doesn't belong here.
   - **Project layout** — tree showing top-level dirs with one-line descriptions. Use the actual structure, not aspirational.
   - **Common commands / scripts** — test, lint, build, deploy. Cite the script source (Makefile, package.json scripts, etc.).
   - **Architecture** — link to `docs/architecture/system.drawio` and `docs/decisions/` rather than restating.
   - **Contributing** — link to `docs/contributing.md` if present, otherwise a 2–3 line summary.
   - **License.**
3. **Don't add** without evidence:
   - Badges (CI, coverage, license) — only if the underlying services exist and the badge links are real.
   - Performance claims, benchmarks, comparisons.
   - Roadmaps. Those go in `docs/plans/`.
4. **Write the README** and double-check every command, path, and file reference exists.

## Voice

- Direct, second-person. "Run X" not "Users should run X".
- Avoid emoji headers and decorative dividers.
- No "Welcome!" or "Thanks for checking us out!" preambles.

## What this skill does NOT do

- Generate marketing copy.
- Document every config option exhaustively — link to a `docs/configuration.md` for that.
- Replace `docs/onboarding.md` for new team members; the README is for any visitor, onboarding is for joiners.

## Output

`README.md` at the project root.
