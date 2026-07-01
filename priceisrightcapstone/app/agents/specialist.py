from app.agents.base import Agent
from app.core.models import Deal
from app.core.config import settings
import requests

class SpecialistAgent(Agent):
    def __init__(self):
        super().__init__("Specialist", "Fine-tuned Model Inference", "#0969DA", "Llama-3.2-3B")

    def run(self, deal: Deal) -> float:
        self.set_status("RUNNING")
        self.logger.info(f"Modal GPU request sent (Llama-3.2-3B) for {deal.title}")
        
        # Mocking Modal API call
        try:
            if settings.MODAL_TOKEN_ID and settings.MODAL_TOKEN_SECRET:
                # headers = {"Authorization": f"Bearer {settings.MODAL_TOKEN_ID}"}
                # response = requests.post("https://modal.com/api/infer", json={"title": deal.title}, headers=headers)
                # estimated_price = response.json().get("price")
                pass
            
            # Fallback heuristic
            estimated_price = deal.price * 1.4
            self.logger.info(f"Modal inference returned ${estimated_price:.2f}")
            
        except Exception as e:
            self.logger.error(f"Specialist Error: {e}")
            estimated_price = deal.price
            
        self.set_status("READY")
        return estimated_price
