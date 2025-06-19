# app/services/report_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport
from app.models.monthly_emotion_summary import MonthlyEmotionReport
from sqlalchemy.exc import SQLAlchemyError
from openai import OpenAI
from app.core.config import settings
from collections import defaultdict
import json

client = OpenAI(api_key=settings.openai_api_key)

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
        # daily report 저장 후, 월간 리포트도 조건부 갱신
        year = date_obj.year
        month = date_obj.month
        first_day = date(year, month, 1)
        next_month = date(year + int(month == 12), (month % 12) + 1, 1)

        daily_reports = db.query(DailyEmotionReport).filter(
            DailyEmotionReport.USER_ID == user_id,
            DailyEmotionReport.DATE >= first_day,
            DailyEmotionReport.DATE < next_month
        ).all()

        if len(daily_reports) >= 3:
            print("3개 이상 일일 리포트 존재 → 월간 리포트 생성 시도")
            generate_monthly_report_from_daily(db, user_id, year, month)

    except SQLAlchemyError as e:
        db.rollback()
        print("DB 저장 실패:", str(e))
        raise
    
def gpt_generate_monthly_summary(avg_scores: dict, session_count: int, ym: str) -> str:
    prompt = f"""
    다음은 {ym} 한 달간 사용자의 감정 평균 점수입니다.
    - 감정 점수: {avg_scores}
    - 총 상담 횟수: {session_count}
    이 데이터를 바탕으로 아래 내용을 작성해주세요:
    [지침 사항]
    1) 점수 데이터를 바탕으로 하는건 좋으나 감정을 수치화, 점수화하여 적지말것.
    1) 한 문단 총평 (따뜻하고 공감되는 어조)
    2) 긍정적 변화를 말해주세요. 
    3) 개선을 위한 제안 2가지
    각 항목을 줄바꿈으로 구분하세요.
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 공감에 기반한 심리상담가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=400
    )
    return res.choices[0].message.content.strip()



def generate_monthly_report_from_daily(db: Session, user_id: str, year: int, month: int):
    first_day = date(year, month, 1)
    next_month = date(year + int(month == 12), (month % 12) + 1, 1)

    daily_reports = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE >= first_day,
        DailyEmotionReport.DATE < next_month
    ).all()

    if len(daily_reports) < 3:
        print(f"❌ {len(daily_reports)}건밖에 없어 월간 리포트 생략됨")
        return None

    emotion_sum = defaultdict(float)
    for r in daily_reports:
        emotion_sum["joy"] += r.JOY
        emotion_sum["sadness"] += r.SADNESS
        emotion_sum["anger"] += r.ANGER
        emotion_sum["anxiety"] += r.ANXIETY
        emotion_sum["stable"] += r.STABLE

    count = len(daily_reports)
    averages = {k: round(emotion_sum[k]/count, 3) for k in emotion_sum}
    summary = gpt_generate_monthly_summary(averages, count, f"{year}-{month:02d}")
    dominant = max(averages, key=averages.get)

    existing = db.query(MonthlyEmotionReport).filter_by(user_id=user_id, year_months=first_day).first()
    if existing:
        existing.total_sessions = count
        existing.gpt_feedback = summary
        existing.dominant_emotion = dominant
        for k in averages:
            setattr(existing, f"avg_{k}", averages[k])
    else:
        report = MonthlyEmotionReport(
            user_id=user_id,
            year_months=first_day,
            total_sessions=count,
            gpt_feedback=summary,
            dominant_emotion=dominant,
            **{f"avg_{k}": v for k, v in averages.items()}
        )
        db.add(report)

    db.commit()
    return existing if existing else report