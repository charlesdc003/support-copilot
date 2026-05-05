Support Copilot

AI-powered system for automatically triaging support tickets, routing them correctly, and generating draft responses — with a rule-based policy engine to ensure reliability in critical cases.

---

What it does

- Classifies incoming support tickets
- Routes tickets based on category and confidence
- Generates draft replies using an LLM
- Enforces strict rules for high-risk scenarios (cannot be overridden by AI)

---

Why this matters

Support teams deal with high ticket volume and inconsistent handling of critical issues.
This system improves both speed and reliability by combining AI with deterministic rules.

---

Example

Input:
"Customer cannot access enterprise account after payment"

Output:

- Category: Account / Enterprise
- Action: Escalate
- Draft reply: Request for verification details

---

Architecture

Ticket → Semantic Search (pgvector) → LLM (Llama 3.2, structured JSON) → Policy Engine → Validated Response

---

Key Feature: Policy Engine (AI Guardrails)

The policy engine runs after the model and cannot be overridden:

- Auth issues → always escalate
- Enterprise bugs → always escalate
- Low-confidence outputs → request more information

---

Tech Stack

- FastAPI + Pydantic
- PostgreSQL + pgvector
- Ollama (local LLM + embeddings)
- Weights & Biases (tracing)
- pytest + GitHub Actions

---

Evaluation (100 labeled tickets)

- Action accuracy: 78%
- Category accuracy: 51%
- Policy compliance: 100% (0 failures)

---

Key Failure Modes

- Over-escalation of billing/refund tickets
- Overuse of "needs_info" for simple queries
- Poor bug severity classification
- Category collapse to "general" for ambiguous tickets

---

Planned Improvements

- Expand knowledge base with policy documents
- Add few-shot examples to prompts
- Upgrade to larger model (e.g. Llama 70B)
- Separate classification and generation steps

---

Run Locally

docker compose up -d
uv sync
uv run python scripts/setup.py
uv run uvicorn src.app.main:app --reload

---

Dataset

100 labeled tickets available in:
"evals/tickets.jsonl"