from app.agents.base import Agent
from app.core.models import Deal
from app.core.config import settings
from app.core.rag import rag_db
from openai import OpenAI

class FrontierAgent(Agent):
    def __init__(self):
        super().__init__("Frontier", "RAG-based Price Estimation", "#4ECDC4", settings.FRONTIER_MODEL)
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def run(self, deal: Deal) -> float:
        self.set_status("RUNNING")
        self.logger.info(f"Analyzing '{deal.title}'... Querying ChromaDB 'products' collection.")
        
        try:
            # Query RAG
            results = rag_db.query_similar(f"{deal.title} {deal.description}")
            self.logger.info(f"Retrieved similar items. Estimating price via RAG context...")
            
            # Mocking LLM call for sandbox
            # context = str(results)
            # prompt = f"Estimate true market price for {deal.title} given context: {context}. Return ONLY a float number."
            
            # Dummy logic
            estimated_price = deal.price * 1.5
            
        except Exception as e:
            self.logger.error(f"Frontier Agent Error: {e}")
            estimated_price = deal.price
            
        self.set_status("READY")
        return estimated_price
