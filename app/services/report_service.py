# app/services/report_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport
from sqlalchemy.exc import SQLAlchemyError

# 1. 하루 동안의 대화 메시지 추출
def get_day_conversations(user_id: str, date: str, db: Session) -> list[str]:
    date_start = datetime.strptime(date, "%Y-%m-%d")
    date_end = date_start + timedelta(days=1)  # 다음 날 00:00:00

    chats = db.query(ChatLog).filter(
        ChatLog.USER_ID == user_id,
        ChatLog.CREATED_AT >= date_start,
        ChatLog.CREATED_AT < date_end  # 다음 날 0시 미만까지 포함
    ).all()

    return [chat.SENDER for chat in chats] + [chat.RESPONDER for chat in chats]


def save_or_update_daily_report(db: Session, user_id: str, date: str, result: dict):

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        existing = db.query(DailyEmotionReport).filter(
            DailyEmotionReport.USER_ID == user_id,
            DailyEmotionReport.DATE == date_obj
        ).first()

        result["USER_ID"] = user_id
        result["DATE"] = date_obj
        result["CREATED_AT"] = datetime.now()

        if existing:
            print("기존 리포트 있음 → UPDATE 시도")
            for key, value in result.items():
                setattr(existing, key, value)
        else:
            print("리포트 없음 → INSERT 시도")
            report = DailyEmotionReport(**result)
            db.add(report)

        db.commit()
        print("DB 저장 성공")
    except SQLAlchemyError as e:
        db.rollback()
        print("DB 저장 실패:", str(e))
        raise