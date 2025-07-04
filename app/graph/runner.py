# app/graph/runner.py

from app.graph.graph import build_graph
from app.graph.state import ChatState
from sqlalchemy.orm import Session
import uuid

# LangGraph 실행 진입점
async def run_chat(user_input: str, user_id: str, db: Session) -> str:
    # 상태 초기화
    session_id = user_id or str(uuid.uuid4())
    state: ChatState = {
        "user_input": user_input,
        "user_id": user_id,
        "session_id": session_id
    }

    # LangGraph 빌드 및 실행
    graph = build_graph(db)
    result = await graph.ainvoke(state)
    return result["output"]
