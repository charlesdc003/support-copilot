from .schemas import CustomerTier, ResolutionAction, TicketCategory


ALWAYS_ESCALATE_CATEGORIES = {
    TicketCategory.AUTH,
}

ALWAYS_ESCALATE_TIERS_FOR_BUGS = {
    CustomerTier.ENTERPRISE,
}

AUTO_REPLY_ELIGIBLE_TIERS = {
    CustomerTier.FREE,
    CustomerTier.PRO,
    CustomerTier.ENTERPRISE,
}


def apply_policies(
    action: ResolutionAction,
    category: TicketCategory,
    customer_tier: CustomerTier,
    confidence: float,
) -> ResolutionAction:

    # Auth issues always escalate regardless of model confidence
    if category == TicketCategory.AUTH:
        return ResolutionAction.ESCALATE

    # Enterprise bugs always escalate
    if category == TicketCategory.BUG and customer_tier == CustomerTier.ENTERPRISE:
        return ResolutionAction.ESCALATE

    # Low confidence always goes to needs_info
    if confidence < 0.4:
        return ResolutionAction.NEEDS_INFO

    return action