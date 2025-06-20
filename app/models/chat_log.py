# app/models/chat_log.py
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base

# 챗봇 대화 로그 테이블
# 사용자 입력과 챗봇 응답 쌍을 저장하며, 시계열 정렬 가능
class ChatLog(Base):
    # 테이블 이름
    __tablename__ = "chat_log_TB"

    # 고유 대화 ID (자동 증가)
    CHAT_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # 사용자 ID (users_TB.USER_ID 참조, 탈퇴 시 연쇄 삭제)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)
    
    # 사용자 입력 문장
    SENDER = Column(Text, nullable=False)
    
    # 챗봇 응답 문장
    RESPONDER = Column(Text, nullable=False)
    
    # 대화 생성 시각
    CREATED_AT = Column(DateTime, default=datetime.now, nullable=False)
