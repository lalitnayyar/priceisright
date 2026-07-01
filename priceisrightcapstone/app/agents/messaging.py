from app.agents.base import Agent
from app.core.models import Deal, EnsembleResult
from app.core.config import settings
import requests

class MessagingAgent(Agent):
    def __init__(self):
        super().__init__("Messaging", "Push Notification Generation", "#F85149", settings.MESSAGING_MODEL)

    def run(self, deal: Deal, result: EnsembleResult) -> bool:
        self.set_status("RUNNING")
        
        # Mock LLM generation
        message = f"🔥 {deal.title}: {result.discount_pct:.0f}% Off Arbitrage! Snipe now: {deal.url}"
        self.logger.info(f"Claude crafting notification... '{message}'")
        
        success = False
        if settings.PUSHOVER_USER and settings.PUSHOVER_TOKEN:
            try:
                resp = requests.post("https://api.pushover.net/1/messages.json", data={
                    "token": settings.PUSHOVER_TOKEN,
                    "user": settings.PUSHOVER_USER,
                    "message": message,
                    "title": "The Price Is Right Alert"
                })
                if resp.status_code == 200:
                    self.logger.info("Pushover API returned 200 OK. Notification sent.")
                    success = True
                else:
                    self.logger.error(f"Pushover Error: {resp.text}")
                    self.set_status("ERROR")
            except Exception as e:
                self.logger.error(f"Messaging Error: {e}")
                self.set_status("ERROR")
        else:
            self.logger.warning("Pushover credentials not set. Simulating send.")
            success = True
            
        if success:
            self.set_status("READY")
            
        return success
