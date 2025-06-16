# app/services/memory.py
from langchain_community.chat_message_histories import ChatMessageHistory

# 세션별 대화 기록을 메모리로 관리
session_histories = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in session_histories:
        session_histories[session_id] = ChatMessageHistory()
    return session_histories[session_id]
