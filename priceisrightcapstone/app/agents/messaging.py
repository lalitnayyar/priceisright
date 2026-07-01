from app.agents.base import Agent
from app.core.models import Deal, EnsembleResult
from app.core.config import settings
import requests

class MessagingAgent(Agent):
    """Agent 6 — Uses Claude to craft push notification message, sends via Pushover."""

    def __init__(self):
        super().__init__("Messaging", "Push Notification Generation", "#F85149", settings.MESSAGING_MODEL)
        self._client = None

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client

    def _craft_message_with_claude(self, deal: Deal, result: EnsembleResult) -> str:
        """Use Claude to write a compelling push notification for the deal."""
        if not settings.ANTHROPIC_API_KEY:
            return (
                f"🔥 DEAL ALERT: {deal.title}\n"
                f"Listed: ${deal.price:.2f} | Est. Value: ${result.estimated_price:.2f}\n"
                f"Discount: {result.discount_pct:.1f}% off!\n"
                f"👉 {deal.url}"
            )
        try:
            client = self._get_client()
            prompt = f"""Write a short, punchy push notification for this deal opportunity.
Keep it under 180 characters. Include the product name, discount percentage, and a call to action.
Use 1-2 relevant emojis. Be enthusiastic but professional.

Product: {deal.title}
Listed Price: ${deal.price:.2f}
Estimated True Value: ${result.estimated_price:.2f}
Discount: {result.discount_pct:.1f}%
URL: {deal.url}

Return ONLY the notification text, nothing else."""

            message = client.messages.create(
                model=settings.MESSAGING_MODEL,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            crafted = message.content[0].text.strip()
            self.logger.info(f"Claude crafted notification: '{crafted[:80]}...'")
            return crafted
        except Exception as e:
            self.logger.error(f"Claude message crafting failed: {e} — using template.")
            return (
                f"🔥 {deal.title}: {result.discount_pct:.0f}% Off! "
                f"${deal.price:.2f} (Est. value ${result.estimated_price:.2f}) → {deal.url}"
            )

    def run(self, deal: Deal, result: EnsembleResult) -> bool:
        self.set_status("RUNNING")
        self.logger.info(f"Crafting notification for '{deal.title}' ({result.discount_pct:.1f}% off)...")

        # Step 1: Craft message
        message = self._craft_message_with_claude(deal, result)

        # Step 2: Send via Pushover
        success = False
        if settings.PUSHOVER_USER and settings.PUSHOVER_TOKEN:
            try:
                resp = requests.post(
                    "https://api.pushover.net/1/messages.json",
                    data={
                        "token": settings.PUSHOVER_TOKEN,
                        "user": settings.PUSHOVER_USER,
                        "message": message,
                        "title": "🏷️ The Price Is Right — Deal Alert",
                        "url": deal.url,
                        "url_title": "View Deal",
                        "priority": 1 if result.discount_pct >= 50 else 0,
                    },
                    timeout=10
                )
                if resp.status_code == 200:
                    self.logger.info(f"Pushover notification sent successfully (HTTP 200).")
                    success = True
                else:
                    self.logger.error(f"Pushover returned HTTP {resp.status_code}: {resp.text}")
                    self.set_status("ERROR")
            except Exception as e:
                self.logger.error(f"Pushover request failed: {e}")
                self.set_status("ERROR")
        else:
            self.logger.warning(
                "Pushover credentials not configured (PUSHOVER_USER / PUSHOVER_TOKEN missing). "
                "Notification simulated (not sent)."
            )
            success = True  # Simulate success so pipeline continues

        if success:
            self.set_status("READY")
        return success
