from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi import Request
from typing import List
import os
from app.agents.planning import PlanningAgent
from app.core.models import DealResult, AgentStatus
from app.core.config import settings

app = FastAPI(title="The Price Is Right API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = PlanningAgent()

# Serve static files (settings.html etc.)
_static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")

class ScanResponse(BaseModel):
    status: str
    message: str

@app.get("/health")
def read_root():
    """Health check endpoint — use /health to verify the API is online.
    The root path / is reserved for the Gradio dashboard in dashboard mode."""
    return {"status": "online", "version": "1.2.0", "app": "The Price Is Right"}

@app.get("/settings")
def get_ui_settings():
    """Return current settings using JS field names.
    Priority: ui_settings.json overrides .env overrides code defaults."""
    from app.core.config import get_settings
    from app.core.settings_store import SettingsStore

    s = get_settings()          # merged: .env + ui_settings.json
    ui = SettingsStore.read()   # raw saved dict for fields not in Settings model

    return {
        # API Keys
        "OPENAI_API_KEY":     s.OPENAI_API_KEY,
        "ANTHROPIC_API_KEY":  s.ANTHROPIC_API_KEY,
        "PUSHOVER_USER":      s.PUSHOVER_USER,
        "PUSHOVER_TOKEN":     s.PUSHOVER_TOKEN,
        "MODAL_TOKEN_ID":     s.MODAL_TOKEN_ID,
        "MODAL_TOKEN_SECRET": s.MODAL_TOKEN_SECRET,
        # Agent config — use JS key names
        "DEAL_THRESHOLD":         s.DEAL_THRESHOLD,
        "SCAN_INTERVAL_MINUTES":  s.SCAN_INTERVAL_MINUTES,
        "SCANNER_MODEL":          s.SCANNER_MODEL,
        "FRONTIER_MODEL":         s.FRONTIER_MODEL,
        "MESSAGING_MODEL":        s.MESSAGING_MODEL,
        "ENSEMBLE_WEIGHTS":       f"{s.ENSEMBLE_FRONTIER_WEIGHT}, {s.ENSEMBLE_SPECIALIST_WEIGHT}, {s.ENSEMBLE_DNN_WEIGHT}",
        # RAG
        "CHROMA_DB_PATH":    s.CHROMA_DB_PATH,
        "EMBEDDING_MODEL":   s.EMBEDDING_MODEL,
        "CHROMA_RESULTS":    s.CHROMA_RESULTS_COUNT,
        "RAG_MAX_POINTS":    int(ui.get("RAG_MAX_POINTS", 1000)),
        # Notifications
        "PUSHOVER_SOUND":       ui.get("PUSHOVER_SOUND", "pushover"),
        "NOTIFICATION_TITLE":   ui.get("NOTIFICATION_TITLE", "The Price Is Right Alert"),
        "NOTIF_MIN_INTERVAL":   int(ui.get("NOTIF_MIN_INTERVAL", 5)),
        # Feed Sources
        "RSS_FEEDS":          s.RSS_FEED_URLS.replace(",", "\n"),
        "MAX_DEALS_PER_SCAN": int(ui.get("MAX_DEALS_PER_SCAN", 50)),
        # System
        "MEMORY_FILE":      s.MEMORY_FILE,
        "LOG_LEVEL":        s.LOG_LEVEL,
        "DNN_WEIGHTS_PATH": s.DNN_WEIGHTS_PATH,
        "DASHBOARD_PORT":   s.DASHBOARD_PORT,
        "API_PORT":         s.API_PORT,
    }

@app.post("/settings")
async def save_ui_settings(request: Request):
    """Save settings to ui_settings.json (persisted via Docker volume mount).
    String values are trimmed of whitespace. RSS_FEEDS list items are trimmed too."""
    data = await request.json()
    from app.core.settings_store import SettingsStore

    # Trim all string values
    cleaned = {}
    for k, v in data.items():
        if isinstance(v, str):
            cleaned[k] = v.strip()
        elif isinstance(v, list):
            cleaned[k] = [item.strip() if isinstance(item, str) else item for item in v]
        else:
            cleaned[k] = v

    SettingsStore.write(cleaned)
    return {"status": "success", "saved": len(cleaned)}

@app.post("/scan", response_model=ScanResponse)
def trigger_scan(background_tasks: BackgroundTasks):
    if planner.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Scan already in progress")
    
    background_tasks.add_task(planner.run)
    return {"status": "accepted", "message": "Scan triggered in background"}

@app.get("/status", response_model=List[AgentStatus])
def get_status():
    return planner.get_all_statuses()

@app.post("/test-api/{service}")
async def test_api_connection(service: str, request: Request):
    """Test connectivity for a given API service using the keys submitted from the UI."""
    import httpx
    data = await request.json()

    if service == "openai":
        key = (data.get("OPENAI_API_KEY") or "").strip()
        if not key:
            return {"ok": False, "message": "OpenAI API key is empty"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(
                    "https://api.openai.com/v1/models",
                    headers={"Authorization": f"Bearer {key}"}
                )
            if r.status_code == 200:
                return {"ok": True, "message": "Connected — OpenAI API is valid"}
            else:
                return {"ok": False, "message": f"HTTP {r.status_code}: {r.text[:120]}"}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    elif service == "anthropic":
        key = (data.get("ANTHROPIC_API_KEY") or "").strip()
        if not key:
            return {"ok": False, "message": "Anthropic API key is empty"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={"model": "claude-3-haiku-20240307", "max_tokens": 1,
                          "messages": [{"role": "user", "content": "hi"}]}
                )
            if r.status_code in (200, 400):
                return {"ok": True, "message": "Connected — Anthropic API is valid"}
            else:
                return {"ok": False, "message": f"HTTP {r.status_code}: {r.text[:120]}"}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    elif service == "pushover":
        user = (data.get("PUSHOVER_USER") or "").strip()
        token = (data.get("PUSHOVER_TOKEN") or "").strip()
        if not user or not token:
            return {"ok": False, "message": "Pushover User Key or App Token is empty"}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.post(
                    "https://api.pushover.net/1/users/validate.json",
                    data={"token": token, "user": user}
                )
            body = r.json()
            if body.get("status") == 1:
                return {"ok": True, "message": "Connected — Pushover credentials are valid"}
            else:
                return {"ok": False, "message": body.get("errors", ["Invalid credentials"])[0]}
        except Exception as e:
            return {"ok": False, "message": str(e)}

    elif service == "modal":
        token_id = (data.get("MODAL_TOKEN_ID") or "").strip()
        token_secret = (data.get("MODAL_TOKEN_SECRET") or "").strip()
        if not token_id or not token_secret:
            return {"ok": False, "message": "Modal Token ID or Secret is empty"}
        # Modal does not have a simple REST ping — validate format only
        if token_id.startswith("ak-") and len(token_secret) > 10:
            return {"ok": True, "message": "Format looks valid — full validation requires Modal CLI"}
        else:
            return {"ok": False, "message": "Token ID should start with ak- and secret must be non-empty"}

    else:
        return {"ok": False, "message": f"Unknown service: {service}"}


@app.get("/results", response_model=List[DealResult])
def get_results():
    # Return last run results from memory file
    import json
    import os
    if os.path.exists(settings.MEMORY_FILE):
        try:
            with open(settings.MEMORY_FILE, 'r') as f:
                data = json.load(f)
                return data[-10:] # Return last 10
        except:
            return []
    return []


@app.get("/logs")
def get_logs(n: int = 100):
    """Return the last N lines from the application log or scan activity."""
    import glob
    # Check common log file locations
    log_candidates = [
        "/tmp/app_test.log",
        "/app/logs/app.log",
        "/tmp/priceisright.log",
    ]
    log_candidates += glob.glob("/app/logs/*.log")
    lines = []
    for log_path in log_candidates:
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', errors='replace') as f:
                    all_lines = f.readlines()
                    lines = [l.rstrip() for l in all_lines[-n:]]
                if lines:
                    break
            except Exception:
                continue
    if not lines:
        lines = ["No log file found. Run a scan to generate activity logs."]
    return {"lines": lines, "count": len(lines)}
