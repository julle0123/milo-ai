# app/services/memory.py
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session
from app.models.chat_log import ChatLog

# 세션 히스토리 저장소 (In-memory 기반)[초기화용]
# - 각 session_id → ChatMessageHistory 객체로 저장
# - 역할극과 일반 챗봇 공통 사용 가능
session_histories = {}

# DB에서 과거 대화 이력을 불러와 메모리에 적재
# - 주로 세션 최초 호출 시 실행됨
# - session_id를 기준으로 history 생성
# - 순서 보장 위해 CREATED_AT 오름차순 정렬
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

# 세션 ID 기준으로 메모리 반환 [조회용] 
# - 세션이 존재하지 않을 경우, DB에서 preload 수행 (필요시)
# - config에는 "user_id", "db" 포함되어야 DB에서 preload 가능
# - config가 없으면 빈 히스토리 객체 생성
def get_session_history(session_id: str, config: dict = None) -> ChatMessageHistory:
    if session_id not in session_histories:
        if config and "user_id" in config and "db" in config:
            preload_chat_history(session_id, config["user_id"], config["db"])
        else:
            session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]
