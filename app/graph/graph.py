# app/graph/graph.py

from langgraph.graph import StateGraph
from app.graph.state import ChatState
from app.graph.nodes import get_load_context_node, get_respond_node  # ✅ 수정
from sqlalchemy.orm import Session

def build_graph(db: Session):
    builder = StateGraph(ChatState)

    # ✅ 노드 함수 가져오기
    load_node = get_load_context_node(db)
    respond_node = get_respond_node()

    builder.add_node("load_context_and_tools", load_node)
    builder.add_node("generate_response", respond_node)

    builder.set_entry_point("load_context_and_tools")
    builder.add_edge("load_context_and_tools", "generate_response")

    return builder.compile()
