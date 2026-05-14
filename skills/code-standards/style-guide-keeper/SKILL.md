---
name: style-guide-keeper
description: Create and maintain docs/standards/style-guide.md — the team's source of truth for code style decisions per language. Use when starting a new project, when a style debate needs to be settled, or when the user says "style guide", "code style", "formatting rules", "how should we write X in this codebase".
---

# style-guide-keeper

## Purpose

Avoid re-litigating style in every PR. The style guide is a thin, opinionated doc that points at an authoritative external guide per language and lists ONLY the project's deviations and additions. Don't rewrite PEP 8 or Airbnb in your own words.

## When to use

- Starting a new project.
- A style debate has come up in PR review and needs to be made durable.
- User says: "style guide", "code style", "formatting rules", "how should we write X".

## Process

1. **Read the project** to detect languages in use.
2. **For each language, pick the authoritative external guide** and pin a version:
   - Python: [PEP 8](https://peps.python.org/pep-0008/) + project formatter (ruff / black).
   - TypeScript / JavaScript: [Google TS style](https://google.github.io/styleguide/tsguide.html) or [Airbnb JS](https://github.com/airbnb/javascript) + project formatter (prettier / biome).
   - Rust: rustfmt defaults + Clippy.
   - Go: gofmt + golangci-lint config.
   - Java: Google Java style.
3. **Compose `docs/standards/style-guide.md`** with this structure (template below). One section per language, each section: pointer to external guide, project deviations, formatter config link.
4. **Cross-link** with `linter-config`, `naming-conventions`, `error-handling-standards`, `logging-standards`, `typing-strictness`.
5. **Resist scope creep.** The style guide is for syntax, layout, and small-scale conventions. Architecture lives in ADRs; error handling, logging, naming, and typing each have their own dedicated doc.

## Template structure

```markdown
# Style guide

Last updated: YYYY-MM-DD
Enforced via: <linter / formatter — link to config>

## Python

**Base:** PEP 8.
**Formatter:** ruff format (see `pyproject.toml`).
**Linter:** ruff (see `pyproject.toml`).

### Project deviations
- Max line length: 100 (PEP 8 suggests 79).
- ...

### Project additions
- Type hints required on all public functions (see `typing-strictness`).
- ...

## TypeScript

**Base:** <Google TS style | Airbnb>.
**Formatter:** prettier (see `.prettierrc`).
**Linter:** ESLint (see `.eslintrc`).

### Project deviations
- ...

### Project additions
- ...

## <other language>
...
```

## Rules of thumb

- **No "preference" entries.** Every rule has a reason in one line: consistency, performance, safety, readability with X tool.
- **No rules the linter can't enforce** unless they're unenforceable in principle (then they belong here as discipline).
- **If a rule and the linter disagree, fix the linter** so the guide stays accurate.

## What this skill does NOT do

- Restate PEP 8 / Airbnb / etc. in your own words. Link them.
- Cover architecture, error handling, logging, naming, typing — those have dedicated skills.

## Output

`docs/standards/style-guide.md`
