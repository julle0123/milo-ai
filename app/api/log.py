from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.chat_log import ChatLog
from app.models.schemas import ChatLogCreate, ChatLogResponse

router = APIRouter()

@router.post("/", response_model=ChatLogResponse)
def create_chat_log(data: ChatLogCreate, db: Session = Depends(get_db)):
    new_log = ChatLog(**data.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log

@router.get("/{chat_id}", response_model=ChatLogResponse)
def read_chat_log(chat_id: int, db: Session = Depends(get_db)):
    log = db.query(ChatLog).filter(ChatLog.CHAT_ID == chat_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log
