---
name: llm-evals
description: Build and maintain an evaluation suite for LLM-powered features — golden datasets, automated graders, regression detection — that gates prompt and model changes the way tests gate code changes. Use when adding any LLM feature, when iterating on a prompt, when changing model versions, or when the user says "eval", "evaluation", "golden set", "LLM regression test", "is this prompt better".
---

# llm-evals

## Purpose

Without evals, LLM features regress invisibly: a "small prompt tweak" silently breaks 8% of cases. Evals turn LLM development into engineering by giving every change a measurable delta. They're the CI of AI features.

## When to use

- Adding a new LLM-powered feature.
- Iterating on a prompt (`prompt-engineering`).
- Migrating to a new model version.
- Adding RAG (see `rag-design`).
- Introducing a guardrail (see `hallucination-guardrails`, `llm-safety`).
- User says: "eval", "evaluation", "golden set", "regression test for the prompt", "is this prompt better".

## The eval stack (build all four layers)

### 1. Golden dataset
A curated set of input → expected-output pairs, written by humans who understand the task. Each item has:
- **Input** — exact prompt input, plus any context (retrieved docs, user info).
- **Expected output / criteria** — either an exact match, a structured rubric, or a model-graded judgment.
- **Tags** — category (happy path / edge case / adversarial / refusal), difficulty, source.
- **Owner** — who curated it; who reviews disagreements.

**Size**: start with 20-50 items spanning the behavior space. Grow to hundreds as patterns emerge. Quality over quantity.

**Where it comes from**:
- Synthetic seed (you generate them based on the spec).
- Production traces (with PII scrubbed; cross-ref `pii-data-handling`).
- Edge cases surfaced by bugs.
- Adversarial inputs (jailbreaks, prompt-injection attempts).

### 2. Graders

The way you decide "did the output meet the criterion?" Pick the cheapest grader that's accurate for the task:

| Grader | Use for |
| --- | --- |
| **Exact match** | Structured outputs, classifications |
| **Regex / schema match** | "Output is valid JSON with field X" |
| **Programmatic check** | "Numeric answer within 5% of expected" |
| **Embedding similarity** | Free-form text where meaning matters, exact wording doesn't |
| **LLM-as-judge** | Last resort. Use a different / stronger model than the one under test. Validate that the judge agrees with humans on a held-out set. |
| **Human review** | For high-stakes evals, sample N% for human grading periodically |

**Don't trust LLM-as-judge blindly.** Always validate the judge's agreement rate with humans, and re-validate periodically.

### 3. Metrics
Choose a small, focused set:
- **Accuracy / pass rate** — % of golden items passing.
- **Per-category breakdown** — happy path vs. adversarial vs. refusal.
- **Latency** — p50, p95 (model time + total time).
- **Cost** — tokens × $/token; see `llm-cost-management`.
- **Refusal rate** — when applicable. Should be high for adversarial inputs, low for legitimate ones.

Don't average to a single score. A change that improves happy path while breaking refusals is a regression.

### 4. Regression gating
- The eval suite runs on every prompt change AND every model-version change.
- **Block merge** if pass rate drops on any category.
- **Surface the deltas** in the PR (per-category gain/loss, sample failing items).
- For high-volume features, run periodically in production against held-out inputs (catch drift from external dependencies).

## Process

1. **Spec the feature behavior** in writing. Without a clear spec, you can't build a golden set.
2. **Seed the golden set** — 20-50 items minimum. Mix happy / edge / adversarial / refusal.
3. **Pick graders** per item (or per category).
4. **Implement the eval harness** — run all items through the prompt, grade, report deltas.
5. **Wire into CI** — eval runs on every PR that touches the prompt or model version.
6. **Calibrate thresholds**:
   - Pass rate floor per category (e.g. happy path ≥ 95%, refusal ≥ 99%).
   - Latency / cost ceiling.
7. **Document** at `docs/ai/evals.md`:
   - Where the golden set lives.
   - How to add items.
   - Who owns each prompt's eval.
   - The CI integration.
8. **Update with bugs** — every reported bug becomes a golden-set item before the fix lands. Permanent regression coverage.

## Tools

- **Open source / framework-agnostic**: `promptfoo`, `Inspect AI`, custom scripts.
- **LangChain ecosystem**: LangSmith (record traces, build datasets, run evals).
- **Vendor-specific**: Anthropic Evals, OpenAI Evals.
- **Custom**: a few hundred lines of Python is often enough for a starter harness.

## Anti-patterns

- **"It works for the cases I tried."** That's a manual spot-check, not an eval.
- **One score, averaged across everything.** Hides regressions in important sub-populations.
- **LLM-as-judge with no human validation.** The judge agrees with itself; you have no idea if it agrees with reality.
- **Eval items written by the same person who tuned the prompt to pass them.** Self-fulfilling.
- **Evals only run on prompt PRs.** Model versions update too; run on those.
- **No production evals.** Lab evals diverge from prod inputs over time.

## Cross-references

- `prompt-engineering` — what you're evaluating.
- `llm-cost-management` — evals must measure cost as well as quality.
- `llm-safety` — separate eval suite for adversarial / injection inputs.
- `rag-design` — RAG has its own retrieval-quality evals.

## Output

- Golden datasets under `tests/evals/<feature-name>/`.
- Eval harness wired into CI.
- `docs/ai/evals.md` — index of suites and ownership.
