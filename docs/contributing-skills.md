# Contributing a new skill

A skill is a directory under `skills/<category>/<skill-name>/` containing at minimum a `SKILL.md` file.

## SKILL.md format

```markdown
---
name: skill-name
description: One or two sentences describing when this skill should trigger. Be specific — this is what the model uses to decide whether to load the skill.
---

# Skill name

## Purpose
What this skill does, and why a team would want it.

## When to use
Concrete triggers — phrases, file types, situations.

## Process
Step-by-step instructions the model should follow.

## Output
Where the artifact lands (path, filename convention).

## Template
Either inline or a reference to `templates/<file>.md` in the repo root.
```

## Conventions

- **Description is load-bearing.** Skills are triggered by description match. Write the description so a model can tell whether it applies — name the artifacts produced, the file paths involved, and the triggering phrases.
- **Keep skills focused.** One artifact, one workflow per skill. If you find yourself writing "or you can also...", split it.
- **Output paths follow the standard `docs/` layout** — see the table in the root README. Don't invent new top-level directories without updating `docs-directory-keeper`.
- **Templates live in `templates/`** at the repo root and are referenced by skills. Don't duplicate template content inside `SKILL.md`.
- **Stack-agnostic.** Skills should work on any tech stack. If you have stack-specific guidance (Flask, LangChain, etc.), put it in a `skills/stack-<name>/` namespace, not in a general skill.

## After adding a skill

1. Add a one-line entry to [INDEX.md](../INDEX.md) under the right category.
2. If the skill ships hooks, document them under `hooks/` and update `hooks/README.md`.
3. Open a PR with a description that includes an example of the skill being used.
