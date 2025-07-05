# app/graph/graph.py

from langgraph.graph import StateGraph
from app.graph.state import ChatState
from app.graph.nodes import load_context, generate_response
from app.graph.tools import (
    analyze_emotion_tool,
    search_similar_cases_tool,
    recommend_recovery_content_tool
)
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.client import llm

# LangChain Tools 등록
tools = [
    analyze_emotion_tool,
    search_similar_cases_tool,
    recommend_recovery_content_tool
]

# Agent 프롬프트 정의
prompt = ChatPromptTemplate.from_messages([
    ("system", "아래는 상담 중 수집된 정보입니다. 필요한 경우 도구를 사용해 응답을 생성하세요."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# LangChain AgentExecutor 구성
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,
    max_iterations=5,
    verbose=True
)

async def generate_response_node(state):
    return await generate_response(state)


# LangGraph 상태 흐름 정의
def build_graph(db):
    builder = StateGraph(ChatState)

    # 비동기 노드 정의
    async def load_context_node(state):
        return await load_context(state, db)

    # async def save_daily_report_node(state):
    #     return await save_daily_report(state, db)

    async def agent_node(state):
        # 필수 키 보장
        if "input" not in state and "user_input" in state:
            state["input"] = state["user_input"]
        return await agent_executor.ainvoke(state)

    # 노드 등록
    builder.add_node("load_context", load_context_node)
    builder.add_node("agent", agent_node)
    builder.add_node("generate_response", generate_response_node)

    # 노드 연결
    builder.set_entry_point("load_context")
    builder.add_edge("load_context", "agent")
    builder.add_edge("agent", "generate_response")

    return builder.compile()
