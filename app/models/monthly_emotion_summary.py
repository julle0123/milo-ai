from sqlalchemy import Column, BigInteger, String, Date, Integer, Float, Text, DateTime, UniqueConstraint, func
from app.models.base import Base

class MonthlyEmotionReport(Base):
    __tablename__ = "monthly_emotion_summary_TB"

    summary_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(50), nullable=False)
    year_months = Column(Date, nullable=False)  # 2025-06-01
    total_sessions = Column(Integer, default=0, nullable=False)

    avg_stable = Column(Float, default=0)
    avg_joy = Column(Float, default=0)
    avg_sadness = Column(Float, default=0)
    avg_anger = Column(Float, default=0)
    avg_anxiety = Column(Float, default=0)

    dominant_emotion = Column(String(20))
    gpt_feedback = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("user_id", "year_months"),)
