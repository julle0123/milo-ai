# app/models/daily_emotion_report.py
from sqlalchemy import Column, BigInteger, String, Float, Text, DateTime, Date, ForeignKey, UniqueConstraint
from datetime import datetime
from app.models.base import Base  # ✅ 통합 Base 사용

class DailyEmotionReport(Base):
    __tablename__ = "daily_emotion_report_TB"
    __table_args__ = (
        UniqueConstraint("USER_ID", "DATE", name="uix_user_date"),
    )

    REPORT_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)
    DATE = Column(Date, nullable=False)
    MAIN_EMOTION = Column(String(20), nullable=False)
    SCORE = Column(Float, nullable=False)
    STABLE = Column(Float, nullable=False)
    JOY = Column(Float, nullable=False)
    SADNESS = Column(Float, nullable=False)
    ANGER = Column(Float, nullable=False)
    ANXIETY = Column(Float, nullable=False)
    SUMMARY = Column(Text, nullable=False)
    FEEDBACK = Column(Text, nullable=False)
    ENCOURAGEMENT = Column(Text, nullable=False)
    CREATED_AT = Column(DateTime, default=datetime.now, nullable=False)
