# app/api/report.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.report_service import generate_monthly_report_from_daily
from app.models.schemas import MonthlyReportRequest

router = APIRouter()

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
