from fastapi import FastAPI
from .schemas import TicketRequest, TicketResponse
from .service import process_ticket

app = FastAPI(title="Support Copilot")


@app.post("/ticket", response_model=TicketResponse)
def score_ticket(request: TicketRequest) -> TicketResponse:
    return process_ticket(request)