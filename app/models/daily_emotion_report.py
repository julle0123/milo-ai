# app/models/daily_emotion_report.py
from sqlalchemy import Column, BigInteger, String, Float, Text, DateTime, Date, ForeignKey, UniqueConstraint
from datetime import datetime
from app.models.base import Base 

# 하루 단위 감정 리포트 테이블
# 사용자별로 하루에 하나의 리포트만 저장됨 (USER_ID + DATE 유니크)
class DailyEmotionReport(Base):
    __tablename__ = "daily_emotion_report_TB"
    __table_args__ = (
        UniqueConstraint("USER_ID", "DATE", name="uix_user_date"), # 사용자-날짜 조합 유니크 제약
    )

    # 고유 리포트 ID
    REPORT_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # 사용자 ID (users_TB.USER_ID 참조)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)
    
    # 리포트 기준 날짜 (YYYY-MM-DD)
    DATE = Column(Date, nullable=False)
    
    # 대표 감정
    MAIN_EMOTION = Column(String(20), nullable=False)
    
    # 전체 감정 종합 점수
    SCORE = Column(Float, nullable=False)
    
    # 감정별 스코어
    STABLE = Column(Float, nullable=False)
    JOY = Column(Float, nullable=False)
    SADNESS = Column(Float, nullable=False)
    ANGER = Column(Float, nullable=False)
    ANXIETY = Column(Float, nullable=False)
    
    # GPT 기반 요약 텍스트
    SUMMARY = Column(Text, nullable=False)
    FEEDBACK = Column(Text, nullable=False)
    ENCOURAGEMENT = Column(Text, nullable=False)
    
    # 리포트 생성 시각
    CREATED_AT = Column(DateTime, default=datetime.now, nullable=False)
