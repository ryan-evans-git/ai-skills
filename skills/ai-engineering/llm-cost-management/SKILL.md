---
name: llm-cost-management
description: Track, attribute, and reduce LLM API spend — per feature, per user, per model — and apply concrete cost-reduction techniques (caching, model routing, prompt compression, context trimming, batch). Use when LLM costs are growing, before launching an LLM feature at scale, or when the user says "LLM cost", "token spend", "API bill", "prompt caching", "cheaper model", "model routing".
---

# llm-cost-management

## Purpose

LLM costs scale with usage in ways that surprise teams. This skill makes spend visible (attribution), then attacks the dominant cost drivers in priority order. Most teams can cut spend 50-90% with disciplined application of well-known techniques.

## When to use

- Before launching an LLM feature at scale.
- LLM bill is growing faster than usage.
- A specific endpoint is expensive.
- Migrating to a new model.
- User says: "LLM cost", "token spend", "API bill", "prompt caching", "cheaper model", "model routing", "context too long".

## Visibility first — you can't optimize what you can't see

1. **Log every LLM call** with structured fields:
   - `feature` / `endpoint` — which feature originated the call.
   - `model` — model name + version.
   - `input_tokens` / `output_tokens` / `cached_tokens` (where supported).
   - `cost_usd` — compute from token counts × current rates.
   - `latency_ms`.
   - `user_id` / `tenant_id` (PII-safe; see `pii-data-handling`).
   - `trace_id` for cross-correlation.
2. **Build a dashboard** that breaks down cost by feature, by model, by tenant, by day.
3. **Set per-feature budgets** with alerts (cross-ref `cloud-cost-budget` in finops).
4. **Identify the top 3 cost drivers** — usually 80% of the bill.

## Cost-reduction techniques (apply in priority order)

### 1. Prompt caching (often the biggest single win)
- Anthropic's prompt caching: mark stable prefixes (system prompt, large context) as cacheable. Cached reads are ~10% the cost of fresh reads and dramatically faster.
- Effective when: large system prompt + reusable context + many requests with that same context.
- Order matters: put the most-stable content first, dynamic content last.
- For Anthropic SDK in particular, use `cache_control` blocks. **Default behavior for any new Anthropic-API integration in this library should include prompt caching.**

### 2. Model routing (tier the work)
- Most "AI features" are 80% easy questions, 20% hard ones. Don't pay Opus prices for trivial classifications.
- Pattern: **router → cheap model handles N% of cases → escalate to capable model only when needed.**
- Examples: Haiku for classification, Sonnet for normal work, Opus for the genuinely hard.
- Eval each tier independently (cross-ref `llm-evals`).

### 3. Context trimming
- The biggest input tokens are usually irrelevant context.
- For RAG: tighter retrieval (top-k=3 not 20); shorter chunks; relevance reranking before send.
- For agents: drop tool outputs no longer needed; summarize long histories.
- For chat: don't send the whole history every turn — summarize past N turns.

### 4. Output capping
- `max_tokens` set deliberately, not at the default. A reply that needs 200 tokens shouldn't have a 4000-token ceiling.
- Structured output (JSON schema, tool calls) is typically shorter than free-form prose.

### 5. Batch processing
- Anthropic Message Batches API / OpenAI Batch API: 50% discount on workloads that don't need real-time response.
- Use for: nightly reprocessing, dataset generation, eval runs, non-interactive scoring.

### 6. Caching outputs
- Memoize prompt+input → output for stable transformations (e.g., "summarize this document version").
- Invalidate by content hash.
- See `caching-strategy` for the five-question framework.

### 7. Smaller / faster models within a family
- Haiku before Sonnet, Sonnet before Opus.
- Use evals to verify the cheaper model passes; don't downgrade by gut feel.

### 8. Streaming + early-stop
- Stream tokens; if you can detect "done enough" client-side, close the stream.
- Useful for classifications and structured outputs.

### 9. Prompt compression
- Shorter prompts cost less and often work as well. Run an eval gated A/B between long and short variants.

## Process

1. **Measure** — instrument every LLM call with the fields above. Until you can attribute spend per feature, optimization is guessing.
2. **Find the top cost drivers** — usually 1-3 features dominate.
3. **For each driver, apply techniques in priority order** — start with prompt caching (often 50-90% win for cached-prefix workloads).
4. **Eval-gate every change** — cost reductions that break quality are not wins.
5. **Set per-feature budgets + alerts.**
6. **Document at `docs/ai/cost-management.md`**:
   - Current monthly spend by feature.
   - Active techniques per feature.
   - Budget per feature.
   - Owner.
7. **Quarterly review** — the LLM landscape changes fast; today's cheap model is tomorrow's overpriced one.

## Anti-patterns

- **No per-feature attribution.** Total bill is up; nobody knows why.
- **Routing by token count.** "If prompt > 10K tokens, use the big model." Token count doesn't correlate with task difficulty.
- **Disabling prompt caching to "keep it simple."** This is the biggest single lever; turn it on.
- **Free-form output where structured output would do.** Verbose outputs cost more and parse worse.
- **No `max_tokens`.** Costs are unbounded.
- **Optimizing without evals.** Cheap-and-wrong is worse than expensive-and-right.
- **Batch API ignored for non-real-time workloads.** Leaving 50% on the table.

## Cross-references

- `prompt-engineering` — shorter / structured prompts save tokens.
- `llm-evals` — gate cost optimizations with quality measurements.
- `rag-design` — retrieval tuning controls a major cost driver.
- `caching-strategy` — output caching is the same five-question framework.
- `cloud-cost-budget` (finops) — wire LLM cost into overall budgets.

## Output

- LLM call instrumentation in code.
- Cost dashboard.
- `docs/ai/cost-management.md` — running record of techniques applied + spend trend.
