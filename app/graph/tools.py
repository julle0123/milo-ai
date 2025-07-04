# app/graph/tools.py

from langchain.tools import tool
from app.services.emotion_service import analyze_emotion_gpt
from app.services.rag_service import (
    retrieve_similar_cases_for_rag,
    retrieve_emotion_recovery_contents
)

# 감정 분석 GPT Tool
@tool
async def analyze_emotion_tool(user_input: str) -> str:
    """문장을 분석해 '[감정: OO] 문장' 형태로 반환.
    반드시 수행되어야 함."""
    return analyze_emotion_gpt(user_input)

# 유사 상담 사례 검색 RAG Tool
@tool
async def search_similar_cases_tool(user_input: str) -> str:
    """Qdrant에서 유사 상담 사례 검색 (GPT로 감정 분석된 문장을 기반)."""
    return await retrieve_similar_cases_for_rag(user_input)

# 회복 콘텐츠 추천 Tool
@tool
async def recommend_recovery_content_tool(user_input: str) -> str:
    """Qdrant에서 회복 콘텐츠(RAG) 검색 (명상, 호흡, 유튜브 링크 등)."""
    return await retrieve_emotion_recovery_contents(user_input)
