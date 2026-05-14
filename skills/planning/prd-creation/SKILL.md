---
name: prd-creation
description: Author a Product Requirements Document for a new feature, epic, or product. Use whenever the user asks for a PRD, says "let's spec out X", proposes a new feature without a written brief, or asks to formalize a loose idea before implementation. Produces a markdown PRD under docs/prds/.
---

# prd-creation

## Purpose

Turn a loose feature idea into a written PRD that defines the problem, the users, the goals, the non-goals, the success metrics, and the constraints — before any code is written or any plan is broken down.

## When to use

- User says: "write a PRD", "spec this out", "we need a PRD for X", "let's formalize this", "what should we build for X".
- User describes a feature in conversation without a written brief.
- Any time `story-breakdown` is requested but no PRD exists yet — author the PRD first.

## Process

1. **Locate or create the PRD directory.** Ensure `docs/prds/` exists. If not, create it (and create the rest of the standard `docs/` tree if missing — see `docs-directory-keeper`).
2. **Choose a filename.** Format: `YYYY-MM-DD-short-kebab-case-title.md`. Use today's date.
3. **Gather the information** by reading the conversation and the codebase. If something is genuinely unknowable, write `TODO: clarify with <stakeholder>` rather than guessing — but make a strong reasonable-default first pass before asking the user. Required sections:
   - **Problem** — what's broken / missing / suboptimal today, written from the user's POV.
   - **Users** — who experiences this problem; primary vs. secondary users.
   - **Goals** — what success looks like, in user-visible terms.
   - **Non-goals** — what this explicitly is NOT trying to solve. (Critical — non-goals prevent scope creep.)
   - **Success metrics** — how we'll know it worked. Quantitative where possible.
   - **Constraints** — technical, regulatory, timeline, headcount, integration boundaries.
   - **Open questions** — anything you couldn't resolve, with owner if known.
   - **Out-of-scope ideas** — things mentioned in discussion that we're deferring.
4. **Write the PRD** using `templates/PRD.md` as the structure.
5. **Link it** from `docs/progress/CURRENT.md` so the next session knows it exists.
6. **Don't break down stories or write code in this skill.** When the PRD is approved, trigger `story-breakdown` for the next step.

## Output

`docs/prds/YYYY-MM-DD-feature-name.md`

## Template

See [PRD.md](../../../templates/PRD.md).
