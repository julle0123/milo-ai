# app/api/log.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.chat_log import ChatLog
from app.models.schemas import ChatLogCreate, ChatLogResponse

# 라우터 객체 생성 (챗봇 대화 로그 관련 API 등록 용도)
router = APIRouter()

# POST /log/
# 챗봇 대화 로그 1건 생성
# 입력 데이터: 사용자 ID, 발화문, 응답문 (ChatLogCreate)
# 처리: chat_log_TB에 레코드 저장 및 생성된 데이터 반환
@router.post("/", response_model=ChatLogResponse)
def create_chat_log(data: ChatLogCreate, db: Session = Depends(get_db)):
    new_log = ChatLog(**data.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

# GET /log/{chat_id}
# 특정 chat_id에 해당하는 대화 로그 1건 조회
# 처리: chat_log_TB에서 chat_id 기준으로 단건 조회
# 예외: 데이터 없을 경우 404 에러 반환
@router.get("/{chat_id}", response_model=ChatLogResponse)
def read_chat_log(chat_id: int, db: Session = Depends(get_db)):
    log = db.query(ChatLog).filter(ChatLog.CHAT_ID == chat_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log