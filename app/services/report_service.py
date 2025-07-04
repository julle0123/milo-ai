# app/services/report_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date, timezone
from app.models.chat_log import ChatLog
from app.models.daily_emotion_report import DailyEmotionReport
from app.models.monthly_emotion_summary import MonthlyEmotionReport
from sqlalchemy.exc import SQLAlchemyError
from openai import OpenAI
from app.core.config import settings
from collections import defaultdict
import asyncio
import json

KST = timezone(timedelta(hours=9))

# GPT 호출 클라이언트 (OpenAI API)
client = OpenAI(api_key=settings.openai_api_key)

# 1. 하루 동안의 대화 메시지 추출
# - sender, responder 모두 포함
# - 날짜 기준으로 00:00 ~ 23:59까지 포함
def get_day_conversations(user_id: str, date: str, db: Session) -> list[str]:
    date_start = datetime.strptime(date, "%Y-%m-%d")
    date_end = date_start + timedelta(days=1)

    chats = db.query(ChatLog).filter(
        ChatLog.USER_ID == user_id,
        ChatLog.CREATED_AT >= date_start,
        ChatLog.CREATED_AT < date_end
    ).all()

    return [chat.SENDER for chat in chats] + [chat.RESPONDER for chat in chats]

# 2. 하루 감정 분석 결과 저장 (daily_emotion_report_TB)
# - 기존 데이터 있으면 UPDATE, 없으면 INSERT
# - 저장 후, 해당 월 일별 리포트가 3개 이상이면 → 월간 리포트 자동 생성
async def save_or_update_daily_report(db: Session, user_id: str, date_str: str, result: dict):
    def sync_save(db: Session, user_id: str, date_str: str, result: dict):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # 기존 리포트 존재 여부 확인
            existing = db.query(DailyEmotionReport).filter(
                DailyEmotionReport.USER_ID == user_id,
                DailyEmotionReport.DATE == date_obj
            ).first()

            # 저장할 값 정리
            result_to_save = {
                "USER_ID": user_id,
                "DATE": date_obj,
                "CREATED_AT": datetime.now(KST),
                "MAIN_EMOTION": result.get("MAIN_EMOTION"),
                "SCORE": result.get("SCORE"),
                "STABLE": result.get("STABLE"),
                "JOY": result.get("JOY"),
                "SADNESS": result.get("SADNESS"),
                "ANGER": result.get("ANGER"),
                "ANXIETY": result.get("ANXIETY"),
                "SUMMARY": result.get("SUMMARY"),
                "FEEDBACK": result.get("FEEDBACK"),
                "ENCOURAGEMENT": result.get("ENCOURAGEMENT")
            }
            
            # UPDATE 또는 INSERT 수행
            if existing:
                print("기존 리포트 있음 → UPDATE 강제 수행")
                diffs = []
                for emotion in ["JOY", "SADNESS", "ANGER", "ANXIETY", "STABLE"]:
                    prev = getattr(existing, emotion)
                    curr = result_to_save[emotion]
                    delta = round(curr - prev, 4)
                    diffs.append(f"{emotion}: {prev:.3f} → {curr:.3f} (Δ {delta:+.4f})")
                print("[변동 로그]", " / ".join(diffs))
                for key, value in result_to_save.items():
                    try:
                        setattr(existing, key, value)
                        print(f"필드 '{key}' 덮어쓰기 완료")
                    except Exception as e:
                        print(f"필드 '{key}' 설정 중 오류 발생: {e}")
            else:
                print("리포트 없음 → INSERT 시도")
                report = DailyEmotionReport(**result_to_save)
                db.add(report)

            db.commit()

            # INSERT 또는 UPDATE 완료 로그
            if not existing:
                db.refresh(report)
                print("INSERT 완료 후 MAIN_EMOTION:", report.MAIN_EMOTION)
            else:
                db.refresh(existing)
                print("UPDATE 완료 후 MAIN_EMOTION:", existing.MAIN_EMOTION)

            # 월간 리포트 자동 생성 조건 확인 (해당 월에 3개 이상이면)
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
    
    # sync 함수를 run_in_executor로 비동기 래핑
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: sync_save(db, user_id, date_str, result))

# 3. GPT 기반 월간 요약 문장 생성
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
        temperature=0.4,
        max_tokens=400
    )
    return res.choices[0].message.content.strip()

# 4. 월간 리포트 생성 or 업데이트
# - 해당 월의 Daily 리포트들을 평균내어 감정 통계 생성
# - 가장 높은 감정을 대표 감정으로 지정
# - GPT 총평과 함께 MonthlyEmotionReport에 저장
def generate_monthly_report_from_daily(db: Session, user_id: str, year: int, month: int):
    first_day = date(year, month, 1)
    next_month = date(year + int(month == 12), (month % 12) + 1, 1)

    # 해당 월의 일일 리포트 조회
    daily_reports = db.query(DailyEmotionReport).filter(
        DailyEmotionReport.USER_ID == user_id,
        DailyEmotionReport.DATE >= first_day,
        DailyEmotionReport.DATE < next_month
    ).all()

    if len(daily_reports) < 3:
        print(f"{len(daily_reports)}건밖에 없어 월간 리포트 생략됨")
        return None

    # 감정 벡터 평균 계산
    emotion_sum = defaultdict(float)
    for r in daily_reports:
        emotion_sum["joy"] += r.JOY
        emotion_sum["sadness"] += r.SADNESS
        emotion_sum["anger"] += r.ANGER
        emotion_sum["anxiety"] += r.ANXIETY
        emotion_sum["stable"] += r.STABLE

    count = len(daily_reports)
    averages = {k: round(emotion_sum[k] / count, 3) for k in emotion_sum}
    summary = gpt_generate_monthly_summary(averages, count, f"{year}-{month:02d}")
    dominant = max(averages, key=averages.get) # 대표 감정 선정

    # 기존 월간 리포트가 있으면 UPDATE, 없으면 INSERT
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

# 5. 전체 감정 리포트 요약 텍스트로 반환
# - 날짜 + 대표 감정 + 요약문 조합으로 리스트 구성
def get_all_summaries(user_id: str, db: Session) -> str:
    rows = (
        db.query(
            DailyEmotionReport.DATE,
            DailyEmotionReport.MAIN_EMOTION,
            DailyEmotionReport.SUMMARY
        )
        .filter(DailyEmotionReport.USER_ID == user_id)
        .order_by(DailyEmotionReport.DATE.asc())
        .all()
    )
    if not rows:
        return "감정 요약 데이터가 없습니다."

    lines = [f"{r.DATE} - {r.MAIN_EMOTION}: {r.SUMMARY}" for r in rows]
    return "\n".join(lines)

