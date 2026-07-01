import argparse
import uvicorn
import logging
import os
from app.core.config import settings

# ── Configure logging ──────────────────────────────────────────────────────
# Write to BOTH console AND a known log file so the /logs endpoint can read it.
# The log file path can be overridden via APP_LOG_FILE env var.
LOG_FILE = os.environ.get("APP_LOG_FILE", "/tmp/priceisright_agent.log")

_log_fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

_file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
_file_handler.setFormatter(_log_fmt)

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_log_fmt)

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    handlers=[_file_handler, _stream_handler],
    force=True
)

_startup_logger = logging.getLogger("priceisright.startup")
_startup_logger.info(f"Logging to file: {LOG_FILE}")


def run_dashboard():
    import gradio as gr
    from app.ui.dashboard import create_dashboard
    from app.api import app as fastapi_app

    # Create the Gradio app
    gradio_app = create_dashboard()

    # Mount the Gradio app onto the FastAPI app
    # This means FastAPI handles all routes, and Gradio handles the root '/'
    app = gr.mount_gradio_app(fastapi_app, gradio_app, path="/")

    # Run the unified app on the dashboard port
    uvicorn.run(app, host="0.0.0.0", port=settings.DASHBOARD_PORT, reload=False)

def run_api():
    # Still available as a standalone API on API_PORT if needed
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
