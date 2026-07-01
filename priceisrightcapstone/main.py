import argparse
import uvicorn
import logging
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def run_dashboard():
    from app.ui.dashboard import create_dashboard
    app = create_dashboard()
    app.launch(server_name="0.0.0.0", server_port=settings.DASHBOARD_PORT, share=False)

def run_api():
    uvicorn.run("app.api:app", host="0.0.0.0", port=settings.API_PORT, reload=False)

def init_rag():
    from app.core.rag import rag_db
    import uuid
    import random
    
    print("Initializing RAG database with sample products...")
    categories = ["Electronics", "Clothing", "Books", "Home & Garden", "Sports", "Toys", "Automotive"]
    
    for i in range(200):
        rag_db.add_product(
            product_id=str(uuid.uuid4()),
            title=f"Sample Product {i}",
            description=f"This is a high quality {random.choice(categories).lower()} item.",
            price=random.uniform(5.0, 2000.0),
            category=random.choice(categories),
            source="init_script"
        )
    print("RAG database initialized with 200 items.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The Price Is Right")
    parser.add_argument("--mode", choices=["dashboard", "api", "init-rag"], required=True, help="Run mode")
    
    args = parser.parse_args()
    
    if args.mode == "dashboard":
        run_dashboard()
    elif args.mode == "api":
        run_api()
    elif args.mode == "init-rag":
        init_rag()
