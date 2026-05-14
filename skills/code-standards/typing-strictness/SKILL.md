---
name: typing-strictness
description: Enable and maintain strict type-checking — mypy --strict / pyright strict, TypeScript strict, Rust deny(warnings), etc. Use when starting a new project, when retrofitting types onto an existing codebase, or when the user says "strict types", "mypy", "pyright", "typescript strict", "type coverage".
---

# typing-strictness

## Purpose

Strong types catch a class of bugs at edit time that would otherwise need tests. This skill sets up strict type checking for the project, documents exceptions, and makes type coverage visible.

## When to use

- Starting a new project.
- User says: "strict types", "mypy", "pyright", "typescript strict", "any types", "type coverage", "tighten types".
- Retrofitting types onto a partially-typed codebase (do this gradually — see below).

## Process

### Greenfield project

1. **Pick the checker and configure for strict mode:**
   - **Python** — pyright in strict mode, or mypy with `strict = True` in `pyproject.toml`. Pyright is generally faster and stricter.
   - **TypeScript** — `tsconfig.json`: `"strict": true`, plus `"noUncheckedIndexedAccess": true`, `"exactOptionalPropertyTypes": true`, `"noImplicitOverride": true`.
   - **Rust** — types are mandatory; turn on `#![warn(missing_docs)]` and clippy.
   - **Go** — types are mandatory; use `golangci-lint` with strict rules.
2. **Wire it into CI** as a required check.
3. **Document config** in `docs/standards/typing.md` with rationale per non-default option.

### Retrofitting onto existing code

1. **Don't flip strict mode globally on day one.** It will be all-red and ignored.
2. **Choose a starting beachhead** (one package or module) and make it strict using per-file / per-package overrides:
   - mypy: `[mypy-myproject.beachhead.*] strict = True`
   - pyright: `# pyright: strict` at file top, or `executionEnvironments` in `pyrightconfig.json`.
   - TS: `// @ts-strict-ignore` deny-listed in tsconfig.
3. **Expand the strict surface** one PR at a time until the whole project is covered. Then flip global strict on and remove the per-package overrides.
4. **Track progress** — strict files / total files. Aim for monotonically increasing.

## The rules in the doc

1. **No `Any` / `unknown` / `dyn`** at module boundaries. Internal use OK with a `# type-justification: <reason>` comment.
2. **No `# type: ignore` / `// @ts-expect-error`** without a reason in the comment, and ideally an issue link.
3. **Public function signatures** have explicit parameter AND return types. Inference is fine internally.
4. **Generics are typed**, not raw — `list[User]`, not `list`; `Promise<UserId>`, not `Promise<any>`.
5. **Type narrowing is required** for `Optional` / `T | None` before use. No `!` non-null assertions in TS without a code-comment reason.
6. **`Union` types are exhaustively matched** — `match` in Python, discriminated unions + `never` exhaustiveness in TS, `match` in Rust.
7. **External data is parsed, not asserted.** Anything crossing the boundary (HTTP, DB, file) goes through a validating parser (`pydantic`, `zod`, `serde`) — type the parsed result, not the raw input.
8. **Avoid `Any` in test code too.** Tests are documentation; well-typed tests document better.

## Anti-patterns to call out

- `# type: ignore[misc]` to silence the checker without understanding why.
- Casting in tests because the production type is "too strict to test easily" — usually means the production type is wrong.
- Using `dict[str, Any]` as a function parameter ("config object") — define a TypedDict / dataclass.
- TS `as` casts to bypass narrowing.

## What this skill does NOT do

- Generate types from runtime introspection. Use schema generators (`mypy --install-types`, `openapi-typescript`) for spec-derived types.
- Replace runtime validation at boundaries. Types are static; you still need `pydantic`/`zod` parsing for incoming data.

## Output

`docs/standards/typing.md` plus updated config in `pyproject.toml` / `pyrightconfig.json` / `tsconfig.json` / `Cargo.toml`.
