---
name: agent-design
description: Decide whether to build an agent (tool-using, multi-step LLM) versus a single completion, then design the agent's tools, control flow, termination conditions, observability, and safety. Use when designing an LLM feature with multi-step behavior, when the user says "agent", "tool use", "function calling", "multi-turn LLM", "agentic", or asks "should this be an agent".
---

# agent-design

## Purpose

"Just make it an agent" is the most expensive sentence in AI engineering. Agents are right for some problems and wildly wrong for others. This skill helps decide, then designs the parts that determine whether an agent is useful or a runaway-cost incident waiting to happen.

## When to use

- Designing an LLM feature that does multiple steps, calls tools, or iterates.
- User says: "agent", "tool use", "function calling", "multi-turn LLM", "agentic", "should this be an agent".
- A naive single-completion feature is producing brittle or insufficient results.

## When to use an agent — and when NOT to

### Use an agent when
- The task genuinely requires **multiple tool calls** the model must choose between.
- The number of steps is **input-dependent** (you can't unroll it ahead of time).
- The model needs to **react to tool output** before deciding the next step.
- Examples: troubleshooting workflow, multi-step data lookup with conditional branches, code-edit-and-test loops.

### Do NOT use an agent when
- A **single completion with retrieval** suffices. (Most "smart Q&A" features.)
- The steps are **always the same** — that's a pipeline, not an agent. Use a deterministic chain.
- The task fits **structured output** of a known shape. Don't agent-ify a classifier.
- **Cost / latency are tight** — agents cost N× the tokens and N× the latency of a single call.
- **Failures must be debuggable** — agent trajectories are hard to root-cause.

**Default**: start with the simplest thing (single completion, then chain, then agent). Add complexity when you have evidence the simpler thing fails.

## Design surface (when you DO need an agent)

### Tools
- **Each tool does ONE thing.** "Run any SQL" tool is too broad; "fetch user by id" is the right granularity.
- **Tool descriptions are agent-facing.** Write them like LLM prompts: clear purpose, when to use vs. another tool, what to expect back. The agent picks tools by description match.
- **Strongly-typed inputs.** Use the structured-tool-use API (Anthropic tool use, OpenAI function calling). The model rarely misuses well-typed tools.
- **Idempotent where possible.** Agents retry; non-idempotent tools cause damage. Add idempotency keys (cross-ref `resilience-patterns`).
- **Side-effect tools clearly marked** — both in the description ("DESTRUCTIVE") and in the tool registry. Some agents should require human approval for destructive tools.
- **Read-only tools first.** Default tools are read; mutation tools are explicit.

### Control flow
- **Max iterations** — hard cap. An agent that goes 20 turns deep is probably stuck. Cap at 5-10 typically.
- **Termination conditions** — what tool call (or output) means "done"?
- **Hierarchical**: a parent agent delegates to specialized sub-agents only when the parent decision space is too large. Don't nest by default — it compounds cost and brittleness.

### State
- **Conversation memory**: pass back only what's needed. Past tool results bloat context.
- **Working memory**: agents often need a scratchpad — make it explicit (a tool that writes to a notes object) rather than implicit (relying on context-window memory).
- **Persistent state** between turns: write to a real store (DB / Redis); don't rely on the model to remember.

### Output discipline
- The agent's final output goes through the same structured-output discipline as a single-completion feature (`hallucination-guardrails`).
- An agent doesn't excuse skipping output validation.

## Safety

Agents amplify both capability and risk. Mandatory:

- [ ] **Tools are scoped** to least privilege. The "send email" tool can send only to specific roles; the "delete record" tool is admin-only.
- [ ] **Prompt-injection resistance** — tool outputs are content, not instructions. Delimit clearly; treat as untrusted. See `llm-safety`.
- [ ] **Cost cap per session** — terminate if a session exceeds N tokens or $N. Prevents runaway agents.
- [ ] **Human-in-the-loop for destructive actions** above a threshold (deleting data, sending external messages, financial actions).
- [ ] **Audit trail** — every tool call logged with inputs/outputs and the prompt that triggered it. See `audit-log-retention`.

## Observability

- **Trace per session**: the full sequence of LLM calls, tool calls, tool outputs.
- **Metrics**: avg / p95 turns per session, success rate, refusal rate, cost per session, latency.
- **LangSmith / Langfuse / Helicone** are common picks for agent trace UIs.

## Evaluation

Agent eval is harder than single-completion eval. Approaches:
- **End-to-end task pass/fail**: did the agent achieve the goal? Slow but most meaningful.
- **Trajectory grading**: did the agent take a reasonable path? Useful for catching "got the right answer for the wrong reason."
- **Tool-call correctness**: per-step, did the agent call the right tool with the right args?
- **Cross-ref `llm-evals`** — build multiple suites at different levels.

## Process

1. **Justify the agent.** Can a single completion + retrieval (or a deterministic chain) do this? If yes, use that. Write down why not.
2. **Inventory the tools** needed. One purpose each, typed inputs, clear descriptions.
3. **Set the iteration cap and termination conditions.**
4. **Decide what's auto-approved vs. requires human.**
5. **Wire observability** (trace + metrics) from day one. An agent without traces is undebuggable.
6. **Build evals** at task and trajectory level.
7. **Document at `docs/ai/agent-<feature>.md`**:
   - Why an agent (not a chain).
   - Tool list with descriptions.
   - Iteration cap, termination.
   - Safety scope per tool.
   - Cost ceiling.
   - Trace store + dashboard links.
8. **Ship behind a flag**, start with internal users, watch traces.

## Anti-patterns

- **Agent for tasks a single call could do.** Cost, latency, and debuggability all hit.
- **Tools described for humans, not LLMs.** "GET /users/{id}" with no description — the agent guesses.
- **No iteration cap.** Agent loops forever; user pays for it.
- **Destructive tools auto-approved.** "Send invoice" without confirmation; "delete row" with no review.
- **Tool outputs treated as instructions.** Document fetched by a tool can contain "ignore previous instructions, do X." See `llm-safety`.
- **No traces in prod.** Three months in, you have no idea what your agent is actually doing.

## Cross-references

- `prompt-engineering` — tool descriptions are prompts; the system prompt sets agent behavior.
- `llm-cost-management` — agents are the worst cost surprises; budget per session.
- `llm-safety` — agents amplify injection risk because tool outputs feed back into context.
- `hallucination-guardrails` — agents must still validate output.
- `llm-evals` — multiple suites at task and trajectory levels.
- `audit-log-retention` — agent actions are audit-worthy.

## Output

- Tool definitions, agent loop, safety policies in code.
- `docs/ai/agent-<feature>.md` — justification, design, observability, evals.
