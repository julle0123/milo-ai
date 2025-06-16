from sqlalchemy.orm import Session
from datetime import datetime
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport

# 1. 하루 동안의 대화 메시지 추출
def get_day_conversations(user_id: str, date: str, db: Session) -> list[str]:
    date_start = datetime.strptime(date, "%Y-%m-%d")
    date_end = date_start.replace(hour=23, minute=59, second=59)

    chats = db.query(ChatLog).filter(
        ChatLog.USER_ID == user_id,
        ChatLog.CREATED_AT >= date_start,
        ChatLog.CREATED_AT <= date_end
    ).all()

    return [chat.SENDER for chat in chats] + [chat.RESPONDER for chat in chats]

# 2. 기존에 있다면 UPDATE, 없다면 INSERT
def save_or_update_daily_report(db: Session, user_id: str, date: str, result: dict):
    existing = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE == date
    ).first()

    if existing:
        for key, value in result.items():
            setattr(existing, key, value)
        existing.CREATED_AT = datetime.now()
    else:
        report = DailyEmotionReport(**result)
        db.add(report)

    db.commit()
