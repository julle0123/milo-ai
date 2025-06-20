# app/main.py
from fastapi import FastAPI
from app.api import chat, roleplay, log, chat_end, report
from app.models.base import Base            # SQLAlchemy Base 모델
from app.core.db import engine              # DB 연결 유지

# FastAPI 앱 인스턴스 생성
app = FastAPI(title="Milo 마음 돌봄 챗봇")

# DB 테이블 생성 (서버 최초 실행 시 자동 반영)
# - models/base.py에 정의된 Base를 기준으로 생성됨
Base.metadata.create_all(bind=engine)
# 라우터 등록
# - chat: 일반 챗봇 대화 API
# - roleplay: 역할극 기반 감정 표현 API
# - log: ChatLog 단건 저장/조회 API
# - chat_end: 하루 대화 종료 및 일일 감정 리포트 생성 API
# - report: 월간 리포트 생성 및 요약 응답 API
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(roleplay.router, prefix="/api/roleplay", tags=["Roleplay"])
app.include_router(log.router, prefix="/api/log", tags=["Log"])
app.include_router(chat_end.router, prefix="/api", tags = ["daily_report"])
app.include_router(report.router, prefix="/api/reports", tags=["monthly_report"])

# 기본 루트 엔드포인트
@app.get("/")
def root():
    return {"message": "Milo 마음 돌봄 챗봇 API"}

