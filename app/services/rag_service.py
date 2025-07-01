# app/services/rag_service.py
import os
import httpx
import asyncio
from app.core.client import vectorstore  # vectorstore.asimilarity_search 지원 필요
from app.services.emotion_service import analyze_emotion_gpt # 감정 태그 추출
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import SearchRequest # (명시적으로 사용되지는 않지만 유지 가능)
from dotenv import load_dotenv

# 유사 사례 검색 함수 (RAG)
# - 사용자 입력 문장을 감정 분석한 뒤, 해당 감정이 포함된 문장 전체를
#   Qdrant 벡터 DB에 질의하여 유사 상담 사례를 검색
# - 감정 표현이 포함된 텍스트를 임베딩 쿼리로 사용함
# - 검색된 응답은 "[감정] 응답문장" 형태로 정리되어 리턴됨
# - 검색 결과가 없을 경우는 안내 문구 반환
async def retrieve_similar_cases_for_rag(user_input: str, k: int = 3) -> str:
    """
    감정 분석 결과가 포함된 문장을 기반으로 Qdrant에서 유사 사례 검색
    """
    query = await asyncio.to_thread(analyze_emotion_gpt, user_input)
    
    # Qdrant를 통한 벡터 유사도 기반 문서 검색
    docs = await vectorstore.asimilarity_search(query, k=k)
    if not docs:
        return "유사한 상담 사례를 찾을 수 없습니다."

    # 검색된 문서에서 감정 라벨 + 챗봇 응답 추출
    results = []
    for doc in docs:
        answer = doc.metadata.get("bot_response") or doc.page_content or ""
        emotion = doc.metadata.get("emotion", "")
        results.append(f"[{emotion}] {answer}")
        
    return "\n".join(results)

# 감정 회복 콘텐츠 추천 (예: 유튜브 영상, 명상 콘텐츠 등)
# - 입력 문장을 OpenAI 임베딩 후 Qdrant에서 유사 콘텐츠 검색
# - 결과는 "번호. 링크 + 설명" 형태로 정리되어 출력
async def retrieve_emotion_recovery_contents(user_input: str, top_k: int = 3) -> str:
    """
    사용자의 입력을 OpenAI 임베딩 후, 감정 회복 콘텐츠에서 유사한 콘텐츠를 검색함.
    """
    # 비동기 HTTP 클라이언트를 생성하고 OpenAI Embedding API 호출
    async with httpx.AsyncClient(timeout=10.0) as client:
        
        # OpenAI Embedding API에 POST 요청
        response = await client.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}", # OpenAI 인증 토큰
                "Content-Type": "application/json"                        # JSON 형식 명시
            },
            json={
                "model": "text-embedding-3-small",
                "input": user_input
            }
        )
        # 응답에서 첫 번째 임베딩 벡터만 추출 (리스트 내 딕셔너리 구조)
        # 응답 구조: {"data": [{"embedding": [...]}], ...}
        embedding = response.json()["data"][0]["embedding"]

    # Qdrant 비동기 클라이언트로 유사 콘텐츠 검색
    async_qdrant = AsyncQdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    results = await async_qdrant.search(
        collection_name="emotion_recovery_rag",
        query_vector=embedding,
        limit=top_k,
        with_payload=True
    )

    # 검색된 콘텐츠를 출력 포맷으로 정리 (번호. 링크 + 설명)
    output = ""
    for i, hit in enumerate(results, 1):
        payload = hit.payload
        output += f"{i}. {payload.get('youtube_url', '')}\n{payload.get('page_content', '')}\n\n"

    return output.strip() or "유사한 콘텐츠를 찾을 수 없습니다."
