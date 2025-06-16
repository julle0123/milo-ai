from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str

    qdrant_url: str
    qdrant_api_key: str
    collection_name: str = "chatbot_embeddings"

    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_endpoint: str | None = None
    langsmith_project: str | None = None

    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}?charset=utf8mb4"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()