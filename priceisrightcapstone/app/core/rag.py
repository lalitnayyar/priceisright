import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RAGDatabase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.EMBEDDING_MODEL
        )
        self.collection = self.client.get_or_create_collection(
            name="products",
            embedding_function=self.embedding_fn
        )

    def add_product(self, product_id: str, title: str, description: str, price: float, category: str, source: str):
        self.collection.add(
            ids=[product_id],
            documents=[f"{title} {description}"],
            metadatas=[{"price": price, "category": category, "source": source}]
        )

    def query_similar(self, query_text: str, n_results: int = settings.CHROMA_RESULTS_COUNT):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results

rag_db = RAGDatabase()
