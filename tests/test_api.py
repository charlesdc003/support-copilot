from unittest.mock import patch
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def mock_process(request):
    from src.app.schemas import TicketResponse, ResolutionAction, TicketCategory
    return TicketResponse(
        ticket_id=request.ticket_id,
        action=ResolutionAction.ESCALATE,
        confidence=0.9,
        category=TicketCategory.AUTH,
        draft_reply="Escalating to engineering team.",
        justification="Auth issue detected."
    )


def test_ticket_endpoint_returns_200():
    with patch("src.app.main.process_ticket", side_effect=mock_process):
        response = client.post("/ticket", json={
            "ticket_id": "test-001",
            "customer_tier": "enterprise",
            "subject": "Cannot login",
            "message": "Authentication is broken for all users."
        })
    assert response.status_code == 200
    data = response.json()
    assert data["ticket_id"] == "test-001"
    assert data["action"] == "escalate"


def test_invalid_tier_rejected():
    response = client.post("/ticket", json={
        "ticket_id": "test-002",
        "customer_tier": "vip",
        "subject": "Need help",
        "message": "Something is not working correctly."
    })
    assert response.status_code == 422


def test_short_subject_rejected():
    response = client.post("/ticket", json={
        "ticket_id": "test-003",
        "customer_tier": "pro",
        "subject": "Hi",
        "message": "I need some help please."
    })
    assert response.status_code == 422