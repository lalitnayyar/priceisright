from app.agents.base import Agent
from app.core.models import DealResult
from app.core.config import settings
from app.agents.scanner import ScannerAgent
from app.agents.frontier import FrontierAgent
from app.agents.specialist import SpecialistAgent
from app.agents.dnn import NeuralNetworkAgent
from app.agents.ensemble import EnsembleAgent
from app.agents.messaging import MessagingAgent
import json
import os
import time
import threading

class PlanningAgent(Agent):
    def __init__(self):
        super().__init__("Planning", "Pipeline Orchestration", "#5DD9D0", "GPT-4o")
        self.scanner = ScannerAgent()
        self.frontier = FrontierAgent()
        self.specialist = SpecialistAgent()
        self.dnn = NeuralNetworkAgent()
        self.ensemble = EnsembleAgent()
        self.messaging = MessagingAgent()
        
        self.agents = [
            self.scanner, self.frontier, self.specialist, 
            self.dnn, self.ensemble, self.messaging, self
        ]

    def get_all_statuses(self):
        return [a.get_status().model_dump() for a in self.agents]

    def run(self):
        self.set_status("RUNNING")
        self.logger.info("Initiating global scan sequence via RSS_FEED_URLS...")
        
        results = []
        deals = self.scanner.run()
        
        for deal in deals:
            # Run Frontier, Specialist, DNN (in parallel in real scenario, sequential here for simplicity)
            frontier_price = self.frontier.run(deal)
            specialist_price = self.specialist.run(deal)
            dnn_price = self.dnn.run(deal)
            
            ensemble_result = self.ensemble.run(deal, frontier_price, specialist_price, dnn_price)
            
            notification_sent = False
            if ensemble_result.is_great_deal:
                notification_sent = self.messaging.run(deal, ensemble_result)
                
            deal_result = DealResult(
                deal=deal,
                ensemble_result=ensemble_result,
                notification_sent=notification_sent
            )
            results.append(deal_result)
            
        # Save to memory
        self._save_memory(results)
        
        self.logger.info(f"Awaiting next RSS scan interval ({settings.SCAN_INTERVAL_MINUTES}m)...")
        self.set_status("READY")
        return results
        
    def _save_memory(self, results):
        try:
            os.makedirs(os.path.dirname(settings.MEMORY_FILE), exist_ok=True)
            
            existing = []
            if os.path.exists(settings.MEMORY_FILE):
                with open(settings.MEMORY_FILE, 'r') as f:
                    try:
                        existing = json.load(f)
                    except json.JSONDecodeError:
                        pass
                        
            new_data = [r.model_dump(mode='json') for r in results]
            existing.extend(new_data)
            
            with open(settings.MEMORY_FILE, 'w') as f:
                json.dump(existing[-100:], f, indent=2) # Keep last 100
        except Exception as e:
            self.logger.error(f"Failed to save memory: {e}")
            
    def start_background_loop(self):
        def loop():
            while True:
                self.run()
                time.sleep(settings.SCAN_INTERVAL_MINUTES * 60)
                
        thread = threading.Thread(target=loop, daemon=True)
        thread.start()
        return thread
