# app/services/context_service.py

import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.services.emotion_service import (
    get_user_nickname,
    get_emotion_trend_text,
    summarize_full_chat_history,
    extract_emotion_label
)
from app.services.rag_service import (
    retrieve_emotion_recovery_contents,
    retrieve_similar_cases_for_rag
)
from app.graph.prompts import load_prompt_template

async def load_context_parallel(user_id: str, user_input: str, persona: str, db: Session) -> dict:
    nickname_task = asyncio.to_thread(get_user_nickname, user_id, db)
    trend_task = asyncio.to_thread(get_emotion_trend_text, user_id, db)
    summary_task = asyncio.to_thread(summarize_full_chat_history, user_id, db)
    recovery_task = retrieve_emotion_recovery_contents(user_input)
    retrieved_task = retrieve_similar_cases_for_rag(user_input)

    nickname, trend, summary, recovery, retrieved = await asyncio.gather(
        nickname_task, trend_task, summary_task, recovery_task, retrieved_task
    )

    system_text = load_prompt_template(persona)
    system_text = system_text.replace("{nickname}", nickname)
    system_text += (
        f"\n\n[최근 감정 흐름 요약]\n{trend}"
        f"\n\n[전체 감정 요약]\n{summary}"
        f"\n\n[회복 콘텐츠 목록]\n{recovery}"
        f"\n\n[규칙] 위 정보를 반영해 정서적 피드백을 제공하세요."
    )

    return {
        "input": user_input,
        "nickname": nickname,
        "trend": trend,
        "summary": summary,
        "recovery_candidates": recovery,
        "retrieved": retrieved,
        "system_text": system_text,
        "history": []
    }
