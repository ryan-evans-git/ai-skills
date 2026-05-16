# Installing this library for OpenAI Codex CLI

`install.sh` targets Claude Code. `install-codex.sh` targets OpenAI's Codex CLI. The skills themselves — being markdown playbooks — translate well; the triggering model is what changes.

## Quick start

```sh
# Personal install — symlink skills as ~/.codex/prompts/*.md
./install-codex.sh

# Project install — symlink skills into ./.codex/prompts/*.md
./install-codex.sh --project

# Emit AGENTS.md at the project root from templates/CLAUDE.md
./install-codex.sh --emit-agents-md

# See what would happen without writing anything
./install-codex.sh --dry-run
```

After install, invoke a skill in Codex with `/<name>` — for example `/prd-creation`, `/tdd-enforcer`, `/security-review`.

## The translation table

| Claude Code | Codex equivalent | Notes |
| --- | --- | --- |
| `~/.claude/skills/<name>/SKILL.md` | `~/.codex/prompts/<name>.md` | Symlinked by `install-codex.sh`. |
| Auto-trigger by description match | Slash command `/<name>` | **Biggest behavioral difference.** In Codex you (or your workflow) decide when to invoke a skill; Claude Code's main agent decides for you. The description field remains useful as documentation. |
| `CLAUDE.md` (per-project) | `AGENTS.md` (per-project) | `--emit-agents-md` renders the template with placeholders substituted. AGENTS.md is recognized by Codex, Cursor, and several other tools — it's effectively cross-tool now. |
| `~/.claude/agents/<name>.md` (subagents) | *(no direct equivalent)* | Codex doesn't have the Agent-tool / fresh-context / scoped-tools model. You can compose via shell-out, but it's not a 1:1. |
| `hooks/refresh_claude_md.py` (SessionStart) | *(not auto-wired)* | Could be re-implemented as a shell rc snippet or a Codex-startup script. The Python is portable. |
| `hooks/require_plan.py` + `require_failing_test.py` (PreToolUse) | *(not auto-wired)* | Best Codex-side equivalent is a pre-commit hook (block git commits that violate the rules). The hook scripts are tool-agnostic — they read a file and exit non-zero. |
| `install.sh` | `install-codex.sh` | This file. |

## What works without changes

Most of the value is in the skill content, and the skill content is just markdown. The "house rules" in CLAUDE.md / AGENTS.md are tool-agnostic — TDD, phased delivery, docs/ layout, code standards, security defaults all apply regardless of which AI tool reads them.

The `(skill: X)` references inside CLAUDE.md / AGENTS.md keep their meaning. They tell any agent reading the file that there's a playbook named X to apply when its conditions arise. The mechanism for finding and loading that playbook differs per tool, but the directive transfers.

## What changes meaningfully

**Auto-trigger → explicit invoke.** This is the load-bearing difference. In Claude Code, you say "let's plan this feature" and `prd-creation` fires because its description matches. In Codex, you say `/prd-creation` (or have a workflow that does). Consequences:

- **Codex slash commands need short, memorable names.** Our skill names are kebab-case and reasonably memorable, but if you find yourself typing the same prompt frequently in Codex, consider shorter aliases via symlinks.
- **Discovery matters more.** Without auto-triggering, users need to know what's available. The [INDEX.md](../INDEX.md) catalog and AGENTS.md cross-references become more important in a Codex setup.
- **Workflows can be scripted.** Codex supports shell composition; a useful pattern is to wrap common multi-step workflows (e.g. "run requirements-clarification then prd-creation then story-breakdown") in a thin shell script.

**No subagents.** The 8 agents in `agents/` rely on Claude Code's `Agent` tool — a separate isolated context with a tool allowlist. Codex doesn't have that primitive. You can:

- Run multiple `codex` instances in parallel terminals for parallel work.
- Use the slash-prompt files directly (`/code-reviewer`, `/qa-engineer`) but they'll run in the same context as everything else.
- Treat the agent definitions as documentation for what role/scope is *expected* even if it can't be enforced.

If you want a clean separation, run a second `codex` session in another tab — the OS is the isolation boundary.

**Hooks become opt-in plumbing.** The Python scripts in `hooks/` don't depend on Claude Code; they just read `docs/plans/CURRENT.md` and tool-call payload JSON. To get equivalent enforcement in a Codex workflow:

- `require_plan.py` / `require_failing_test.py` → wire as a `pre-commit` framework hook that blocks `git commit` instead of blocking the tool call. Slightly later in the lifecycle, but the discipline is the same.
- `refresh_claude_md.py` → call manually (`./hooks/refresh_claude_md.py`) before starting a Codex session, or wire into a `direnv` / shell rc snippet so it runs on `cd` into the repo. The script doesn't care which tool is about to read the resulting file.

## Maintaining a multi-tool install

If you use Claude Code at your laptop and Codex on a server (or different team members use different tools), run **both** install scripts. The skills directory is the same source of truth; each install just creates a different "view" of it (`~/.claude/skills/` for Claude Code, `~/.codex/prompts/` for Codex). The skills update via `git pull` in the library directory regardless of which view picks them up.

## Verifying after install

After running `install-codex.sh`:

```sh
ls -la ~/.codex/prompts/ | head             # symlinks should point at this repo
codex                                       # start codex
# In codex: try `/` to see the slash-command list; verify prompts show up.
```

If Codex's slash-command surface differs from what's described here (e.g. uses a different config path or expects different frontmatter), the symlinks themselves are still useful — you can manually configure Codex to look at them, or copy the content. The skills are portable; the install script is the convenience.
