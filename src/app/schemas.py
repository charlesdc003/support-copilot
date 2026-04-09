from enum import Enum
from pydantic import BaseModel, Field


class CustomerTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class ResolutionAction(str, Enum):
    AUTO_REPLY = "auto_reply"
    ESCALATE = "escalate"
    NEEDS_INFO = "needs_info"


class TicketCategory(str, Enum):
    BILLING = "billing"
    AUTH = "auth"
    FEATURE_REQUEST = "feature_request"
    BUG = "bug"
    GENERAL = "general"


class TicketRequest(BaseModel):
    ticket_id: str
    customer_tier: CustomerTier
    subject: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=10, max_length=5000)


class TicketResponse(BaseModel):
    ticket_id: str
    action: ResolutionAction
    confidence: float = Field(ge=0.0, le=1.0)
    category: TicketCategory
    draft_reply: str
    justification: str