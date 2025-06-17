# app/models/chat_log.py
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.models.base import Base

class ChatLog(Base):
    __tablename__ = "chat_log_TB"

    CHAT_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    USER_ID = Column(String(50), ForeignKey("users_TB.USER_ID", ondelete="CASCADE"), nullable=False)
    SENDER = Column(Text, nullable=False)
    RESPONDER = Column(Text, nullable=False)
    CREATED_AT = Column(DateTime, default=datetime.now, nullable=False)
