# app/api/chat_end.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.db import get_db
from app.services.report_service import get_day_conversations, save_or_update_daily_report
from app.services.emotion_service import summarize_day_conversation

router = APIRouter()

@router.post("/session/end")
async def end_session(user_id: str, db: Session = Depends(get_db)):
    today = datetime.now().strftime("%Y-%m-%d")
    messages = get_day_conversations(user_id, today, db)

    if messages:
        try:
            result = await summarize_day_conversation(messages, user_id, today)

            required_keys = {
                "MAIN_EMOTION", "SCORE", "STABLE", "JOY", "SADNESS", "ANGER",
                "ANXIETY", "SUMMARY", "FEEDBACK", "ENCOURAGEMENT"
            }
            missing_keys = required_keys - result.keys()
            if missing_keys:
                raise ValueError(f"누락된 키 존재: {missing_keys}")

            await save_or_update_daily_report(db, user_id, today, result)

            return {"status": "saved", "main_emotion": result["MAIN_EMOTION"]}

        except Exception as e:
            msg = f"{e}"
            return {"status": "error", "message": msg}
    else:
        return {"status": "no_messages"}