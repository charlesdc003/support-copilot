import json
import ollama
from .schemas import TicketRequest

GENERATE_MODEL = "llama3.2"


def call_llm(request: TicketRequest, context: list[dict]) -> dict:
    if context:
        context_text = "\n\n".join(r["content"] for r in context)
    else:
        context_text = "No context available."

    prompt = (
        "You are a support ticket assistant. Classify and respond to this ticket.\n\n"
        "Respond with only a JSON object using these exact fields:\n"
        "action: one of auto_reply, escalate, needs_info\n"
        "confidence: float between 0.0 and 1.0\n"
        "category: one of billing, auth, feature_request, bug, general\n"
        "draft_reply: the reply to send to the customer\n"
        "justification: one sentence explaining your decision\n\n"
        f"Context:\n{context_text}\n\n"
        f"Customer tier: {request.customer_tier.value}\n"
        f"Subject: {request.subject}\n"
        f"Message: {request.message}\n\n"
        "JSON response:"
    )

    response = ollama.chat(
        model=GENERATE_MODEL,
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )

    content = response.message.content
    if not content:
        return {
            "action": "needs_info",
            "confidence": 0.3,
            "category": "general",
            "draft_reply": "We received your request and will follow up shortly.",
            "justification": "Model returned empty response."
        }

    return json.loads(content)