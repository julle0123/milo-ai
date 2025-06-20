from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# SQLAlchemy 엔진 생성 (MySQL + PyMySQL)
engine = create_engine(
    settings.database_url, 
    echo=True # 쿼리 로그 출력 (개발용)
)

# 세션 팩토리 설정 (autocommit, autoflush 비활성화)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# FastAPI에서 사용할 DB 세션 의존성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db # 의존성 주입 시 사용
    finally:
        db.close()