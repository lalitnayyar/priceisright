from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Request
from typing import List
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
    from app.core.settings_store import SettingsStore
    from app.ui.dashboard import DEFAULTS
    saved = SettingsStore.read()
    return {**DEFAULTS, **saved}

@app.post("/settings")
async def save_ui_settings(request: Request):
    data = await request.json()
    from app.core.settings_store import SettingsStore
    from app.ui.dashboard import _write_env
    SettingsStore.write(data)
    _write_env(data)
    return {"status": "success"}

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
