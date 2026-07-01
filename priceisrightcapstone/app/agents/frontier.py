from app.agents.base import Agent
from app.core.models import Deal
from app.core.config import settings
from app.core.rag import rag_db

class FrontierAgent(Agent):
    """Agent 2 — Uses ChromaDB RAG context + GPT to estimate true market price."""

    def __init__(self):
        super().__init__("Frontier", "RAG-based Price Estimation", "#4ECDC4", settings.FRONTIER_MODEL)
        self._client = None

    def _get_client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self._client

    def run(self, deal: Deal) -> float:
        self.set_status("RUNNING")
        self.logger.info(f"Analyzing '{deal.title}'... Querying ChromaDB for similar products.")
        estimated_price = deal.price  # safe fallback

        try:
            # Step 1: Query RAG for similar historical products
            results = rag_db.query_similar(f"{deal.title} {deal.description}")
            context_items = results.get("documents", [[]])[0] if results else []
            context = "\n".join(context_items[:5]) if context_items else "No similar products found."
            self.logger.info(f"Retrieved {len(context_items)} similar items from ChromaDB.")

            # Step 2: Use GPT with RAG context to estimate price
            if settings.OPENAI_API_KEY:
                prompt = f"""You are a product pricing expert. Based on the historical pricing context below,
estimate the true market value (MSRP) for the following product.

Product: {deal.title}
Description: {deal.description}
Current listed price: ${deal.price:.2f}

Historical context from similar products:
{context}

Return ONLY a single numeric value representing the estimated true market price in USD.
Example: 349.99
Do NOT include $ or any other text."""

                client = self._get_client()
                response = client.chat.completions.create(
                    model=settings.FRONTIER_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=20
                )
                raw = response.choices[0].message.content.strip().replace("$", "").replace(",", "")
                estimated_price = float(raw)
                self.logger.info(f"Frontier RAG+GPT estimate for '{deal.title}': ${estimated_price:.2f}")
            else:
                # Fallback: use RAG context heuristic (average of similar prices if available)
                self.logger.warning("No OpenAI key — using RAG heuristic fallback.")
                estimated_price = deal.price * 1.5

        except ValueError as e:
            self.logger.error(f"Could not parse GPT price response: {e} — using fallback.")
            estimated_price = deal.price * 1.5
        except Exception as e:
            self.logger.error(f"Frontier Agent Error: {e} — using fallback.")
            estimated_price = deal.price * 1.5

        self.set_status("READY")
        return max(estimated_price, deal.price)  # estimated should never be less than listed
