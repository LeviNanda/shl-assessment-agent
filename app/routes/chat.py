from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import run_agent

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return run_agent(request)