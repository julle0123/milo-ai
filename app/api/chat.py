# app/api/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import chat_with_bot
from app.models.chat_log import ChatLog
from app.core.db import get_db
from app.services.report_service import get_day_conversations, save_or_update_daily_report
from app.services.emotion_service import summarize_day_conversation

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. 챗봇 응답 생성
    output_text = chat_with_bot(req.input, req.session_id, req.persona)

    # 2. 대화 로그 저장
    log = ChatLog(USER_ID=req.session_id, SENDER=req.input, RESPONDER=output_text)
    db.add(log)
    db.commit()

    # 3. 대화 저장 후 → 당일 감정 리포트 자동 생성/업데이트
    today = datetime.now().strftime("%Y-%m-%d")
    messages = get_day_conversations(req.session_id, today, db)

    if messages:
        try:
            result = summarize_day_conversation(messages, req.session_id, today)
            save_or_update_daily_report(db, req.session_id, today, result)
        except Exception as e:
            print(f"리포트 생성 오류: {e}")

    return ChatResponse(output=output_text)