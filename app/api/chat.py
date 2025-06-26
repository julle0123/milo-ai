# app/api/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz

from app.models.schemas import ChatRequest, ChatResponse
from app.services.agent import chat_with_bot
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport
from app.core.db import get_db
from app.services.emotion_service import get_user_nickname, get_emotion_trend_text

# 라우터 객체 생성 (챗봇 세션 관련 API 등록 용도)
router = APIRouter()

# POST /session/end
# 하루 대화 종료 시 감정 요약 분석 후 DB에 감정 리포트 저장
# 사용자는 하루 대화를 종료하고, 시스템은 그 시점의 감정을 기록
@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    output_text = chat_with_bot(
        user_input=req.input,
        session_id=req.user_id,
        user_id=req.user_id,
        persona=req.persona,
        db=db,
        force_summary=req.force_summary,
    )

    db.add(ChatLog(USER_ID=req.user_id, SENDER=req.input, RESPONDER=output_text))
    db.commit()

    return ChatResponse(output=output_text)

# GET /init
# 첫 진입 시 사용자에게 인사말 + 감정 흐름 요약 제공
@router.get("/init", response_model=ChatResponse)
def chat_initial_greeting(user_id: str, db: Session = Depends(get_db)):
    # 1. 사용자 닉네임 조회
    nickname = get_user_nickname(user_id, db)

    # 2. 최근 감정 흐름 요약 텍스트 생성
    trend = get_emotion_trend_text(user_id, db)

    # 3. 한국(KST) 기준 오늘/어제 날짜 계산
    korea = pytz.timezone("Asia/Seoul")
    now_kst = datetime.now(korea)
    today = now_kst.date()
    yesterday = today - timedelta(days=1)

    # 4. 오늘/어제 감정 리포트 조회
    today_report = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE == today
    ).first()

    yesterday_report = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE == yesterday
    ).first()

    # 5. 조건에 따른 인삿말 분기
    if today_report is not None:
        message = (
            f"{nickname}님, 방금 전까지 '{today_report.MAIN_EMOTION}' 감정을 느끼신 것 같아요. "
            f"대화를 이어가 볼까요?"
        )
    elif yesterday_report is not None:
        message = (
            f"{nickname}님, 어제는 '{yesterday_report.MAIN_EMOTION}' 감정이 드셨던 것 같아요. "
            f"오늘은 어떤 기분이신가요?"
        )
    else:
        message = f"{nickname}님, 처음 만났네요. 편하게 이야기 나눠보면 좋겠어요."

    # 6. 감정 흐름 요약 추가
    message += f"\n\n[최근 감정 흐름 요약]\n{trend}"

    return ChatResponse(output=message)
