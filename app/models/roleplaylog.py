# app/models/role_play_log.py

from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

# 역할극 대화 로그 테이블
# 사용자와 정의된 역할 캐릭터 간의 대화 쌍을 저장
class RolePlayLog(Base):  
    __tablename__ = "role_play_log_TB"

    # 고유 역할 대화 ID
    ROLE_CHAT_ID = Column(BigInteger, primary_key=True, autoincrement=True)

    # 사용자 ID (users_TB.USER_ID 참조)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)

    # 캐릭터 ID (role_character_TB.CHARACTER_ID 참조)
    CHARACTER_ID = Column(BigInteger, ForeignKey("role_character_TB.CHARACTER_ID", ondelete="CASCADE"), nullable=False)

    # 사용자 입력 문장
    SENDER = Column(Text, nullable=False)

    # 캐릭터 응답 문장
    RESPONDER = Column(Text, nullable=False)

    # 생성 시각
    CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())
