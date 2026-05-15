---
name: rag-design
description: Design retrieval-augmented generation systems — chunking strategy, embedding model choice, retrieval pipeline (hybrid / rerank / filter), freshness/invalidation, citation handling, evaluation. Use when building a feature that needs to answer questions over a knowledge base, when the user says "RAG", "vector search", "retrieval", "semantic search", "knowledge base", "answer from docs".
---

# rag-design

## Purpose

RAG sounds simple ("embed docs, query embeddings, stuff into prompt") and is hard to do well. Most production failures come from sloppy chunking, single-retriever pipelines, missing reranking, or staleness. This skill is the design playbook plus the evaluation discipline.

## When to use

- Building a feature that answers questions over a knowledge base, docs, codebase, or customer data.
- A RAG feature exists but answers are wrong / vague / stale.
- User says: "RAG", "vector search", "retrieval", "semantic search", "knowledge base", "answer from docs", "embeddings".

## The pipeline (each stage matters)

```
[ Source documents ]
       ↓
[ Ingestion: clean, chunk, enrich with metadata ]
       ↓
[ Embed → store in vector DB ]
       ↓                              ↑
[ Query → embed ]                  [ Re-embed on doc updates ]
       ↓
[ Retrieval: vector + keyword (hybrid) + filters ]
       ↓
[ Rerank (cross-encoder or LLM) → top N ]
       ↓
[ Prompt assembly: instructions + retrieved chunks + citation rules ]
       ↓
[ Generation with structured output + citations ]
       ↓
[ Verification: citations match the provided chunks ]
       ↓
[ Response ]
```

## Design decisions

### Chunking
- **Don't chunk by token count alone.** Respect structural boundaries: paragraphs, sections, function boundaries (for code), table rows.
- **Smaller chunks (200–500 tokens)** are usually better than larger — more precise retrieval, more space for context.
- **Overlap** adjacent chunks by 10-20% so a relevant fact split across a boundary isn't lost.
- **Preserve metadata** on every chunk: source doc, section, last_updated, doc type, access permissions (if multi-tenant).
- **For code**: chunk per function / class with surrounding imports.

### Embedding model
- **Start with a strong general-purpose model** (e.g. OpenAI `text-embedding-3-large`, Voyage, Cohere). Most teams over-tune here too early.
- **Higher dimensionality = better recall, more storage** — measure the tradeoff for your data.
- **Domain-tuned embeddings** (e.g. code-specific) help for narrow domains; not worth it for general doc Q&A.
- **Re-embed on model upgrade.** Embedding spaces aren't compatible across versions.

### Vector store
- **Postgres + pgvector** is enough for many production cases (single source of truth, joins with metadata).
- **Dedicated stores** (Pinecone, Qdrant, Weaviate, Milvus) for larger scale or specialized features.
- **Index choice** (HNSW, IVF) is a recall/latency/memory tradeoff — measure.

### Retrieval — *always hybrid*
- Vector similarity alone has gaps on rare terms, exact-match needs (IDs, names, code), and keyword-bearing queries.
- **Hybrid retrieval**: vector + BM25 (keyword) results merged with reciprocal rank fusion or similar.
- **Metadata filters**: respect user tenancy, document type, recency.
- **Top-k**: retrieve more than you need (e.g. 20-30), let the reranker prune.

### Reranking
- A reranker scores each retrieved chunk against the query with a stronger (and slower) model — cross-encoder or LLM.
- Typically improves precision 20-40%.
- Use Cohere Rerank, BGE Reranker, or LLM-as-reranker.
- Reduce to final top-N (3-7 chunks) for the prompt.

### Prompt assembly
- **Cite sources mandatory** — schema requires `{ claim, chunk_id, quote }`. See `hallucination-guardrails`.
- **Instructions before context** — model treats earlier content as more authoritative.
- **Delimited chunks** — `<chunk id="...">...</chunk>` so model can cite them.
- **Refuse on insufficient context** — "If the chunks don't support an answer, say so."
- **Cache the stable parts** of the prompt (`llm-cost-management`).

### Freshness / invalidation
- **Trigger**: on source-doc change, re-chunk and re-embed.
- **Strategy options**:
  - **Recompute on write** — small corpora.
  - **Batch nightly** — large corpora with low change rate.
  - **Event-driven** — message queue triggers re-index on source change.
- **TTL on retrieved chunks** — for time-sensitive content, mark stale chunks at query time.
- **Index per environment** — dev/staging/prod indices distinct; promotion is a deliberate event.

### Citations + verification
- Output schema mandates citations.
- **Verify post-generation**: the quoted text actually appears in the cited chunk (substring or near-match).
- Surface citations to the user; let them click through to source.

## Evaluation (essential — RAG without evals is RAG that silently degrades)

Separate eval suites for each stage:
- **Retrieval eval**: known query → known relevant chunks; measure recall@k.
- **End-to-end eval**: query → answer; grade for accuracy + citation correctness (cross-ref `llm-evals`).
- **Adversarial eval**: queries outside the corpus should trigger refusal.
- **Staleness eval**: insert a known fact into the corpus; verify it's retrievable within X minutes.

## Process

1. **Define the corpus** — what docs, what update cadence, what access controls.
2. **Pick chunking + metadata strategy.**
3. **Pick embedding model + vector store** — start with defaults; tune later if evals show problems.
4. **Build hybrid retrieval + reranker.**
5. **Design prompt + citation schema** (`prompt-engineering`, `hallucination-guardrails`).
6. **Build eval suites** for retrieval and end-to-end.
7. **Wire freshness** — re-index trigger appropriate to corpus.
8. **Document at `docs/ai/rag-<feature>.md`**:
   - Corpus + update cadence.
   - Pipeline diagram (one of the above, customized).
   - Metrics: retrieval recall@k, end-to-end accuracy, citation correctness, staleness.
   - Owners.

## Anti-patterns

- **Vector-only retrieval.** Misses exact matches and rare terms. Hybrid by default.
- **No reranking.** Top-5 vector hits are noisy; reranking is the cheapest precision win.
- **No citations / unverified citations.** Hallucinated facts with hallucinated sources.
- **One giant chunk per doc.** Wastes context budget; precision tanks.
- **Re-index never.** Index drifts from source; users see stale info.
- **Tuning chunk size endlessly before measuring retrieval recall.** Build evals first.
- **Mixing tenants in one index** without metadata filtering — data leak.

## Cross-references

- `prompt-engineering` — citation-bearing prompt schema.
- `hallucination-guardrails` — schema enforcement and post-generation verification.
- `llm-evals` — both retrieval-stage and end-to-end suites.
- `llm-cost-management` — retrieval tuning controls token spend.
- `pii-data-handling` — multi-tenant retrieval must respect access controls.

## Output

- The retrieval pipeline code.
- `docs/ai/rag-<feature>.md` — design + metrics + ownership.
