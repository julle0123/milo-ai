# app/api/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import chat_with_bot
from app.models.chat_log import ChatLog
from app.core.db import get_db

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. 챗봇 응답 생성
    output_text = chat_with_bot(req.input, req.session_id, req.persona, db=db)

    # 2. 대화 로그 저장만 수행
    log = ChatLog(USER_ID=req.session_id, SENDER=req.input, RESPONDER=output_text)
    db.add(log)
    db.commit()

    return ChatResponse(output=output_text)