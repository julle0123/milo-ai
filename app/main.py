# app/main.py
from fastapi import FastAPI
from app.api import chat
from app.api import roleplay
from app.api import log

app = FastAPI(title="Milo 마음 돌봄 챗봇")

# 기본 감정형/실용형 상담 라우터 등록
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(roleplay.router, prefix="/api/roleplay", tags=["Roleplay"])  
app.include_router(log.router, prefix="/api/log", tags=["Log"])

# 기본 루트 엔드포인트
@app.get("/")
def root():
    return {"message": "Milo 마음 돌봄 챗봇 API"}