---
name: linter-config
description: Pick, configure, and document linters and formatters for each language in the project — ruff, prettier, ESLint, biome, clippy, golangci-lint, etc. Use when starting a new project, when lint rules need to change, or when the user says "linter", "formatter", "pre-commit", "ruff", "prettier", "lint config".
---

# linter-config

## Purpose

Run the linter and formatter as a first-class part of every commit. Decisions about which rules apply belong in committed config, not in heads. Disabled rules are explicitly listed with reasons so future-you doesn't re-enable something on purpose-of-disabling that's been lost.

## When to use

- Starting a new project.
- Adding a new language to the project.
- User says: "linter", "formatter", "pre-commit", "ruff", "prettier", "lint config", "what rules are off".
- Lint rules need to be added/removed.

## Recommended toolchain per language

| Language | Formatter | Linter | Config file |
| --- | --- | --- | --- |
| **Python** | `ruff format` | `ruff` | `pyproject.toml` `[tool.ruff]` |
| **TypeScript / JS** | `prettier` or `biome format` | `eslint` or `biome lint` | `.prettierrc`, `eslint.config.js` |
| **Rust** | `rustfmt` | `clippy` | `rustfmt.toml`, `clippy.toml` |
| **Go** | `gofmt` / `goimports` | `golangci-lint` | `.golangci.yml` |
| **Markdown** | `prettier` / `dprint` | `markdownlint` | `.markdownlint.jsonc` |
| **YAML** | `prettier` | `yamllint` | `.yamllint` |

Prefer fewer, more comprehensive tools (ruff covers most Python lints; biome covers most JS/TS formatting+linting).

## Process

1. **Pick the toolchain.** Match the team's existing tools if any; otherwise use the table above.
2. **Commit config files** at the repo root. Don't rely on tool defaults — make the rules explicit even if they're the defaults.
3. **Author `docs/standards/linting.md`** with:
   - Which tools are used per language.
   - How to run them locally (`make lint`, `npm run lint`, etc.).
   - Pre-commit hook setup.
   - CI integration.
   - **A list of disabled / overridden rules**, each with a one-line reason.
4. **Wire pre-commit hooks** (`pre-commit` framework or husky for JS) so lint+format run on every commit. Hook can fail the commit on lint errors but only auto-format if the dev opts in (don't surprise people).
5. **Wire CI** to run the linters as required checks. Same versions as local; pin in lockfiles or `pyproject.toml` / `package.json`.
6. **Cross-link** with `style-guide-keeper`, `error-handling-standards` (lint rules that enforce error handling), and `typing-strictness` (type checker is conceptually a linter).

## Rules of thumb

- **Pin tool versions** — formatter version drift is a frequent source of churn-only diffs.
- **Format on save in IDEs** so devs never argue about formatting.
- **One source of truth per rule.** If `prettier` formats and `eslint` also has a formatting rule, turn off the eslint rule.
- **Auto-fix in CI is OK locally; in CI it should fail** — auto-fixes in CI mean a dev committed un-linted code.
- **Lint config changes need a reason.** When disabling a rule, the commit message and the `linting.md` doc both explain why.

## Anti-patterns

- `# noqa` / `// eslint-disable` without a reason in the same line/comment.
- Disabling a rule project-wide because one file is noncompliant — fix the file or scope the disable.
- Two competing formatters that fight each other on save.
- A `.editorconfig` that says one thing and the formatter that says another.

## Pre-commit hook example (Python + Markdown)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.41.0
    hooks:
      - id: markdownlint
```

## Output

- Tool config files at the repo root (e.g. `pyproject.toml`, `.eslintrc`, `.prettierrc`).
- `.pre-commit-config.yaml` if using pre-commit.
- `docs/standards/linting.md`.
