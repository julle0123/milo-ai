# app/models/user.py
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.models.base import Base  

class User(Base):
    __tablename__ = "users_TB"
    USER_ID = Column(String(50), primary_key=True)
    PASSWORD = Column(String(100), nullable=False)
    NICKNAME = Column(String(50), nullable=True)
    EMAIL = Column(String(100), nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
