---
name: hallucination-guardrails
description: Apply concrete guardrails against hallucinated output — schema validation, citation/grounding requirements, structured refusal, confidence scoring, and post-generation verification. Use when designing any LLM feature where wrong output has real cost (factual claims, code, financial advice, customer-facing), or when the user says "hallucination", "made up", "ground the output", "factual accuracy", "citations".
---

# hallucination-guardrails

## Purpose

LLMs hallucinate. Acting like they don't is how AI features ship that confidently invent customer names, fictional API endpoints, and incorrect financial advice. This skill lays in the guardrails — schema, grounding, refusal, verification — so wrong outputs are caught before they reach the user.

## When to use

- Any feature where wrong output has cost: factual claims, code generation, financial / medical / legal advice, customer-facing copy, structured data extraction.
- After a hallucination incident.
- User says: "hallucination", "made up", "ground the output", "factual accuracy", "citations", "confidence score".

## Guardrails (apply in layers — defense in depth)

### Layer 1: Schema enforcement
- Use the model's **structured output / tool-call** APIs (Anthropic tool use, OpenAI structured outputs, JSON schema mode) — not "please output JSON" in the prompt.
- Validate the parsed output against a strict schema (Pydantic / Zod / JSON Schema). Reject and retry on schema mismatch.
- Disallow extra fields — `additionalProperties: false`.
- Constrain enum-like fields to a closed set.

### Layer 2: Grounding (when the output should be factual)
- **Retrieval-grounded**: provide source documents; require the model to cite them; reject outputs without citations. See `rag-design`.
- **Citation format**: structured (`{ "claim": "...", "source_doc_id": "...", "quote": "..." }`) — easy to verify.
- **Verifiable claims**: every factual claim in the output maps to a quote in the provided context.
- **Refuse if not in context**: explicit prompt rule — "If the context doesn't support a claim, say so."

### Layer 3: Refusal and uncertainty
- **Structured uncertainty**: the output schema includes `confidence: "high" | "medium" | "low"` and `unable_to_answer: bool` + `reason`.
- **Threshold actions**: low confidence → escalate to human / fallback / "I don't know."
- **Don't bury refusal in prose** — make it a schema field so it's easy to detect and route.

### Layer 4: Post-generation verification
- **Structural checks**: the output is valid JSON / valid code / valid SQL / etc.
- **Semantic checks**:
  - For code: does it compile / parse / type-check?
  - For SQL: does it parse and reference only known tables/columns?
  - For factual claims: do cited sources actually contain the claimed text? (String-match the quote.)
  - For numeric answers: in the expected range? Reasonable order of magnitude?
- **Cross-model check** (expensive but powerful): a second model verifies the first model's output. Use for high-stakes only.

### Layer 5: Adversarial / out-of-domain handling
- **Out-of-scope inputs**: classify the input first; reject if outside what the feature is designed to handle.
- **Adversarial inputs**: see `llm-safety`.
- **Empty / nonsense input**: explicit handling, not "let the model figure it out."

## Required components per feature

For any feature shipping to production, this baseline:

- [ ] Structured output via tool-use / JSON schema (not prompt-and-pray).
- [ ] Output schema validated programmatically; reject and retry once on mismatch.
- [ ] Explicit refusal mechanism in the schema.
- [ ] Confidence / uncertainty field in the schema.
- [ ] For factual features: citations to provided context, with quote-match verification.
- [ ] For code/SQL features: parse / compile check.
- [ ] Eval suite includes adversarial inputs that *should* trigger refusal (cross-ref `llm-evals`).
- [ ] Telemetry: log refusals, retries, schema failures as separate metrics so you can see hallucination rate.

## Process

1. **Define what wrong looks like** for this feature. Be specific.
2. **Pick the layers** from above that apply.
3. **Schema first** — design the output shape, including uncertainty / refusal fields.
4. **Implement validation** — structured output API → schema check → semantic verification → only then return to the user.
5. **Wire telemetry** — track refusal rate, retry rate, schema-failure rate per feature.
6. **Eval against the failure modes** (`llm-evals`):
   - Adversarial inputs should trigger refusal.
   - Out-of-context queries should trigger "unable_to_answer."
   - In-context queries should produce verifiable citations.
7. **Document** at `docs/ai/guardrails-<feature>.md`:
   - What layers are in place.
   - What's NOT covered and what the residual risk is.
   - Where the user-facing fallback goes.

## When NOT to over-engineer

For low-stakes, internal-only features (brainstorming, draft assistance, summarization-with-edit), Layer 1 + Layer 3 is often enough. Don't burn budget grounding outputs that a user will manually verify anyway.

## Anti-patterns

- "Please output JSON" with no structured-output API. Will eventually output non-JSON.
- Free-form citations ("Source: the docs") with no verifiable mapping.
- Confidence field that the model always says "high" for. Test it — if it never says low, it's not useful.
- Catching hallucinations in post-process and silently rewriting. Worse than refusing.
- No telemetry. You have no idea how often the guardrails fire.

## Cross-references

- `prompt-engineering` — schema design and refusal handling start in the prompt.
- `llm-evals` — adversarial inputs and refusal-correctness in the eval suite.
- `llm-safety` — adversarial inputs / injection / jailbreak.
- `rag-design` — citation grounding lives here.

## Output

- Structured-output schema in code.
- Validation + verification layers.
- `docs/ai/guardrails-<feature>.md` — layers + residual risk per feature.
