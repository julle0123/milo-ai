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
def detect_crisis_and_respond(text: str) -> str:
    """사용자 입력에서 위기 단어를 감지하고 응급 대응 메시지를 반환합니다."""
    CRISIS_KEYWORDS = [
        "자해", "죽고 싶", "사라지고 싶", "존재하고 싶지 않", 
        "끝내고 싶", "무의미해", "견딜 수 없", "없어지고 싶", "더 이상 못 버티겠"
        ]
    if any(keyword in text for keyword in CRISIS_KEYWORDS):
        return (
            "[⚠️ 위기 감지]\n"
            "지금 매우 힘든 상황일 수 있어요.\n"
            "혹시 아래와 같은 기관에 도움을 요청해보는 건 어떨까요?\n\n"
            "- 정신건강위기상담전화 1577-0199\n"
            "- 자살예방센터 1393\n"
            "- 청소년상담센터 1388\n\n"
            "💬 당신의 마음은 소중하고, 이 순간도 지나갈 수 있어요.\n"
            "함께 이겨낼 수 있도록 도와드릴게요."
        )
    else:
        return "문제없음: 위기 단어는 감지되지 않았습니다."

@tool
def analyze_emotion_tool(user_input: str) -> str:
    """문장을 분석해 '[감정: OO] 문장' 형태로 반환."""
    return analyze_emotion_gpt(user_input)

tools = [analyze_emotion_tool, detect_crisis_and_respond]

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
        lambda session_id: get_session_history(session_id, {"user_id": user_id, "db": db}),
        input_messages_key="input",
        history_messages_key="history"
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
