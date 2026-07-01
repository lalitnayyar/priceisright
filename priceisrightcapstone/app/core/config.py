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

def get_settings() -> Settings:
    """Load settings dynamically from ui_settings.json if available, fallback to .env/defaults."""
    import json
    # In Docker, we are at /app, so data is at /app/data
    # Locally, we might be running from the root
    if os.path.exists("/app/data"):
        settings_path = "/app/data/ui_settings.json"
    else:
        settings_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ui_settings.json")
        settings_path = os.path.normpath(settings_path)
    
    base_settings = Settings()
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r") as f:
                ui_data = json.load(f)
            
            # Map ui_settings.json keys to Settings object
            if "OPENAI_API_KEY" in ui_data: base_settings.OPENAI_API_KEY = ui_data["OPENAI_API_KEY"]
            if "ANTHROPIC_API_KEY" in ui_data: base_settings.ANTHROPIC_API_KEY = ui_data["ANTHROPIC_API_KEY"]
            if "PUSHOVER_USER" in ui_data: base_settings.PUSHOVER_USER = ui_data["PUSHOVER_USER"]
            if "PUSHOVER_TOKEN" in ui_data: base_settings.PUSHOVER_TOKEN = ui_data["PUSHOVER_TOKEN"]
            if "MODAL_TOKEN_ID" in ui_data: base_settings.MODAL_TOKEN_ID = ui_data["MODAL_TOKEN_ID"]
            if "MODAL_TOKEN_SECRET" in ui_data: base_settings.MODAL_TOKEN_SECRET = ui_data["MODAL_TOKEN_SECRET"]
            
            if "DEAL_THRESHOLD" in ui_data: base_settings.DEAL_THRESHOLD = float(ui_data["DEAL_THRESHOLD"])
            if "SCAN_INTERVAL_MINUTES" in ui_data: base_settings.SCAN_INTERVAL_MINUTES = int(ui_data["SCAN_INTERVAL_MINUTES"])
            if "SCANNER_MODEL" in ui_data: base_settings.SCANNER_MODEL = ui_data["SCANNER_MODEL"]
            if "FRONTIER_MODEL" in ui_data: base_settings.FRONTIER_MODEL = ui_data["FRONTIER_MODEL"]
            if "MESSAGING_MODEL" in ui_data: base_settings.MESSAGING_MODEL = ui_data["MESSAGING_MODEL"]
            
            if "ENSEMBLE_WEIGHTS" in ui_data:
                parts = [float(x.strip()) for x in ui_data["ENSEMBLE_WEIGHTS"].split(",")]
                if len(parts) == 3:
                    base_settings.ENSEMBLE_FRONTIER_WEIGHT = parts[0]
                    base_settings.ENSEMBLE_SPECIALIST_WEIGHT = parts[1]
                    base_settings.ENSEMBLE_DNN_WEIGHT = parts[2]
            
            if "CHROMA_DB_PATH" in ui_data: base_settings.CHROMA_DB_PATH = ui_data["CHROMA_DB_PATH"]
            if "CHROMA_RESULTS" in ui_data: base_settings.CHROMA_RESULTS_COUNT = int(ui_data["CHROMA_RESULTS"])
            if "EMBEDDING_MODEL" in ui_data: base_settings.EMBEDDING_MODEL = ui_data["EMBEDDING_MODEL"]
            
            if "RSS_FEEDS" in ui_data:
                base_settings.RSS_FEED_URLS = ",".join(line.strip() for line in ui_data["RSS_FEEDS"].splitlines() if line.strip())
                
            if "MEMORY_FILE" in ui_data: base_settings.MEMORY_FILE = ui_data["MEMORY_FILE"]
            if "LOG_LEVEL" in ui_data: base_settings.LOG_LEVEL = ui_data["LOG_LEVEL"]
            if "DASHBOARD_PORT" in ui_data: base_settings.DASHBOARD_PORT = int(ui_data["DASHBOARD_PORT"])
            if "API_PORT" in ui_data: base_settings.API_PORT = int(ui_data["API_PORT"])
            if "DNN_WEIGHTS_PATH" in ui_data: base_settings.DNN_WEIGHTS_PATH = ui_data["DNN_WEIGHTS_PATH"]
            
        except Exception as e:
            print(f"Warning: Failed to load dynamic settings from {settings_path}: {e}")
            
    return base_settings

# Provide a dynamic proxy object so `from app.core.config import settings` 
# always fetches the latest values when accessed
class SettingsProxy:
    def __getattr__(self, name):
        return getattr(get_settings(), name)

settings = SettingsProxy()
