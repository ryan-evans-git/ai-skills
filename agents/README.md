# Subagents

Specialized agent roles that pair with the skills in this library. Each agent has its own system prompt, a curated tool allowlist, and a focused role description that drives auto-routing from the main agent's `Agent` tool.

## How agents differ from skills

| | Skills | Agents |
| --- | --- | --- |
| **Where they run** | In the main agent's context | In a separate, isolated context window |
| **Tools** | Whatever the main agent has | Limited to what the agent's frontmatter declares |
| **State on entry** | Aware of the full conversation | Cold start — only sees the prompt the main agent passes |
| **Parallelism** | One at a time | Can run multiple in parallel |
| **Cost** | Cheap (just a prompt fragment) | Heavier (fresh context window, separate spawn) |
| **Purpose** | "How to do X" playbooks | "Specialist that does X" with isolation |

Skills are the playbooks. Agents are the actors equipped to run them with the right tools and a clean room.

## When to use a subagent (rather than just applying a skill in the main thread)

- **Independent review** — code review, security audit, dependency audit. The cold start IS the point: independence from the main thread's prior context.
- **Parallel work** — running 3 audits at once vs. serially.
- **Tool scoping** — when a task should NOT have edit/write access ("review only"), the agent's allowlist enforces it.
- **Context preservation** — when the investigation would bloat the main thread's context (large diff review, deep profiling session).

For most everyday work — applying a skill to the current task — stay in the main thread.

## The roster

| Agent | Tools | Use when |
| --- | --- | --- |
| [code-reviewer](code-reviewer.md) | Read, Grep, Glob, Bash | Independent diff/PR review; finds issues, doesn't fix them |
| [qa-engineer](qa-engineer.md) | Read, Grep, Glob, Bash | Test plans, coverage audits, bug investigation writeups |
| [architect](architect.md) | Read, Grep, Glob, Bash, Write, Edit | ADRs, threat models, service-boundary analysis, API design |
| [planner](planner.md) | Read, Grep, Glob, Write, Edit | Requirements clarification + PRD + phased plan |
| [prompt-evaluator](prompt-evaluator.md) | Read, Grep, Glob, Bash | Run eval suite for a prompt/model change; produce before/after delta |
| [dependency-auditor](dependency-auditor.md) | Read, Grep, Glob, Bash | CVEs, abandoned packages, license posture, committed secrets |
| [performance-investigator](performance-investigator.md) | Read, Grep, Glob, Bash | Reproduce → measure → profile → propose fix → recommend regression guard |
| [incident-responder](incident-responder.md) | Read, Grep, Glob, Bash, Write, Edit | Blameless postmortem after a production incident |

## Read-only vs. write-capable

The roster splits into two patterns:

- **Read-only** (code-reviewer, qa-engineer, prompt-evaluator, dependency-auditor, performance-investigator): they find things and report. The main agent (or a human) applies fixes. Independence + accountability.
- **Write-capable** (architect, planner, incident-responder): their primary output IS a document. They write the artifact directly under `docs/`.

## Installing

`install.sh` symlinks every agent in this directory into `~/.claude/agents/` (personal install) or `.claude/agents/` (project install) — the same way it does skills. No extra configuration required; Claude Code auto-discovers the agent files at session start.

## Composing with skills

Each agent's system prompt references the skills it relies on. For example, `code-reviewer` leans on `self-review` + `security-review`; `architect` uses `adr-writer` + `threat-model` + `service-boundaries`. This way, updating a skill's playbook automatically updates how the relevant agent works.

## Adding a new agent

Convention:

```yaml
---
name: kebab-case-name
description: One or two sentences for the routing model — when this agent should be invoked. Be specific.
tools: Read, Grep, Glob, Bash  # least-privilege; only what's actually needed
---

# <Agent name>

You are <role>. ...

## Your job
...

## Inputs you'll typically receive
...

## Process
...

## Output format
...

## What you do NOT do
...
```

Keep agents focused — one role, one return shape. If you find yourself writing "you also do X", split into two agents.
