from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

# 역할극 챗봇에서 사용하는 사용자 정의 역할 캐릭터 테이블
# 사용자당 하나의 캐릭터만 등록 가능 (제약은 서비스 로직에서 처리)
class RoleCharacter(Base):
    __tablename__ = "role_character_TB"

    # 캐릭터 고유 ID
    CHARACTER_ID = Column(BigInteger, primary_key=True, autoincrement=True)

    # 사용자 ID (users_TB.USER_ID 참조)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)

    # 캐릭터 이름
    NAME = Column(String(50), nullable=False)

    # 사용자와의 관계 (ex. 친구, 가족 등)
    RELATIONSHIP = Column(String(50), nullable=False)

    # 말투 스타일 (ex. 부드럽게, 직설적으로 등)
    TONE = Column(String(50), nullable=False)

    # 성격 설명
    PERSONALITY = Column(Text, nullable=False)

    # 상황 설명
    SITUATION = Column(Text, nullable=False)

    # 생성 시각
    CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())
