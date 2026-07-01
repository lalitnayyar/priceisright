import os
import json
import logging

logger = logging.getLogger(__name__)

class SettingsStore:
    """Standalone module for reading/writing UI settings safely."""
    
    @staticmethod
    def get_path() -> str:
        # In Docker, we are at /app, so data is at /app/data
        if os.path.exists("/app/data"):
            return "/app/data/ui_settings.json"
        
        # Locally, fallback to relative path
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ui_settings.json")
        return os.path.normpath(path)
        
    @staticmethod
    def read() -> dict:
        path = SettingsStore.get_path()
        if not os.path.exists(path):
            return {}
            
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read settings from {path}: {e}")
            return {}
            
    @staticmethod
    def write(data: dict) -> bool:
        path = SettingsStore.get_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            logger.error(f"Failed to write settings to {path}: {e}")
            return False
