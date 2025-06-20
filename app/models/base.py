# app/models/base.py
from sqlalchemy.orm import declarative_base

# SQLAlchemy ORM Base 클래스 정의
# 모든 모델 클래스는 Base를 상속받아 정의됨
Base = declarative_base()
