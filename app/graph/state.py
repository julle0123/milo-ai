# app/graph/state.py

from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage

class ChatState(TypedDict, total=False):
    user_input: str
    user_id: str
    session_id: str

    # 컨텍스트 정보
    nickname: str
    trend: str
    summary: str
    retrieved: str
    recovery_candidates: str

    # GPT Tool 결과
    emotion_result: str
    
    system_text: str         
    input: str              
    # 대화 기록
    history: List[BaseMessage]

    # GPT 응답
    output: str
