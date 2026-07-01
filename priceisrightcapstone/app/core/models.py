from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Deal(BaseModel):
    id: str
    title: str
    price: float
    url: str
    description: str
    source: str
    timestamp: datetime = datetime.now()

class EnsembleResult(BaseModel):
    estimated_price: float
    discount_pct: float
    is_great_deal: bool
    weights_used: Dict[str, float]

class DealResult(BaseModel):
    deal: Deal
    ensemble_result: EnsembleResult
    notification_sent: bool = False
    
class AgentStatus(BaseModel):
    name: str
    role: str
    model: str
    status: str # READY, RUNNING, ERROR
    last_active: datetime = datetime.now()
