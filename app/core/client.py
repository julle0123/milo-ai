# app/core/client.py
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant as QdrantVectorStore
from app.core.config import settings

# API Key 설정
os.environ["OPENAI_API_KEY"] = settings.openai_api_key
# LangSmith 연동 설정
if os.getenv("LANGSMITH_TRACING") == "true":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
# LLM 클라이언트
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    openai_api_key=settings.openai_api_key  # 이 부분!
)
embedding = OpenAIEmbeddings(model="text-embedding-3-small")

# Qdrant 클라이언트
qdrant_client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=settings.collection_name,
    embeddings=embedding
)
print("✅ OpenAI KEY:", settings.openai_api_key)