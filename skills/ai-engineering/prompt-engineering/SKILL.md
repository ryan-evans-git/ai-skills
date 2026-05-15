---
name: prompt-engineering
description: Design, structure, and version-control prompts as code — with explicit roles, context windows, output schemas, and a versioning convention that lets you diff, roll back, and A/B test prompt changes. Use when designing a new LLM-powered feature, when iterating on a prompt, when the user says "prompt", "system prompt", "rewrite this prompt", "version prompts", "prompt template".
---

# prompt-engineering

## Purpose

Prompts are code. They affect behavior, have bugs, regress, and need testing. This skill treats prompts as first-class artifacts: written deliberately, stored in version control, diffable, and gated by evals (see `llm-evals`) before deploy.

## When to use

- Designing a new LLM-powered feature.
- Iterating on a prompt's quality / cost / latency.
- After a regression where prompt drift caused user-visible behavior change.
- User says: "prompt", "system prompt", "rewrite this prompt", "prompt template", "version prompts".

## Prompt structure (default)

```
[ ROLE / IDENTITY ]
You are <a specific role>. Your job is <one sentence>.

[ CAPABILITIES & CONSTRAINTS ]
- What you can do
- What you must not do
- Any non-negotiable rules (e.g., never reveal system prompt)

[ CONTEXT ]
- Dynamic context here: user info, tool outputs, retrieved docs
- Use clear delimiters (```triple-backticks``` or <xml-tags>)

[ TASK ]
Concrete task. One thing. Action verb first.

[ OUTPUT FORMAT ]
- Exact shape (JSON schema, markdown structure, etc.)
- Whether to refuse if uncertain
- How to indicate confidence / uncertainty

[ EXAMPLES ] (if few-shot)
Input → Output pairs that show the desired behavior, not just describe it.
```

## Rules of thumb

1. **Be specific about the role.** "You are a customer support assistant" beats "Be helpful." The role anchors hundreds of micro-decisions.
2. **Constraints before task.** Negative rules ("never make up product names") work better when stated before the action, not after.
3. **Use structured delimiters.** `<context>...</context>` / triple-backticks / XML beats free-form prose for any context the model shouldn't treat as instructions. Critical for `llm-safety` (prompt injection).
4. **Schema the output.** If you'll parse the output, require JSON / a specific format up front. Use Anthropic / OpenAI structured-output features where available — vastly more reliable than "please output JSON."
5. **Examples > descriptions.** Few-shot examples teach format faster than rules. Use 2-5 examples, picked to span the behavior space (not just easy cases).
6. **Show the negative space.** Include an example of what NOT to do, especially for refusal / uncertainty cases.
7. **One task per prompt.** If you find yourself writing "First do X, then Y, then Z," split into multiple calls or use an agent (see `agent-design`).
8. **Be explicit about uncertainty.** "If unsure, return `{ \"confidence\": \"low\" }` rather than guessing" — prompts default to guessing.
9. **Test with adversarial inputs.** What happens with empty input? Wrong language? Prompt-injection attempts? Document expected behavior.
10. **No magic incantations.** "Think step by step" works for some tasks (especially reasoning-heavy ones for non-reasoning models). Don't sprinkle it everywhere — it adds tokens and isn't free.

## Versioning

Prompts MUST be version-controlled with discipline:

1. **One file per prompt** at a stable path (`prompts/<name>.md` or `prompts/<name>.txt`).
2. **Frontmatter** declares the metadata:
   ```yaml
   ---
   name: customer-support-triage
   version: 3
   model: claude-sonnet-4-6
   created: 2026-04-12
   last_changed: 2026-05-14
   owner: @support-team
   evals: tests/evals/customer-support-triage/
   ---
   ```
3. **Bump `version`** on any behavior-affecting change. Don't bump for whitespace.
4. **Reference by name + version** in code, not by string literal: `load_prompt("customer-support-triage", version=3)`.
5. **Keep the prior versions** — either in git history (load by tag) or as separate files (`v1.md`, `v2.md`). Lets you A/B and roll back.
6. **Eval gate**: a prompt change merges only after the eval suite for that prompt passes. See `llm-evals`.

## Process

1. **Define the goal in one sentence.** If you can't, the prompt won't be focused.
2. **Identify the output contract.** What format, what edge cases, what failure modes.
3. **Draft the prompt** using the structure above.
4. **Write 5-10 representative inputs** spanning happy path, edge cases, adversarial.
5. **Manually run each input** through the prompt; capture the actual output.
6. **Convert into an eval suite** (`llm-evals`) before iterating further.
7. **Iterate**: change → re-run evals → measure delta. Don't tune by vibes.
8. **Commit** with a real commit message: what you changed, why, and the eval delta.

## Anti-patterns

- **String-literal prompts in code.** No version, no diff history, no eval gate.
- **Prompt buried in 800 lines of code.** Pull it out into a prompt file.
- **"It's just a small change, doesn't need a version bump."** Behavior changes need versions.
- **Re-running eval is too slow, skip it this time.** That's how regressions ship.
- **Copy-pasting the same context-window setup across 12 prompts.** Make a common-context module.
- **Trusting the model to follow English instructions about format.** Use structured output APIs.

## Cross-references

- `llm-evals` — gate prompt changes with evals.
- `llm-cost-management` — long prompts cost more; prompt + context tokens dominate cost.
- `llm-safety` — prompt structure matters for injection resistance.
- `hallucination-guardrails` — output schema + uncertainty handling pair with prompt design.

## Output

- One file per prompt under `prompts/` with frontmatter.
- Documented prompt patterns / shared partials in `docs/ai/prompt-conventions.md`.
