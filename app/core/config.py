# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

# .env 파일 기반 설정 클래스
class Settings(BaseSettings):
    # OpenAI API 키
    openai_api_key: str

    # Qdrant 벡터 DB 접속 정보
    qdrant_url: str
    qdrant_api_key: str
    collection_name: str = "chatbot_embeddings"
    collection_nameu : str = "emotion_recovery_rag"
    emotion_recovery_collection: str = Field("emotion_recovery_rag", alias="COLLECTION_NAMEU")
     
    # LangSmith 설정
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_endpoint: str | None = None
    langsmith_project: str | None = None

    # MySQL 접속 정보
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str

    # SQLAlchemy에서 사용할 DB URL 반환 프로퍼티
    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}?charset=utf8mb4"

    # Pydantic 설정
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# 설정 객체 전역 인스턴스
settings = Settings()