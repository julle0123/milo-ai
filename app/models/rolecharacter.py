from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

class RoleCharacter(Base):
    __tablename__ = "role_character_TB"

    CHARACTER_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)
    NAME = Column(String(50), nullable=False)
    RELATIONSHIP = Column(String(50), nullable=False)
    TONE = Column(String(50), nullable=False)
    PERSONALITY = Column(Text, nullable=False)
    SITUATION = Column(Text, nullable=False)
    CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())
