# app/api/chat.py
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import chat_with_bot

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    output = chat_with_bot(req.input, req.session_id, req.persona)
    return ChatResponse(output=output)