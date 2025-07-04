# app/models/user.py
from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from app.models.base import Base  

# 사용자 테이블
# 기본 회원가입 정보 저장 (인증, 감정 로그 연동 등)
class User(Base):
    __tablename__ = "users_TB"

    # 사용자 ID (PK)
    USER_ID = Column(String(50), primary_key=True)

    # 비밀번호 (암호화 저장 권장)
    PASSWORD = Column(String(100), nullable=True)

    # 사용자 닉네임 (선택)
    NICKNAME = Column(String(50), nullable=True)

    # 이메일 주소 (선택)
    EMAIL = Column(String(100), nullable=True)

    # 가입 시각
    CREATED_AT = Column(DateTime, default=datetime.utcnow)

    EMOTION_PROMPT = Column(Boolean, default=False)
    
    provider = Column(String(20), default="local")
    
    provider_id = Column(String(100), nullable=True)