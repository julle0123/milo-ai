import uuid
from typing import Optional          
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session

from app.core.client import llm # GPT 모델 인스턴스
from app.services.memory import get_session_history # 세션 기반 히스토리 관리 함수
from app.services.emotion_service import (
    get_emotion_trend_text,      # 최근 감정 흐름 요약 (DB 기반)
    analyze_emotion_gpt,         # 감정 분석 도구 (GPT 기반)
    get_user_nickname            # 사용자 닉네임 조회
)
from app.services.rag_service import retrieve_similar_cases_for_rag  # 유사 사례 검색 (RAG)
from langchain.tools import tool

# LangChain tool 등록 
# 사용자 입력을 "[감정: OO] 문장" 형식으로 변환하는 GPT 기반 분석 도구
# - 필수 실행 도구로 agent 프롬프트에 삽입됨
@tool
def analyze_emotion_tool(user_input: str) -> str:
    """문장을 분석해 '[감정: OO] 문장' 형태로 반환.
       반드시 수행 되어야 함."""
    return analyze_emotion_gpt(user_input)

# Agent에 등록할 Tool 리스트
tools = [analyze_emotion_tool]

# 프롬프트 템플릿 경로 
# 사용자 선택(persona)에 따라 감성형 / 실용형 프롬프트 로딩
# - 템플릿 내부에는 {nickname}, {trend} 등의 placeholder가 포함됨
PROMPT_PATH = {
    "emotional": "app/prompt/emotion_prompt_emotional.txt",
    "practical": "app/prompt/emotion_prompt_practical.txt",
}

def load_prompt_template(persona: str) -> str:
    path = PROMPT_PATH.get(persona, PROMPT_PATH["emotional"])
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# 메인 대화 함수 
# 사용자 입력과 세션 기반 정보, 유사사례, 감정 분석 등을 종합하여 응답 생성
# 입력:
#   - user_input: 사용자 입력 문장
#   - session_id: 세션 ID (없으면 UUID 생성)
#   - user_id: 사용자 ID
#   - persona: 프롬프트 스타일 (emotional/practical)
#   - db: SQLAlchemy DB 세션
# 출력:
#   - GPT 기반 감정 상담 응답 문자열
def chat_with_bot(
        user_input: str,
        session_id: Optional[str] = None,      # None이면 uuid로 생성
        user_id: Optional[str] = None,         # 실제 사용자 ID
        persona: str = "emotional",
        db: Optional[Session] = None
) -> str:
 
    # 1) 세션 ID 생성 또는 유지
    session_id = session_id or str(uuid.uuid4())
    print(f"▶️ [Agent] 세션 ID: {session_id}")

    # 2) 프롬프트 시스템 메시지 구성 (닉네임, 감정 트렌드 삽입)
    system_text = load_prompt_template(persona)
    nickname = get_user_nickname(user_id, db=db)            
    trend    = get_emotion_trend_text(user_id, db=db)       
    retrieved = retrieve_similar_cases_for_rag(user_input)

    system_text = system_text.replace("{nickname}", nickname)
    system_text += f"\n\n[최근 감정 흐름 요약]\n{trend}"

    # 3) 프롬프트 구성
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

    # 5) 메모리 래핑 (RunnableWithMessageHistory 사용)
    memory_agent = RunnableWithMessageHistory(
        executor,
        lambda session_id: get_session_history(session_id, {"user_id": user_id, "db": db}),
        input_messages_key="input",
        history_messages_key="history"
    )

    # 6) 실행 및 예외 처리
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
