from app.agents.base import Agent
from app.core.models import Deal, EnsembleResult
from app.core.config import settings

class EnsembleAgent(Agent):
    def __init__(self):
        super().__init__("Ensemble", "Weighted Average Combiner", "#5DD9D0", "Heuristic")

    def run(self, deal: Deal, frontier_price: float, specialist_price: float, dnn_price: float) -> EnsembleResult:
        self.set_status("RUNNING")
        
        w_f = settings.ENSEMBLE_FRONTIER_WEIGHT
        w_s = settings.ENSEMBLE_SPECIALIST_WEIGHT
        w_d = settings.ENSEMBLE_DNN_WEIGHT
        
        # Normalize weights if they don't sum to 1
        total = w_f + w_s + w_d
        if total != 1.0 and total > 0:
            w_f, w_s, w_d = w_f/total, w_s/total, w_d/total
            
        self.logger.info(f"Aggregating estimates (W: {w_f:.1f}/{w_s:.1f}/{w_d:.1f})...")
        
        estimated_price = (frontier_price * w_f) + (specialist_price * w_s) + (dnn_price * w_d)
        
        discount_pct = 0.0
        if estimated_price > 0:
            discount_pct = ((estimated_price - deal.price) / estimated_price) * 100
            
        is_great_deal = discount_pct >= settings.DEAL_THRESHOLD
        
        if is_great_deal:
            self.logger.info(f"Discount detected: {discount_pct:.2f}% (${deal.price} vs ${estimated_price:.2f}). TRIGGERING DEAL THRESHOLD.")
            
        result = EnsembleResult(
            estimated_price=estimated_price,
            discount_pct=discount_pct,
            is_great_deal=is_great_deal,
            weights_used={"frontier": w_f, "specialist": w_s, "dnn": w_d}
        )
        
        self.set_status("READY")
        return result
