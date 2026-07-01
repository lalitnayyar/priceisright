import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    PUSHOVER_USER: str = ""
    PUSHOVER_TOKEN: str = ""
    MODAL_TOKEN_ID: str = ""
    MODAL_TOKEN_SECRET: str = ""

    # Agent Configuration
    DEAL_THRESHOLD: float = 50.0
    SCAN_INTERVAL_MINUTES: int = 5
    SCANNER_MODEL: str = "gpt-4o-mini"
    FRONTIER_MODEL: str = "gpt-4o"
    MESSAGING_MODEL: str = "claude-3-5-sonnet-20241022"
    ENSEMBLE_FRONTIER_WEIGHT: float = 0.8
    ENSEMBLE_SPECIALIST_WEIGHT: float = 0.1
    ENSEMBLE_DNN_WEIGHT: float = 0.1

    # RAG Database
    CHROMA_DB_PATH: str = "./data/products_vectorstore"
    CHROMA_HOST: str = "chromadb"
    CHROMA_PORT: int = 8000
    CHROMA_RESULTS_COUNT: int = 5
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # RSS Feeds
    RSS_FEED_URLS: str = "https://www.dealnews.com/rss.html,https://feeds.feedburner.com/techbargains"

    # Application
    MEMORY_FILE: str = "./data/memory.json"
    LOG_LEVEL: str = "INFO"
    DASHBOARD_PORT: int = 7860
    API_PORT: int = 8000
    DNN_WEIGHTS_PATH: str = "./data/dnn_weights.pt"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
