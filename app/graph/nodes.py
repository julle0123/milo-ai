from app.services.emotion_service import (
    get_user_nickname,
    get_emotion_trend_text,
    summarize_full_chat_history,
    extract_emotion_label
)
from app.services.report_service import save_or_update_daily_report
from app.services.rag_service import (
    retrieve_emotion_recovery_contents,
    retrieve_similar_cases_for_rag
)
from langchain_core.messages import SystemMessage
from app.graph.state import ChatState
from app.core.client import llm
from app.graph.prompts import load_prompt_template  # 프롬프트 불러오기
from sqlalchemy.orm import Session
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
import asyncio

# 1. 상태: 사용자 정보 및 트렌드 불러오기
async def load_context(state: ChatState, db: Session) -> ChatState:
    user_id = state["user_id"]
    user_input = state["user_input"]
    persona = state.get("persona", "emotional")

    # 동기 작업은 바로 처리
    nickname = get_user_nickname(user_id, db)
    trend = get_emotion_trend_text(user_id, db)

    loop = asyncio.get_event_loop()

    # GPT/벡터 작업 병렬 처리
    summary_task = loop.run_in_executor(None, lambda: summarize_full_chat_history(user_id, db))
    recovery_task = retrieve_emotion_recovery_contents(user_input)  # 이미 async
    retrieved_task = retrieve_similar_cases_for_rag(user_input)     # 이미 async

    summary, recovery, retrieved = await asyncio.gather(summary_task, recovery_task, retrieved_task)

    # 시스템 프롬프트 구성
    system_text = load_prompt_template(persona)
    system_text = system_text.replace("{nickname}", nickname)
    system_text += (
        f"\n\n[최근 감정 흐름 요약]\n{trend}"
        f"\n\n[전체 감정 요약]\n{summary}"
        f"\n\n[회복 콘텐츠 목록]\n{recovery}"
        f"\n\n[규칙] 위 정보를 반영해 정서적 피드백을 제공하세요."
    )

    return {
        **state,
        "input": user_input,
        "nickname": nickname,
        "trend": trend,
        "summary": summary,
        "recovery_candidates": recovery,
        "retrieved": retrieved,
        "system_text": system_text,
        "history": []
    }



# 2. 상태: GPT 응답 생성 (system prompt 포함)
async def generate_response(state: ChatState) -> ChatState:
    input_msg = HumanMessage(content=state["input"])
    history = state.get("history", [])

    # system prompt는 메시지 리스트에 SystemMessage로 추가
    messages = [SystemMessage(content=state["system_text"]), *history, input_msg]
    response = await llm.ainvoke(messages)

    return {
        **state,
        "output": response.content,
        "history": history + [input_msg, response]
    }