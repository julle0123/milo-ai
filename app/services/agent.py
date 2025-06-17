# app/services/agent.py
import os
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from app.services.report_service import get_emotion_trend_text
from app.services.emotion_service import analyze_emotion_gpt
from app.services.rag_service import retrieve_similar_cases_for_rag
from app.services.memory import get_session_history
from app.core.client import llm

# 툴 등록 (감정 분석만 tool로 제공)
from langchain.tools import tool

@tool
def analyze_emotion_tool(user_input: str) -> str:
    """입력된 문장에서 감정을 분석하여 '[감정: OO] 문장' 형태로 반환합니다."""
    return analyze_emotion_gpt(user_input)

tools = [analyze_emotion_tool]

# 프롬프트 불러오기
PROMPT_PATH = {
    "emotional": "app/prompt/emotion_prompt_emotional.txt",
    "practical": "app/prompt/emotion_prompt_practical.txt"
}

def load_prompt_template(persona: str) -> str:
    path = PROMPT_PATH.get(persona, PROMPT_PATH["emotional"])
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chat_with_bot(user_input: str, session_id: str = "default", persona: str = "emotional", db: Session = None) -> str:
    system_text = load_prompt_template(persona)
    retrieved = retrieve_similar_cases_for_rag(user_input)

    # ✅ 감정 흐름 삽입 (정상적으로 db 사용)
    trend = get_emotion_trend_text(session_id, db=db)
    system_text += f"\n\n[최근 감정 흐름 요약]\n{trend}"

    prompt = ChatPromptTemplate.from_messages([
        ("system", f"{{system_text}}\n\n[참고할 유사 상담사례]\n{{retrieved}}"),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=5)

    memory_agent = RunnableWithMessageHistory(
        executor,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

    try:
        response = memory_agent.invoke(
            {
                "input": user_input,
                "system_text": system_text,
                "retrieved": retrieved,
            },
            config={"configurable": {"session_id": session_id}}
        )
        return response["output"] if isinstance(response, dict) else str(response)
    except Exception as e:
        return f"오류: {str(e)}"
