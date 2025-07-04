# app/api/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
import pytz

from app.models.schemas import ChatRequest, ChatResponse
from app.graph.runner import run_chat
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport
from app.core.db import get_db
from app.services.emotion_service import get_user_nickname, get_emotion_trend_text

KST = timezone(timedelta(hours=9))
router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    output_text = await run_chat(
        user_input=req.input,
        user_id=req.user_id,
        db=db
    )

    db.add(ChatLog(USER_ID=req.user_id, SENDER=req.input, RESPONDER=output_text))
    db.commit()

    return ChatResponse(output=output_text)


@router.get("/init", response_model=ChatResponse)
def chat_initial_greeting(user_id: str, db: Session = Depends(get_db)):
    nickname = get_user_nickname(user_id, db)
    now_kst = datetime.now(KST)
    today = now_kst.date()
    yesterday = today - timedelta(days=1)

    today_report = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE == today
    ).first()

    yesterday_report = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE == yesterday
    ).first()

    last_report = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id
    ).order_by(DailyEmotionReport.DATE.desc()).first()

    trend = get_emotion_trend_text(user_id, db)

    if today_report:
        message = (
            f"{nickname}님, 방금 전까지 '{today_report.MAIN_EMOTION}' 감정을 느끼신 것 같아요. "
            f"대화를 이어가 볼까요?"
        )
    elif yesterday_report:
        message = (
            f"{nickname}님, 어제는 '{yesterday_report.MAIN_EMOTION}' 감정을 느끼셨던 것 같아요. "
            f"오늘은 어떤 기분이신가요?"
        )
    elif last_report:
        days_since = (today - last_report.DATE).days
        if days_since <= 3:
            message = f"{nickname}님, 며칠 만에 다시 뵙네요. 잘 지내셨어요?"
        elif days_since <= 7:
            message = f"{nickname}님, 일주일 가까이 소식이 없었네요. 무슨 일 있으셨어요?"
        else:
            message = f"{nickname}님, 오랜만이에요. 다시 찾아와 주셔서 반가워요."
    else:
        message = f"{nickname}님, 처음 만났네요. 편하게 이야기 나눠보면 좋겠어요."

    message += f"\n\n[최근 감정 흐름 요약]\n{trend}"
    return ChatResponse(output=message)