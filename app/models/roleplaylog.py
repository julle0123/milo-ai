# app/models/role_play_log.py

from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

class RolePlayLog(Base):  
    __tablename__ = "role_play_log_TB"

    ROLE_CHAT_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)
    CHARACTER_ID = Column(BigInteger, ForeignKey("role_character_TB.CHARACTER_ID", ondelete="CASCADE"), nullable=False)
    SENDER = Column(Text, nullable=False)
    RESPONDER = Column(Text, nullable=False)
    CREATED_AT = Column(DateTime, nullable=False, server_default=func.now())
