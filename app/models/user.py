# app/models/user.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users_TB"
    USER_ID = Column(String(50), primary_key=True)
    PASSWORD = Column(String(100), nullable=False)
    NICKNAME = Column(String(50), nullable=True)
    EMAIL = Column(String(100), nullable=True)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
