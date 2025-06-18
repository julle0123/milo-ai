import uuid
from typing import Optional                # ✅ Optional 정의
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from app.core.client import llm
from app.services.memory import get_session_history
from app.services.emotion_service import (
    get_emotion_trend_text,
    analyze_emotion_gpt,
    get_user_nickname
)
from app.services.rag_service import retrieve_similar_cases_for_rag

# ───── LangChain tool 등록 ────────────────────────────────────────────────────
from langchain.tools import tool

@tool
def analyze_emotion_tool(user_input: str) -> str:
    """문장을 분석해 '[감정: OO] 문장' 형태로 반환."""
    return analyze_emotion_gpt(user_input)

tools = [analyze_emotion_tool]

# ───── 프롬프트 템플릿 경로 ──────────────────────────────────────────────────
PROMPT_PATH = {
    "emotional": "app/prompt/emotion_prompt_emotional.txt",
    "practical": "app/prompt/emotion_prompt_practical.txt",
}

def load_prompt_template(persona: str) -> str:
    path = PROMPT_PATH.get(persona, PROMPT_PATH["emotional"])
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ───── 메인 대화 함수 ────────────────────────────────────────────────────────
def chat_with_bot(
        user_input: str,
        session_id: Optional[str] = None,      # None이면 uuid로 생성
        user_id: Optional[str] = None,         # 실제 사용자 ID
        persona: str = "emotional",
        db: Optional[Session] = None
) -> str:

    # 1) 세션 ID 보장
    session_id = session_id or str(uuid.uuid4())
    print(f"▶️ [Agent] 세션 ID: {session_id}")

    # 2) 시스템 프롬프트 생성
    system_text = load_prompt_template(persona)
    nickname = get_user_nickname(user_id, db=db)            
    trend    = get_emotion_trend_text(user_id, db=db)       
    retrieved = retrieve_similar_cases_for_rag(user_input)

    system_text = system_text.replace("{nickname}", nickname)
    system_text += f"\n\n[최근 감정 흐름 요약]\n{trend}"

    # 3) 프롬프트 컨테이너
    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_text}\n\n[참고할 유사 상담사례]\n{retrieved}"),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    # 4) LangChain Agent 준비
    agent    = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools,
                             handle_parsing_errors=True, max_iterations=5)

    memory_agent = RunnableWithMessageHistory(
        executor,
        get_session_history,              # 세션별 히스토리 딕셔너리
        input_messages_key="input",
        history_messages_key="history",
    )

    # 5) 실행
    try:
        response = memory_agent.invoke(
            {
                "input": user_input,
                "system_text": system_text,
                "retrieved":   retrieved,
            },
            config={"configurable": {"session_id": session_id}}
        )
        return response["output"] if isinstance(response, dict) else str(response)
    except Exception as e:
        return f"오류: {e}"
