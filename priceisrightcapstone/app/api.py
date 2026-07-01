from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

@app.get("/")
def read_root():
    return {"status": "online", "version": "1.2.0", "app": "The Price Is Right"}

@app.post("/scan", response_model=ScanResponse)
def trigger_scan(background_tasks: BackgroundTasks):
    if planner.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Scan already in progress")
    
    background_tasks.add_task(planner.run)
    return {"status": "accepted", "message": "Scan triggered in background"}

@app.get("/status", response_model=List[AgentStatus])
def get_status():
    return planner.get_all_statuses()

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
