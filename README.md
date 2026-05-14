# ai-skills

A shareable library of Claude Code / Claude Enterprise **skills** that codify a consistent way of working across a team: PRDs, phased delivery, TDD, retros, ADRs, draw.io diagrams, OpenAPI-first APIs, structured `docs/` directories, and more.

Designed so engineers, QA, and other AI agents all operate from the same playbook — and so a new project always starts with the same set of artifacts.

## What's in here

Skills are organized into six categories:

| Category | What it covers |
| --- | --- |
| **planning** | PRD creation, story breakdown into phases, sprint retrospectives, ADRs, estimation |
| **development** | TDD enforcement, phased implementation, PR descriptions, self-review |
| **documentation** | `docs/` directory structure, draw.io diagrams, OpenAPI/Swagger (MCP-ready), decision log, CHANGELOG, README |
| **quality** | QA test plans, bug investigation, test pyramid audits, coverage gaps |
| **operations** | Incident postmortems, deploy checklists, rollback plans |
| **collaboration** | Handoff prep, onboarding walkthroughs, context snapshots |

Browse the full catalog in [INDEX.md](INDEX.md).

## Installing

### Personal install (across all your projects)

```sh
git clone https://github.com/ryan-evans-git/ai-skills.git ~/code/ai-skills
~/code/ai-skills/install.sh
```

`install.sh` symlinks each skill directory into `~/.claude/skills/` so Claude picks them up everywhere.

### Project-scoped install (so QA, other devs, and CI agents pick them up automatically)

From inside a project repo:

```sh
git submodule add https://github.com/ryan-evans-git/ai-skills.git .claude/skills/ai-skills
```

Claude Code auto-loads skills from `.claude/skills/`. Anyone who clones the repo with `--recurse-submodules` gets the same skill set.

### Enforcement hooks (TDD + phased implementation)

Two skills — **tdd-enforcer** and **phased-implementation** — ship with PreToolUse hook scripts that **block edits** when their preconditions aren't met (no failing test exists, no current plan in `docs/plans/CURRENT.md`).

See [hooks/README.md](hooks/README.md) for how to wire them into a project's `.claude/settings.json`. Hooks are opt-in per project.

## Conventions

Every project that uses this library is expected to grow this directory tree:

```
docs/
├── prds/             ← product requirement docs (one per feature/epic)
├── plans/            ← phase/story plans; CURRENT.md is the live one
│   └── CURRENT.md
├── decisions/        ← ADRs, numbered, one per file
├── retros/           ← end-of-phase retrospectives
├── progress/         ← session-by-session progress notes + handoffs
├── architecture/     ← draw.io diagrams + supporting notes
├── postmortems/      ← incident writeups
├── qa/               ← QA test plans
└── api/              ← OpenAPI / Swagger specs
```

The **docs-directory-keeper** skill knows this layout and will create / maintain it.

## Contributing a new skill

See [docs/contributing-skills.md](docs/contributing-skills.md).

## License

MIT — see [LICENSE](LICENSE).
