# app/main.py
from fastapi import FastAPI
from app.api import chat, roleplay, log, chat_end, report
from app.models.base import Base            # 수정된 Base
from app.core.db import engine              # DB 연결 유지


app = FastAPI(title="Milo 마음 돌봄 챗봇")

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(roleplay.router, prefix="/api/roleplay", tags=["Roleplay"])
app.include_router(log.router, prefix="/api/log", tags=["Log"])
app.include_router(chat_end.router, prefix="/api", tags = ["report"])
app.include_router(report.router, prefix="/api/reports")

@app.get("/")
def root():
    return {"message": "Milo 마음 돌봄 챗봇 API"}

