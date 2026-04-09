import os
import weave
from .schemas import (
    TicketRequest, TicketResponse, ResolutionAction, TicketCategory
)
from .retrieval import retrieve
from .llm import call_llm
from .policies import apply_policies


def process_ticket(request: TicketRequest) -> TicketResponse:
    if os.getenv("WANDB_API_KEY"):
        weave.init("support-copilot")

    context = retrieve(request.subject + " " + request.message)

    raw = call_llm(request, context)

    try:
        action = ResolutionAction(raw.get("action", "needs_info"))
    except ValueError:
        action = ResolutionAction.NEEDS_INFO

    try:
        category = TicketCategory(raw.get("category", "general"))
    except ValueError:
        category = TicketCategory.GENERAL

    confidence = float(raw.get("confidence", 0.5))
    confidence = max(0.0, min(1.0, confidence))

    action = apply_policies(action, category, request.customer_tier, confidence)

    return TicketResponse(
        ticket_id=request.ticket_id,
        action=action,
        confidence=confidence,
        category=category,
        draft_reply=raw.get("draft_reply", ""),
        justification=raw.get("justification", "")
    )