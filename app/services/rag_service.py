# app/services/rag_service.py
from app.core.client import vectorstore
from app.services.emotion_service import analyze_emotion_gpt

def retrieve_similar_cases_for_rag(user_input: str, k: int = 3) -> str:
    """
    감정 분석 결과가 포함된 문장을 기반으로 Qdrant에서 유사 사례 검색
    """
    query = analyze_emotion_gpt(user_input)
    docs = vectorstore.similarity_search(query, k=k)
    if not docs:
        return "유사한 상담 사례를 찾을 수 없습니다."

    results = []
    for doc in docs:
        answer = doc.metadata.get("bot_response") or doc.page_content or ""
        emotion = doc.metadata.get("emotion", "")
        results.append(f"[{emotion}] {answer}")
    return "\n".join(results)
