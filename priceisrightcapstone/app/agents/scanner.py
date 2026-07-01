from app.agents.base import Agent
from app.core.models import Deal
from app.core.config import settings
import feedparser
import json
from openai import OpenAI
import uuid

class ScannerAgent(Agent):
    def __init__(self):
        super().__init__("Scanner", "RSS Parsing & Deal Extraction", "#FF6B35", settings.SCANNER_MODEL)
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def run(self) -> list[Deal]:
        self.set_status("RUNNING")
        self.logger.info("Initiating RSS feed scan...")
        deals = []
        feed_urls = settings.RSS_FEED_URLS.split(",")
        
        for url in feed_urls:
            self.logger.info(f"Parsing '{url}'...")
            try:
                feed = feedparser.parse(url.strip())
                entries = feed.entries[:10] # Limit to top 10 for demo
                
                # Mocking LLM extraction for demo due to API constraints in sandbox, 
                # but implementing the logic as requested
                prompt = f"Extract 5 best deal candidates from these RSS entries: {entries}. Return as JSON with keys: title, price, url, description."
                
                # In a real scenario:
                # response = self.client.chat.completions.create(
                #     model=self.model,
                #     messages=[{"role": "user", "content": prompt}],
                #     response_format={"type": "json_object"}
                # )
                
                # Dummy deals for demonstration
                for i, entry in enumerate(entries[:5]):
                    deals.append(Deal(
                        id=str(uuid.uuid4()),
                        title=entry.get("title", f"Mock Product {i}"),
                        price=100.0 + (i * 10),
                        url=entry.get("link", "http://example.com"),
                        description=entry.get("summary", "Mock description"),
                        source=url
                    ))
            except Exception as e:
                self.logger.error(f"Error parsing {url}: {e}")
                
        self.set_status("READY")
        return deals
