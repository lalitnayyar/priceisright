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
    MESSAGING_MODEL: str = "claude-3-5-sonnet-latest"
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
    """Load settings: .env/env-vars first, then ui_settings.json overrides on top."""
    from app.core.settings_store import SettingsStore

    base_settings = Settings()
    ui_data = SettingsStore.read()

    if ui_data:
        try:
            # ── API Keys ──────────────────────────────────────────────────────
            for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "PUSHOVER_USER",
                      "PUSHOVER_TOKEN", "MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET"):
                if k in ui_data and ui_data[k]:
                    setattr(base_settings, k, str(ui_data[k]).strip())

            # ── Agent config ──────────────────────────────────────────────────
            # Support both new key (DEAL_THRESHOLD) and legacy key (DEAL_THRESHOLD_PCT)
            if "DEAL_THRESHOLD" in ui_data:
                base_settings.DEAL_THRESHOLD = float(ui_data["DEAL_THRESHOLD"])
            elif "DEAL_THRESHOLD_PCT" in ui_data:
                base_settings.DEAL_THRESHOLD = float(ui_data["DEAL_THRESHOLD_PCT"])

            if "SCAN_INTERVAL_MINUTES" in ui_data:
                base_settings.SCAN_INTERVAL_MINUTES = int(ui_data["SCAN_INTERVAL_MINUTES"])

            for k in ("SCANNER_MODEL", "FRONTIER_MODEL", "MESSAGING_MODEL"):
                if k in ui_data and ui_data[k]:
                    setattr(base_settings, k, str(ui_data[k]).strip())

            if "ENSEMBLE_WEIGHTS" in ui_data:
                parts = [float(x.strip()) for x in str(ui_data["ENSEMBLE_WEIGHTS"]).split(",")]
                if len(parts) == 3:
                    base_settings.ENSEMBLE_FRONTIER_WEIGHT = parts[0]
                    base_settings.ENSEMBLE_SPECIALIST_WEIGHT = parts[1]
                    base_settings.ENSEMBLE_DNN_WEIGHT = parts[2]

            # ── RAG ───────────────────────────────────────────────────────────
            # Support both new key (CHROMA_DB_PATH) and legacy key (CHROMADB_STORAGE_PATH)
            if "CHROMA_DB_PATH" in ui_data and ui_data["CHROMA_DB_PATH"]:
                base_settings.CHROMA_DB_PATH = str(ui_data["CHROMA_DB_PATH"]).strip()
            elif "CHROMADB_STORAGE_PATH" in ui_data and ui_data["CHROMADB_STORAGE_PATH"]:
                base_settings.CHROMA_DB_PATH = str(ui_data["CHROMADB_STORAGE_PATH"]).strip()

            if "EMBEDDING_MODEL" in ui_data and ui_data["EMBEDDING_MODEL"]:
                base_settings.EMBEDDING_MODEL = str(ui_data["EMBEDDING_MODEL"]).strip()

            if "CHROMA_RESULTS" in ui_data:
                base_settings.CHROMA_RESULTS_COUNT = int(ui_data["CHROMA_RESULTS"])

            # ── RSS Feeds ─────────────────────────────────────────────────────
            if "RSS_FEEDS" in ui_data:
                feeds = ui_data["RSS_FEEDS"]
                if isinstance(feeds, list):
                    base_settings.RSS_FEED_URLS = ",".join(f.strip() for f in feeds if f.strip())
                else:
                    base_settings.RSS_FEED_URLS = ",".join(
                        line.strip() for line in str(feeds).splitlines() if line.strip()
                    )

            # ── System ────────────────────────────────────────────────────────
            if "LOG_LEVEL" in ui_data and ui_data["LOG_LEVEL"]:
                base_settings.LOG_LEVEL = str(ui_data["LOG_LEVEL"]).strip()
            if "MEMORY_FILE" in ui_data and ui_data["MEMORY_FILE"]:
                base_settings.MEMORY_FILE = str(ui_data["MEMORY_FILE"]).strip()
            if "DNN_WEIGHTS_PATH" in ui_data and ui_data["DNN_WEIGHTS_PATH"]:
                base_settings.DNN_WEIGHTS_PATH = str(ui_data["DNN_WEIGHTS_PATH"]).strip()
            if "DASHBOARD_PORT" in ui_data:
                base_settings.DASHBOARD_PORT = int(ui_data["DASHBOARD_PORT"])
            if "API_PORT" in ui_data:
                base_settings.API_PORT = int(ui_data["API_PORT"])

        except Exception as e:
            print(f"Warning: Failed to apply ui_settings.json overrides: {e}")

    return base_settings


# Dynamic proxy — `from app.core.config import settings` always returns fresh values
class SettingsProxy:
    def __getattr__(self, name):
        return getattr(get_settings(), name)

settings = SettingsProxy()
