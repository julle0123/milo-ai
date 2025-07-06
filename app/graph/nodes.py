# app/graph/nodes.py
from app.graph.state import ChatState
from app.services.emotion_service import (
    get_user_nickname,
    get_emotion_trend_text,
    summarize_full_chat_history,
    analyze_emotion_gpt,
)
from app.services.rag_service import (
    retrieve_emotion_recovery_contents,
    retrieve_similar_cases_for_rag
)
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.core.client import llm
from app.graph.prompts import load_prompt_template
from sqlalchemy.orm import Session
import asyncio

# Async Memory Wrapper
class AsyncMemoryWrapper:
    def __init__(self, memory):
        self.memory = memory

    async def aget_messages(self):
        result = await asyncio.to_thread(self.memory.load_memory_variables, {})
        return result["history"]

    async def asave_context(self, inputs, outputs):
        await asyncio.to_thread(self.memory.save_context, inputs, outputs)

    async def aclear(self):
        await asyncio.to_thread(self.memory.clear)

# session_id -> memory 객체 생성
def get_memory(session_id: str):
    base_memory = ConversationBufferMemory(
        return_messages=True,
        memory_key="history"
    )
    return AsyncMemoryWrapper(base_memory)

# 컨텍스트 로딩 노드 (속도 개선 적용)
def get_load_context_node(db: Session):
    async def load_context_and_tools(state: ChatState) -> ChatState:
        user_id = state["user_id"]
        user_input = state["user_input"]
        persona = state.get("persona", "emotional")

        nickname = get_user_nickname(user_id, db)
        trend = get_emotion_trend_text(user_id, db)

        # ✅ GPT 호출 병렬 처리 최적화
        loop = asyncio.get_event_loop()
        summary_task = loop.run_in_executor(None, lambda: asyncio.run(summarize_full_chat_history(user_id, db)))
        emotion_task = analyze_emotion_gpt(user_input)
        retrieved_task = retrieve_similar_cases_for_rag(user_input)
        recovery_task = retrieve_emotion_recovery_contents(user_input)

        summary, emotion_result, retrieved, recovery = await asyncio.gather(
            summary_task, emotion_task, retrieved_task, recovery_task, return_exceptions=True
        )

        summary = summary if not isinstance(summary, Exception) else "[요약 오류 발생]"
        emotion_result = emotion_result if not isinstance(emotion_result, Exception) else "[감정 분석 오류 발생]"
        retrieved = retrieved if not isinstance(retrieved, Exception) else "[유사 사례 오류 발생]"
        recovery = recovery if not isinstance(recovery, Exception) else "[회복 콘텐츠 오류 발생]"

        system_text = load_prompt_template(persona).replace("{nickname}", nickname)
        system_text += (
            f"\n\n[최근 감정 흐름 요약]\n{trend}"
            f"\n\n[전체 감정 요약]\n{summary}"
            f"\n\n[회복 콘텐츠 목록]\n{recovery}"
            f"\n\n[유사 감정 사례]\n{retrieved}"
            f"\n\n[규칙] 위 정보를 반영해 정서적 피드백을 제공하세요."
        )

        return {
            **state,
            "input": user_input,
            "nickname": nickname,
            "trend": trend,
            "summary": summary,
            "emotion_result": emotion_result,
            "retrieved": retrieved,
            "recovery_candidates": recovery,
            "system_text": system_text,
            "history": []
        }
    return load_context_and_tools

# GPT 응답 생성 노드 (Memory 포함)
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_text}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

generate_response = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="input",
    history_messages_key="history"
)

def get_respond_node():
    async def respond_node(state: ChatState):
        result = await generate_response.ainvoke(
            state, config={"configurable": {"session_id": state["session_id"]}}
        )
        return {**state, "output": result.content}
    return respond_node