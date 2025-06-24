# app/services/memory.py

from langchain_community.chat_message_histories import ChatMessageHistory
from sqlalchemy.orm import Session

# LangChain Agent에서 사용하는 히스토리 반환 함수
# 과거 대화 히스토리는 system prompt로 요약 삽입되므로 memory는 비워서 시작

def get_user_history(user_id: str, db: Session) -> ChatMessageHistory:
    return ChatMessageHistory()
