from app.graph.graph import build_graph
from app.graph.state import ChatState
from sqlalchemy.orm import Session
import uuid

# LangGraph 실행 진입점d
async def run_chat(user_input: str, user_id: str, db: Session) -> str:
    session_id = user_id or str(uuid.uuid4())
    state: ChatState = {
        "user_input": user_input,
        "user_id": user_id,
        "session_id": session_id
    }

    graph = build_graph(db)
    result = await graph.ainvoke(
        state,
        config={"configurable": {"session_id": session_id}}
    )

    # 안전하게 반환값 접근
    if "output" in result:
        return result["output"]
    else:
        raise ValueError(f"LangGraph 결과에 'output'이 없습니다: {result}")