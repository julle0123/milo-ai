from sqlalchemy import Column, BigInteger, String, Date, Integer, Float, Text, DateTime, UniqueConstraint, func
from app.models.base import Base

# 월간 감정 리포트 테이블
# daily_emotion_report_TB를 기반으로 집계됨
# 사용자 ID + 연월 기준으로 유니크하게 관리
class MonthlyEmotionReport(Base):
    __tablename__ = "monthly_emotion_summary_TB"

 # 고유 리포트 ID
    summary_id = Column(BigInteger, primary_key=True, autoincrement=True)

    # 사용자 ID
    user_id = Column(String(50), nullable=False)

    # 리포트 기준 연월 (예: 2025-06-01)
    year_months = Column(Date, nullable=False)

    # 월간 상담 횟수
    total_sessions = Column(Integer, default=0, nullable=False)

    # 감정별 평균 점수
    avg_stable = Column(Float, default=0)
    avg_joy = Column(Float, default=0)
    avg_sadness = Column(Float, default=0)
    avg_anger = Column(Float, default=0)
    avg_anxiety = Column(Float, default=0)

    # 가장 강하게 나타난 대표 감정
    dominant_emotion = Column(String(20))

    # GPT 기반 총평 요약
    gpt_feedback = Column(Text)

    # 생성 시각 (자동 기록)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 수정 시각 (자동 갱신)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 사용자-연월 조합에 대한 유니크 제약
    __table_args__ = (UniqueConstraint("user_id", "year_months"),)
