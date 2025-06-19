# app/services/memory.py
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session
from app.models.chat_log import ChatLog

# 메모리 저장소
session_histories = {}

def preload_chat_history(session_id: str, user_id: str, db: Session):
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.USER_ID == user_id)
        .order_by(ChatLog.CREATED_AT.asc())
        .all()
    )
    history = ChatMessageHistory()
    for log in logs:
        history.add_user_message(HumanMessage(content=log.SENDER))
        history.add_ai_message(AIMessage(content=log.RESPONDER))
    session_histories[session_id] = history

def get_session_history(session_id: str, config: dict = None) -> ChatMessageHistory:
    if session_id not in session_histories:
        if config and "user_id" in config and "db" in config:
            preload_chat_history(session_id, config["user_id"], config["db"])
        else:
            session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]
