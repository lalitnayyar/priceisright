from app.agents.base import Agent
from app.core.models import Deal
from app.core.config import settings
import feedparser
import json
import uuid
import re

class ScannerAgent(Agent):
    """Agent 1 — Parses RSS feeds and uses GPT to extract structured deal candidates."""

    def __init__(self):
        super().__init__("Scanner", "RSS Parsing & Deal Extraction", "#FF6B35", settings.SCANNER_MODEL)
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self._client

    def _extract_deals_with_gpt(self, entries: list) -> list[dict]:
        """Use GPT to extract structured deal data from raw RSS entries."""
        if not settings.OPENAI_API_KEY:
            self.logger.warning("No OpenAI API key — falling back to heuristic extraction.")
            return []

        entry_text = "\n".join([
            f"- Title: {e.get('title','')}\n  Link: {e.get('link','')}\n  Summary: {e.get('summary','')[:200]}"
            for e in entries[:10]
        ])

        prompt = f"""You are a deal extraction assistant. Analyze these RSS feed entries and extract up to 5 best deal candidates.
For each deal, extract: title, estimated_price (numeric USD, guess from context), url, description (1 sentence).
Return ONLY a valid JSON array like:
[{{"title":"...", "price": 99.99, "url":"...", "description":"..."}}]

RSS Entries:
{entry_text}

Return ONLY the JSON array, no other text."""

        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=settings.SCANNER_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=800
            )
            raw = response.choices[0].message.content.strip()
            raw = re.sub(r'^```(?:json)?\s*', '', raw)
            raw = re.sub(r'\s*```$', '', raw)
            deals_data = json.loads(raw)
            self.logger.info(f"GPT extracted {len(deals_data)} deal candidates from RSS.")
            return deals_data
        except Exception as e:
            self.logger.error(f"GPT extraction failed: {e}")
            return []

    def _heuristic_extract(self, entries: list, source: str) -> list[Deal]:
        """Fallback: extract deals heuristically from RSS entry titles/summaries."""
        deals = []
        price_pattern = re.compile(r'\$\s*([\d,]+(?:\.\d{1,2})?)')
        for entry in entries[:5]:
            title = entry.get("title", "Unknown Product")
            link = entry.get("link", "https://example.com")
            summary = entry.get("summary", "")
            price_match = price_pattern.search(title + " " + summary)
            price = float(price_match.group(1).replace(",", "")) if price_match else 50.0
            deals.append(Deal(
                id=str(uuid.uuid4()),
                title=title[:120],
                price=price,
                url=link,
                description=summary[:200] if summary else title,
                source=source
            ))
        return deals

    def run(self) -> list[Deal]:
        self.set_status("RUNNING")
        self.logger.info("Initiating RSS feed scan...")
        all_deals = []
        feed_urls = [u.strip() for u in settings.RSS_FEED_URLS.split(",") if u.strip()]

        for url in feed_urls:
            self.logger.info(f"Parsing feed: {url}")
            try:
                feed = feedparser.parse(url)
                entries = feed.entries
                if not entries:
                    self.logger.warning(f"No entries found in feed: {url}")
                    continue
                self.logger.info(f"Found {len(entries)} entries. Sending to GPT for extraction...")

                gpt_deals = self._extract_deals_with_gpt(entries)
                if gpt_deals:
                    for d in gpt_deals:
                        try:
                            all_deals.append(Deal(
                                id=str(uuid.uuid4()),
                                title=str(d.get("title", "Unknown Product"))[:120],
                                price=float(d.get("price", 50.0)),
                                url=str(d.get("url", entries[0].get("link", url))),
                                description=str(d.get("description", ""))[:300],
                                source=url
                            ))
                        except Exception as e:
                            self.logger.warning(f"Skipping malformed deal: {e}")
                else:
                    self.logger.info("Using heuristic extraction as GPT fallback.")
                    all_deals.extend(self._heuristic_extract(entries, url))

            except Exception as e:
                self.logger.error(f"Error parsing feed {url}: {e}")

        self.logger.info(f"Scanner complete. Total deals extracted: {len(all_deals)}")
        self.set_status("READY")
        return all_deals
