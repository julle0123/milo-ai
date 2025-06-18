# app/api/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import chat_with_bot
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport
from app.core.db import get_db
from app.services.emotion_service import get_user_nickname, get_emotion_trend_text

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. 챗봇 응답 생성
    output_text = chat_with_bot(
    user_input=req.input,
    session_id=req.session_id,   # None 이면 내부에서 uuid 생성
    user_id=req.user_id,
    persona=req.persona,
    db=db
)

    # 2. 대화 로그 저장만 수행
    log = ChatLog(USER_ID=req.user_id, SENDER=req.input, RESPONDER=output_text)
    db.add(log)
    db.commit()

    return ChatResponse(output=output_text)


@router.get("/init", response_model=ChatResponse)
def chat_initial_greeting(user_id: str, db: Session = Depends(get_db)):
    nickname = get_user_nickname(user_id, db)
    trend = get_emotion_trend_text(user_id, db)

    yesterday = datetime.now().date() - timedelta(days=1)

    report = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE == yesterday
    ).first()

    if report:
        message = (
            f"{nickname}님, 어제는 '{report.MAIN_EMOTION}' 감정이 드셨던 것 같아요. "
            f"오늘은 어떤 기분이신가요?"
        )
    else:
        message = f"{nickname}님, 처음 만났네요. 편하게 이야기 나눠보면 좋겠어요."

    message += f"\n\n[최근 감정 흐름 요약]\n{trend}"

    return ChatResponse(output=message)
