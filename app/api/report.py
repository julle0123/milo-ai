from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.report_service import generate_monthly_report_from_daily
from app.models.schemas import MonthlyReportRequest

router = APIRouter()

@router.post("/monthly/{year}/{month}")
def trigger_monthly_report(year: int, month: int, body: MonthlyReportRequest, db: Session = Depends(get_db)):
    report = generate_monthly_report_from_daily(db, user_id=body.user_id, year=year, month=month)
    return {
        "status": "success",
        "year_month": report.year_months,
        "dominant_emotion": report.dominant_emotion,
        "summary": report.gpt_feedback
    }
