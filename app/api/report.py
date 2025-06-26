# app/api/report.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.report_service import generate_monthly_report_from_daily
from app.models.schemas import MonthlyReportRequest

# 라우터 객체 생성 (월간 리포트 관련 API 등록 용도)
router = APIRouter()

# POST /monthly/{year}/{month}
# 특정 연도-월에 대한 월간 감정 리포트 생성 요청
# 입력: 연도, 월 (path parameter) + user_id (body)
# 처리: daily_emotion_report_TB의 데이터를 기반으로 집계 후 monthly_emotion_summary_TB에 저장
# 출력: 요약 생성 결과 (대표 감정, GPT 요약 등)
@router.post("/monthly/{year}/{month}")
def trigger_monthly_report(year: int, month: int, body: MonthlyReportRequest, db: Session = Depends(get_db)):
    report = generate_monthly_report_from_daily(db, user_id=body.user_id, year=year, month=month)

    if report is None:
        raise HTTPException(
            status_code=404,
            detail=f"{year}년 {month}월의 월간 리포트를 생성할 수 없습니다. 충분한 일간 데이터가 없을 수 있습니다."
        )

    return {
        "status": "success",
        "year_month": report.year_months,
        "dominant_emotion": report.dominant_emotion,
        "summary": report.gpt_feedback
    }

