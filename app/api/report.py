from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.report_service import generate_monthly_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/monthly/{year}/{month}")
def trigger_monthly_report(year: int, month: int, db: Session = Depends(get_db)):
    report = generate_monthly_report(db, user_id="demo", year=year, month=month)
    return {
        "status": "success",
        "year_month": report.year_months,
        "dominant_emotion": report.dominant_emotion,
        "summary": report.gpt_feedback
    }
