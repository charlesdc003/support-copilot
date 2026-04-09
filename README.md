# Support Copilot

![CI](https://github.com/charlesdc003/support-copilot/actions/workflows/ci.yml/badge.svg)

An AI-powered support ticket triage system that classifies tickets, routes them to the correct action, and generates draft replies — with a deterministic policy engine that overrides the model for critical cases.

## Architecture
Ticket in → pgvector similarity search → policy engine → llama3.2 (structured JSON) → validated response

The policy engine runs after the LLM. It cannot be overridden by model output. Auth tickets always escalate. Enterprise bug tickets always escalate. Low confidence always routes to needs_info.

## Stack

- FastAPI + Pydantic v2
- PostgreSQL + pgvector (semantic retrieval)
- Ollama — nomic-embed-text embeddings + llama3.2 generation (local, RTX 5080)
- W&B Weave tracing
- pytest + GitHub Actions CI

## Evaluation Results (100 labeled tickets)

| Metric | Score |
|---|---|
| Action accuracy | 78% (78/100) |
| Category accuracy | 51% (51/100) |
| Policy compliance | 100% (0 failures) |

## Key failure modes

- Model over-escalates billing tickets — treats refund requests as high risk
- Model over-uses needs_info on simple general questions
- Bug severity assessment is inconsistent — model cannot distinguish minor bugs from critical outages without more context in the knowledge base
- Category classification collapses to "general" for ambiguous tickets

## What would improve accuracy

- Larger knowledge base with more policy documents
- Few-shot examples in the prompt showing correct classifications
- A larger local model (llama3.1:70b or similar)
- Separate classification and generation steps

## Run locally

```bash
docker compose up -d
uv sync
uv run python scripts/setup.py
uv run uvicorn src.app.main:app --reload
```

## Eval dataset

100 labeled tickets in `evals/tickets.jsonl`. Run evals with:

```bash
uv run python scripts/run_evals.py
```