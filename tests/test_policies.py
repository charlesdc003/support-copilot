from src.app.schemas import CustomerTier, ResolutionAction, TicketCategory
from src.app.policies import apply_policies


def test_auth_always_escalates():
    result = apply_policies(
        action=ResolutionAction.AUTO_REPLY,
        category=TicketCategory.AUTH,
        customer_tier=CustomerTier.FREE,
        confidence=0.9
    )
    assert result == ResolutionAction.ESCALATE


def test_enterprise_bug_always_escalates():
    result = apply_policies(
        action=ResolutionAction.AUTO_REPLY,
        category=TicketCategory.BUG,
        customer_tier=CustomerTier.ENTERPRISE,
        confidence=0.9
    )
    assert result == ResolutionAction.ESCALATE


def test_low_confidence_needs_info():
    result = apply_policies(
        action=ResolutionAction.AUTO_REPLY,
        category=TicketCategory.BILLING,
        customer_tier=CustomerTier.PRO,
        confidence=0.3
    )
    assert result == ResolutionAction.NEEDS_INFO


def test_pro_billing_auto_reply():
    result = apply_policies(
        action=ResolutionAction.AUTO_REPLY,
        category=TicketCategory.BILLING,
        customer_tier=CustomerTier.PRO,
        confidence=0.8
    )
    assert result == ResolutionAction.AUTO_REPLY


def test_free_auth_still_escalates():
    result = apply_policies(
        action=ResolutionAction.AUTO_REPLY,
        category=TicketCategory.AUTH,
        customer_tier=CustomerTier.FREE,
        confidence=0.95
    )
    assert result == ResolutionAction.ESCALATE